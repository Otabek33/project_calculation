from datetime import datetime, timezone
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView

from calculator_projects.apps.projects.constants import coefficient
from calculator_projects.apps.projects.forms import ProjectCreateForm
from calculator_projects.apps.projects.models import ProjectPlan, ProjectCreationStage, ProjectStatus, ProjectFact
from calculator_projects.apps.projects.utils import get_coefficient, process_context_percentage_labour_cost, \
    checking_stage_exist, project_plan_fields_regex, update_stages, stage_amount, project_fact_header_info, \
    project_fact_task_amount, project_plan_header_info, project_plan_task_amount
from calculator_projects.apps.stages.models import StagePlan

from calculator_projects.apps.tasks.models import TaskPlan, TaskFact
from calculator_projects.utils.helpers import is_ajax


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
        # project_plan.project_creation_stage = ProjectCreationStage.STAGE_2
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
        project.project_creation_stage = ProjectCreationStage.STAGE_2
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
            project_plan.project_creation_stage = ProjectCreationStage.STAGE_3
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
        project_plan.project_creation_stage = ProjectCreationStage.STAGE_4
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


class ProjectStatusList(ListView):
    model = ProjectPlan
    tm_path = "projects/other/"
    tm_name = "project_status_list.html"
    template_name = f"{tm_path}{tm_name}"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        exclude_list = [ProjectStatus.CANCELLED, ProjectStatus.ACTIVE]
        return qs.filter(
            deleted_status=False, created_by=self.request.user
        ).exclude(project_status__in=exclude_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_stage_list = stage_amount(self.get_queryset())
        context["project_stage_list"] = project_stage_list
        return context


project_list_status = ProjectStatusList.as_view()


class ProjectPlanDelete(DeleteView):
    model = ProjectPlan

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            pk = request.POST.get("id")
            project = self.model.objects.get(id=pk)
            project.deleted_status = True
            project.updated_at = datetime.now(tz=timezone.utc)
            project.updated_by = self.request.user
            project.save()

            return JsonResponse(
                {"success": True, "data": None}
            )
        return JsonResponse({"success": False, "data": None})


project_delete = ProjectPlanDelete.as_view()


class ProjectFactListView(ListView):
    model = ProjectFact
    tm_path = "projects/project_fact/"
    tm_name = "project_fact_list.html"
    template_name = f"{tm_path}{tm_name}"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            deleted_status=False, created_by=self.request.user
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_plan_list = ProjectPlan.objects.filter(
            created_by=self.request.user,
            project_status=ProjectStatus.ACTIVE,
            deleted_status=False,
        )
        context["project_fact_list_header"] = project_fact_header_info(self.get_queryset())
        context["project_plan_list_header"] = project_plan_header_info(project_plan_list)
        context["task_fact_header"] = project_fact_task_amount(self.get_queryset())
        context["task_plan_header"] = project_plan_task_amount(project_plan_list)
        context["project_fact_list"] = self.get_queryset()
        return context


project_fact = ProjectFactListView.as_view()


class ProjectFactDetailView(DetailView):
    model = ProjectFact
    tm_path = "projects/project_fact/"
    tm_name = "project_fact_detail.html"
    template_name = f"{tm_path}{tm_name}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_fact = get_object_or_404(ProjectFact, pk=self.kwargs["pk"])
        task_list = TaskFact.objects.filter(deleted_status=False, project_fact=project_fact)
        context["project_fact"] = project_fact
        context["task_fact_list"] = task_list
        return context


project_fact_detail = ProjectFactDetailView.as_view()
