from datetime import datetime

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from calculator_projects.apps.stages.models import StagePlan
from calculator_projects.apps.stages.serializers import StagePlanSerializer


# Create your views here.
class StagePlanViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing stage instances.
    """

    serializer_class = StagePlanSerializer
    queryset = StagePlan.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, updated_at=datetime.now())
