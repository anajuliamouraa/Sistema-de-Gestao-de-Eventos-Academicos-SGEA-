from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from .models import CustomUser
from .validators import validate_phone_number
import re


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='Nome',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Sobrenome',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu sobrenome'
        })
    )
    
    email = forms.EmailField(
        required=True,
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu e-mail'
        })
    )
    
    telefone = forms.CharField(
        max_length=15,
        required=False,
        label='Telefone',
        validators=[validate_phone_number],
        widget=forms.TextInput(attrs={
            'class': 'form-control phone-mask',
            'placeholder': '(00) 00000-0000',
            'data-mask': '(00) 00000-0000'
        })
    )
    
    instituicao_ensino = forms.CharField(
        max_length=200,
        required=False,
        label='Instituição de Ensino',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua instituição'
        })
    )
    
    perfil = forms.ChoiceField(
        choices=CustomUser.PERFIL_CHOICES,
        required=True,
        label='Perfil',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'telefone', 
                  'instituicao_ensino', 'perfil', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu usuário'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
        self.fields['password1'].help_text = (
            'A senha deve ter no mínimo 8 caracteres, incluindo letras maiúsculas, '
            'minúsculas, números e caracteres especiais.'
        )
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme sua senha'
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está cadastrado.')
        return email
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            digits = re.sub(r'\D', '', telefone)
            if len(digits) == 11:
                return f'({digits[:2]}) {digits[2:7]}-{digits[7:]}'
            elif len(digits) == 10:
                return f'({digits[:2]}) {digits[2:6]}-{digits[6:]}'
        return telefone
    
    def clean(self):
        cleaned_data = super().clean()
        perfil = cleaned_data.get('perfil')
        instituicao_ensino = cleaned_data.get('instituicao_ensino')
        
        if perfil in ['ALUNO', 'PROFESSOR'] and not instituicao_ensino:
            raise forms.ValidationError(
                'Instituição de ensino é obrigatória para alunos e professores.'
            )
        
        return cleaned_data


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuário ou Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu usuário ou email'
        })
    )
    
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
                return user.username
            except CustomUser.DoesNotExist:
                pass
        return username


class UserUpdateForm(forms.ModelForm):
    telefone = forms.CharField(
        max_length=15,
        required=False,
        label='Telefone',
        validators=[validate_phone_number],
        widget=forms.TextInput(attrs={
            'class': 'form-control phone-mask',
            'placeholder': '(00) 00000-0000',
            'data-mask': '(00) 00000-0000'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'telefone', 'instituicao_ensino']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'instituicao_ensino': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            digits = re.sub(r'\D', '', telefone)
            if len(digits) == 11:
                return f'({digits[:2]}) {digits[2:7]}-{digits[7:]}'
            elif len(digits) == 10:
                return f'({digits[:2]}) {digits[2:6]}-{digits[6:]}'
        return telefone
