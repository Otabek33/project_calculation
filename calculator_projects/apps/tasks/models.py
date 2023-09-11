from datetime import datetime

from django.db import models

from calculator_projects.apps.labour_costs.models import LabourCost
from calculator_projects.apps.projects.models import ProjectPlan
from calculator_projects.apps.stages.models import StagePlan
from calculator_projects.apps.users.models import User
import uuid

from calculator_projects.utils.helpers import (defining_duration_per_day, defining_duration_per_hour,
                                               defining_total_price)


# Create your models here.
class TaskPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    start_time = models.DateField()
    finish_time = models.DateField()
    task_number = models.IntegerField(blank=True, null=True)
    duration_per_hour = models.IntegerField(default=0.0)
    duration_per_day = models.IntegerField(default=0.0)
    total_price = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    project = models.ForeignKey(
        ProjectPlan, on_delete=models.CASCADE, blank=True, null=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="task_create",
    )
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="task_update",
    )
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_status = models.BooleanField(default=False)
    stage = models.ForeignKey(
        StagePlan, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self) -> str:
        return self.description

    class Meta:
        verbose_name = "План Задача"
        verbose_name_plural = "План Задачы"

    def process_price_task(self):
        self.duration_per_day = defining_duration_per_day(self.start_time, self.finish_time)
        self.duration_per_hour = defining_duration_per_hour(self.duration_per_day)
        self.total_price = defining_total_price(self.project.coefficient_of_project, self.duration_per_hour)
        self.save()
        self.update_stage_modal_date()

    def update_stage_modal_date(self):
        from django.db.models import Max, Min, Sum
        stage = StagePlan.objects.get(id=self.stage.id)
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
        stage.total_price = defining_total_price(stage.projectPlan.coefficient_of_project, stage.duration_per_hour)
        stage.save()
