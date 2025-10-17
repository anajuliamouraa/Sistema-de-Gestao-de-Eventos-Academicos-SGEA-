from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscription',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscricoes', to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AddField(
            model_name='event',
            name='organizador',
            field=models.ForeignKey(help_text='Usuário responsável pela organização do evento', limit_choices_to={'perfil': 'ORGANIZADOR'}, on_delete=django.db.models.deletion.PROTECT, related_name='eventos_organizados', to=settings.AUTH_USER_MODEL, verbose_name='Organizador'),
        ),
        migrations.AlterUniqueTogether(
            name='inscription',
            unique_together={('evento', 'usuario')},
        ),
    ]

