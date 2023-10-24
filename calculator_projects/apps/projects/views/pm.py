from datetime import datetime, timezone

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from calculator_projects.apps.additionalCosts.models import AdditionalCostFact, AdditionalCostPlan
from calculator_projects.apps.additionalCosts.serializers import AdditionalCostFactSerializer
from calculator_projects.apps.projects.constants import coefficient
from calculator_projects.apps.projects.forms import ProjectCreateForm
from calculator_projects.apps.projects.models import ProjectCreationStage, ProjectFact, ProjectPlan, ProjectStatus
from calculator_projects.apps.projects.utils import (
    checking_date_time,
    checking_stage_exist,
    compare_dashboard,
    compare_dashboard_one_project,
    get_coefficient,
    middle_function,
    process_context_percentage_labour_cost,
    process_formation_fields_with_additional_cost,
    process_formation_four_fields_percentage,
    project_fact_header_info,
    project_fact_task_amount,
    project_plan_fields_regex,
    project_plan_header_info,
    project_plan_task_amount,
    regex_choose_date_range,
    stage_amount,
    update_stages,
)
from calculator_projects.apps.stages.models import StageFact, StagePlan
from calculator_projects.apps.tasks.models import TaskFact, TaskPlan
from calculator_projects.apps.users.mixins import ProjectUsageRequiredMixin
from calculator_projects.apps.users.models import User, UserRoleTypes
from calculator_projects.utils.helpers import defining_total_price, is_ajax


# Create your views here.
class ProjectPlanStageOne(ProjectUsageRequiredMixin, CreateView):
    model = ProjectPlan
    form_class = ProjectCreateForm
    tm_path = "projects/project_plan/"
    tm_name = "project_plan_stage_1.html"
    template_name = f"{tm_path}{tm_name}"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["coefficient_list"] = coefficient
        return context

    def form_valid(self, form):
        project_plan = form.save(commit=False)
        project_plan.created_by = self.request.user
        project_plan.departament = self.request.user.deportment
        project_plan.coefficient_of_project = get_coefficient(self.request.POST.get("coefficient"))
        project_plan.save()
        return redirect("projects:initial_view", pk=project_plan.id)


project_plan_stage_one = ProjectPlanStageOne.as_view()


class ProjectPassportView(ProjectUsageRequiredMixin, DetailView):
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


class ProjectPlanPassportUpdateView(ProjectUsageRequiredMixin, UpdateView):
    model = ProjectPlan
    form_class = ProjectCreateForm
    tm_path = "projects/project_plan/"
    tm_name = "project_plan_stage_1.html"
    template_name = f"{tm_path}{tm_name}"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["coefficient_list"] = coefficient
        return context

    def form_valid(self, form):
        project_plan = form.save(commit=False)
        project_plan.update_by = self.request.user
        project_plan.update_at = datetime.now
        project_plan.coefficient_of_project = get_coefficient(self.request.POST.get("coefficient"))
        project_plan.total_price = 0.0
        project_plan.save()
        return redirect("projects:initial_view", pk=project_plan.id)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


project_passport_update = ProjectPlanPassportUpdateView.as_view()


class ProjectPlanStageTwo(ProjectUsageRequiredMixin, DetailView):
    model = ProjectPlan
    tm_path = "projects/project_plan/"
    tm_name = "project_plan_stage_2.html"
    template_name = f"{tm_path}{tm_name}"

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = process_context_percentage_labour_cost(pk)
        return context

    def post(self, request, *args, **kwargs):
        project_plan = get_object_or_404(ProjectPlan, pk=self.kwargs["pk"])
        stage_count = checking_stage_exist(project_plan)
        if not stage_count:
            messages.error(request, "Добавьте  этап проекта, пожалуйста!")
            return redirect(request.headers["referer"])
        else:
            project_plan.project_creation_stage = ProjectCreationStage.STAGE_3
            project_plan.total_price_with_margin = project_plan.total_price_stage_and_task
            process_formation_fields_with_additional_cost(project_plan, AdditionalCostPlan)
            project_plan.updated_at = datetime.now(tz=timezone.utc)
            project_plan.updated_by = self.request.user
            project_plan.save()

        return redirect("projects:project_creation_stage_three", pk=project_plan.id)


