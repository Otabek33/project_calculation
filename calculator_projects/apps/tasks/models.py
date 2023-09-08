from datetime import datetime

from django.db import models

from calculator_projects.apps.projects.models import ProjectPlan
from calculator_projects.apps.stages.models import StagePlan
from calculator_projects.apps.users.models import User
import uuid


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

    # def process_price_task(self):
    #     import numpy as np
    #     from django.db.models import Sum
    #
    #     self.duration_per_day = np.busday_count(
    #         self.start_time, self.finish_time, holidays=HOLIDAYS
    #     )
    #     self.duration_per_hour = self.duration_per_day * 8
    #     labor_cost = LabourCost.objects.get(calculation_for_projects=True)
    #     salary_cost = labor_cost.salary_cost
    #     salary = self.stage.project.coefficient.coefficient * salary_cost
    #     self.total_price = self.duration_per_hour * (
    #         labor_cost.total_cost - salary_cost + salary
    #     )
    #
    #     self.save()
    #
    #     task_list = TaskOfStage.objects.filter(stage=self.stage).filter(
    #         deleted_status=False
    #     )
    #     labour_cost = LabourCost.objects.get(calculation_for_projects=True)
    #     stage = self.stage
    #     from django.db.models import Max, Min
    #
    #     stage.start_time = task_list.aggregate(Min("start_time"))["start_time__min"]
    #     stage.finish_time = task_list.aggregate(Max("finish_time"))["finish_time__max"]
    #     stage.duration_per_hour = task_list.aggregate(Sum("duration_per_hour"))[
    #         "duration_per_hour__sum"
    #     ]
    #     stage.duration_per_day = task_list.aggregate(Sum("duration_per_day"))[
    #         "duration_per_day__sum"
    #     ]
    #
    #     stage.total_price = stage.duration_per_hour * (
    #         labour_cost.total_cost - labour_cost.salary_cost + salary
    #     )
    #
    #     stage.save()
