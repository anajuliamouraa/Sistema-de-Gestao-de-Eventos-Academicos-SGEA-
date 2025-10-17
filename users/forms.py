from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='Nome',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome'})
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Sobrenome',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu sobrenome'})
    )
    
    email = forms.EmailField(
        required=True,
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu e-mail'})
    )
    
    telefone = forms.CharField(
        max_length=15,
        required=False,
        label='Telefone',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'})
    )
    
    instituicao_ensino = forms.CharField(
        max_length=200,
        required=False,
        label='Instituição de Ensino',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua instituição'})
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
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu usuário'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Digite sua senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme sua senha'})
    
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
        label='Usuário',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu usuário'})
    )
    
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'})
    )

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'telefone', 'instituicao_ensino']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'instituicao_ensino': forms.TextInput(attrs={'class': 'form-control'}),
        }
