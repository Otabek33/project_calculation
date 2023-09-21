from datetime import datetime, timezone
from django.contrib import messages
from django.http import HttpResponse

from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from calculator_projects.apps.projects.constants import coefficient
from calculator_projects.apps.projects.forms import ProjectCreateForm
from calculator_projects.apps.projects.models import ProjectPlan, ProjectCreationStage, ProjectStatus
from calculator_projects.apps.projects.utils import get_coefficient, process_context_percentage_labour_cost, \
    checking_stage_exist, project_plan_fields_regex, update_stages
from calculator_projects.apps.stages.models import StagePlan

from calculator_projects.apps.tasks.models import TaskPlan


# Create your views here.
class ProjectPlanStageOne(CreateView):
    model = ProjectPlan
    form_class = ProjectCreateForm
    tm_path = "projects/project_plan/"
    tm_name = "project_plan_stage_1.html"
    template_name = f"{tm_path}{tm_name}"

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectPlanStageOne, self).get_context_data(*args, **kwargs)
        context['coefficient_list'] = coefficient
        return context

    def form_valid(self, form):
        project_plan = form.save(commit=False)
        project_plan.created_by = self.request.user
        project_plan.departament = self.request.user.deportment
        project_plan.coefficient_of_project = get_coefficient(self.request.POST.get('coefficient'))
        project_plan.project_creation_stage = ProjectCreationStage.STAGE_2
        project_plan.save()
        return redirect("projects:initial_view", pk=project_plan.id)


project_plan_stage_one = ProjectPlanStageOne.as_view()


class ProjectPassportView(DetailView):
    model = ProjectPlan
    tm_path = "projects/project_plan/"
    tm_name = "project_passport.html"
    template_name = f"{tm_path}{tm_name}"

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(ProjectPlan, pk=self.kwargs["pk"])
        project.project_creation_stage = ProjectCreationStage.STAGE_3
        project.save()
        return redirect("projects:project_creation_stage_two", pk=project.id)


project_plan_initial_view = ProjectPassportView.as_view()


class ProjectPlanPassportUpdateView(UpdateView):
    model = ProjectPlan
    form_class = ProjectCreateForm
    tm_path = "projects/project_plan/"
    tm_name = "project_plan_stage_1.html"
    template_name = f"{tm_path}{tm_name}"

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectPlanPassportUpdateView, self).get_context_data(*args, **kwargs)
        context['coefficient_list'] = coefficient
        return context

    def form_valid(self, form):
        project_plan = form.save(commit=False)
        project_plan.update_by = self.request.user
        project_plan.update_at = datetime.now
        project_plan.coefficient_of_project = get_coefficient(self.request.POST.get('coefficient'))
        project_plan.total_price = 0.0
        project_plan.save()
        return redirect("projects:initial_view", pk=project_plan.id)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


project_passport_update = ProjectPlanPassportUpdateView.as_view()


class ProjectPlanStageTwo(DetailView):
    model = ProjectPlan
    tm_path = "projects/project_plan/"
    tm_name = "project_plan_stage_2.html"
    template_name = f"{tm_path}{tm_name}"

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = process_context_percentage_labour_cost(
            pk
        )
        return context

    def post(self, request, *args, **kwargs):
        project_plan = get_object_or_404(ProjectPlan, pk=self.kwargs["pk"])
        stage_count = checking_stage_exist(project_plan)
        if not stage_count:
            messages.error(request, "Добавьте  этап проекта, пожалуйста!")
            return redirect(request.META["HTTP_REFERER"])
        else:
            project_plan.project_creation_stage = ProjectCreationStage.STAGE_4
            project_plan.total_price_with_margin = project_plan.total_price_stage_and_task
            project_plan.process_formation_fields_with_additional_cost()
            project_plan.updated_at = datetime.now(tz=timezone.utc)
            project_plan.updated_by = self.request.user
            project_plan.save()

        return redirect("projects:project_creation_stage_three", pk=project_plan.id)


project_plan_stage_two = ProjectPlanStageTwo.as_view()


class TaskPlanListView(ListView):
    model = TaskPlan
    tm_path = "projects/project_plan/"
    tm_name = "project_plan_task_add.html"
    template_name = f"{tm_path}{tm_name}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        stage_plan = StagePlan.objects.get(id=pk)
        context['stage_plan'] = stage_plan
        context['project_plan'] = ProjectPlan.objects.get(id=stage_plan.projectPlan.id)
        context['task_list'] = TaskPlan.objects.filter(stage=stage_plan, deleted_status=False).order_by('start_time')

        return context


