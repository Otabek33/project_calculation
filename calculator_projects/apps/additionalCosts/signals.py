from datetime import datetime

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from calculator_projects.apps.additionalCosts.models import AdditionalCostPlan, AdditionalCostFact
from calculator_projects.apps.projects.models import ProjectPlan, ProjectFact
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


@receiver(post_save, sender=AdditionalCostFact)
def updating_project_fact_after_creation_additional_cost(sender, instance, created, **kwargs):
    "After creation additional cost or after updating additional cost every time signal updates project fact fields"
    project_fact = ProjectFact.objects.get(id=instance.project.id)
    process_formation_fields_with_additional_cost(project_fact, AdditionalCostFact)
    project_fact.save()
