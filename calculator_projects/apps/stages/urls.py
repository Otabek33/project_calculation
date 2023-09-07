from rest_framework.routers import DefaultRouter

from calculator_projects.apps.stages.views import (StagePlanViewSet,
                                                   )

app_name = "projectstageplan"
router = DefaultRouter()
router.register(r"stages", StagePlanViewSet, basename="stageplan")
urlpatterns = router.urls
