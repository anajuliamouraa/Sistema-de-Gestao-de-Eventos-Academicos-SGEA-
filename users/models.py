from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
import secrets


class CustomUser(AbstractUser):
    PERFIL_CHOICES = [
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
        ('ORGANIZADOR', 'Organizador'),
    ]
    
    telefone = models.CharField('Telefone', max_length=15, blank=True, null=True)
    instituicao_ensino = models.CharField('Instituição de Ensino', max_length=200, blank=True, null=True)
    perfil = models.CharField('Perfil', max_length=15, choices=PERFIL_CHOICES, default='ALUNO')
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    email_confirmed = models.BooleanField('Email Confirmado', default=False)
    activation_code = models.CharField('Código de Ativação', max_length=64, blank=True, null=True)
    activation_code_expires = models.DateTimeField('Expiração do Código', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_perfil_display()})"
    
    def save(self, *args, **kwargs):
        if self.perfil in ['ALUNO', 'PROFESSOR'] and not self.instituicao_ensino:
            from django.core.exceptions import ValidationError
            raise ValidationError('Instituição de ensino é obrigatória para alunos e professores.')
        super().save(*args, **kwargs)
    
    def generate_activation_code(self):
        self.activation_code = secrets.token_urlsafe(32)
        self.activation_code_expires = timezone.now() + timezone.timedelta(hours=24)
        self.save(update_fields=['activation_code', 'activation_code_expires'])
        return self.activation_code
    
    def verify_activation_code(self, code):
        if self.activation_code == code and self.activation_code_expires:
            if timezone.now() <= self.activation_code_expires:
                self.email_confirmed = True
                self.activation_code = None
                self.activation_code_expires = None
                self.save(update_fields=['email_confirmed', 'activation_code', 'activation_code_expires'])
                return True
        return False
    
    def is_organizador(self):
        return self.perfil == 'ORGANIZADOR'
    
    def is_professor(self):
        return self.perfil == 'PROFESSOR'
    
    def is_aluno(self):
        return self.perfil == 'ALUNO'
    
    def can_inscribe_events(self):
        return self.perfil in ['ALUNO', 'PROFESSOR'] and self.email_confirmed
    
    def can_be_responsible(self):
        return self.perfil == 'PROFESSOR'
