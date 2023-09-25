from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404

from calculator_projects.apps.labour_costs.models import LabourCost
from calculator_projects.apps.projects.constants import coefficient
from calculator_projects.apps.projects.models import ProjectPlan, ProjectCreationStage, ProjectStatus
from calculator_projects.apps.stages.models import StagePlan
from calculator_projects.apps.stages.signals import update_project
from calculator_projects.apps.stages.utils import disconnect_signal, reconnect_signal


def get_coefficient(post_coefficient: str):
    return coefficient.get(post_coefficient)


def process_context_percentage_labour_cost(pk: str):
    project = get_object_or_404(ProjectPlan, pk=pk)
    labour_cost = LabourCost.objects.get(calculation_for_projects=True)

    salary_cost = labour_cost.salary_cost * project.coefficient_of_project
    total_cost = labour_cost.total_cost - labour_cost.salary_cost + salary_cost
    p_salary_cost = salary_cost / total_cost * 100
    p_cost_price = labour_cost.cost_price / total_cost * 100
    p_percent_period_expenses = (
        (
            total_cost
            - salary_cost
            - labour_cost.cost_price
            - labour_cost.contributions_to_IT_park
        )
        / total_cost
        * 100
    )
    p_tax = labour_cost.contributions_to_IT_park / total_cost * 100

    context = {
        "labour_cost": labour_cost,
        "projectplan": project,
        "total_cost": total_cost,
        "salary_cost": salary_cost,
        "p_salary_cost": p_salary_cost,
        "p_cost_price": p_cost_price,
        "p_percent_period_expenses": p_percent_period_expenses,
        "p_tax": p_tax,
    }
    return context


def checking_stage_exist(project):
    stage_list = StagePlan.objects.filter(
        deleted_status=False, projectPlan=project
    ).exists()
    return stage_list


def project_plan_fields_regex(total_price_with_margin: str, tax_amount: str, margin_amount: str):
    from decimal import Decimal
    total_price_with_margin = (
        total_price_with_margin.replace(" ", "").replace(",", ".").replace("сўм", "")
    )
    project_tax = tax_amount.replace(" ", "").replace(",", ".").replace("сўм", "")
    margin = margin_amount.replace(" ", "").replace(",", ".").replace("сўм", "")

    return [Decimal(total_price_with_margin), Decimal(project_tax), Decimal(margin)]


def update_stages(project_plan, margin_percentage):
    from decimal import Decimal
    stage_list = StagePlan.objects.filter(projectPlan=project_plan)
    disconnect_signal(post_save, update_project, StagePlan)
    for stage in stage_list:
        stage.margin = stage.total_price_stage_and_task * margin_percentage
        total_price_without_tax = stage.total_price_without_tax()
        total_price_with_margin = stage.margin + total_price_without_tax
        stage.total_price_with_margin = total_price_with_margin / Decimal(0.99)
        stage.contributions_to_IT_park = stage.total_price_with_margin - total_price_with_margin
        stage.save()

    reconnect_signal(post_save, update_project, StagePlan)


def stage_amount(project):
    from django.db.models import Count, Q
    project_stage_list = project.aggregate(
        stage_1=Count(
            "project_creation_stage",
            filter=(Q(project_creation_stage=ProjectCreationStage.STAGE_1)),
        ),
        stage_2=Count(
            "project_creation_stage",
            filter=Q(project_creation_stage=ProjectCreationStage.STAGE_2),
        ),
        stage_3=Count(
            "project_creation_stage",
            filter=Q(project_creation_stage=ProjectCreationStage.STAGE_3),
        ),
        stage_4=Count(
            "project_creation_stage",
            filter=Q(project_creation_stage=ProjectCreationStage.STAGE_4),
        ),
    )
    return project_stage_list


def project_amount(project):
    from django.db.models import Count, Q
    project_status_list = project.aggregate(
        cancelled=Count(
            "project_status",
            filter=Q(project_status=ProjectStatus.CANCELLED),
        ),
        conform=Count(
            "project_status",
            filter=Q(project_status=ProjectStatus.CONFORM),
        ),
        active=Count(
            "project_status",
            filter=Q(project_status=ProjectStatus.ACTIVE),
        ),
    )
    return project_status_list
