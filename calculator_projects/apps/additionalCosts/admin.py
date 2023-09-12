from django.contrib import admin

from calculator_projects.apps.additionalCosts.models import AdditionalCostPlan


# Register your models here.
class AdditionalCostPlanAdmin(admin.ModelAdmin):
    model = AdditionalCostPlan
    list_display = ["cost_type", "comment", "amount", "project"]


admin.site.register(AdditionalCostPlan, AdditionalCostPlanAdmin)
