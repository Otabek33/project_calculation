from datetime import datetime

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from calculator_projects.apps.additionalCosts.models import AdditionalCostPlan
from calculator_projects.apps.projects.models import ProjectPlan
from calculator_projects.apps.projects.utils import process_formation_fields_with_additional_cost


@receiver(post_save, sender=AdditionalCostPlan)
def updating_project_plan(sender, instance, created, **kwargs):
    "After creation additional cost or after updating additional cost every time signal updates project plan fields"
    project_plan = ProjectPlan.objects.get(id=instance.project.id)
    process_formation_fields_with_additional_cost(project_plan, AdditionalCostPlan)
    project_plan.save()


@receiver(post_delete, sender=AdditionalCostPlan)
def updating_project_plan_after_delete(sender, instance, **kwargs):
    project_plan = ProjectPlan.objects.get(id=instance.project.id)
    process_formation_fields_with_additional_cost(project_plan, AdditionalCostPlan)
    project_plan.save()
