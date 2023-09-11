from django.urls import path
from .views import (project_plan_stage_one, project_plan_initial_view, project_passport_update, project_plan_stage_two,
                    task_add, project_plan_stage_three)

app_name = "projects"

urlpatterns = [
    path("plan/stage~1/", project_plan_stage_one, name="project_creation_stage_one"),
    path("plan/stage~1/<uuid:pk>", project_plan_initial_view, name="initial_view"),
    path("plan/~update/<uuid:pk>", project_passport_update, name="project_passport_update"),
    path("plan/stage~2/<uuid:pk>", project_plan_stage_two, name="project_creation_stage_two"),
    path("plan/stage~3/<uuid:pk>", project_plan_stage_three, name="project_creation_stage_three"),
    path("tasks/<uuid:pk>", task_add, name="task_list"),
]
