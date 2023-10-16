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
        instance = self.get_object()
        print("ishladi")
        print("ishladi")
        print(instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
