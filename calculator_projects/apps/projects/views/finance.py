from django.views.generic import ListView

from calculator_projects.apps.projects.models import ProjectPlan
from calculator_projects.apps.projects.utils import project_amount


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
