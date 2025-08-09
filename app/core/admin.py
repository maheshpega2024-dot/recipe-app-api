"""
Django admin configuration for the core app.

"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


from core import models

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    """ users list"""
    ordering = ['id']
    list_display = ['email', 'name', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff']

    """for one user view"""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Important Dates', {'fields': ('last_login',)}),
    )

    search_fields = ['email']
    ordering = ['email']
    readonly_fields = ['last_login']

    """ for new user creation"""
    add_fieldsets = (
        (None, {
            #classes to style the form
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','name', 'is_active', 'is_staff','is_superuser')
        }
        ),
    )


admin.site.register(models.User, UserAdmin)

admin.site.register(models.Recipe)
