from django import forms
from .models import Certificate

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['carga_horaria', 'observacoes']
        widgets = {
            'carga_horaria': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Carga horária em horas'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações adicionais (opcional)'
            }),
        }
        labels = {
            'carga_horaria': 'Carga Horária (horas)',
            'observacoes': 'Observações',
        }

class CertificateVerificationForm(forms.Form):
    codigo_verificacao = forms.UUIDField(
        label='Código de Verificação',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o código de verificação do certificado'
        })
    )
