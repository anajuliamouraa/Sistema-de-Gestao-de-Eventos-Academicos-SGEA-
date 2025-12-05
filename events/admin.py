from django.contrib import admin
from .models import Event, Inscription


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo_evento', 'data_inicio', 'data_fim', 'local', 'vagas', 'vagas_disponiveis', 'ativo']
    list_filter = ['tipo_evento', 'ativo', 'data_inicio']
    search_fields = ['titulo', 'descricao', 'local']
    date_hierarchy = 'data_inicio'
    readonly_fields = ['vagas_disponiveis', 'data_criacao', 'data_atualizacao']
    ordering = ['-data_inicio']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'tipo_evento', 'banner')
        }),
        ('Data e Local', {
            'fields': ('data_inicio', 'data_fim', 'horario_inicio', 'horario_fim', 'local')
        }),
        ('Vagas e Status', {
            'fields': ('vagas', 'vagas_disponiveis', 'ativo')
        }),
        ('Responsáveis', {
            'fields': ('organizador', 'professor_responsavel')
        }),
        ('Informações do Sistema', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'evento', 'status', 'presenca_confirmada', 'data_inscricao']
    list_filter = ['status', 'presenca_confirmada', 'data_inscricao']
    search_fields = ['usuario__username', 'usuario__email', 'evento__titulo']
    date_hierarchy = 'data_inscricao'
    ordering = ['-data_inscricao']
    raw_id_fields = ['usuario', 'evento']
