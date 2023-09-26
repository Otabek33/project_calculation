from django.contrib import admin

from calculator_projects.apps.tasks.models import TaskPlan, TaskFact


# Register your models here.
class TaskPlanAdmin(admin.ModelAdmin):
    model = TaskPlan
    list_display = [
        "id",
        "description",
        "stage",
        "project",
        "start_time",
        "finish_time",
        "total_price",
        "deleted_status",
    ]


admin.site.register(TaskPlan, TaskPlanAdmin)


class TaskFactAdmin(admin.ModelAdmin):
    model = TaskFact
    list_display = [
        "description",
        "stage",
        "project",
        "start_time",
        "finish_time",
        "total_price",
    ]


admin.site.register(TaskFact, TaskFactAdmin)
