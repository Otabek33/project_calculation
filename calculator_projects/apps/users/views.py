from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import auth, messages

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert self.request.user.is_authenticated  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


def login_request(request):
    if request.method == "POST":
        user = auth.authenticate(
            username=request.POST.get("username"), password=request.POST.get("password")
        )

        if user is not None:
            auth.login(request, user)
            return redirect("accounts:user-detail")
            # try:
            #     return redirect("accounts:user-detail", user.role.code)
            # except AttributeError:
            #     messages.error(request, 'Пользователь должен иметь роль!')
            # return redirect('accounts:login')
        else:
            messages.error(request, "Неправильное имя пользователя или пароль")
            return redirect("accounts:login")

    if request.user.is_authenticated:
        return redirect("users:user-detail", request.user.pk)

    return render(request, "account/login.html")
