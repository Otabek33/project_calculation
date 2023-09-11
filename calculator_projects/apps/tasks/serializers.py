from rest_framework import serializers

from calculator_projects.apps.tasks.models import TaskPlan


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPlan
        fields = [
            "id",
            "stage",
            "description",
            "start_time",
            "finish_time",
            "duration_per_day",
            "duration_per_hour",
            "created_by",
            "project",
            "total_price",
        ]

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.project = instance.stage.projectPlan
        instance.process_price_task()

        return instance
