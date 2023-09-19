from datetime import datetime

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from calculator_projects.apps.projects.models import ProjectPlan
from calculator_projects.apps.stages.utils import project_plan_update
from calculator_projects.apps.tasks.models import TaskPlan
from calculator_projects.apps.tasks.utils import stage_plan_update


@receiver(post_save, sender=TaskPlan)
def update_project_stage(sender, instance, created, **kwargs):
    "After creation task or after updating task every time signal updates project plan stage"
    stage_plan_update(instance)
    project_plan_update(instance.stage)


@receiver(post_delete, sender=TaskPlan)
def update_project_stage_delete(sender, instance, **kwargs):
    stage_plan_update(instance)
    project_plan_update(instance.stage)