task_add = TaskPlanListView.as_view()


class ProjectPlanStageThree(DetailView):
    model = ProjectPlan
    tm_path = "projects/project_plan/"
    tm_name = "project_plan_stage_3.html"
    template_name = f"{tm_path}{tm_name}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        stage_plan = StagePlan.objects.filter(projectPlan=pk, deleted_status=False)
        context['stage_plan_list'] = stage_plan
        return context

    def post(self, request, *args, **kwargs):
        total_price_with_margin = request.POST.get("total_price_with_margin_for_backend")
        tax_amount = request.POST.get("tax_for_backend")
        margin_amount = request.POST.get("margin_for_backend")
        three_fields = project_plan_fields_regex(total_price_with_margin, tax_amount, margin_amount)
        pk = kwargs.get("pk")
        project_plan = get_object_or_404(ProjectPlan, pk=pk)
        project_plan.updated_by = self.request.user
        project_plan.updated_at = datetime.now(tz=timezone.utc)
        project_plan.project_creation_stage = ProjectCreationStage.STAGE_5
        project_plan.project_status = ProjectStatus.CONFORM
        project_plan.total_price_with_margin = three_fields[0]
        project_plan.contributions_to_IT_park = three_fields[1]
        project_plan.margin = three_fields[2]
        project_plan.save()
        project_plan.process_formation_four_fields_percentage()
        project_plan.save()
        project_plan.process_formation_fields_with_additional_cost()
        project_plan.save()
        margin_percentage = three_fields[2] / project_plan.total_price_stage_and_task
        update_stages(project_plan, margin_percentage)
        return redirect("projects:project_plan_final_view", pk=pk)


project_plan_stage_three = ProjectPlanStageThree.as_view()


class ProjectPlanFinalView(DetailView):
    model = ProjectPlan
    tm_path = "projects/project_plan/"
    tm_name = "project_plan_final_view.html"
    template_name = f"{tm_path}{tm_name}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        stage_plan = StagePlan.objects.filter(projectPlan=pk, deleted_status=False)
        context['stage_plan_list'] = stage_plan
        return context


project_plan_final_view = ProjectPlanFinalView.as_view()


class InvoicePDFView(DetailView):
    model = ProjectPlan
    tm_path = "projects/project_plan/"
    tm_name = "project_plan_final_view.html"
    template_name = f"{tm_path}{tm_name}"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     pk = self.kwargs["pk"]
    #     stage_plan = StagePlan.objects.filter(projectPlan=pk, deleted_status=False)
    #     context['projectplan'] = ProjectPlan.objects.get(id=pk)
    #     context['stage_plan_list'] = stage_plan
    #     return context
    #
    # def get(self, request, *args, **kwargs):
    #     response = PDFTemplateResponse(request=request,
    #                                    template=self.template_name,
    #                                    filename="hello.pdf",
    #                                    context=self.get_context_data(),
    #                                    show_content_in_browser=False,
    #                                    cmd_options={'margin-top': 50, }
    #                                    )
    #     return response


# render_project_plan_pdf_view = InvoicePDFView.as_view()


class GeneratePdf(View):
    model = ProjectPlan
    tm_path = "projects/project_plan/"
    tm_name = "project_plan_final_view.html"
    template_name = f"{tm_path}{tm_name}"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     pk = self.kwargs["pk"]
    #     stage_plan = StagePlan.objects.filter(projectPlan=pk, deleted_status=False)
    #     context['projectplan'] = ProjectPlan.objects.get(id=pk)
    #     context['stage_plan_list'] = stage_plan
    #     context['user'] = self.request.user
    #     return context

    # def get(self, request, *args, **kwargs):
    #     # getting the template
    #     context = {}
    #     pk = self.kwargs["pk"]
    #     stage_plan = StagePlan.objects.filter(projectPlan=pk, deleted_status=False)
    #     context['projectplan'] = ProjectPlan.objects.get(id=pk)
    #     context['stage_plan_list'] = stage_plan
    #     context['user'] = self.request.user
    #     pdf = html_to_pdf(self.template_name, context)
    #
    #     # rendering the template
    #     return HttpResponse(pdf, content_type='application/pdf')


render_project_plan_pdf_view = GeneratePdf.as_view()
