from django.contrib import admin
from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['codigo_verificacao', 'get_participante', 'get_evento', 'carga_horaria', 'data_emissao']
    list_filter = ['data_emissao', 'carga_horaria']
    search_fields = ['codigo_verificacao', 'inscricao__usuario__username', 'inscricao__evento__titulo']
    date_hierarchy = 'data_emissao'
    ordering = ['-data_emissao']
    readonly_fields = ['codigo_verificacao', 'data_emissao']
    raw_id_fields = ['inscricao', 'emitido_por']
    
    def get_participante(self, obj):
        return obj.participante.get_full_name()
    get_participante.short_description = 'Participante'
    
    def get_evento(self, obj):
        return obj.evento.titulo
    get_evento.short_description = 'Evento'
