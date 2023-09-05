from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView

from calculator_projects.apps.projects.forms import ProjectCreateForm
from calculator_projects.apps.projects.models import ProjectPlan, ProjectCreationStage


# Create your views here.
class ProjectPlanStageOne(CreateView):
    model = ProjectPlan
    form_class = ProjectCreateForm
    tm_path = "projects/project_plan/"
    tm_name = "project_plan_stage_1.html"
    template_name = f"{tm_path}{tm_name}"

    def form_valid(self, form):
        project = form.save(commit=False)
        project.created_by = self.request.user
        project.departament = self.request.user.deportment
        project.project_creation_stage = ProjectCreationStage.STAGE_1
        project.save()
        return redirect("project:project_passport_without_calculation", pk=project.id)


project_plan_stage_one = ProjectPlanStageOne.as_view()
