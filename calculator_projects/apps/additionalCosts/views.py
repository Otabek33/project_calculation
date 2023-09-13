from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated

from .models import AdditionalCostPlan
from .serializers import (AdditionalCostSerializer,
                          )


# Create your views here.
class AdditionalCostViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing stage instances.
    """

    serializer_class = AdditionalCostSerializer
    queryset = AdditionalCostPlan.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, updated_at=datetime.now())
