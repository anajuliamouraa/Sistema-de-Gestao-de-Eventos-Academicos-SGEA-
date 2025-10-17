from django import forms
from .models import Event, Inscription

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['titulo', 'descricao', 'tipo_evento', 'data_inicio', 'data_fim',
                  'horario_inicio', 'horario_fim', 'local', 'vagas', 'imagem', 'ativo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do evento'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição detalhada do evento'}),
            'tipo_evento': forms.Select(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'horario_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'horario_fim': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local do evento'}),
            'vagas': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'tipo_evento': 'Tipo de Evento',
            'data_inicio': 'Data de Início',
            'data_fim': 'Data de Término',
            'horario_inicio': 'Horário de Início',
            'horario_fim': 'Horário de Término',
            'local': 'Local',
            'vagas': 'Quantidade de Vagas',
            'imagem': 'Imagem do Evento',
            'ativo': 'Evento Ativo',
        }

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['observacoes']
        widgets = {
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações adicionais (opcional)'
            }),
        }
        labels = {
            'observacoes': 'Observações',
        }

class EventSearchForm(forms.Form):
    busca = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar eventos...'
        })
    )
    
    tipo_evento = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos os tipos')] + list(Event.TIPO_EVENTO_CHOICES),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    apenas_com_vagas = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
