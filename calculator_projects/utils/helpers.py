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
    total_price = duration_per_hour * (
        labor_cost.total_cost - salary_cost + salary
    )
    return total_price


# def update_stage_modal_date(stage_id):
#     from django.db.models import Max, Min, Sum
#     # stage = StagePlan.objects.get(id=stage_id)
#     # task_plan_list = TaskPlan.objects.filter(stage=stage,
#     #                                          deleted_status=False
#     #                                          )
#     # stage.start_time = task_plan_list.aggregate(Min("start_time"))["start_time__min"]
#     # stage.finish_time = task_plan_list.aggregate(Max("finish_time"))["finish_time__max"]
#     # stage.duration_per_hour = task_plan_list.aggregate(Sum("duration_per_hour"))[
#     #     "duration_per_hour__sum"
#     # ]
#     # stage.duration_per_day = task_plan_list.aggregate(Sum("duration_per_day"))[
#     #     "duration_per_day__sum"
#     # ]
#     # stage.total_price = defining_total_price(stage.projectPlan.coefficient_of_project, stage.duration_per_hour)
#     # stage.save()
