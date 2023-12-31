import uuid
from datetime import datetime

from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

from calculator_projects.apps.users.models import Department, User


# Create your models here.
class ProjectResponsibleSubject(models.IntegerChoices):
    UZINFOCOM = 1, _("«Единый интегратор по созданию государственных информационных систем UZINFOCOM»")
    OTHER = 2, _("Другой")


# Create your models here.
class ProjectSourceOfFinancing(models.IntegerChoices):
    FRIKT = 1, _("ФРИКТ")
    GOVERNMENT_SECTOR = 2, _("Государственное учреждение")
    PRIVET_SECTOR = 3, _("Частный сектор")
    OTHER = 4, _("Другой")


class ProjectCustomerStatus(models.IntegerChoices):
    LAW_ENFORCEMENT = 1, _("ПРАВООХРАНИТЕЛЬНЫЕ ОРГАНЫ")
    CHARITY = 2, _("БЛАГОТВОРИТЕЛЬНОСТЬ")
    GOVERNMENT_SECTOR = 3, _("ГОССЕКТОР")
    AGROINDUSTRY = 4, _("АГРОПРОМЫШЛЕННОСТЬ")
    EDUCATION = 5, _("ОБРАЗОВАНИЕ")
    INTERNET_AND_INFORMATION_TECHNOLOGY = 6, _("ИНТЕРНЕТ И ИНФОРМАЦИОННЫЕ ТЕХНОЛОГИИ")
    MEDICINE = 7, _("МЕДИЦИНА")
    FINANCE = 8, _("ФИНАНСОВЫЕ ТЕХНОЛОГИИ")


class ProjectCreationStage(models.IntegerChoices):
    STAGE_1 = 1, _("Этап 1")
    # STAGE_2 = 2, _("Паспорт проекта")
    STAGE_2 = 2, _("Этап 2")
    STAGE_3 = 3, _("Этап 3")
    STAGE_4 = 4, _("В подтверждении")


# When creating project stage 5 is sending it to director to approve it

# Active: The project is currently being worked on by the project team.
# Completed: Work on the project has finished, and all deliverables/tasks have been completed.
# Cancelled: The project has not finished, and work on the project will not continue.
# On Hold: The project has not finished, and work on the project has been temporarily suspended.


class ProjectStatus(models.IntegerChoices):
    CREATION = 1, _("В создании")
    CONFORM = 2, _("В подтверждении")
    ACTIVE = 3, _("Активный")
    COMPLETED = 4, _("Завершенный")
    CANCELLED = 5, _("Отменено")
    ON_HOLD = 6, _("На удерживании")


# Project Phase
# Plan: The project workplan is being created.
# Build and Implement: The project solution is being created or launched.
# Transition & Close: Project deliverables are being finalized and handed
# off to the operational team.
# Completed: The project is completed. Ongoing operations and maintenance
# have been transitioned to the operational team.


class ProjectPhase(models.IntegerChoices):
    PLAN = 1, _("План")
    BUILD_AND_IMPLEMENT = 2, _("Активный")
    COMPLETED = 3, _("Завершенный")


class ProjectPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=True, null=True)
    customer = models.CharField(max_length=400, blank=True, null=True)
    responsible_subject_for_project = models.IntegerField(
        choices=ProjectResponsibleSubject.choices,
        default=ProjectResponsibleSubject.UZINFOCOM,
    )
    legal_basis = models.CharField(max_length=500, blank=True, null=True)
    source_of_financing = models.IntegerField(
        choices=ProjectSourceOfFinancing.choices,
        default=ProjectSourceOfFinancing.GOVERNMENT_SECTOR,
    )
    involved_in_development_country = models.BooleanField(default=True)

    expert_conclusion = models.FileField(upload_to="uploads/expert_conclusion")

    customer_status = models.IntegerField(
        choices=ProjectCustomerStatus.choices,
        default=ProjectCustomerStatus.GOVERNMENT_SECTOR,
    )

    purpose = RichTextField()
    objective = RichTextField()
    start_time = models.DateField()
    finish_time = models.DateField()
    expecting_results = RichTextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="_created_by",
    )
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="_updated_by",
    )
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_status = models.BooleanField(default=False)

    salary_cost = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)
    cost_price = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)
    period_expenses = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)

    contributions_to_IT_park = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)
    margin = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)
    total_price = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    total_price_stage_and_task = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    total_price_with_margin = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    total_price_with_additional_cost = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    additional_cost = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    duration_per_hour = models.IntegerField(default=0.0)
    duration_per_day = models.IntegerField(default=0.0)

    percent_salary_cost = models.DecimalField(max_digits=1000, decimal_places=20, default=0.0)
    percent_cost_price = models.DecimalField(max_digits=1000, decimal_places=20, default=0.0)
    percent_contributions_to_IT_park = models.DecimalField(max_digits=1000, decimal_places=20, default=0.0)
    percent_margin = models.DecimalField(max_digits=1000, decimal_places=20, default=0.0)
    percent_period_expenses = models.DecimalField(max_digits=1000, decimal_places=20, default=0.0)
    profitability_percentage = models.DecimalField(max_digits=1000, decimal_places=20, default=0.0)

    project_creation_stage = models.IntegerField(
        choices=ProjectCreationStage.choices, default=ProjectCreationStage.STAGE_1
    )
    project_status = models.IntegerField(choices=ProjectStatus.choices, default=ProjectStatus.CREATION)
    project_phase = models.IntegerField(choices=ProjectPhase.choices, default=ProjectPhase.PLAN)
    accepted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="accepted_by",
    )
    accepted_at = models.DateTimeField(blank=True, null=True)
    departament = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="project")
    coefficient_of_project = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "План Проект"
        verbose_name_plural = "План Проекты"

    def is_active(self):
        return self.project_status not in [ProjectStatus.CREATION, ProjectStatus.CONFORM]

    def stage_counter(self):
        return self.stageplan_set.filter(deleted_status=False).count()

    def task_counter(self):
        return self.project_plan_task.filter(deleted_status=False).count()

    def additional_cost_exist(self):
        return self.additionalcostplan_set.filter(deleted_status=False).exists()

    def additional_cost_list(self):
        return self.additionalcostplan_set.filter(deleted_status=False)

    def stage_list(self):
        from calculator_projects.apps.stages.models import StagePlan

        return StagePlan.objects.filter(projectPlan=self.id, deleted_status=False).order_by("stage_number")

    def additional_cost_plan_list(self):
        from calculator_projects.apps.additionalCosts.models import AdditionalCostPlan

        return AdditionalCostPlan.objects.filter(project=self.id, deleted_status=False)


