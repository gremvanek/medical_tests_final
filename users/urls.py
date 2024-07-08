# user.urls
from django.contrib.auth.views import LoginView
from django.urls import path
from users.views import (
    user_list,
    user_detail,
    user_create,
    user_update,
    user_delete,
    user_logout,
    RegisterView,
    activate_user,
    user_registration_success,
    user_verification,
)

app_name = "users"

urlpatterns = [
    path("users/", user_list, name="u_list"),
    path("user/<int:pk>/", user_detail, name="u_detail"),
    path("user/create/", user_create, name="u_create"),
    path("user/create/success/", user_registration_success, name="u_success"),
    path("user/verification/success/", user_verification, name="u_verification"),
    path("user/<int:pk>/update/", user_update, name="u_update"),
    path("user/<int:pk>/delete/", user_delete, name="u_delete"),
    path(
        "login/", LoginView.as_view(template_name="users/u_login.html"), name="u_login"
    ),
    path("user/verify/<str:token>/", activate_user, name="verify"),
    path("logout/", user_logout, name="u_logout"),
    path("register/", RegisterView.as_view(), name="u_register"),
]