project_plan_stage_two = ProjectPlanStageTwo.as_view()


class TaskPlanListView(ProjectUsageRequiredMixin, ListView):
    model = TaskPlan
    tm_path = "projects/project_plan/"
    tm_name = "project_plan_task_add.html"
    template_name = f"{tm_path}{tm_name}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        stage_plan = StagePlan.objects.get(id=pk)
        context["stage_plan"] = stage_plan
        context["project_plan"] = ProjectPlan.objects.get(id=stage_plan.projectPlan.id)
        context["task_list"] = TaskPlan.objects.filter(stage=stage_plan, deleted_status=False).order_by("start_time")
        return context


task_add = TaskPlanListView.as_view()


class ProjectPlanStageThree(ProjectUsageRequiredMixin, DetailView):
    model = ProjectPlan
    tm_path = "projects/project_plan/"
    tm_name = "project_plan_stage_3.html"
    template_name = f"{tm_path}{tm_name}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        stage_plan = StagePlan.objects.filter(projectPlan=pk, deleted_status=False).order_by("stage_number")
        context["stage_plan_list"] = stage_plan
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
        process_formation_four_fields_percentage(project_plan)
        project_plan.save()
        process_formation_fields_with_additional_cost(project_plan, AdditionalCostPlan)
        project_plan.save()
        margin_percentage = three_fields[2] / project_plan.total_price_stage_and_task
        update_stages(project_plan, margin_percentage)
        return redirect("projects:project_plan_final_view", pk=pk)


project_plan_stage_three = ProjectPlanStageThree.as_view()


class ProjectPlanFinalView(ProjectUsageRequiredMixin, DetailView):
    model = ProjectPlan
    tm_path = "projects/project_plan/"
    tm_name = "project_plan_final_view.html"
    template_name = f"{tm_path}{tm_name}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        stage_plan = StagePlan.objects.filter(projectPlan=pk, deleted_status=False).order_by("stage_number")
        context["stage_plan_list"] = stage_plan
        return context


project_plan_final_view = ProjectPlanFinalView.as_view()


