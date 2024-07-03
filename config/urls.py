from django.contrib import admin
from django.urls import path, include

from medical_services.views import HomePageView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("main/", HomePageView.as_view(), name="index"),
    path('', include(('users.urls', 'user'), namespace='users')),
    path('', include('medical_services.urls')),
]
