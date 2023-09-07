from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, DetailView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin
from datetime import datetime
from django.utils import timezone
from calculator_projects.apps.labour_costs.forms import LabourCostAddForm, LabourCostUpdateForm
from calculator_projects.apps.labour_costs.models import LabourCost
from calculator_projects.apps.labour_costs.utils import labour_cost_change_status
from calculator_projects.utils.helpers import is_ajax


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

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.updated_by = self.request.user
        obj.save()
        return super().form_valid(form)


labour_cost_add = LabourCostAddView.as_view()


class LabourCostUpdateView(UpdateView):
    model = LabourCost
    form_class = LabourCostUpdateForm
    template_name = "labour_cost/labour_cost_add.html"
    success_url = reverse_lazy("labour_cost:view")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        obj.save()
        return super().form_valid(form)


labour_cost_update = LabourCostUpdateView.as_view()


class LabourCostUpdateStatus(DetailView):
    model = LabourCost

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            LabourCost.objects.filter(deleted_status=False).update(
                calculation_for_projects=False
            )

            pk = request.POST.get("id")
            labour_cost = LabourCost.objects.get(id=pk)
            labour_cost_change_status(labour_cost)
            labour_cost.updated_at = datetime.now(tz=timezone.utc)
            labour_cost.updated_by = self.request.user
            labour_cost.save()
            return JsonResponse(
                {
                    "success": True,
                    "data": None
                }
            )
        return JsonResponse({"success": False, "data": None})


labour_cost_update_status = LabourCostUpdateStatus.as_view()


class LabourCostDeleteView(DeleteView):
    model = LabourCost

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            pk = request.POST.get("id")
            labour_cost = LabourCost.objects.get(id=pk)
            labour_cost.deleted_status = True
            labour_cost.updated_at = datetime.now(tz=timezone.utc)
            labour_cost.updated_by = self.request.user
            labour_cost.save()
            return JsonResponse(
                {
                    "success": True,
                    "data": None
                    # "data": ProjectStageSerializer(stage, many=False).data,
                }
            )
        return JsonResponse({"success": False, "data": None})


labour_cost_delete = LabourCostDeleteView.as_view()
