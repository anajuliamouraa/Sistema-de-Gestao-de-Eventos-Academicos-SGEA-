from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

class Event(models.Model):
    TIPO_EVENTO_CHOICES = [
        ('SEMINARIO', 'Seminário'),
        ('PALESTRA', 'Palestra'),
        ('MINICURSO', 'Minicurso'),
        ('SEMANA_ACADEMICA', 'Semana Acadêmica'),
    ]
    
    titulo = models.CharField(
        'Título',
        max_length=200
    )
    
    descricao = models.TextField(
        'Descrição'
    )
    
    tipo_evento = models.CharField(
        'Tipo de Evento',
        max_length=20,
        choices=TIPO_EVENTO_CHOICES
    )
    
    data_inicio = models.DateField(
        'Data de Início'
    )
    
    data_fim = models.DateField(
        'Data de Término'
    )
    
    horario_inicio = models.TimeField(
        'Horário de Início'
    )
    
    horario_fim = models.TimeField(
        'Horário de Término'
    )
    
    local = models.CharField(
        'Local',
        max_length=200
    )
    
    vagas = models.PositiveIntegerField(
        'Quantidade de Vagas'
    )
    
    vagas_disponiveis = models.PositiveIntegerField(
        'Vagas Disponíveis',
        editable=False
    )
    
    organizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='eventos_organizados',
        verbose_name='Organizador',
        limit_choices_to={'perfil': 'ORGANIZADOR'}
    )
    
    imagem = models.ImageField(
        'Imagem',
        upload_to='eventos/',
        blank=True,
        null=True
    )
    
    ativo = models.BooleanField(
        'Ativo',
        default=True
    )
    
    data_criacao = models.DateTimeField(
        'Data de Criação',
        auto_now_add=True
    )
    
    data_atualizacao = models.DateTimeField(
        'Data de Atualização',
        auto_now=True
    )
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-data_inicio', '-horario_inicio']
    
    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_evento_display()})"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.vagas_disponiveis = self.vagas
        if self.data_fim < self.data_inicio:
            raise ValidationError('Data de término não pode ser anterior à data de início.')
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.data_fim < self.data_inicio:
            raise ValidationError('Data de término não pode ser anterior à data de início.')
        if self.data_inicio == self.data_fim and self.horario_fim <= self.horario_inicio:
            raise ValidationError('Horário de término deve ser posterior ao horário de início.')
    
    def tem_vagas(self):
        return self.vagas_disponiveis > 0
    def get_inscritos_count(self):
        return self.inscricoes.filter(status='CONFIRMADA').count()
    def is_futuro(self):
        return self.data_inicio > timezone.now().date()
    def is_em_andamento(self):
        hoje = timezone.now().date()
        return self.data_inicio <= hoje <= self.data_fim
    def is_passado(self):
        return self.data_fim < timezone.now().date()

class Inscription(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    evento = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='inscricoes',
        verbose_name='Evento'
    )
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inscricoes',
        verbose_name='Usuário'
    )
    
    status = models.CharField(
        'Status',
        max_length=15,
        choices=STATUS_CHOICES,
        default='CONFIRMADA'
    )
    
    data_inscricao = models.DateTimeField(
        'Data de Inscrição',
        auto_now_add=True
    )
    
    observacoes = models.TextField(
        'Observações',
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        ordering = ['-data_inscricao']
        unique_together = ['evento', 'usuario']
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.evento.titulo}"
    
    def save(self, *args, **kwargs):
        is_new = not self.pk
        old_status = None
        if not is_new:
            old_instance = Inscription.objects.get(pk=self.pk)
            old_status = old_instance.status
        
        super().save(*args, **kwargs)
        
        if is_new and self.status == 'CONFIRMADA':
            if self.evento.vagas_disponiveis > 0:
                self.evento.vagas_disponiveis -= 1
                self.evento.save()
            else:
                raise ValidationError('Não há vagas disponíveis para este evento.')
        elif not is_new and old_status != self.status:
            if old_status == 'CONFIRMADA' and self.status == 'CANCELADA':
                self.evento.vagas_disponiveis += 1
                self.evento.save()
            elif old_status == 'CANCELADA' and self.status == 'CONFIRMADA':
                if self.evento.vagas_disponiveis > 0:
                    self.evento.vagas_disponiveis -= 1
                    self.evento.save()
                else:
                    raise ValidationError('Não há vagas disponíveis para este evento.')
    def delete(self, *args, **kwargs):
        if self.status == 'CONFIRMADA':
            self.evento.vagas_disponiveis += 1
            self.evento.save()
        super().delete(*args, **kwargs)
