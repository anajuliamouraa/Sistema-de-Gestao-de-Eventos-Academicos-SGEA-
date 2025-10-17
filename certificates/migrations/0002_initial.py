from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('certificates', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='emitido_por',
            field=models.ForeignKey(help_text='Organizador que emitiu o certificado', on_delete=django.db.models.deletion.PROTECT, related_name='certificados_emitidos', to=settings.AUTH_USER_MODEL, verbose_name='Emitido Por'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='inscricao',
            field=models.OneToOneField(help_text='Inscrição vinculada ao certificado', on_delete=django.db.models.deletion.PROTECT, related_name='certificado', to='events.inscription', verbose_name='Inscrição'),
        ),
    ]

