from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 
                    'is_staff', 'is_active', 'telefone')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'telefone')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Pessoais', {
            'fields': ('telefone', 'data_nascimento', 'avatar')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Pessoais', {
            'fields': ('telefone', 'data_nascimento')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)