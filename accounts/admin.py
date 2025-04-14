from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'phone_number', 'gender', 'is_staff')
    list_filter = ('gender', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username', 'phone_number')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': (
            'username', 'first_name', 'last_name', 'gender',
            'phone_number', 'date_of_birth', 'adress', 'emergency_contact'
        )}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
        )}),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Location'), {'fields': ('default_latitude', 'default_longitude')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
