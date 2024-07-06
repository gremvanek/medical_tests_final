from django.urls import path

from . import views
from .views import *

app_name = "medical_services"

urlpatterns = [
    path("contact/", views.contact_form, name="contact_form"),

    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),

    path('carts/', CartListView.as_view(), name='cart-list'),
    path('carts/create/', CartCreateView.as_view(), name='cart-create'),
    path('carts/<int:pk>/update/', CartUpdateView.as_view(), name='cart-update'),
    path('carts/<int:pk>/delete/', CartDeleteView.as_view(), name='cart-delete'),

    path('services/', ServiceListView.as_view(), name='services-list'),
    path('services/create/', ServiceCreateView.as_view(), name='service-create'),
    path('services/<int:pk>/update/', ServiceUpdateView.as_view(), name='service-update'),
    path('services/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service-delete'),
]
