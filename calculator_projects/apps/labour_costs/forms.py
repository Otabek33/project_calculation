from django import forms

from calculator_projects.apps.labour_costs.mixin import AttachRequestToFormMixin
from calculator_projects.apps.labour_costs.models import LabourCost


class DateInput(forms.DateInput):
    input_type = "month"


class LabourCostAddForm(forms.ModelForm):
    report_month = forms.CharField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "month",
            }
        )
    )

    salary_cost = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={"class": "form-control amount", 'onchange': "findTotal()", "step": 0.0000000000000001}
        ),
        decimal_places=15,
        min_value=0,
        required=True,
    )
    cost_price = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={"class": "form-control amount", 'onchange': "findTotal()", "step": 0.0000000000000001}
        ),
        decimal_places=15,
        min_value=0,
        required=True,
    )

    contributions_to_IT_park = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={"class": "form-control amount", 'onchange': "findTotal()", "step": 0.0000000000000001}
        ),
        decimal_places=15,
        min_value=0,
        required=True,
    )
    period_expenses = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={"class": "form-control amount", 'onchange': "findTotal()", "step": 0.0000000000000001}
        ),
        decimal_places=15,
        min_value=0,
        required=True,
    )

    file_order = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
                          " application/vnd.ms-excel",
                "class": "form-control",
            }
        ),
        required=True,
    )

    class Meta:
        model = LabourCost
        fields = [
            "salary_cost",
            "cost_price",
            "contributions_to_IT_park",
            "period_expenses",
            "report_month",
            "file_order",
            "total_cost",
        ]

    widgets = {
        "salary_cost": forms.NumberInput(
            attrs={"class": "form-control", "step": 0.0000000000000001}
        ),
        "cost_price": forms.NumberInput(
            attrs={"class": "form-control", "step": 0.0000000000000001}
        ),
        "contributions_to_IT_park": forms.NumberInput(
            attrs={"class": "form-control", "step": 0.0000000000000001}
        ),
    }

    def save(self, commit=True):
        instance = super().save()
        instance.total_cost_calculation()
        instance.percentage_calculation()
        instance.save()
        return instance


class LabourCostUpdateForm(forms.ModelForm):
    report_month = forms.CharField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "month",
            }
        )
    )
    salary_cost = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "step": 0.0000000000000001}
        ),
        decimal_places=15,
        min_value=0,
        required=True,
    )
    cost_price = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "step": 0.0000000000000001}
        ),
        decimal_places=15,
        min_value=0,
        required=True,
    )

    contributions_to_IT_park = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "step": 0.0000000000000001}
        ),
        decimal_places=15,
        min_value=0,
        required=True,
    )
    period_expenses = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "step": 0.0000000000000001}
        ),
        decimal_places=15,
        min_value=0,
        required=True,
    )
    file_order = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
                          " application/vnd.ms-excel",
                "class": "form-control",
            }
        ),
        required=True,
    )

    class Meta:
        model = LabourCost
        fields = [
            "salary_cost",
            "cost_price",
            "contributions_to_IT_park",
            "period_expenses",
            "report_month",
            "file_order",
            "total_cost",
        ]

    def save(self, commit=True):
        instance = super().save()
        instance.total_cost_calculation()
        instance.percentage_calculation()
        instance.save()
        return instance

