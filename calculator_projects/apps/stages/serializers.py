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

    def validate(self, data):
        stage_number = data['stage_number']
        # project_id = data['projectPlan'].id
        if data['start_time'] > data['finish_time']:
            message = "Неправильно выбранная дата"
            raise serializers.ValidationError(
                {"error": message})
        elif stage_number < 0:
            message = "Номер этапа должен быть положительным"
            raise serializers.ValidationError({"error": message})
        # stage = StagePlan.objects.filter(projectPlan=project_id, stage_number=stage_number).exists()
        # if stage:
        #     message = "Этот этап уже существует"
        #     raise serializers.ValidationError({"error": message})
        return data

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.process_price()
        process_formation_fields_with_labour_cost(instance)
        return instance

    def update(self, instance, validated_data):
        instance.process_price()
        process_formation_fields_with_labour_cost(instance)

        return super().update(instance, validated_data)
