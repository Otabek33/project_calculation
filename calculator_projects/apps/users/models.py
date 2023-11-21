import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoleTypes(models.IntegerChoices):
    FINANCE = 1, _("Финансист")
    PROJECT_MANAGER = 2, _("Менеджер проекта")
    BUSINESS_ANALYTIC = 3, _("Бизнес-аналитик")
    SUPER_USER = 4, _("Супер пользователь")
    PUBLIC_USER = 5, _("Пользователь")


class JobTitle(models.Model):
    name = models.CharField(_("Должность"), blank=True, max_length=55)
    code = models.CharField(_("Код"), max_length=55)

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Название рабочих должностей"

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    name = models.CharField(_("Подразделение"), max_length=155, blank=True, null=True)
    code = models.CharField(_("Код"), max_length=55, default=0.0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = _("Подразделение")
        verbose_name_plural = _("Подразделении")


class User(AbstractUser):
    """
    Default custom user model for calculator-projects.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_("Имя"), max_length=50, blank=True, null=True)
    last_name = models.CharField(_("Фамилия"), max_length=50, blank=True, null=True)
    mid_name = models.CharField(_("Отчество"), max_length=50, blank=True, null=True)
    email = models.EmailField(_("Эл.почта"), blank=True, default="uzinfocom@gmail.com")
    photo = models.ImageField(upload_to="avatars", default="media/avatars/user.png")
    user_role = models.IntegerField(
        _("Тип пользователя"), choices=UserRoleTypes.choices, default=UserRoleTypes.PUBLIC_USER
    )
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True, blank=True)
    deportment = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="deportment",
    )

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def user_role_display(self):
        """
        Get user role display name.
        """
        return UserRoleTypes(self.user_role).label

    @property
    def is_finance(self):
        return self.user_role == UserRoleTypes.FINANCE

    @property
    def is_pm(self):
        return self.user_role == UserRoleTypes.PROJECT_MANAGER

    @property
    def is_business_analytic(self):
        return self.user_role == UserRoleTypes.BUSINESS_ANALYTIC

    @property
    def is_universal_user(self):
        return self.user_role == UserRoleTypes.PUBLIC_USER

    @property
    def is_super_user(self):
        return self.user_role == UserRoleTypes.SUPER_USER
