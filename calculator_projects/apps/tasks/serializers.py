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

    def validate(self, data):
        if data['start_time'] > data['finish_time']:
            message = "Неправильно выбранная дата"
            raise serializers.ValidationError(
                {"error": message})

        return data

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.project = instance.stage.projectPlan
        instance.process_price_task()
        return instance

    def update(self, instance, validated_data):
        instance.process_price_task()
        return super().update(instance, validated_data)
