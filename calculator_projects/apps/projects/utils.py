from datetime import datetime, timezone

from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404

from calculator_projects.apps.additionalCosts.models import AdditionalCostFact, AdditionalCostPlan
from calculator_projects.apps.labour_costs.models import LabourCost
from calculator_projects.apps.projects.constants import coefficient
from calculator_projects.apps.projects.models import ProjectCreationStage, ProjectFact, ProjectPlan, ProjectStatus
from calculator_projects.apps.stages.models import StageFact, StagePlan
from calculator_projects.apps.tasks.models import TaskFact, TaskFactStatus, TaskPlan
from calculator_projects.utils.constants import HOLIDAYS


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
        (total_cost - salary_cost - labour_cost.cost_price - labour_cost.contributions_to_IT_park) / total_cost * 100
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
    stage_list = StagePlan.objects.filter(deleted_status=False, projectPlan=project).exists()
    return stage_list


def project_plan_fields_regex(total_price_with_margin: str, tax_amount: str, margin_amount: str):
    from decimal import Decimal

    total_price_with_margin = total_price_with_margin.replace(" ", "").replace(",", ".").replace("сўм", "")
    project_tax = tax_amount.replace(" ", "").replace(",", ".").replace("сўм", "")
    margin = margin_amount.replace(" ", "").replace(",", ".").replace("сўм", "")

    return [Decimal(total_price_with_margin), Decimal(project_tax), Decimal(margin)]


def update_stages(project_plan, margin_percentage):
    from decimal import Decimal

    from calculator_projects.apps.stages.signals import update_project_plan_after_stage_change
    from calculator_projects.apps.stages.utils import disconnect_signal, reconnect_signal

    stage_list = StagePlan.objects.filter(projectPlan=project_plan)
    disconnect_signal(post_save, update_project_plan_after_stage_change, StagePlan)
    for stage in stage_list:
        stage.margin = stage.total_price_stage_and_task * margin_percentage
        total_price_without_tax = stage.total_price_without_tax()
        total_price_with_margin = stage.margin + total_price_without_tax
        stage.total_price_with_margin = total_price_with_margin / Decimal(0.99)
        stage.contributions_to_IT_park = stage.total_price_with_margin - total_price_with_margin
        stage.save()

    reconnect_signal(post_save, update_project_plan_after_stage_change, StagePlan)


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


def project_fact_header_info(project_fact):
    from django.db.models import Sum

    return project_fact.aggregate(
        project_fact_total_price_with_additional_cost=Sum("total_price_with_additional_cost"),
        project_fact_duration_per_hour=Sum("duration_per_hour"),
    )


def project_plan_header_info(project_plan_list):
    from django.db.models import Sum

    return project_plan_list.aggregate(
        project_plan_total_price_with_additional_cost=Sum("total_price_with_additional_cost"),
        project_plan_duration_per_hour=Sum("duration_per_hour"),
    )


def project_fact_task_amount(project_fact):
    from django.db.models import Count

    return project_fact.aggregate(project_fact_task_amount=Count("project_fact"))


def project_plan_task_amount(project_plan_list):
    from django.db.models import Count

    return project_plan_list.aggregate(project_plan_task_amount=Count("project_plan_task"))


def project_fields_generation(prefix, project, project_initial):
    project_initial["total_price_" + prefix] = project["total_price"]
    project_initial["total_expenses_" + prefix] = project["total_expenses"]
    project_initial["additional_cost_" + prefix] = project["additional_cost"]
    project_initial["margin_" + prefix] = project["margin"]
    project_initial["profitability_percentage_" + prefix] = project["profitability_percentage"]
    project_initial["duration_per_hour_" + prefix] = project["duration_per_hour"]
    return project_initial


def compare_fields(project_initial):
    project_initial["total_price_compare"] = project_initial["total_price_plan"] - project_initial["total_price_fact"]
    project_initial["total_expenses_compare"] = (
        project_initial["total_expenses_plan"] - project_initial["total_expenses_fact"]
    )
    project_initial["additional_cost_compare"] = (
        project_initial["additional_cost_plan"] - project_initial["additional_cost_fact"]
    )
    project_initial["margin_compare"] = project_initial["margin_fact"] - project_initial["margin_plan"]
    return project_initial


