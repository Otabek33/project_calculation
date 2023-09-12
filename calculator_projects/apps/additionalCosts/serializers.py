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

    # def save(self, *args, **kwargs):
    #     instance = super().save(*args, **kwargs)
    #     return instance

    def update(self, instance, validated_data):
        instance.cost_type = validated_data.get('cost_type')
        instance.comment = validated_data.get('comment')
        instance.amount = validated_data.get('amount')
        instance.save()
        instance.process_update_total_price_after_update()
        return instance
