from django.contrib import admin

from calculator_projects.apps.stages.models import StagePlan, StageFact


# Register your models here.
class StagePlanAdmin(admin.ModelAdmin):
    model = StagePlan
    list_display = [
        "description",
        "projectPlan",
        "start_time",
        "finish_time",
        "total_price",
        "total_price_stage_and_task",
    ]


admin.site.register(StagePlan, StagePlanAdmin)


class StageFactAdmin(admin.ModelAdmin):
    model = StageFact
    list_display = [
        "description",
        "project_fact",
        "start_time",
        "finish_time",
    ]


admin.site.register(StageFact, StageFactAdmin)
