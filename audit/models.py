from django.db import models
from django.conf import settings
from django.utils import timezone


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('USER_CREATED', 'Criação de Usuário'),
        ('USER_LOGIN', 'Login de Usuário'),
        ('USER_LOGOUT', 'Logout de Usuário'),
        ('USER_EMAIL_CONFIRMED', 'Confirmação de Email'),
        ('EVENT_CREATED', 'Criação de Evento'),
        ('EVENT_UPDATED', 'Alteração de Evento'),
        ('EVENT_DELETED', 'Exclusão de Evento'),
        ('EVENT_API_QUERY', 'Consulta de Evento via API'),
        ('INSCRIPTION_CREATED', 'Inscrição em Evento'),
        ('INSCRIPTION_CANCELLED', 'Cancelamento de Inscrição'),
        ('INSCRIPTION_API', 'Inscrição via API'),
        ('CERTIFICATE_GENERATED', 'Geração de Certificado'),
        ('CERTIFICATE_VIEWED', 'Visualização de Certificado'),
        ('CERTIFICATE_DOWNLOADED', 'Download de Certificado'),
        ('CERTIFICATE_AUTO_GENERATED', 'Certificado Gerado Automaticamente'),
        ('PRESENCE_CONFIRMED', 'Presença Confirmada'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        verbose_name='Usuário'
    )
    action = models.CharField('Ação', max_length=30, choices=ACTION_CHOICES)
    description = models.TextField('Descrição', blank=True, null=True)
    ip_address = models.GenericIPAddressField('Endereço IP', blank=True, null=True)
    user_agent = models.TextField('User Agent', blank=True, null=True)
    object_type = models.CharField('Tipo de Objeto', max_length=100, blank=True, null=True)
    object_id = models.PositiveIntegerField('ID do Objeto', blank=True, null=True)
    object_repr = models.CharField('Representação do Objeto', max_length=255, blank=True, null=True)
    extra_data = models.JSONField('Dados Extras', blank=True, null=True)
    timestamp = models.DateTimeField('Data/Hora', default=timezone.now, db_index=True)
    
    class Meta:
        verbose_name = 'Registro de Auditoria'
        verbose_name_plural = 'Registros de Auditoria'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['object_type', 'object_id']),
        ]
    
    def __str__(self):
        user_str = self.user.username if self.user else 'Sistema'
        return f"[{self.timestamp.strftime('%d/%m/%Y %H:%M')}] {user_str} - {self.get_action_display()}"
    
    @classmethod
    def log(cls, action, user=None, description=None, request=None, obj=None, extra_data=None):
        log_entry = cls(
            user=user,
            action=action,
            description=description,
            extra_data=extra_data
        )
        
        if request:
            log_entry.ip_address = cls.get_client_ip(request)
            log_entry.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        
        if obj:
            log_entry.object_type = obj.__class__.__name__
            log_entry.object_id = obj.pk
            log_entry.object_repr = str(obj)[:255]
        
        log_entry.save()
        return log_entry
    
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
