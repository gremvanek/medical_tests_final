from django.urls import path

from . import views

app_name = "medical_services"

urlpatterns = [
    path("contact/", views.contact_form, name="contact_form"),

    path('categories/', views.category_list_view, name='category-list'),
    path('categories/create/', views.category_create_view, name='category-create'),
    path('categories/<int:pk>/update/', views.category_update_view, name='category-update'),
    path('categories/<int:pk>/delete/', views.category_delete_view, name='category-delete'),

    path('carts/', views.cart_list_view, name='cart-list'),
    path('carts/create/', views.cart_create_view, name='cart-create'),
    path('carts/<int:pk>/update/', views.cart_update_view, name='cart-update'),
    path('carts/<int:pk>/delete/', views.cart_delete_view, name='cart-delete'),

    path('services/', views.service_list_view, name='services-list'),
    path('services/create/', views.service_create_view, name='service-create'),
    path('services/<int:pk>/update/', views.service_update_view, name='service-update'),
    path('services/<int:pk>/delete/', views.service_delete_view, name='service-delete'),
]
