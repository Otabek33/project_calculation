from ckeditor.widgets import CKEditorWidget
from django import forms

from calculator_projects.apps.projects.models import ProjectResponsibleSubject, ProjectCustomerStatus, \
    ProjectSourceOfFinancing, ProjectPlan


class DateInput(forms.DateInput):
    input_type = "date"


class ProjectCreateForm(forms.ModelForm):
    start_time = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
            }
        )
    )
    finish_time = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    involved_in_development_country = (
        forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-control"})),
    )

    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    customer = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )

    legal_basis = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "row": 1}), required=True
    )

    responsible_subject_for_project = forms.Field(
        widget=forms.Select(
            choices=ProjectResponsibleSubject.choices, attrs={"class": "form-control"}
        ),
    )

    customer_status = forms.Field(
        widget=forms.Select(
            choices=ProjectCustomerStatus.choices, attrs={"class": "form-control"}
        ),
    )

    source_of_financing = forms.Field(
        widget=forms.Select(
            choices=ProjectSourceOfFinancing.choices, attrs={"class": "form-control"}
        ),
    )

    expert_conclusion = forms.FileField(
        widget=forms.FileInput(attrs={"class": "form-control"}), required=True
    )

    purpose = forms.CharField(widget=CKEditorWidget()),
    objective = forms.CharField(widget=CKEditorWidget()),
    expecting_results = forms.CharField(widget=CKEditorWidget()),

    class Meta:
        model = ProjectPlan
        fields = [
            "name",
            "customer",
            "responsible_subject_for_project",
            "legal_basis",
            "involved_in_development_country",
            "customer_status",
            "purpose",
            "objective",
            "start_time",
            "finish_time",
            "source_of_financing",
            "expecting_results",
            "expert_conclusion",
        ]

    widgets = {
        "name": forms.TextInput(attrs={"class": "form-control"}),
        "customer": forms.TextInput(attrs={"class": "form-control"}),
        "legal_basis": forms.Textarea(attrs={"class": "form-control", "row": 1}),
        "expert_conclusion": forms.FileInput(attrs={"class": "form-control"}),
        # "coefficient": forms.Select(attrs={"class": "form-control", }),
    }

    # def clean(self):
    #     from utils.helpers import checking_date
    #     cleaned_data = super().clean()
    #     checking_date(self, cleaned_data)
    #     return cleaned_data
    #
    # def save(self, commit=True):
    #     instance = super(ProjectCreateForm, self).save(commit=True)
    #     if not instance.coefficient_of_project:
    #         instance.coefficient_of_project = 1
    #         instance.save()
    #     return instance
