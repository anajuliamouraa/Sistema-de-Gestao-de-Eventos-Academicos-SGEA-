from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_verificacao', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Código único para verificação de autenticidade do certificado', unique=True, verbose_name='Código de Verificação')),
                ('data_emissao', models.DateTimeField(auto_now_add=True, help_text='Data em que o certificado foi emitido', verbose_name='Data de Emissão')),
                ('carga_horaria', models.PositiveIntegerField(help_text='Carga horária do evento em horas', verbose_name='Carga Horária')),
                ('observacoes', models.TextField(blank=True, help_text='Observações adicionais sobre o certificado', null=True, verbose_name='Observações')),
            ],
            options={
                'verbose_name': 'Certificado',
                'verbose_name_plural': 'Certificados',
                'ordering': ['-data_emissao'],
            },
        ),
    ]

