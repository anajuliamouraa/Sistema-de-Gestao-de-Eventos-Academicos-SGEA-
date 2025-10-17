from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(help_text='Título do evento', max_length=200, verbose_name='Título')),
                ('descricao', models.TextField(help_text='Descrição detalhada do evento', verbose_name='Descrição')),
                ('tipo_evento', models.CharField(choices=[('SEMINARIO', 'Seminário'), ('PALESTRA', 'Palestra'), ('MINICURSO', 'Minicurso'), ('SEMANA_ACADEMICA', 'Semana Acadêmica')], help_text='Tipo do evento acadêmico', max_length=20, verbose_name='Tipo de Evento')),
                ('data_inicio', models.DateField(help_text='Data de início do evento', verbose_name='Data de Início')),
                ('data_fim', models.DateField(help_text='Data de término do evento', verbose_name='Data de Término')),
                ('horario_inicio', models.TimeField(help_text='Horário de início do evento', verbose_name='Horário de Início')),
                ('horario_fim', models.TimeField(help_text='Horário de término do evento', verbose_name='Horário de Término')),
                ('local', models.CharField(help_text='Local onde o evento será realizado', max_length=200, verbose_name='Local')),
                ('vagas', models.PositiveIntegerField(help_text='Número máximo de participantes', verbose_name='Quantidade de Vagas')),
                ('vagas_disponiveis', models.PositiveIntegerField(editable=False, help_text='Número de vagas ainda disponíveis', verbose_name='Vagas Disponíveis')),
                ('imagem', models.ImageField(blank=True, help_text='Imagem de divulgação do evento', null=True, upload_to='eventos/', verbose_name='Imagem')),
                ('ativo', models.BooleanField(default=True, help_text='Indica se o evento está ativo para inscrições', verbose_name='Ativo')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'ordering': ['-data_inicio', '-horario_inicio'],
            },
        ),
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDENTE', 'Pendente'), ('CONFIRMADA', 'Confirmada'), ('CANCELADA', 'Cancelada')], default='CONFIRMADA', help_text='Status da inscrição', max_length=15, verbose_name='Status')),
                ('data_inscricao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Inscrição')),
                ('observacoes', models.TextField(blank=True, help_text='Observações sobre a inscrição', null=True, verbose_name='Observações')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscricoes', to='events.event', verbose_name='Evento')),
            ],
            options={
                'verbose_name': 'Inscrição',
                'verbose_name_plural': 'Inscrições',
                'ordering': ['-data_inscricao'],
            },
        ),
    ]

