from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['codigo_verificacao', 'get_participante', 'get_evento', 
                    'carga_horaria', 'data_emissao', 'emitido_por']
    list_filter = ['data_emissao', 'inscricao__evento__tipo_evento']
    search_fields = ['codigo_verificacao', 'inscricao__usuario__username', 
                     'inscricao__usuario__first_name', 'inscricao__usuario__last_name',
                     'inscricao__evento__titulo']
    readonly_fields = ['codigo_verificacao', 'data_emissao']
    date_hierarchy = 'data_emissao'
    
    fieldsets = [
        ('Informações do Certificado', {
            'fields': ['inscricao', 'codigo_verificacao', 'carga_horaria']
        }),
        ('Emissão', {
            'fields': ['emitido_por', 'data_emissao']
        }),
        ('Observações', {
            'fields': ['observacoes'],
            'classes': ['collapse']
        }),
    ]
    
    def get_participante(self, obj):
        return obj.participante.get_full_name()
    get_participante.short_description = 'Participante'
    def get_evento(self, obj):
        return obj.evento.titulo
    get_evento.short_description = 'Evento'
