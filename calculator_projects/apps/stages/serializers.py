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
        # project_id = data['projectPlan'].id
        if data["start_time"] > data["finish_time"]:
            message = "Неправильно выбранная дата"
            raise serializers.ValidationError({"error": message})
        elif stage_number < 0:
            message = "Номер этапа должен быть положительным"
            raise serializers.ValidationError({"error": message})
        return data

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.process_price()
        process_formation_fields_with_labour_cost(instance)
        return instance

    def update(self, instance, validated_data):
        task_plan_list = instance.task_list()
        print("ishladi")
        print("ishladi")
        print("ishladi")
        print(validated_data)
        print(validated_data.get("description"))

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