class ProjectFact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=True, null=True)
    start_time = models.DateField()
    finish_time = models.DateField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="fact_created_by",
    )
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="fact_updated_by",
    )
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_status = models.BooleanField(default=False)

    salary_cost = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)
    cost_price = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)
    period_expenses = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)
    project_plan = models.ForeignKey(
        ProjectPlan,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="project_fact",
    )

    contributions_to_IT_park = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)
    margin = models.DecimalField(max_digits=1000, decimal_places=8, default=0.0)
    total_price_stage_and_task = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    total_price_with_margin = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    total_price_with_additional_cost = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    additional_cost = models.DecimalField(max_digits=1000, decimal_places=2, default=0.0)
    duration_per_hour = models.IntegerField(default=0.0)
    duration_per_day = models.IntegerField(default=0.0)

    percent_salary_cost = models.DecimalField(max_digits=1000, decimal_places=20, default=0.0)
    percent_cost_price = models.DecimalField(max_digits=1000, decimal_places=20, default=0.0)
    percent_contributions_to_IT_park = models.DecimalField(max_digits=1000, decimal_places=20, default=0.0)
    percent_margin = models.DecimalField(max_digits=1000, decimal_places=20, default=0.0)
    percent_period_expenses = models.DecimalField(max_digits=1000, decimal_places=20, default=0.0)
    profitability_percentage = models.DecimalField(max_digits=1000, decimal_places=20, default=0.0)

    project_status = models.IntegerField(choices=ProjectStatus.choices, default=ProjectStatus.ACTIVE)
    project_phase = models.IntegerField(choices=ProjectPhase.choices, default=ProjectPhase.BUILD_AND_IMPLEMENT)
    coefficient_of_project = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Факт Проект"
        verbose_name_plural = "Факт Проекты"

    def task_fact_amount(self):
        return self.project_fact.filter(deleted_status=False).count()

    def task_plan_amount(self):
        return self.project_plan.project_plan_task.filter(deleted_status=False).count()

    def additional_cost_list(self):
        from calculator_projects.apps.additionalCosts.models import AdditionalCostFact

        return AdditionalCostFact.objects.filter(project=self.id, deleted_status=False).order_by("created_at")

    def project_plan_additional_cost(self):
        return self.project_plan.additional_cost

    def project_plan_total_price_with_additional_cost(self):
        return self.project_plan.total_price_with_additional_cost

    def stage_list(self):
        from calculator_projects.apps.stages.models import StageFact

        return StageFact.objects.filter(project_fact=self.id, deleted_status=False).order_by("stage_number")

    def plan_fact_difference(self):
        return self.project_plan.total_price_with_additional_cost - self.total_price_with_additional_cost

    def task_fact_finish_status(self):
        from django.db.models import Q, Sum

        from calculator_projects.apps.tasks.models import TaskFact, TaskFactStatus

        task_fact_list = TaskFact.objects.filter(
            deleted_status=False, created_by=self.created_by, project_fact=self.id
        )
        task_fact_list = task_fact_list.aggregate(
            finish=Sum("total_price", filter=Q(action_status=TaskFactStatus.COMPLETED)),
        )
        if task_fact_list["finish"] is None:
            return task_fact_list, False
        else:
            return task_fact_list, True

    def completed_status(self):
        task_fact, status = self.task_fact_finish_status()

        if status:
            return round((task_fact["finish"] / self.total_price_stage_and_task * 100), 1)
        else:
            return 0
