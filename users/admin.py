from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active', 'is_staff')
    fieldsets = (
        (None, {
            "fields": (
                'email',
                'password'
            ),
        }),
        (
            'Personal Info', {
                "fields": (
                    'first_name',
                    'last_name',
                    'address',
                    'phone_number',
                )
            }
        ),
        (
            'Permissions',{
                'fields':
                (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions'
                )
            }
        ),
        (
            'Important Dates',{
                'fields':(
                    'last_login',
                    'date_joined'
                )
            }
        )
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','password1','password2','is_active','is_staff')
        })
    )
    ordering = ('email',)
admin.site.register(User, CustomUserAdmin)