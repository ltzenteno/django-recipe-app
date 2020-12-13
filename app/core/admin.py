from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    # overriding values from `BaseUserAdmin`
    ordering = ['id']
    list_display = ['email', 'name']

    # to make the user change page work with our custom model
    # each tuple is a section
    fieldsets = (
        # title, fields
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important Dates'), {'fields': ('last_login',)}),
    )

    # to make the user add page work
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
         ),
    )


admin.site.register(models.User, UserAdmin)
