# medical_services/views.py
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'main/index.html'