def generation_total_amount_fields(project_fact, project_plan):
    project_fact = generation_project(project_fact)
    project_plan = generation_project(project_plan)
    project_initial = {}
    project_initial = project_fields_generation("fact", project_fact, project_initial)
    project_initial = project_fields_generation("plan", project_plan, project_initial)
    project_initial["margin_fact"] = project_initial["total_price_plan"] - project_initial["total_price_fact"]
    project_initial["profitability_percentage_fact"] = (
        project_initial["margin_fact"] / project_initial["total_price_fact"]
    ) * 100
    project_initial["profitability_percentage_plan"] = (
        project_initial["margin_plan"] / project_initial["total_price_plan"]
    ) * 100
    project_initial = compare_fields(project_initial)

    return project_initial


def generation_project(qs):
    from django.db.models import Sum

    return qs.aggregate(
        total_price=Sum("total_price_with_additional_cost"),
        total_expenses=Sum("total_price_stage_and_task"),
        additional_cost=Sum("additional_cost"),
        margin=Sum("margin"),
        profitability_percentage=Sum("profitability_percentage"),
        duration_per_hour=Sum("duration_per_hour"),
    )


def dictionary_check(status_amount, project_fact_total_price):
    if status_amount is not None:
        return (status_amount / project_fact_total_price) * 100
    else:
        return 0


def generation_task_status_fields(user, project_fact_total_price):
    from django.db.models import Q, Sum

    task_fact_list = TaskFact.objects.filter(deleted_status=False, created_by=user)
    task_fact_list = task_fact_list.aggregate(
        plan=Sum("total_price", filter=Q(action_status=TaskFactStatus.PLAN)),
        active=Sum("total_price", filter=Q(action_status=TaskFactStatus.ACTIVE)),
        finish=Sum("total_price", filter=Q(action_status=TaskFactStatus.COMPLETED)),
        cancel=Sum("total_price", filter=Q(action_status=TaskFactStatus.CANCELLED)),
        on_hold=Sum("total_price", filter=Q(action_status=TaskFactStatus.ON_HOLD)),
    )

    task_fact_list["plan_p"] = dictionary_check(task_fact_list["plan"], project_fact_total_price)
    task_fact_list["active_p"] = dictionary_check(task_fact_list["active"], project_fact_total_price)
    task_fact_list["finish_p"] = dictionary_check(task_fact_list["finish"], project_fact_total_price)
    task_fact_list["cancel_p"] = dictionary_check(task_fact_list["cancel"], project_fact_total_price)
    task_fact_list["on_hold_p"] = dictionary_check(task_fact_list["on_hold"], project_fact_total_price)
    return task_fact_list


def generation_task_status_amount(user):
    from django.db.models import Count, Q

    task_fact_list = TaskFact.objects.filter(deleted_status=False, created_by=user)
    task_fact_status_amount = task_fact_list.aggregate(
        plan=Count("action_status", filter=Q(action_status=TaskFactStatus.PLAN)),
        active=Count("action_status", filter=Q(action_status=TaskFactStatus.ACTIVE)),
        finish=Count("action_status", filter=Q(action_status=TaskFactStatus.COMPLETED)),
        cancel=Count("action_status", filter=Q(action_status=TaskFactStatus.CANCELLED)),
        on_hold=Count("action_status", filter=Q(action_status=TaskFactStatus.ON_HOLD)),
    )
    return task_fact_status_amount


def generation_project_task_fact_and_plan_amount_by_project_fact(project_fact_list):
    projects = {}
    counter = 0
    for project in project_fact_list:
        counter += 1
        projects[f"project-{counter}"] = {
            "task_fact": project.task_fact_amount(),
            "task_plan": project.task_plan_amount(),
        }
    return projects


def project_change_status(pk, user, status):
    project = get_object_or_404(ProjectPlan, pk=pk)
    project.accepted_by = user
    project.project_status = status
    project.accepted_at = datetime.now(tz=timezone.utc)
    project.save()
    return project


def copy_project_plan_to_fact(project_plan):
    project_fact = ProjectFact()
    project_fact.__dict__.update(project_plan.__dict__)
    project_fact.project_plan = project_plan
    project_fact.save()
    return project_fact


def copy_stage_plan_to_fact(project_plan, project_fact_id):
    stage_plan_list = StagePlan.objects.filter(projectPlan=project_plan.id)
    project_fact = ProjectFact.objects.get(pk=project_fact_id)

    for stage_plan in stage_plan_list:
        stage_fact = StageFact()
        stage_fact.__dict__.update(stage_plan.__dict__)
        stage_fact.stage_plan = stage_plan
        stage_fact.project_fact = project_fact
        stage_fact.save()
        copy_plan_to_fact_task(stage_plan, stage_fact.id, project_fact)


