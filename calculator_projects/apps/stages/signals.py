from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from calculator_projects.apps.stages.models import StagePlan
from calculator_projects.apps.stages.utils import project_plan_update


@receiver(post_save, sender=StagePlan)
def update_project(sender, instance, created, **kwargs):
    "After creation stage or after updating stage every time signal updates project plan"

    project_plan_update(instance)


@receiver(post_delete, sender=StagePlan)
def update_project_delete(sender, instance, **kwargs):
    project_plan_update(instance)
