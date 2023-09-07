from datetime import datetime

from django.db import models

from calculator_projects.apps.labour_costs.models import LabourCost
from calculator_projects.apps.projects.models import ProjectPlan
from calculator_projects.apps.users.models import User
from calculator_projects.utils.constants import HOLIDAYS


# Create your models here.
class StagePlan(models.Model):
    description = models.CharField(max_length=200, blank=True, null=True)
    start_time = models.DateField()
    finish_time = models.DateField()
    stage_number = models.IntegerField(blank=True, null=True)
    duration_per_hour = models.IntegerField(default=0.0)
    duration_per_day = models.IntegerField(default=0.0)
    total_price = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)

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
        import numpy as np

        self.duration_per_day = np.busday_count(
            self.start_time, self.finish_time, holidays=HOLIDAYS
        )
        self.duration_per_hour = self.duration_per_day * 8
        labor_cost = LabourCost.objects.get(calculation_for_projects=True)
        salary_cost = labor_cost.salary_cost
        salary = self.projectPlan.coefficient_of_project * salary_cost
        self.total_price = self.duration_per_hour * (
            labor_cost.total_cost - salary_cost + salary
        )
        self.save()
