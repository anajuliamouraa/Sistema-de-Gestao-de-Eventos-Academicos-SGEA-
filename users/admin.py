from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'perfil', 'instituicao_ensino', 'is_active']
    list_filter = ['perfil', 'is_active', 'is_staff', 'data_cadastro']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'instituicao_ensino']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('telefone', 'instituicao_ensino', 'perfil')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('telefone', 'instituicao_ensino', 'perfil')
        }),
    )
