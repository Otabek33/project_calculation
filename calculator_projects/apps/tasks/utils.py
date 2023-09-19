from calculator_projects.apps.stages.models import StagePlan
from calculator_projects.apps.tasks.models import TaskPlan
from calculator_projects.utils.helpers import defining_total_price, process_formation_fields_with_labour_cost


def stage_plan_update(obj):
    from django.db.models import Max, Min, Sum
    stage = StagePlan.objects.get(id=obj.stage.id)
    task_plan_list = TaskPlan.objects.filter(stage=stage,
                                             deleted_status=False
                                             )
    stage.start_time = task_plan_list.aggregate(Min("start_time"))["start_time__min"]
    stage.finish_time = task_plan_list.aggregate(Max("finish_time"))["finish_time__max"]
    stage.duration_per_hour = task_plan_list.aggregate(Sum("duration_per_hour"))[
        "duration_per_hour__sum"
    ]
    stage.duration_per_day = task_plan_list.aggregate(Sum("duration_per_day"))[
        "duration_per_day__sum"
    ]
    stage.total_price_stage_and_task = defining_total_price(stage.projectPlan.coefficient_of_project,
                                                            stage.duration_per_hour)
    stage.save()
    process_formation_fields_with_labour_cost(stage)
