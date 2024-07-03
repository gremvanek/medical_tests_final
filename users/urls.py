# user.urls
from django.contrib.auth.views import LoginView
from django.urls import path

from users.views import user_list, user_detail, user_create, user_update, user_delete, user_logout, \
    ResetPasswordView, CustomPasswordResetConfirmView, RegisterView, activate_user

app_name = 'users'  # Пространство имен для приложения

urlpatterns = [
    path('users/', user_list, name='u_list'),
    path('user/<int:pk>/', user_detail, name='u_detail'),
    path('user/create/', user_create, name='u_create'),
    path('user/<int:pk>/update/', user_update, name='u_update'),
    path('user/<int:pk>/delete/', user_delete, name='u_delete'),
    path('', LoginView.as_view(template_name='users/u_login.html'), name='u_login'),
    path('user/verify/', activate_user, name='verify'),
    path('logout/', user_logout, name='u_logout'),
    path('register/', RegisterView.as_view(), name='u_register'),
    path('password_reset/', ResetPasswordView.as_view(), name='u_reset'),
    path('reset_password/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]