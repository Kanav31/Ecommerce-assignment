from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Extends Django's built-in UserAdmin.
    We override fieldsets because our model has no `username` field —
    showing it would cause a crash.
    """
    list_display  = ('email', 'name', 'role', 'is_active', 'created_at')
    list_filter   = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'name')
    ordering      = ('-created_at',)

    # Controls what fields appear on the edit user page in admin
    fieldsets = (
        (None,           {'fields': ('email', 'password')}),
        ('Personal',     {'fields': ('name', 'role')}),
        ('Permissions',  {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # Controls what fields appear on the create user page in admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':  ('email', 'name', 'role', 'password1', 'password2'),
        }),
    )
