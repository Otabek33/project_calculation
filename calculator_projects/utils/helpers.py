import numpy as np

from calculator_projects.apps.labour_costs.models import LabourCost

from calculator_projects.utils.constants import HOLIDAYS


def is_ajax(request):
    return (
        True if request.headers.get("x-requested-with") == "XMLHttpRequest" else False
    )


def defining_duration_per_day(start_time, finish_time):
    return np.busday_count(start_time, finish_time, holidays=HOLIDAYS)


def defining_duration_per_hour(duration_per_hour):
    return duration_per_hour * 8


def defining_total_price(coefficient_of_project, duration_per_hour):
    labor_cost = LabourCost.objects.get(calculation_for_projects=True)
    salary_cost = labor_cost.salary_cost
    salary = coefficient_of_project * salary_cost
    total_price_stage_and_task = duration_per_hour * (
        labor_cost.total_cost - salary_cost + salary
    )
    return total_price_stage_and_task


def process_formation_fields_with_labour_cost(obj):
    from calculator_projects.apps.labour_costs.models import LabourCost
    labour_cost = LabourCost.objects.get(calculation_for_projects=True)
    obj.salary_cost = (
        obj.total_price_stage_and_task * labour_cost.percent_salary_cost
    )

    obj.cost_price = (
        obj.total_price_stage_and_task * labour_cost.percent_cost_price
    )
    obj.contributions_to_IT_park = (
        obj.total_price_stage_and_task
        * labour_cost.percent_contributions_to_IT_park
    )

    obj.period_expenses = (
        obj.total_price_stage_and_task * labour_cost.percent_period_expenses
    )
    obj.save()
