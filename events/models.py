from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from PIL import Image
import os


def validate_image_file(value):
    if value:
        ext = os.path.splitext(value.name)[1].lower()
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        if ext not in valid_extensions:
            raise ValidationError(
                f'Formato de arquivo não suportado. Use: {", ".join(valid_extensions)}'
            )
        
        if value.size > 5 * 1024 * 1024:
            raise ValidationError('O arquivo de imagem não pode exceder 5MB.')
        
        try:
            img = Image.open(value)
            img.verify()
        except Exception:
            raise ValidationError('O arquivo não é uma imagem válida.')


class Event(models.Model):
    TIPO_EVENTO_CHOICES = [
        ('SEMINARIO', 'Seminário'),
        ('PALESTRA', 'Palestra'),
        ('MINICURSO', 'Minicurso'),
        ('SEMANA_ACADEMICA', 'Semana Acadêmica'),
    ]
    
    titulo = models.CharField('Título', max_length=200)
    descricao = models.TextField('Descrição')
    tipo_evento = models.CharField('Tipo de Evento', max_length=20, choices=TIPO_EVENTO_CHOICES)
    data_inicio = models.DateField('Data de Início')
    data_fim = models.DateField('Data de Término')
    horario_inicio = models.TimeField('Horário de Início')
    horario_fim = models.TimeField('Horário de Término')
    local = models.CharField('Local', max_length=200)
    vagas = models.PositiveIntegerField('Quantidade de Vagas')
    vagas_disponiveis = models.PositiveIntegerField('Vagas Disponíveis', editable=False)
    
    organizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='eventos_organizados',
        verbose_name='Organizador',
        limit_choices_to={'perfil': 'ORGANIZADOR'}
    )
    
    professor_responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='eventos_responsavel',
        verbose_name='Professor Responsável',
        limit_choices_to={'perfil': 'PROFESSOR'},
        help_text='Professor responsável pelo evento',
        null=True,
        blank=True
    )
    
    banner = models.ImageField(
        'Banner do Evento',
        upload_to='eventos/banners/',
        blank=True,
        null=True,
        validators=[validate_image_file],
        help_text='Imagem de divulgação do evento (máx. 5MB, formatos: JPG, PNG, GIF, WebP)'
    )
    
    imagem = models.ImageField(
        'Imagem',
        upload_to='eventos/',
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    
    ativo = models.BooleanField('Ativo', default=True)
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Data de Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-data_inicio', '-horario_inicio']
    
    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_evento_display()})"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.vagas_disponiveis = self.vagas
        super().save(*args, **kwargs)
    
    def clean(self):
        if not self.pk and self.data_inicio:
            if self.data_inicio < timezone.now().date():
                raise ValidationError({
                    'data_inicio': 'Não é permitido cadastrar eventos com data de início anterior à data atual.'
                })
        
        if self.data_fim and self.data_inicio:
            if self.data_fim < self.data_inicio:
                raise ValidationError({
                    'data_fim': 'Data de término não pode ser anterior à data de início.'
                })
        
        if self.data_inicio == self.data_fim and self.horario_fim and self.horario_inicio:
            if self.horario_fim <= self.horario_inicio:
                raise ValidationError({
                    'horario_fim': 'Horário de término deve ser posterior ao horário de início.'
                })
    
    def get_banner_url(self):
        if self.banner:
            return self.banner.url
        elif self.imagem:
            return self.imagem.url
        return None
    
    def tem_vagas(self):
        return self.vagas_disponiveis > 0
    
    def get_inscritos_count(self):
        return self.inscricoes.filter(status='CONFIRMADA').count()
    
    def get_inscritos_com_presenca(self):
        return self.inscricoes.filter(status='CONFIRMADA', presenca_confirmada=True)
    
    def is_futuro(self):
        return self.data_inicio > timezone.now().date()
    
    def is_em_andamento(self):
        hoje = timezone.now().date()
        return self.data_inicio <= hoje <= self.data_fim
    
    def is_passado(self):
        return self.data_fim < timezone.now().date()
    
    def pode_emitir_certificados(self):
        return self.is_passado()


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
    
    status = models.CharField('Status', max_length=15, choices=STATUS_CHOICES, default='CONFIRMADA')
    presenca_confirmada = models.BooleanField('Presença Confirmada', default=False, help_text='Indica se o participante teve presença confirmada no evento')
    data_inscricao = models.DateTimeField('Data de Inscrição', auto_now_add=True)
    observacoes = models.TextField('Observações', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        ordering = ['-data_inscricao']
        unique_together = ['evento', 'usuario']
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.evento.titulo}"
    
    def clean(self):
        if self.usuario.is_organizador():
            raise ValidationError('Organizadores não podem se inscrever em eventos.')
        
        if not self.pk and self.evento and not self.evento.tem_vagas():
            raise ValidationError('Não há vagas disponíveis para este evento.')
    
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
