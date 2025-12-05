from django.core.management.base import BaseCommand
from django.utils import timezone
from events.models import Event, Inscription
from certificates.models import Certificate
from audit.models import AuditLog
from users.emails import send_certificate_available_email


class Command(BaseCommand):
    help = 'Gera certificados automaticamente para eventos finalizados'

    def add_arguments(self, parser):
        parser.add_argument('--event-id', type=int, help='ID do evento específico para gerar certificados')
        parser.add_argument('--dry-run', action='store_true', help='Apenas simula a geração sem criar os certificados')
        parser.add_argument('--no-email', action='store_true', help='Não envia emails de notificação')

    def handle(self, *args, **options):
        event_id = options.get('event_id')
        dry_run = options.get('dry_run', False)
        no_email = options.get('no_email', False)
        
        if dry_run:
            self.stdout.write(self.style.WARNING('🔄 Modo de simulação ativado'))
        
        if event_id:
            events = Event.objects.filter(pk=event_id)
        else:
            events = Event.objects.filter(data_fim__lt=timezone.now().date())
        
        total_generated = 0
        total_skipped = 0
        
        for event in events:
            self.stdout.write(f'\n📅 Processando evento: {event.titulo}')
            
            inscriptions = Inscription.objects.filter(
                evento=event,
                status='CONFIRMADA',
                presenca_confirmada=True
            ).exclude(certificado__isnull=False).select_related('usuario')
            
            if not inscriptions.exists():
                self.stdout.write(self.style.WARNING('  ⚠ Nenhuma inscrição elegível para certificado'))
                continue
            
            self.stdout.write(f'  📋 {inscriptions.count()} certificados a gerar')
            carga_horaria = self.calculate_carga_horaria(event)
            
            for inscription in inscriptions:
                if dry_run:
                    self.stdout.write(f'    [SIMULAÇÃO] Certificado para: {inscription.usuario.get_full_name()}')
                    total_generated += 1
                    continue
                
                try:
                    certificate = Certificate.objects.create(
                        inscricao=inscription,
                        emitido_por=event.organizador,
                        carga_horaria=carga_horaria,
                        observacoes=f'Certificado gerado automaticamente em {timezone.now().strftime("%d/%m/%Y")}'
                    )
                    
                    AuditLog.log(
                        action='CERTIFICATE_AUTO_GENERATED',
                        user=event.organizador,
                        description=f'Certificado automático gerado para {inscription.usuario.get_full_name()}',
                        obj=certificate,
                        extra_data={
                            'evento_id': event.pk,
                            'evento_titulo': event.titulo,
                            'participante': inscription.usuario.username
                        }
                    )
                    
                    if not no_email:
                        send_certificate_available_email(certificate)
                    
                    self.stdout.write(self.style.SUCCESS(f'    ✓ Certificado gerado: {inscription.usuario.get_full_name()}'))
                    total_generated += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'    ✗ Erro ao gerar certificado para {inscription.usuario.get_full_name()}: {e}'))
                    total_skipped += 1
        
        self.stdout.write('\n' + '='*50)
        if dry_run:
            self.stdout.write(self.style.WARNING(f'🔄 SIMULAÇÃO: {total_generated} certificados seriam gerados'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ Total de certificados gerados: {total_generated}'))
            if total_skipped:
                self.stdout.write(self.style.WARNING(f'⚠ Total de erros: {total_skipped}'))
    
    def calculate_carga_horaria(self, event):
        from datetime import datetime
        inicio = datetime.combine(event.data_inicio, event.horario_inicio)
        fim = datetime.combine(event.data_inicio, event.horario_fim)
        duracao_diaria = (fim - inicio).seconds / 3600
        num_dias = (event.data_fim - event.data_inicio).days + 1
        carga_total = int(duracao_diaria * num_dias)
        return max(carga_total, 1)
