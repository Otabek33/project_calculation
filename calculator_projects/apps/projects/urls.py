from django.urls import path
from .views import (project_plan_stage_one)

app_name = "projects"

urlpatterns = [
    path("plan/stage~1/", project_plan_stage_one, name="project_creation_stage_one"),
]
