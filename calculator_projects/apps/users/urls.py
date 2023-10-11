from django.urls import path

from calculator_projects.apps.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    login_request, entrance, logout, workload

)

app_name = "users"

urlpatterns = [
    path("", login_request, name="login"),
    path("logout/", logout, name="logout"),
    path("~main-page", entrance, name="entrance"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/<uuid:pk>", view=user_update_view, name="update"),
    path("<uuid:pk>/", view=user_detail_view, name="detail"),
    path("~workload/", workload, name="workload"),
]
