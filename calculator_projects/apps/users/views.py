from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, TemplateView, UpdateView

from calculator_projects.apps.tasks.models import TaskFact
from calculator_projects.apps.users.forms import UserUpdateForm
from calculator_projects.apps.users.mixins import ProjectUsageRequiredMixin
from calculator_projects.apps.users.models import UserRoleTypes

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/user_detail.html"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = "users/user_form.html"
    form_class = UserUpdateForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return redirect("users:detail", pk=self.object.id)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


def login_request(request):
    if request.method == "POST":
        user = auth.authenticate(username=request.POST.get("username"), password=request.POST.get("password"))

        if user is not None:
            auth.login(request, user)
            return redirect("users:entrance")
        else:
            messages.error(request, "Неправильное имя пользователя или пароль")
            return redirect("users:login")

    if request.user.is_authenticated:
        return redirect("users:entrance")

    return render(request, "account/login.html")


class EntranceView(LoginRequiredMixin, TemplateView):
    template_name = "base.html"


entrance = EntranceView.as_view()


def logout(request):
    auth.logout(request)
    return redirect("users:login")


class WorkloadView(ProjectUsageRequiredMixin, ListView):
    model = TaskFact
    tm_path = "users/"
    tm_name = "workload.html"
    template_name = f"{tm_path}{tm_name}"

    def get_queryset(self):
        print("ishladi")
        qs = super().get_queryset()
        user_role = self.request.user.user_role
        if user_role == UserRoleTypes.SUPER_USER or user_role == UserRoleTypes.FINANCE:
            return qs.filter(deleted_status=False).order_by("worker")
        else:
            return qs.filter(deleted_status=False, created_by=self.request.user).order_by("worker")


workload = WorkloadView.as_view()
