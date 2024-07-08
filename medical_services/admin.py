from django.contrib import admin

from medical_services.models import Category, Service, Cart


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'category', 'deadline')
    list_filter = ('name', 'description', 'price', 'category', 'deadline')
    search_fields = ()
    list_per_page = 10


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('client',)
    list_filter = ('client',)
