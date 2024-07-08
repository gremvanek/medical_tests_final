from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import CategoryForm, ServiceForm, CartForm
from .models import Category, Service, Cart
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "main/index.html"


def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        # Отправка электронной почты
        send_mail(
            subject,
            f'From: {name} <{email}>\n\n{message}',
            email,  # Используем email отправителя
            ['gremvanek@gmail.com'],  # Замените на адрес получателя
            fail_silently=False,
        )

        # Возвращаем сообщение об успешной отправке
        success_message = 'Сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время!'
        return HttpResponse(success_message)

    # Если запрос не POST, возвращаем пустой ответ с кодом 400
    return HttpResponse('Bad Request', status=400)


# Представление для создания новой категории
@login_required
def category_create_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('medical_services:category-list')
    else:
        form = CategoryForm()
    return render(request, 'medical_services/category_form.html', {'form': form})


# Представление для чтения списка категорий
@login_required
def category_list_view(request):
    categories = Category.objects.all()
    return render(request, 'medical_services/category_list.html', {'categories': categories})


# Представление для обновления категории
@login_required
def category_update_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('medical_services:category-list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'medical_services/category_form.html', {'form': form})


# Представление для удаления категории
@login_required
@require_POST  # Декоратор для POST-запросов
def category_delete_view(pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('medical_services:category-list')


# Представление для создания новой услуги
@login_required
def service_create_view(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('medical_services:services-list')
    else:
        form = ServiceForm()
    return render(request, 'medical_services/service_form.html', {'form': form})


# Представление для чтения списка услуг
@login_required
def service_list_view(request):
    services = Service.objects.all()
    return render(request, 'medical_services/services_list.html', {'services': services})


# Представление для обновления услуги
@login_required
def service_update_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('medical_services:services-list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'medical_services/service_form.html', {'form': form})


# Представление для удаления услуги
@login_required
@require_POST  # Декоратор для POST-запросов
def service_delete_view(pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    return redirect('medical_services:services-list')


# Представление для создания новой корзины
@login_required
def cart_create_view(request):
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            cart = form.save(commit=False)
            cart.client = request.user
            cart.save()
            form.save_m2m()
            return redirect('medical_services:cart-list')
    else:
        form = CartForm()
    return render(request, 'medical_services/cart_form.html', {'form': form})


# Представление для чтения списка корзин
@login_required
def cart_list_view(request):
    carts = Cart.objects.all()
    return render(request, 'medical_services/cart_list.html', {'carts': carts})


# Представление для обновления корзины
@login_required
def cart_update_view(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    if request.method == 'POST':
        form = CartForm(request.POST, instance=cart)
        if form.is_valid():
            form.save()
            return redirect('medical_services:cart-list')
    else:
        form = CartForm(instance=cart)
    return render(request, 'medical_services/cart_form.html', {'form': form})


# Представление для удаления корзины
@login_required
@require_POST  # Декоратор для POST-запросов
def cart_delete_view(pk):
    cart = get_object_or_404(Cart, pk=pk)
    cart.delete()
    return redirect('medical_services:cart-list')
