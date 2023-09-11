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
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskPlan.objects.filter(deleted_status=False)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, updated_at=datetime.now())

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        task_plan = self.get_object()
        task_plan.deleted_status = True
        task_plan.updated_by = self.request.user
        task_plan.updated_at = datetime.now()
        task_plan.save()
        task_plan.update_stage_modal_date()
        return Response(status=status.HTTP_204_NO_CONTENT)
