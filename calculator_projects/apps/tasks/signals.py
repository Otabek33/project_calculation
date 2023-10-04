from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from calculator_projects.apps.stages.utils import project_plan_update, project_fact_update
from calculator_projects.apps.tasks.models import TaskPlan, TaskFact
from calculator_projects.apps.tasks.utils import stage_plan_update, stage_fact_update


@receiver(post_save, sender=TaskPlan)
def update_project_stage(sender, instance, created, **kwargs):
    "After creation task or after updating task every time signal updates project plan stage and project"
    stage_plan_update(instance)
    project_plan_update(instance.stage)


@receiver(post_delete, sender=TaskPlan)
def update_project_stage_delete(sender, instance, **kwargs):
    stage_plan_update(instance)
    project_plan_update(instance.stage)


@receiver(post_save, sender=TaskFact)
def update_project_fact_stage_and_project_fact_change(sender, instance, created, **kwargs):
    "After creation task fact or after updating task  fact every time signal updates project fact stage and project fact"
    stage_fact_update(instance)
    project_fact_update(instance)
