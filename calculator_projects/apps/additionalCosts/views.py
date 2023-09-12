from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import AdditionalCostPlan
from .serializers import (AdditionalCostSerializer,
                          )
from ..projects.models import ProjectPlan


# Create your views here.
class AdditionalCostViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing stage instances.
    """

    serializer_class = AdditionalCostSerializer
    queryset = AdditionalCostPlan.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        additional_cost = self.get_object()
        from django.utils import timezone

        project = ProjectPlan.objects.get(id=additional_cost.project.id)
        project.updated_at = datetime.now(tz=timezone.utc)
        project.additional_cost = project.additional_cost - additional_cost.amount
        project.total_price_with_additional_cost = (
            project.total_price_with_additional_cost - additional_cost.amount
        )
        project.save()
        additional_cost.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
