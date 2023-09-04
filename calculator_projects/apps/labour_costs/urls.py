from django.urls import path
# labour_cost_add, labour_cost_delete_without_id,
#                     labour_cost_update,
from calculator_projects.apps.labour_costs.views import (
    labour_cost_view, labour_cost_add, labour_cost_update, labour_cost_update_status,labour_cost_delete )

app_name = "labour_cost"

urlpatterns = [
    path("add/", labour_cost_add, name="add"),
    path("update/<int:pk>/", labour_cost_update, name="update"),
    path("update/", labour_cost_update_status, name="update_status"),
    path("", labour_cost_view, name="view"),
    path("delete/", labour_cost_delete, name="delete"),
]
