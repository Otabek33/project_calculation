from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from calculator_projects.apps.additionalCosts.models import AdditionalCostPlan
from calculator_projects.apps.projects.models import ProjectPlan


@receiver(post_save, sender=AdditionalCostPlan)
def updating_project_plan(sender, instance, created, **kwargs):
    if created:
        project_plan = ProjectPlan.objects.get(id=instance.project.id)
        project_plan.process_formation_fields_with_additional_cost()
        project_plan.save()