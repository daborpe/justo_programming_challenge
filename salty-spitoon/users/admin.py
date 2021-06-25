from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import User, ManagerUser


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    list_display = ('email', 'first_name', 'last_name', 'role',
                    'created_at', 'is_active', 'is_superuser')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )


@admin.register(ManagerUser)
class ManagerUserAdmin(admin.ModelAdmin):
    list_display = ('manager', 'lackey', 'created_at')
