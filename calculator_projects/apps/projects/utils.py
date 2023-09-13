from django.shortcuts import get_object_or_404

from calculator_projects.apps.labour_costs.models import LabourCost
from calculator_projects.apps.projects.constants import coefficient
from calculator_projects.apps.projects.models import ProjectPlan, ProjectCreationStage
from calculator_projects.apps.stages.models import StagePlan


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
