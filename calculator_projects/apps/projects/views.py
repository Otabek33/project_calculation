from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView

from calculator_projects.apps.projects.constants import coefficient
from calculator_projects.apps.projects.forms import ProjectCreateForm
from calculator_projects.apps.projects.models import ProjectPlan, ProjectCreationStage
from calculator_projects.apps.projects.utils import get_coefficient


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
        project_plan.project_creation_stage = ProjectCreationStage.STAGE_2
        project_plan.total_price = 0.0
        project_plan.save()
        return redirect("projects:initial_view", pk=project_plan.id)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


project_passport_update = ProjectPlanPassportUpdateView.as_view()