def copy_plan_to_fact_task(stage_plan, stage_fact_id, project_fact):
    from calculator_projects.apps.stages.utils import disconnect_signal, reconnect_signal
    from calculator_projects.apps.tasks.signals import update_project_fact_stage_and_project_fact_change

    task_list = TaskPlan.objects.filter(stage=stage_plan.id)
    stage_fact = StageFact.objects.get(pk=stage_fact_id)
    disconnect_signal(post_save, update_project_fact_stage_and_project_fact_change, TaskFact)
    for task_plan in task_list:
        task_fact = TaskFact()
        task_fact.__dict__.update(task_plan.__dict__)
        task_fact.task_plan = task_plan
        task_fact.updated_at = datetime.now()
        task_fact.stage_fact = stage_fact
        task_fact.project_fact = project_fact
        task_fact.save()
    reconnect_signal(post_save, update_project_fact_stage_and_project_fact_change, TaskFact)


def copy_plan_to_fact_additional_cost(project_plan, project_fact):
    from calculator_projects.apps.additionalCosts.signals import updating_project_plan
    from calculator_projects.apps.stages.utils import disconnect_signal, reconnect_signal

    disconnect_signal(post_save, updating_project_plan, AdditionalCostFact)
    additional_cost_plan_list = AdditionalCostPlan.objects.filter(project=project_plan, deleted_status=False)
    for additional_cost_plan in additional_cost_plan_list:
        additional_cost_fact = AdditionalCostFact()
        additional_cost_fact.__dict__.update(additional_cost_plan.__dict__)
        additional_cost_fact.project = project_fact
        additional_cost_fact.save()
    reconnect_signal(post_save, updating_project_plan, AdditionalCostFact)


def separate_date(date):
    date_list = date.split("-")
    date_list[0] = date_list[0].strip()
    date_list[1] = date_list[1].strip()
    return date_list


def get_task_fact_datetime_from_string(date_string):
    from datetime import datetime

    date = datetime.strptime(date_string, "%d/%m/%Y %H:%M")
    return date


def get_time_dif_from_string(start, finish):
    from datetime import datetime

    start_time = datetime.strptime(start, "%H:%M:%S")
    end_time = datetime.strptime(finish, "%H:%M:%S")
    delta = end_time - start_time
    hours = delta.total_seconds() / (60 * 60)
    return hours


def checking_date_time(start_time, finish_time):
    return start_time.time() > finish_time.time()


def generation_two_date(date_list):
    return get_task_fact_datetime_from_string(date_list[0]), get_task_fact_datetime_from_string(date_list[1])


def regex_choose_date_range(daterange):
    import numpy as np

    start_time, finish_time = middle_function(daterange)
    if checking_date_time(start_time, finish_time):
        return False, {}
    else:
        duration_per_day_new = np.busday_count(start_time.date(), finish_time.date(), holidays=HOLIDAYS)
        hours = get_time_dif_from_string(str(start_time.time()), str(finish_time.time()))
        duration_per_hour = duration_per_day_new * 8 + hours
        return True, {
            "start_time": start_time,
            "finish_time": finish_time,
            "duration_per_day": duration_per_day_new,
            "duration_per_hour": duration_per_hour,
        }


def middle_function(daterange):
    date_list = separate_date(daterange)
    start_time, finish_time = generation_two_date(date_list)
    return start_time, finish_time


def process_formation_four_fields_percentage(project):
    project.percent_cost_price = project.cost_price / project.total_price_stage_and_task * 100
    project.percent_salary_cost = project.salary_cost / project.total_price_stage_and_task * 100
    project.percent_period_expenses = project.period_expenses / project.total_price_stage_and_task * 100
    project.percent_margin = project.margin / project.total_price_stage_and_task * 100
    project.save()


def process_formation_fields_with_additional_cost(project, additional_cost):
    from django.db.models import Sum

    add_costs = additional_cost.objects.filter(project=project, deleted_status=False)
    if add_costs:
        additional_cost_of_project = add_costs.aggregate(total_amount=Sum("amount"))
        project.additional_cost = additional_cost_of_project["total_amount"]
        project.total_price_with_additional_cost = (
            project.total_price_with_margin + additional_cost_of_project["total_amount"]
        )
    else:
        project.total_price_with_additional_cost = project.total_price_stage_and_task
        project.additional_cost = 0.0
    project.profitability_percentage = project.margin / project.total_price_with_additional_cost
    project.save()
