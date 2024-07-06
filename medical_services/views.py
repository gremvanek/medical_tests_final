# medical_services/views.py
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from config import settings
from .forms import CategoryForm, ServiceForm, CartForm
from .models import Category, Service, Cart


class HomePageView(TemplateView):
    template_name = "main/index.html"


@require_POST
def contact_form(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        subject = request.POST.get("subject", "")
        message = request.POST.get("message", "")

        # Отправка электронной почты
        send_mail(
            subject,
            f"From: {name} <{email}>\n\n{message}",
            email,  # Используем email отправителя
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )


# Декоратор login_required для всех представлений
@login_required
def login_required_decorator(view_func):
    return method_decorator(login_required)(view_func)


# Представление для создания новой категории
class CategoryCreateView(View):

    @login_required_decorator
    def get(self, request):
        form = CategoryForm()
        return render(request, 'category_form.html', {'form': form})

    @login_required_decorator
    def post(self, request):
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category-list')
        return render(request, 'category_form.html', {'form': form})


# Представление для чтения списка категорий
class CategoryListView(View):

    @login_required_decorator
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'category_list.html', {'categories': categories})


# Представление для обновления категории
class CategoryUpdateView(View):

    @login_required_decorator
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)
        return render(request, 'category_form.html', {'form': form})

    @login_required_decorator
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-list')
        return render(request, 'category_form.html', {'form': form})


# Представление для удаления категории
class CategoryDeleteView(View):

    @login_required_decorator
    def post(self, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect('category-list')


# Представление для создания новой услуги
class ServiceCreateView(View):

    @login_required_decorator
    def get(self, request):
        form = ServiceForm()
        return render(request, 'service_form.html', {'form': form})

    @login_required_decorator
    def post(self, request):
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('medical_services:services-list')
        return render(request, 'service_form.html', {'form': form})


# Представление для чтения списка услуг
class ServiceListView(View):

    @login_required_decorator
    def get(self, request):
        services = Service.objects.all()
        return render(request, 'services_list.html', {'services': services})


# Представление для обновления услуги
class ServiceUpdateView(View):

    @login_required_decorator
    def get(self, request, pk):
        services = get_object_or_404(Service, pk=pk)
        form = ServiceForm(instance=services)
        return render(request, 'service_form.html', {'form': form})

    @login_required_decorator
    def post(self, request, pk):
        services = get_object_or_404(Service, pk=pk)
        form = ServiceForm(request.POST, request.FILES, instance=services)
        if form.is_valid():
            form.save()
            return redirect('services_list')
        return render(request, 'service_form.html', {'form': form})


# Представление для удаления услуги
class ServiceDeleteView(View):

    @login_required_decorator
    def post(self, pk):
        services = get_object_or_404(Service, pk=pk)
        services.delete()
        return redirect('services_list')


class CartCreateView(View):

    @login_required_decorator
    def get(self, request):
        form = CartForm()
        return render(request, 'cart_form.html', {'form': form})

    @login_required_decorator
    def post(self, request):
        form = CartForm(request.POST)
        if form.is_valid():
            cart = form.save(commit=False)
            cart.client = request.user  # Привязка текущего пользователя к корзине
            cart.save()
            form.save_m2m()  # Сохранение ManyToMany полей
            return redirect('cart-list')  # Перенаправление на страницу списка корзин
        return render(request, 'cart_form.html', {'form': form})


class CartListView(View):

    @login_required_decorator
    def get(self, request):
        carts = Cart.objects.all()
        return render(request, 'cart_list.html', {'carts': carts})


class CartUpdateView(View):

    @login_required_decorator
    def get(self, request, pk):
        cart = get_object_or_404(Cart, pk=pk)
        form = CartForm(instance=cart)
        return render(request, 'cart_form.html', {'form': form})

    @login_required_decorator
    def post(self, request, pk):
        cart = get_object_or_404(Cart, pk=pk)
        form = CartForm(request.POST, instance=cart)
        if form.is_valid():
            form.save()
            return redirect('cart-list')
        return render(request, 'cart_form.html', {'form': form})


class CartDeleteView(View):

    @login_required_decorator
    def post(self, pk):
        cart = get_object_or_404(Cart, pk=pk)
        cart.delete()
        return redirect('cart-list')
