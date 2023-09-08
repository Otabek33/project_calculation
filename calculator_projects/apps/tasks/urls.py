from rest_framework.routers import DefaultRouter

from calculator_projects.apps.tasks.views import (TaskPlanViewSet,
                                                  )

app_name = "project_task"
router = DefaultRouter()
router.register(r"project-tasks", TaskPlanViewSet, basename="tasks")
urlpatterns = router.urls
