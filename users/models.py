from django.db import models
from django.contrib.auth.models import AbstractUser

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
    
    def is_organizador(self):
        return self.perfil == 'ORGANIZADOR'
    
    def is_professor(self):
        return self.perfil == 'PROFESSOR'
    
    def is_aluno(self):
        return self.perfil == 'ALUNO'
