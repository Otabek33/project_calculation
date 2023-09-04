from django.contrib import admin

from calculator_projects.apps.labour_costs.models import LabourCost

# Register your models here.


class LabourCostAdmin(admin.ModelAdmin):
    model = LabourCost
    list_display = [
        "total_cost",
        "salary_cost",
        "cost_price",
        "period_expenses",
        "contributions_to_IT_park",
        "created_by",
        "created_at",
        "calculation_for_projects",
    ]


admin.site.register(LabourCost, LabourCostAdmin)
