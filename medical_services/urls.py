from django.urls import path

from .views import contact_form

app_name = 'medical_services'

urlpatterns = [
    path('contact/', contact_form, name='contact_form'),
]
