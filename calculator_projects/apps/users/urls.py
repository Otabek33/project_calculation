from django.urls import path

from calculator_projects.apps.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    login_request,

)

app_name = "users"

urlpatterns = [
    path("", login_request, name="login"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
