from django.contrib import admin
from django.urls import path, include

from medical_services.views import HomePageView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePageView.as_view(), name="index"),
    path("users/", include(("users.urls", "user"), namespace="users")),
    path(
        "med_serv/",
        include(("medical_services.urls", "med_services"), namespace="med_services"),
    ),
]
