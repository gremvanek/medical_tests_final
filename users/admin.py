from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'avatar', 'is_superuser', 'is_staff', 'country', 'have_permissions', 'is_blocked')
