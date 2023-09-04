from datetime import datetime

from django.db import models
from django.urls import reverse

from calculator_projects.apps.users.models import User


# Create your models here.
class LabourCost(models.Model):
    salary_cost = models.DecimalField(max_digits=25, decimal_places=10, default=0.0)
    cost_price = models.DecimalField(max_digits=25, decimal_places=10, default=0.0)
    period_expenses = models.DecimalField(max_digits=25, decimal_places=10, default=0.0)
    contributions_to_IT_park = models.DecimalField(
        max_digits=25, decimal_places=10, default=0.0
    )
    total_cost = models.DecimalField(max_digits=25, decimal_places=10, default=0.0)
    file_order = models.FileField(upload_to="uploads/finance/calculation_order/")
    report_month = models.CharField(max_length=25, blank=True, null=True)
    calculation_for_projects = models.BooleanField(default=False)

    percent_salary_cost = models.DecimalField(
        max_digits=25, decimal_places=10, default=0.0
    )
    percent_cost_price = models.DecimalField(
        max_digits=25, decimal_places=10, default=0.0
    )
    percent_period_expenses = models.DecimalField(
        max_digits=25, decimal_places=10, default=0.0
    )
    percent_contributions_to_IT_park = models.DecimalField(
        max_digits=25, decimal_places=10, default=0.0
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="labour_cost_created_by",
    )
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="labour_cost_updated_by",
    )
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.total_cost)

    def get_absolute_url(self):
        return reverse("app_namespace:view_name", args=[self.pk])

    def total_cost_calculation(self):
        self.total_cost = self.salary_cost + self.cost_price + self.period_expenses + self.contributions_to_IT_park

    def percentage_calculation(self):
        self.percent_salary_cost = self.salary_cost / self.total_cost
        self.percent_cost_price = self.cost_price / self.total_cost
        self.percent_period_expenses = self.period_expenses / self.total_cost
        self.percent_contributions_to_IT_park = (
            self.contributions_to_IT_park / self.total_cost
        )
        self.updated_at = datetime.now()
        self.save()

    class Meta:
        verbose_name = "Cтоимость труда в час"
        verbose_name_plural = "Cтоимость труда в час"
