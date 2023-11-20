from django.urls import path

from calculator_projects.apps.projects.file_generation import (
    export_excel,
    export_excel_compare_plan_fact,
    export_excel_cost_estimation_by_stage,
    export_excel_overall_project,
    export_excel_plan_graph_project,
    generate_pdf,
)
from calculator_projects.apps.projects.views.finance import confirm_list, project_confirm, project_reject
from calculator_projects.apps.projects.views.pm import (
    additional_cost_fact_add,
    additional_cost_fact_delete,
    additional_cost_fact_edit,
    analyze_list,
    compare_plan_vs_fact,
    project_delete,
    project_fact,
    project_fact_detail,
    project_fact_select,
    project_fact_status_update,
    project_fact_task_update,
    project_list_status,
    project_passport_update,
    project_plan_final_view,
    project_plan_initial_view,
    project_plan_stage_one,
    project_plan_stage_three,
    project_plan_stage_two,
    task_add,
    task_fact_add,
)

app_name = "projects"

urlpatterns = [
    path("plan/stage~1/", project_plan_stage_one, name="project_creation_stage_one"),
    path("plan/stage~1/<uuid:pk>", project_plan_initial_view, name="initial_view"),
    path("plan/~update/<uuid:pk>", project_passport_update, name="project_passport_update"),
    path("plan/stage~2/<uuid:pk>", project_plan_stage_two, name="project_creation_stage_two"),
    path("plan/stage~3/<uuid:pk>", project_plan_stage_three, name="project_creation_stage_three"),
    path("plan/<uuid:pk>", project_plan_final_view, name="project_plan_final_view"),
    path("tasks/<uuid:pk>", task_add, name="task_list"),
    path("status/<uuid:pk>", project_list_status, name="status_list"),
    path("delete/", project_delete, name="project_delete"),
    path("confirm-list/", confirm_list, name="confirm_list"),
    path("project-reject/", project_reject, name="project_reject"),
    path("project-confrim/", project_confirm, name="project_confirm"),
    path("fact/<uuid:pk>", project_fact, name="project_fact"),
    path("fact/<uuid:pk>/detail/", project_fact_detail, name="project_fact_detail"),
    path("fact/task-update/", project_fact_task_update, name="project_fact_task_update"),
    path("fact/task-add/", task_fact_add, name="task_fact_add"),
    path("fact/additional-fact-cost-add/", additional_cost_fact_add, name="additional_cost_fact_add"),
    path("fact/additional-fact-cost-delete/", additional_cost_fact_delete, name="additional_cost_fact_delete"),
    path("fact/additional-fact-cost-edit/", additional_cost_fact_edit, name="additional_cost_fact_edit"),
    path("fact/project-fact-status-update/", project_fact_status_update, name="status_update"),
    path("<uuid:pk>/compare", compare_plan_vs_fact, name="compare"),
    path("<uuid:pk>/analyze", analyze_list, name="analyze_list"),
    path("<uuid:pk>/pdf_generation", generate_pdf, name="pdf_generation"),
    path("<uuid:pk>/excel_generation", export_excel, name="export_excel"),
    path(
        "<uuid:pk>/export_excel_plan_graph_project",
        export_excel_plan_graph_project,
        name="export_excel_plan_graph_project",
    ),
    path(
        "<uuid:pk>/export_excel_cost_estimation_by_stage",
        export_excel_cost_estimation_by_stage,
        name="export_excel_cost_estimation_by_stage",
    ),
    path(
        "<uuid:pk>/export_excel_overall_project",
        export_excel_overall_project,
        name="export_excel_overall_project",
    ),
    path("project-fact-select/", project_fact_select, name="project_fact_select"),
    path(
        "<uuid:pk>/export-excel-compare-plan-fact",
        export_excel_compare_plan_fact,
        name="export_excel_compare_plan_fact",
    ),
]
