import logging

from django.http import JsonResponse
from django.views.generic import DetailView, ListView

from calculator_projects.apps.projects.models import ProjectPlan, ProjectStatus
from calculator_projects.apps.projects.utils import (
    copy_plan_to_fact_additional_cost,
    copy_project_plan_to_fact,
    copy_stage_plan_to_fact,
    project_amount,
    project_change_status,
)
from calculator_projects.apps.users.mixins import FinanceRequiredMixin
from calculator_projects.utils.helpers import is_ajax

logger = logging.getLogger("main")


class ProjectConfirmView(FinanceRequiredMixin, ListView):
    model = ProjectPlan
    tm_path = "projects/other/"
    tm_name = "project_confirm.html"
    template_name = f"{tm_path}{tm_name}"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return (
            qs.select_related("created_by", "updated_by", "accepted_by")
            .filter(deleted_status=False)
            .exclude(project_status=1)
            .order_by("-created_at", "project_status")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_stage_list = project_amount(self.get_queryset())
        context["project_status_list"] = project_stage_list
        return context


confirm_list = ProjectConfirmView.as_view()


class ProjectPlanRejectView(FinanceRequiredMixin, DetailView):
    model = ProjectPlan

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            pk = request.POST.get("id")
            project_change_status(pk, request.user, ProjectStatus.CANCELLED)
            return JsonResponse({"success": True, "data": None})
        return JsonResponse({"success": False, "data": None})


project_reject = ProjectPlanRejectView.as_view()


class ProjectPlanConfirmView(FinanceRequiredMixin, DetailView):
    model = ProjectPlan

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            pk = request.POST.get("id")
            project_plan = project_change_status(pk, request.user, ProjectStatus.ACTIVE)
            project_fact = copy_project_plan_to_fact(project_plan)
            copy_stage_plan_to_fact(project_plan, project_fact.id)
            copy_plan_to_fact_additional_cost(project_plan, project_fact)

            return JsonResponse({"success": True, "data": None})
        return JsonResponse({"success": False, "data": None})


project_confirm = ProjectPlanConfirmView.as_view()
