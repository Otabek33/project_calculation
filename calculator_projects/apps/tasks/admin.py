from django.contrib import admin

from calculator_projects.apps.tasks.models import TaskPlan


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
    ]


admin.site.register(TaskPlan, TaskPlanAdmin)
