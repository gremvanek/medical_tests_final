import random

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import FormView, CreateView

from config import settings
from config.settings import EMAIL_HOST_USER
from .forms import UserForm, UserRegisterForm, CustomPasswordResetForm, LoginForm
from .models import User


# Список пользователей
@login_required
@permission_required("user.view_user", raise_exception=True)
def user_list(request):
    users = User.objects.all()
    return render(request, "users/u_list.html", {"users": users})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Подставьте URL для перехода после входа
            else:
                form.add_error(None, 'Неверные имя пользователя или пароль.')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


# Получение пользователя или обработка исключения
def get_user_or_404(pk):
    return get_object_or_404(User, pk=pk)


# Отображение деталей пользователя
@login_required
def user_detail(request, pk):
    user = get_user_or_404(pk)
    return render(request, "users/u_detail.html", {"user": user})


# Создание пользователя
@login_required
def user_create(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь успешно создан.")
            return redirect("users:u_list")
    else:
        form = UserForm()
    return render(request, "users/u_form.html", {"form": form})


# Редактирование пользователя
@login_required
def user_update(request, pk):
    user = get_user_or_404(pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь успешно отредактирован.")
            return redirect("users:u_list")
    else:
        form = UserForm(instance=user)
    return render(request, "users/u_form.html", {"form": form})


# Удаление пользователя
@login_required
def user_delete(request, pk):
    user = get_user_or_404(pk)
    user.delete()
    messages.success(request, "Пользователь успешно удален.")
    return redirect("users:user_list")


# Подтверждение почтового адреса пользователя
def activate_user(request, token):
    if token:
        try:
            user = User.objects.get(is_verified=False, token=token)
            user.is_verified = True
            user.token = None
            user.save()
            messages.success(request, "Пользователь успешно верифицирован.")
        except ObjectDoesNotExist:
            messages.error(request, "Пользователь не найден для верификации.")
    else:
        messages.error(request, "Неверный запрос для верификации.")

    return redirect('users:u_verification')


# Выход пользователя
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли.")
    return redirect("users:u_login")


# Регистрация нового пользователя
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:u_success")

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.is_verified = False
        secret_token = "".join([str(random.randint(0, 9)) for _ in range(10)])
        new_user.token = secret_token
        new_user.save()

        # Используйте reverse или reverse_lazy для создания URL
        verification_url = reverse_lazy("users:verify", kwargs={'token': secret_token})

        message = (
            f"Пожалуйста, подтвердите ваш адрес электронной почты, перейдя по ссылке: "
            f"{self.request.build_absolute_uri(verification_url)}"
        )
        send_mail(
            "Подтверждение адреса электронной почты",
            message,
            EMAIL_HOST_USER,
            [new_user.email],
            fail_silently=False,
        )

        messages.success(
            self.request,
            "На ваш email отправлено письмо с инструкциями по верификации.",
        )
        return super().form_valid(form)


def user_registration_success(request):
    template_name = "users/u_register.html"
    return render(request, template_name)


def user_verification(request):
    template_name = "users/u_verification.html"
    return render(request, template_name)


# Сброс пароля пользователя
class ResetPasswordView(FormView):
    form_class = CustomPasswordResetForm
    template_name = "users/change_password.html"
    success_url = reverse_lazy("users:u_login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_password_link = (
                f"http://{self.request.get_host()}/reset_password/{uid}/{token}/"
            )
            send_mail(
                "Сброс пароля",
                f"Ваш новый пароль: {new_password}. Или перейдите по ссылке для установки нового пароля: "
                f"{reset_password_link}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            messages.success(
                self.request,
                "На ваш email отправлено письмо с инструкциями по сбросу пароля.",
            )
        except ObjectDoesNotExist:
            messages.error(self.request, "Пользователь с таким email не найден.")
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


# Подтверждение сброса пароля пользователя
class CustomPasswordResetCompleteView(TemplateView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:u_login')
