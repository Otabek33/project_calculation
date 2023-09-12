from rest_framework import serializers

from calculator_projects.apps.additionalCosts.models import AdditionalCostPlan


class AdditionalCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalCostPlan
        fields = [
            "id",
            "cost_type",
            "comment",
            "amount",
            "project",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["cost_type_name"] = instance.get_cost_type_display()
        return representation
