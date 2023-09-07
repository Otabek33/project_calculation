from calculator_projects.apps.labour_costs.models import LabourCost


def labour_cost_change_status(labour_cost):
    LabourCost.objects.filter(deleted_status=False).update(calculation_for_projects=False)
    labour_cost.calculation_for_projects = True
    labour_cost.save()
