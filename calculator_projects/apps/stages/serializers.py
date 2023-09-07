from rest_framework import serializers

from calculator_projects.apps.stages.models import StagePlan


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
        return instance
