from datetime import datetime

from django.db import models

from calculator_projects.apps.labour_costs.models import LabourCost
from calculator_projects.apps.projects.models import ProjectPlan, ProjectFact
from calculator_projects.apps.stages.models import StagePlan, StageFact
from calculator_projects.apps.users.models import User
import uuid

from calculator_projects.utils.helpers import (defining_duration_per_day, defining_duration_per_hour,
                                               defining_total_price)
from django.utils.translation import gettext_lazy as _


class TaskFactStatus(models.IntegerChoices):
    PLAN = 1, _("План")
    ACTIVE = 2, _("Активный")
    COMPLETED = 3, _("Завершенный")
    CANCELLED = 4, _("Отменено")
    ON_HOLD = 5, _("На удерживании")


# Create your models here.
class TaskPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    start_time = models.DateField()
    finish_time = models.DateField()
    duration_per_hour = models.IntegerField(default=0.0)
    duration_per_day = models.IntegerField(default=0.0)
    total_price = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    project = models.ForeignKey(
        ProjectPlan, on_delete=models.CASCADE, blank=True, null=True, related_name="project_plan_task",
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


class TaskFact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    task_number = models.IntegerField(blank=True, null=True)
    duration_per_hour = models.IntegerField(default=0.0)
    duration_per_day = models.IntegerField(default=0.0)
    total_price = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    task_plan = models.ForeignKey(
        TaskPlan, on_delete=models.CASCADE, blank=True, null=True
    )
    worker = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    action_status = models.IntegerField(
        choices=TaskFactStatus.choices,
        default=TaskFactStatus.PLAN,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="fact_task_create",
    )
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="fact_task_update",
    )
    updated_at = models.DateTimeField(blank=True, null=True, default=datetime.now)
    deleted_status = models.BooleanField(default=False)
    stage_fact = models.ForeignKey(
        StageFact, on_delete=models.CASCADE, blank=True, null=True
    )
    project_fact = models.ForeignKey(
        ProjectFact,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="project_fact",
    )

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Факт Задача"
        verbose_name_plural = "Факт Задачы"

    def update_fields(self, task_status, worker, fields):
        self.duration_per_hour = fields['duration_per_hour']
        self.duration_per_day = fields['duration_per_day']
        self.start_time = fields['start_time']
        self.finish_time = fields['finish_time']
        self.action_status = task_status
        self.worker = worker
        self.save()

    def process_price_task(self):
        self.duration_per_day = defining_duration_per_day(self.start_time.date(), self.finish_time.date())
        self.duration_per_hour = defining_duration_per_hour(self.duration_per_day)
        self.total_price = defining_total_price(self.project_fact.coefficient_of_project, self.duration_per_hour)
        self.save()

