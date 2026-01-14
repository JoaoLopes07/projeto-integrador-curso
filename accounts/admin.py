from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'role',
        'is_staff', 'is_active'
    )

    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'telefone')

    fieldsets = UserAdmin.fieldsets + (
        ('Informações adicionais', {
            'fields': ('role', 'telefone', 'data_nascimento', 'avatar')
        }),
    )
