from django.db import models
from django.conf import settings
from events.models import Event, Inscription
import uuid

class Certificate(models.Model):
    inscricao = models.OneToOneField(
        Inscription,
        on_delete=models.PROTECT,
        related_name='certificado',
        verbose_name='Inscrição'
    )
    
    codigo_verificacao = models.UUIDField(
        'Código de Verificação',
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    
    data_emissao = models.DateTimeField(
        'Data de Emissão',
        auto_now_add=True
    )
    
    emitido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='certificados_emitidos',
        verbose_name='Emitido Por'
    )
    
    carga_horaria = models.PositiveIntegerField(
        'Carga Horária'
    )
    
    observacoes = models.TextField(
        'Observações',
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        ordering = ['-data_emissao']
    
    def __str__(self):
        return f"Certificado {self.codigo_verificacao} - {self.inscricao.usuario.get_full_name()}"
    
    @property
    def evento(self):
        return self.inscricao.evento
    @property
    def participante(self):
        return self.inscricao.usuario
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('certificates:view', kwargs={'codigo': self.codigo_verificacao})
