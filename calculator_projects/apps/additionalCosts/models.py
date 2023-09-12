from datetime import datetime
from django.utils.translation import gettext_lazy as _

from django.db import models
from calculator_projects.apps.users.models import User

from calculator_projects.apps.projects.models import ProjectPlan


class AdditionalCostType(models.IntegerChoices):
    OUTSOURCING = 1, _("Аутсорсинг")
    EQUIPMENT = 2, _("Оборудование")
    OTHER_EXPENSES = 3, _("Прочие расходы")


# Create your models here.
class AdditionalCostPlan(models.Model):
    cost_type = models.IntegerField(
        choices=AdditionalCostType.choices,
        default=AdditionalCostType.OTHER_EXPENSES,
    )
    comment = models.TextField(max_length=500, blank=True, null=True)
    amount = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    project = models.ForeignKey(
        ProjectPlan, on_delete=models.CASCADE, blank=True, null=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="additional_cost_created_by",
    )
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="additional_cost_updated_by",
    )
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.comment

    class Meta:
        verbose_name = "План Доп. расход"
        verbose_name_plural = "План Доп. расходы"
