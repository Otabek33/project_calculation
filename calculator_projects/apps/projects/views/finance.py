from datetime import datetime, timezone

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from calculator_projects.apps.projects.models import ProjectPlan, ProjectStatus
from calculator_projects.apps.projects.utils import project_amount, project_change_status
from django.contrib import messages

from calculator_projects.utils.helpers import is_ajax


class ProjectConfirmView(ListView):
    model = ProjectPlan
    tm_path = "projects/other/"
    tm_name = "project_confirm.html"
    template_name = f"{tm_path}{tm_name}"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("created_by", "updated_by", "accepted_by").filter(deleted_status=False).exclude(
            project_status=1).order_by("-created_at", "project_status")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_stage_list = project_amount(self.get_queryset())
        context["project_status_list"] = project_stage_list
        return context


confirm_list = ProjectConfirmView.as_view()


# @login_required
# def accept_project(request, id):
#     project_plan = ProjectPlan.objects.get(id=id)
#     project_plan.accepted_by = request.user
#     project_plan.project_status = ProjectStatus.ACTIVE
#     project_plan.accepted_at = datetime.now(tz=timezone.utc)
#     project_plan.save()
#     # project_fact_id = copy_plan_to_fact_project(project_plan)
#     # copy_plan_to_fact_stage(project_plan, project_fact_id)
#     messages.success(request, message="Проект успешно одобрен")
#     return redirect(request.META["HTTP_REFERER"])


# @login_required
# # @director_required
# def project_reject(request, id):
#     project = ProjectPlan.objects.get(id=id)
#     project.accepted_by = request.user
#     project.project_status = ProjectStatus.CANCELLED
#     project.accepted_at = datetime.now(tz=timezone.utc)
#     project.save()
#     messages.error(request, message="Проект успешно отменен")
#     return redirect(request.META["HTTP_REFERER"])


class ProjectPlanRejectView(DetailView):
    model = ProjectPlan

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            pk = request.POST.get("id")
            project_change_status(pk, request.user, ProjectStatus.CANCELLED)
            return JsonResponse(
                {"success": True, "data": None}
            )
        return JsonResponse({"success": False, "data": None})


project_reject = ProjectPlanRejectView.as_view()


class ProjectPlanConfirmView(DetailView):
    model = ProjectPlan

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            pk = request.POST.get("id")
            project_change_status(pk, request.user, ProjectStatus.ACTIVE)
            return JsonResponse(
                {"success": True, "data": None}
            )
        return JsonResponse({"success": False, "data": None})


project_confirm = ProjectPlanConfirmView.as_view()
