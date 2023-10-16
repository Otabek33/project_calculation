from calculator_projects.apps.additionalCosts.models import AdditionalCostFact
from calculator_projects.apps.projects.models import ProjectPlan, ProjectFact
from calculator_projects.apps.projects.utils import process_formation_four_fields_percentage, \
    process_formation_fields_with_additional_cost
from calculator_projects.apps.stages.models import StageFact
from calculator_projects.utils.helpers import process_formation_fields_with_labour_cost


def generation_fields(project, stage_list, stage_amount):
    from django.db.models import Max, Min, Sum
    from datetime import datetime
    if stage_amount > 0:
        project.duration_per_hour = stage_list.aggregate(Sum("duration_per_hour"))[
            "duration_per_hour__sum"
        ]
        project.duration_per_day = stage_list.aggregate(Sum("duration_per_day"))[
            "duration_per_day__sum"
        ]
        project.total_price_stage_and_task = stage_list.aggregate(Sum("total_price_stage_and_task"))[
            "total_price_stage_and_task__sum"
        ]
        project.start_time = stage_list.aggregate(Min("start_time"))[
            "start_time__min"
        ]
        project.finish_time = stage_list.aggregate(Max("finish_time"))[
            "finish_time__max"
        ]
    else:
        project.start_time = datetime.now()
        project.finish_time = datetime.now()
        project.duration_per_hour = 0
        project.duration_per_day = 0
        project.total_price_stage_and_task = 0
    project.save()
    return project


def project_plan_update(obj):
    from calculator_projects.utils.helpers import process_formation_fields_with_labour_cost
    from calculator_projects.apps.stages.models import StagePlan
    project_plan = ProjectPlan.objects.get(id=obj.projectPlan.id)
    stage_plan_list = StagePlan.objects.filter(
        deleted_status=False, projectPlan=project_plan.id
    )
    project_plan = generation_fields(project_plan, stage_plan_list, len(stage_plan_list))
    project_plan.save()
    process_formation_fields_with_labour_cost(project_plan)


def project_fact_update(obj):
    project_fact = ProjectFact.objects.get(id=obj.project_fact.id)
    stage_fact_list = StageFact.objects.filter(
        deleted_status=False, project_fact=project_fact.id
    )
    project_fact = generation_fields(project_fact, stage_fact_list, len(stage_fact_list))
    project_fact.save()
    process_formation_fields_with_labour_cost(project_fact)
    process_formation_four_fields_percentage(project_fact)
    project_fact.total_price_with_margin = project_fact.total_price_stage_and_task + project_fact.margin
    process_formation_fields_with_additional_cost(project_fact, AdditionalCostFact)


def disconnect_signal(signal, receiver, sender):
    disconnect = getattr(signal, 'disconnect')
    disconnect(receiver, sender)


def reconnect_signal(signal, receiver, sender):
    connect = getattr(signal, 'connect')
    connect(receiver, sender=sender)