class ProjectStatusList(ProjectUsageRequiredMixin, ListView):
    model = ProjectPlan
    tm_path = "projects/other/"
    tm_name = "project_status_list.html"
    template_name = f"{tm_path}{tm_name}"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        exclude_list = [ProjectStatus.CANCELLED, ProjectStatus.ACTIVE]
        return qs.filter(deleted_status=False, created_by=self.request.user).exclude(project_status__in=exclude_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_stage_list = stage_amount(self.get_queryset())
        context["project_stage_list"] = project_stage_list
        return context


project_list_status = ProjectStatusList.as_view()


class ProjectPlanDelete(ProjectUsageRequiredMixin, DeleteView):
    model = ProjectPlan

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            pk = request.POST.get("id")
            project = self.model.objects.get(id=pk)
            project.deleted_status = True
            project.updated_at = datetime.now(tz=timezone.utc)
            project.updated_by = self.request.user
            project.save()

            return JsonResponse({"success": True, "data": None})
        return JsonResponse({"success": False, "data": None})


project_delete = ProjectPlanDelete.as_view()


class ProjectFactListView(ProjectUsageRequiredMixin, ListView):
    model = ProjectFact
    tm_path = "projects/project_fact/"
    tm_name = "project_fact_list.html"
    template_name = f"{tm_path}{tm_name}"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(deleted_status=False, created_by=self.request.user).order_by("-created_at")

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


class ProjectFactDetailView(ProjectUsageRequiredMixin, DetailView):
    model = ProjectFact
    tm_path = "projects/project_fact/"
    tm_name = "project_fact_detail.html"
    template_name = f"{tm_path}{tm_name}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_fact = get_object_or_404(ProjectFact, pk=self.kwargs["pk"])
        task_list = TaskFact.objects.filter(deleted_status=False, project_fact=project_fact).order_by(
            "stage_fact__stage_number", "created_at"
        )
        user_list = User.objects.all()
        context["project_fact"] = project_fact
        context["task_fact_list"] = task_list
        context["user_list"] = user_list
        return context


project_fact_detail = ProjectFactDetailView.as_view()


class ProjectFactTaskUpdateView(ProjectUsageRequiredMixin, UpdateView):
    model = TaskFact

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            from decimal import Decimal

            task_pk = request.POST["id"]
            worker_pk = request.POST["worker"]
            if len(worker_pk) == 0:
                message = "Добавьте работника, пожалуйста"
                return JsonResponse({"error": message}, status=400)
            else:
                status, fields = regex_choose_date_range(request.POST["daterange"])
                if status:
                    task_fact = get_object_or_404(TaskFact, pk=task_pk)
                    task_fact.updated_at = datetime.now()
                    task_fact.updated_by = self.request.user
                    worker = get_object_or_404(User, pk=worker_pk)
                    task_fact.update_fields(int(request.POST["task_status"]), worker, fields)
                    task_fact.total_price = defining_total_price(
                        task_fact.project_fact.coefficient_of_project, Decimal(task_fact.duration_per_hour)
                    )

                    task_fact.save()
                    return JsonResponse({"success": True, "data": None})
                else:
                    message = "Неправильно выбрана дата"
                    return JsonResponse({"error": message}, status=400)


project_fact_task_update = ProjectFactTaskUpdateView.as_view()


class TaskFactAddView(ProjectUsageRequiredMixin, CreateView):
    model = TaskFact

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            name = request.POST["name"]

            if len(name) == 0:
                message = "Добавьте наименование, пожалуйста"
                return JsonResponse({"error": message}, status=400)
            else:
                date_range = request.POST["date"]
                start_time, finish_time = middle_function(date_range)
                if checking_date_time(start_time, finish_time):
                    message = "Неправильно выбрана дата"
                    return JsonResponse({"error": message}, status=400)
                else:
                    task_fact = TaskFact()
                    project_fact = get_object_or_404(ProjectFact, pk=request.POST["project"])
                    stage_fact = get_object_or_404(StageFact, pk=request.POST["stage"])
                    task_fact.description = name
                    task_fact.start_time = start_time
                    task_fact.finish_time = finish_time
                    task_fact.created_at = datetime.now(tz=timezone.utc)
                    task_fact.created_by = self.request.user
                    task_fact.project_fact = project_fact
                    task_fact.stage_fact = stage_fact
                    task_fact.action_status = int(request.POST["status"])
                    task_fact.save()
                    task_fact.process_price_task()
                    message = "Задача успешно добавлен"
                    return JsonResponse({"success": True, "data": None, "msg": message}, status=200)


task_fact_add = TaskFactAddView.as_view()


class AdditionalCostAddFact(ProjectUsageRequiredMixin, CreateView):
    model = AdditionalCostFact

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            comment = request.POST["comment"]
            if len(comment) == 0:
                message = "Добавьте наименование, пожалуйста"
                return JsonResponse({"error": message}, status=400)
            else:
                amount = int(request.POST["amount"])
                if amount < 0:
                    message = "Неправильная сумма"
                    return JsonResponse({"error": message}, status=400)
                else:
                    project_fact = get_object_or_404(ProjectFact, pk=request.POST["project"])
                    additional_cost_fact = AdditionalCostFact()
                    additional_cost_fact.amount = amount
                    additional_cost_fact.comment = comment
                    additional_cost_fact.project = project_fact
                    additional_cost_fact.cost_type = int(request.POST["type"])
                    additional_cost_fact.created_at = datetime.now(tz=timezone.utc)
                    additional_cost_fact.created_by = self.request.user
                    additional_cost_fact.save()
                    message = "Доп. расход успешно добавлен"
                    return JsonResponse({"success": True, "data": None, "msg": message}, status=200)


additional_cost_fact_add = AdditionalCostAddFact.as_view()


class AdditionalCostDelete(ProjectUsageRequiredMixin, DeleteView):
    model = AdditionalCostFact

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            additional_cost_fact = get_object_or_404(AdditionalCostFact, pk=request.POST["additional_cost"])
            additional_cost_fact.delete()
            message = "Доп. расход успешно удален"
            return JsonResponse({"success": True, "data": None, "msg": message}, status=200)


additional_cost_fact_delete = AdditionalCostDelete.as_view()


class AdditionalCostFactEditView(ProjectUsageRequiredMixin, UpdateView):
    model = AdditionalCostFact

    def get(self, request, *args, **kwargs):
        if is_ajax(request):
            pk = int(request.GET["id"])
            additional_cost_fact = AdditionalCostFact.objects.get(pk=pk, created_by=self.request.user)
            return JsonResponse({"data": AdditionalCostFactSerializer(additional_cost_fact, many=False).data})

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            comment = request.POST["comment"]
            if len(comment) == 0:
                message = "Добавьте наименование, пожалуйста"
                return JsonResponse({"error": message}, status=400)
            else:
                amount = int(request.POST["amount"])
                if amount < 0:
                    message = "Неправильная сумма"
                    return JsonResponse({"error": message}, status=400)
                else:
                    project_fact = get_object_or_404(ProjectFact, pk=request.POST["project"])
                    additional_cost_fact = get_object_or_404(AdditionalCostFact, pk=int(request.POST["id"]))
                    additional_cost_fact.amount = amount
                    additional_cost_fact.comment = comment
                    additional_cost_fact.project = project_fact
                    additional_cost_fact.cost_type = int(request.POST["type"])
                    additional_cost_fact.updated_at = datetime.now(tz=timezone.utc)
                    additional_cost_fact.updated_by = self.request.user
                    additional_cost_fact.save()
                    message = "Доп. расход успешно изменен"
                    return JsonResponse({"success": True, "data": None, "msg": message}, status=200)


additional_cost_fact_edit = AdditionalCostFactEditView.as_view()


class ProjectFactStatusUpdateView(ProjectUsageRequiredMixin, TemplateView):
    model = ProjectFact

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            project_fact = get_object_or_404(ProjectFact, pk=request.POST["project"])
            project_fact.project_status = int(request.POST["status"])
            project_fact.updated_at = datetime.now(tz=timezone.utc)
            project_fact.updated_by = self.request.user
            project_fact.save()
            message = "Статус изменен"
            return JsonResponse({"success": True, "data": None, "msg": message}, status=200)


project_fact_status_update = ProjectFactStatusUpdateView.as_view()


class ComparePlanFactView(ProjectUsageRequiredMixin, ListView):
    model = ProjectFact
    tm_path = "projects/project_fact/"
    tm_name = "project_fact_compare.html"
    template_name = f"{tm_path}{tm_name}"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(deleted_status=False, created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_plan_list = ProjectPlan.objects.filter(
            created_by=self.request.user,
            project_status=ProjectStatus.ACTIVE,
            deleted_status=False,
        )
        context = compare_dashboard(self.request.user, context, self.get_queryset(), project_plan_list)

        return context


compare_plan_vs_fact = ComparePlanFactView.as_view()


class ProjectAnalyzeView(ProjectUsageRequiredMixin, ListView):
    model = ProjectFact
    tm_path = "projects/other/"
    tm_name = "project_analyze.html"
    template_name = f"{tm_path}{tm_name}"

    def get_queryset(self):
        qs = super().get_queryset()
        user_role = self.request.user.user_role
        if user_role == UserRoleTypes.SUPER_USER or user_role == UserRoleTypes.FINANCE:
            return qs.filter(deleted_status=False)
        else:
            return qs.filter(deleted_status=False, created_by=self.request.user)


analyze_list = ProjectAnalyzeView.as_view()


class ProjectFactSelect(ProjectUsageRequiredMixin, View):
    model = ProjectFact

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            pk = request.POST["project"]
            project_fact = get_object_or_404(ProjectFact, pk=pk)
            context = {}
            context = compare_dashboard_one_project(
                self.request.user, context, project_fact, project_fact.project_plan
            )
            print("ishladi")
            print("ishladi")
            print(context)
            # print("ishladi")
            # print("ishladi")
            # print("ishladi")
            # print(context)

            message = f"{project_fact.name}"
            return JsonResponse({"success": True, "data": context, "msg": message}, status=200)


project_fact_select = ProjectFactSelect.as_view()
