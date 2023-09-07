from django.contrib import admin

from calculator_projects.apps.stages.models import StagePlan


# Register your models here.
class StagePlanAdmin(admin.ModelAdmin):
    model = StagePlan
    list_display = [
        "description",
        "projectPlan",
        "start_time",
        "finish_time",
        "total_price",
    ]


admin.site.register(StagePlan, StagePlanAdmin)
