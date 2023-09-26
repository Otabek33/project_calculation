from django.contrib import admin

from calculator_projects.apps.projects.models import ProjectPlan, ProjectFact


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    model = ProjectPlan
    list_display = [
        "id",
        "name",
        "customer",
        "created_by",
        "created_at",
        "project_creation_stage",
        "total_price_stage_and_task",
        "total_price_with_margin",
        "total_price_with_additional_cost",
        "deleted_status",
        "project_status",
    ]
    list_editable = ["project_status", "deleted_status"]
    readonly_fields = ["coefficient_of_project"]


admin.site.register(ProjectPlan, ProjectAdmin)


class ProjectFactAdmin(admin.ModelAdmin):
    model = ProjectFact
    list_display = [
        "name",
        "created_by",
        "created_at",
        "total_price_stage_and_task",
        "total_price_with_margin",
        "total_price_with_additional_cost",
        "project_status",
    ]
    list_editable = ["project_status"]


admin.site.register(ProjectFact, ProjectFactAdmin)
