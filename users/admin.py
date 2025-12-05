from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'perfil', 'instituicao_ensino', 'email_confirmed', 'is_active']
    list_filter = ['perfil', 'email_confirmed', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'instituicao_ensino']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('telefone', 'instituicao_ensino', 'perfil', 'email_confirmed', 'activation_code', 'activation_code_expires')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('telefone', 'instituicao_ensino', 'perfil')
        }),
    )
