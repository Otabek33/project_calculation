from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
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
