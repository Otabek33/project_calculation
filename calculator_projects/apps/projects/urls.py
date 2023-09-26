from django.urls import path

from calculator_projects.apps.projects.views.finance import confirm_list, project_reject,project_confirm
from calculator_projects.apps.projects.views.pm import (project_plan_stage_one, project_plan_initial_view,
                                                        project_passport_update, project_plan_stage_two,
                                                        task_add, project_plan_stage_three, project_plan_final_view,
                                                        project_list_status, project_delete, )

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

]
