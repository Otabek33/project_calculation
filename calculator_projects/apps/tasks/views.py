from django.shortcuts import render
from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import TaskPlan
from .serializers import TaskSerializer


# Create your views here.
class TaskPlanViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task instances.
    """

    serializer_class = TaskSerializer
    queryset = TaskPlan.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = RetrieveTaskSerializer(instance)
    #     return Response(serializer.data)

    # def update(self, request, *args, **kwargs):
    #     super().update(request, *args, **kwargs)
    #     instance = self.get_object()
    #     instance.updated_by = request.user
    #     instance.save()
    #     return instance
    #

    # def perform_create(self, serializer):
    #     stage_id = int(self.request.POST.get('stage'))
    #     stage = ProjectStage.objects.get(id=stage_id)
    #     serializer.save(created_by=self.request.user, project=stage.project)
