from datetime import datetime

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from calculator_projects.apps.projects.models import ProjectPlan
from calculator_projects.apps.stages.models import StagePlan
from calculator_projects.apps.tasks.models import TaskPlan
from calculator_projects.utils.helpers import defining_total_price


@receiver(post_save, sender=TaskPlan)
def updating_project_stage(sender, instance, created, **kwargs):
    "After creation task or after updating task every time signal updates project plan stage"
    from django.db.models import Max, Min, Sum
    stage = StagePlan.objects.get(id=instance.stage.id)
    task_plan_list = TaskPlan.objects.filter(stage=stage,
                                             deleted_status=False
                                             )
    stage.start_time = task_plan_list.aggregate(Min("start_time"))["start_time__min"]
    stage.finish_time = task_plan_list.aggregate(Max("finish_time"))["finish_time__max"]
    stage.duration_per_hour = task_plan_list.aggregate(Sum("duration_per_hour"))[
        "duration_per_hour__sum"
    ]
    stage.duration_per_day = task_plan_list.aggregate(Sum("duration_per_day"))[
        "duration_per_day__sum"
    ]
    stage.total_price_stage_and_task = defining_total_price(stage.projectPlan.coefficient_of_project, stage.duration_per_hour)
    stage.save()


@receiver(post_delete, sender=TaskPlan)
def updating_project_stage_after_delete(sender, instance, **kwargs):
    project_plan = ProjectPlan.objects.get(id=instance.project.id)
    project_plan.process_formation_fields_with_additional_cost()
    project_plan.save()
