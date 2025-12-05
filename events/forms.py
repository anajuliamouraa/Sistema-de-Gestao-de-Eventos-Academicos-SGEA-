from django import forms
from django.utils import timezone
from .models import Event, Inscription
from users.models import CustomUser


class EventForm(forms.ModelForm):
    professor_responsavel = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(perfil='PROFESSOR'),
        label='Professor Responsável',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Selecione o professor responsável pelo evento'
    )
    
    class Meta:
        model = Event
        fields = ['titulo', 'descricao', 'tipo_evento', 'data_inicio', 'data_fim',
                  'horario_inicio', 'horario_fim', 'local', 'vagas', 
                  'professor_responsavel', 'banner', 'ativo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do evento'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição detalhada do evento'}),
            'tipo_evento': forms.Select(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control datepicker', 'type': 'text', 'placeholder': 'dd/mm/aaaa'}),
            'data_fim': forms.DateInput(attrs={'class': 'form-control datepicker', 'type': 'text', 'placeholder': 'dd/mm/aaaa'}),
            'horario_inicio': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type': 'text', 'placeholder': 'HH:MM'}),
            'horario_fim': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type': 'text', 'placeholder': 'HH:MM'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local do evento'}),
            'vagas': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Número de vagas'}),
            'banner': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/jpeg,image/png,image/gif,image/webp'}),
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
            'banner': 'Banner do Evento',
            'ativo': 'Evento Ativo',
        }
        help_texts = {
            'banner': 'Imagem de divulgação do evento (máx. 5MB, formatos: JPG, PNG, GIF, WebP)',
            'vagas': 'Número máximo de participantes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['professor_responsavel'].queryset = CustomUser.objects.filter(
            perfil='PROFESSOR'
        ).order_by('first_name', 'last_name')
        
        if not self.fields['professor_responsavel'].queryset.exists():
            self.fields['professor_responsavel'].help_text = (
                'Não há professores cadastrados. Cadastre um professor primeiro.'
            )
    
    def clean_data_inicio(self):
        data_inicio = self.cleaned_data.get('data_inicio')
        if not self.instance.pk and data_inicio:
            if data_inicio < timezone.now().date():
                raise forms.ValidationError(
                    'Não é permitido cadastrar eventos com data de início anterior à data atual.'
                )
        return data_inicio
    
    def clean_data_fim(self):
        data_inicio = self.cleaned_data.get('data_inicio')
        data_fim = self.cleaned_data.get('data_fim')
        if data_inicio and data_fim:
            if data_fim < data_inicio:
                raise forms.ValidationError(
                    'Data de término não pode ser anterior à data de início.'
                )
        return data_fim
    
    def clean_horario_fim(self):
        data_inicio = self.cleaned_data.get('data_inicio')
        data_fim = self.cleaned_data.get('data_fim')
        horario_inicio = self.cleaned_data.get('horario_inicio')
        horario_fim = self.cleaned_data.get('horario_fim')
        if data_inicio == data_fim and horario_inicio and horario_fim:
            if horario_fim <= horario_inicio:
                raise forms.ValidationError(
                    'Horário de término deve ser posterior ao horário de início.'
                )
        return horario_fim
    
    def clean_vagas(self):
        vagas = self.cleaned_data.get('vagas')
        if vagas is not None and vagas < 1:
            raise forms.ValidationError('O número de vagas deve ser pelo menos 1.')
        return vagas
    
    def clean_banner(self):
        banner = self.cleaned_data.get('banner')
        if banner:
            if banner.size > 5 * 1024 * 1024:
                raise forms.ValidationError('O arquivo de imagem não pode exceder 5MB.')
            content_type = getattr(banner, 'content_type', '')
            valid_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if content_type and content_type not in valid_types:
                raise forms.ValidationError('Formato de arquivo não suportado. Use: JPG, PNG, GIF ou WebP.')
        return banner


class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['observacoes']
        widgets = {
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações adicionais (opcional)'}),
        }
        labels = {
            'observacoes': 'Observações',
        }


class PresenceForm(forms.Form):
    inscricoes = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='Participantes Presentes'
    )
    
    def __init__(self, *args, event=None, **kwargs):
        super().__init__(*args, **kwargs)
        if event:
            inscricoes = event.inscricoes.filter(status='CONFIRMADA').select_related('usuario')
            self.fields['inscricoes'].choices = [
                (i.pk, f'{i.usuario.get_full_name()} ({i.usuario.email})')
                for i in inscricoes
            ]


class EventSearchForm(forms.Form):
    busca = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar eventos...'})
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
