from datetime import datetime

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
        stage_number = data["stage_number"]
        if data["start_time"] > data["finish_time"]:
            message = "Неправильно выбранная дата"
            raise serializers.ValidationError({"error": message})
        elif stage_number < 0:
            message = "Номер этапа должен быть положительным"
            raise serializers.ValidationError({"error": message})
        return data

    def create(self, validated_data):
        stage = StagePlan()
        stage.stage_number = validated_data["stage_number"]
        stage.start_time = validated_data["start_time"]
        stage.finish_time = validated_data["finish_time"]
        stage.description = validated_data["description"]
        stage.created_by = validated_data["created_by"]
        stage.created_at = datetime.now()
        stage.projectPlan = validated_data["projectPlan"]
        stage.process_price()
        process_formation_fields_with_labour_cost(stage)
        stage.save()
        return stage

    def update(self, instance, validated_data):
        task_plan_list = instance.task_list()
        if len(task_plan_list) > 0:
            instance.description = validated_data.get("description")
            instance.stage_number = validated_data.get("stage_number")
            instance.start_time = instance.start_time
            instance.finish_time = instance.finish_time
            instance.total_price_stage_and_task = instance.total_price_stage_and_task
            instance.duration_per_hour = instance.duration_per_hour
            instance.duration_per_day = instance.duration_per_day
            instance.save()
            return instance
        else:
            instance.process_price()
            process_formation_fields_with_labour_cost(instance)
            return super().update(instance, validated_data)
