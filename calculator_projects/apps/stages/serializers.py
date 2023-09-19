from rest_framework import serializers

from calculator_projects.apps.stages.models import StagePlan
from calculator_projects.utils.helpers import process_formation_fields_with_labour_cost


class StagePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = StagePlan
        fields = [
            "projectPlan",
            "id",
            "description",
            "stage_number",
            "start_time",
            "finish_time",
            "duration_per_day",
            "duration_per_hour",
            "total_price",
        ]

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.process_price()
        process_formation_fields_with_labour_cost(instance)
        return instance

    def update(self, instance, validated_data):
        instance.process_price()
        process_formation_fields_with_labour_cost(instance)
        return super().update(instance, validated_data)
