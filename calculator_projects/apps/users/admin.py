from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import decorators, get_user_model

from calculator_projects.apps.users.models import Department, JobTitle

User = get_user_model()

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://django-allauth.readthedocs.io/en/stable/advanced.html#admin
    admin.site.login = decorators.login_required(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    model = User
    list_display = [
        "username",
        "first_name",
        "last_name",
        "mid_name",
        "email",
        "user_role",
        "photo",
    ]
    list_editable = ["user_role"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "mid_name",
                    "email",
                    "user_role",
                    "deportment",
                    "job_title",
                    "photo",
                )
            },
        ),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    model = Department
    list_display = ["name"]


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    model = JobTitle
    list_display = [
        "name",
        "code",
    ]
