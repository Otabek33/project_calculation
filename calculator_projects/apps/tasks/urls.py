from rest_framework.routers import DefaultRouter

from calculator_projects.apps.tasks.views import (TaskPlanViewSet,
                                                  )
app_name = "tasks"
router = DefaultRouter()
router.register(r"project-tasks", TaskPlanViewSet, basename="taskPlanList")
urlpatterns = router.urls
