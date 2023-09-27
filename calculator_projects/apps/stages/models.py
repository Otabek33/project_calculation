from datetime import datetime

from django.db import models

from calculator_projects.apps.labour_costs.models import LabourCost
from calculator_projects.apps.projects.models import ProjectPlan, ProjectFact

from calculator_projects.apps.users.models import User

import uuid

from calculator_projects.utils.helpers import defining_duration_per_day, defining_duration_per_hour, \
    defining_total_price


# Create your models here.
class StagePlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    start_time = models.DateField()
    finish_time = models.DateField()
    stage_number = models.IntegerField(blank=True, null=True)
    duration_per_hour = models.IntegerField(default=0.0)
    duration_per_day = models.IntegerField(default=0.0)
    total_price = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    total_price_stage_and_task = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    salary_cost = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)
    cost_price = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)
    period_expenses = models.DecimalField(
        max_digits=1000, decimal_places=8, default=0.0
    )

    contributions_to_IT_park = models.DecimalField(
        max_digits=1000, decimal_places=8, default=0.0
    )
    margin = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)
    total_price_with_margin = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.0
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="stage_create",
    )
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="stage_update",
    )
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_status = models.BooleanField(default=False)
    projectPlan = models.ForeignKey(
        ProjectPlan, on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        verbose_name = "План Этап"
        verbose_name_plural = "План Этапы"

    def __str__(self):
        return str(self.description)

    def process_price(self):
        self.duration_per_day = defining_duration_per_day(self.start_time, self.finish_time)
        self.duration_per_hour = defining_duration_per_hour(self.duration_per_day)
        self.total_price_stage_and_task = defining_total_price(self.projectPlan.coefficient_of_project,
                                                               self.duration_per_hour)
        self.save()

    def task_counter(self):
        return self.taskplan_set.filter(deleted_status=False).count()

    def task_list(self):
        from calculator_projects.apps.tasks.models import TaskPlan
        return TaskPlan.objects.filter(stage=self.id, deleted_status=False)

    def total_price_without_tax(self):
        return self.salary_cost + self.cost_price + self.period_expenses


class StageFact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    start_time = models.DateField()
    finish_time = models.DateField()
    stage_number = models.IntegerField(blank=True, null=True)
    duration_per_hour = models.IntegerField(default=0.0)
    duration_per_day = models.IntegerField(default=0.0)
    total_price = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    total_price_stage_and_task = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    salary_cost = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)
    cost_price = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)
    period_expenses = models.DecimalField(
        max_digits=1000, decimal_places=8, default=0.0
    )

    contributions_to_IT_park = models.DecimalField(
        max_digits=1000, decimal_places=8, default=0.0
    )
    margin = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)
    total_price_with_margin = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.0
    )
    stage_plan = models.ForeignKey(
        StagePlan, on_delete=models.CASCADE, blank=True, null=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="fact_stage_create",
    )
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="fact_stage_update",
    )
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_status = models.BooleanField(default=False)
    project_fact = models.ForeignKey(
        ProjectFact, on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        verbose_name = "Факт Этап"
        verbose_name_plural = "Факт Этапы"

    def __str__(self):
        return self.description
