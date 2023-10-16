from calculator_projects.apps.stages.models import StagePlan, StageFact
from calculator_projects.apps.tasks.models import TaskPlan, TaskFact
from calculator_projects.utils.helpers import defining_total_price, process_formation_fields_with_labour_cost


def generation_fields(stage, task_list, task_amount):
    from django.db.models import Max, Min, Sum
    from datetime import datetime
    if task_amount > 0:
        stage.start_time = task_list.aggregate(Min("start_time"))["start_time__min"]
        stage.finish_time = task_list.aggregate(Max("finish_time"))["finish_time__max"]
        stage.duration_per_hour = task_list.aggregate(Sum("duration_per_hour"))[
            "duration_per_hour__sum"
        ]
        stage.duration_per_day = task_list.aggregate(Sum("duration_per_day"))[
            "duration_per_day__sum"
        ]
    else:
        stage.start_time = datetime.now()
        stage.finish_time = datetime.now()
        stage.duration_per_hour = 0
        stage.duration_per_day = 0

    stage.save()

    return stage


def stage_plan_update(obj):
    stage = StagePlan.objects.get(id=obj.stage.id)
    task_plan_list = TaskPlan.objects.filter(stage=stage,
                                             deleted_status=False
                                             )
    stage = generation_fields(stage, task_plan_list, len(task_plan_list))

    stage.total_price_stage_and_task = defining_total_price(stage.projectPlan.coefficient_of_project,
                                                            stage.duration_per_hour)
    stage.save()
    process_formation_fields_with_labour_cost(stage)


def stage_fact_update(obj):
    stage = StageFact.objects.get(id=obj.stage_fact.id)
    task_fact_list = TaskFact.objects.filter(stage_fact=stage,
                                             deleted_status=False
                                             )
    stage = generation_fields(stage, task_fact_list, len(task_fact_list))
    stage.total_price_stage_and_task = defining_total_price(stage.project_fact.coefficient_of_project,
                                                            stage.duration_per_hour)
    stage.save()
    process_formation_fields_with_labour_cost(stage)
