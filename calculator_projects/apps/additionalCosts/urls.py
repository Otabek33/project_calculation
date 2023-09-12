from rest_framework.routers import DefaultRouter

from .views import (AdditionalCostViewSet)
app_name = "additional_cost"
router = DefaultRouter()
router.register(
    r"additional_costs", AdditionalCostViewSet, basename="additionalcost"
)

urlpatterns = router.urls
