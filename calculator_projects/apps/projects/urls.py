from django.urls import path

from calculator_projects.apps.projects.views.finance import confirm_list, project_reject, project_confirm
from calculator_projects.apps.projects.views.pm import (project_plan_stage_one, project_plan_initial_view,
                                                        project_passport_update, project_plan_stage_two,
                                                        task_add, project_plan_stage_three, project_plan_final_view,
                                                        project_list_status, project_delete, project_fact,
                                                        project_fact_detail, project_fact_task_update, task_fact_add,
                                                        additional_cost_fact_add,additional_cost_fact_delete,additional_cost_fact_edit,project_fact_status_update)

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

]
