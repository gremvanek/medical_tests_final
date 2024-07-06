from django.contrib import admin
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView

from django.urls import path, include

from medical_services.views import HomePageView
from users.views import CustomPasswordResetCompleteView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePageView.as_view(), name="index"),
    path("user/", include(("users.urls", "users"), namespace="user")),
    path('reset_password/', PasswordResetView.as_view(), name='reset_password'),
    path('reset_password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path(
        "med_serv/",
        include(("medical_services.urls", "med_services"), namespace="med_services"),
    ),
]
