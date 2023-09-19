from calculator_projects.apps.projects.models import ProjectPlan
from calculator_projects.utils.helpers import process_formation_fields_with_labour_cost


def project_plan_update(obj):
    from django.db.models import Max, Min, Sum
    from calculator_projects.apps.stages.models import StagePlan
    project_plan = ProjectPlan.objects.get(id=obj.projectPlan.id)
    stage_plan_list = StagePlan.objects.filter(
        deleted_status=False, projectPlan=project_plan.id
    )

    project_plan.duration_per_hour = stage_plan_list.aggregate(Sum("duration_per_hour"))[
        "duration_per_hour__sum"
    ]
    project_plan.duration_per_day = stage_plan_list.aggregate(Sum("duration_per_day"))[
        "duration_per_day__sum"
    ]
    project_plan.total_price_stage_and_task = stage_plan_list.aggregate(Sum("total_price_stage_and_task"))[
        "total_price_stage_and_task__sum"
    ]
    project_plan.start_time = stage_plan_list.aggregate(Min("start_time"))[
        "start_time__min"
    ]
    project_plan.finish_time = stage_plan_list.aggregate(Max("finish_time"))[
        "finish_time__max"
    ]
    project_plan.total_price_with_margin = project_plan.total_price_stage_and_task
    project_plan.save()
    process_formation_fields_with_labour_cost(project_plan)
