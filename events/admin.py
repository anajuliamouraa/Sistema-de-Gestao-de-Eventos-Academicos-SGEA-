from django.contrib import admin
from .models import Event, Inscription

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo_evento', 'data_inicio', 'data_fim', 
                    'local', 'vagas', 'vagas_disponiveis', 'organizador', 'ativo']
    list_filter = ['tipo_evento', 'ativo', 'data_inicio', 'data_criacao']
    search_fields = ['titulo', 'descricao', 'local', 'organizador__username']
    date_hierarchy = 'data_inicio'
    readonly_fields = ['vagas_disponiveis', 'data_criacao', 'data_atualizacao']
    
    fieldsets = [
        ('Informações Básicas', {
            'fields': ['titulo', 'descricao', 'tipo_evento', 'imagem']
        }),
        ('Data e Horário', {
            'fields': ['data_inicio', 'data_fim', 'horario_inicio', 'horario_fim']
        }),
        ('Local e Vagas', {
            'fields': ['local', 'vagas', 'vagas_disponiveis']
        }),
        ('Organização', {
            'fields': ['organizador', 'ativo']
        }),
        ('Metadados', {
            'fields': ['data_criacao', 'data_atualizacao'],
            'classes': ['collapse']
        }),
    ]

@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ['evento', 'usuario', 'status', 'data_inscricao']
    list_filter = ['status', 'data_inscricao', 'evento__tipo_evento']
    search_fields = ['evento__titulo', 'usuario__username', 'usuario__first_name', 'usuario__last_name']
    date_hierarchy = 'data_inscricao'
    
    fieldsets = [
        ('Inscrição', {
            'fields': ['evento', 'usuario', 'status']
        }),
        ('Informações Adicionais', {
            'fields': ['observacoes', 'data_inscricao']
        }),
    ]
    
    readonly_fields = ['data_inscricao']
