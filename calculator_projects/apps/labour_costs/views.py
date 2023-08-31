from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, DetailView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin

from calculator_projects.apps.labour_costs.forms import LabourCostAddForm, LabourCostUpdateForm
from calculator_projects.apps.labour_costs.models import LabourCost


# Create your views here.

class LabourCostView(LoginRequiredMixin, ListView):
    model = LabourCost
    template_name = "labour_cost/labour_cost_list.html"
    paginate_by = 5

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(deleted_status=False).order_by("-created_at")


labour_cost_view = LabourCostView.as_view()


class LabourCostAddView(CreateView):
    model = LabourCost
    form_class = LabourCostAddForm
    template_name = "labour_cost/labour_cost_add.html"
    success_url = reverse_lazy("labour_cost:view")


labour_cost_add = LabourCostAddView.as_view()


class LabourCostUpdateView(UpdateView):
    model = LabourCost
    form_class = LabourCostUpdateForm
    template_name = "labour_cost/labour_cost_add.html"
    success_url = reverse_lazy("labour_cost:view")


labour_cost_update = LabourCostUpdateView.as_view()
