from django.contrib import admin

from calculator_projects.apps.additionalCosts.models import AdditionalCostPlan, AdditionalCostFact


# Register your models here.
class AdditionalCostPlanAdmin(admin.ModelAdmin):
    model = AdditionalCostPlan
    list_display = ["cost_type", "comment", "amount", "project"]


admin.site.register(AdditionalCostPlan, AdditionalCostPlanAdmin)


class AdditionalCostFactAdmin(admin.ModelAdmin):
    model = AdditionalCostFact
    list_display = ["cost_type", "comment", "amount", "project"]


admin.site.register(AdditionalCostFact, AdditionalCostFactAdmin)
