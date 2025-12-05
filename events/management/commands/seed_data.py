from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser
from events.models import Event, Inscription


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais para testes'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando carga de dados...'))
        self.create_users()
        self.create_events()
        self.stdout.write(self.style.SUCCESS('✅ Carga de dados concluída com sucesso!'))
    
    def create_users(self):
        organizador, created = CustomUser.objects.get_or_create(
            username='organizador',
            defaults={
                'email': 'organizador@sgea.com',
                'first_name': 'Organizador',
                'last_name': 'SGEA',
                'perfil': 'ORGANIZADOR',
                'instituicao_ensino': 'UniCEUB',
                'email_confirmed': True,
                'is_staff': True,
            }
        )
        if created:
            organizador.set_password('Admin@123')
            organizador.save()
            self.stdout.write(self.style.SUCCESS(f'  ✓ Usuário criado: organizador@sgea.com (Senha: Admin@123)'))
        else:
            self.stdout.write(self.style.WARNING(f'  ⚠ Usuário já existe: organizador@sgea.com'))
        
        aluno, created = CustomUser.objects.get_or_create(
            username='aluno',
            defaults={
                'email': 'aluno@sgea.com',
                'first_name': 'Aluno',
                'last_name': 'Teste',
                'perfil': 'ALUNO',
                'instituicao_ensino': 'UniCEUB',
                'telefone': '(61) 99999-1111',
                'email_confirmed': True,
            }
        )
        if created:
            aluno.set_password('Aluno@123')
            aluno.save()
            self.stdout.write(self.style.SUCCESS(f'  ✓ Usuário criado: aluno@sgea.com (Senha: Aluno@123)'))
        else:
            self.stdout.write(self.style.WARNING(f'  ⚠ Usuário já existe: aluno@sgea.com'))
        
        professor, created = CustomUser.objects.get_or_create(
            username='professor',
            defaults={
                'email': 'professor@sgea.com',
                'first_name': 'Professor',
                'last_name': 'Teste',
                'perfil': 'PROFESSOR',
                'instituicao_ensino': 'UniCEUB',
                'telefone': '(61) 99999-2222',
                'email_confirmed': True,
            }
        )
        if created:
            professor.set_password('Professor@123')
            professor.save()
            self.stdout.write(self.style.SUCCESS(f'  ✓ Usuário criado: professor@sgea.com (Senha: Professor@123)'))
        else:
            self.stdout.write(self.style.WARNING(f'  ⚠ Usuário já existe: professor@sgea.com'))
        
        extra_users = [
            {'username': 'maria_aluna', 'email': 'maria@teste.com', 'first_name': 'Maria', 'last_name': 'Silva', 'perfil': 'ALUNO', 'instituicao_ensino': 'UniCEUB'},
            {'username': 'joao_aluno', 'email': 'joao@teste.com', 'first_name': 'João', 'last_name': 'Santos', 'perfil': 'ALUNO', 'instituicao_ensino': 'UnB'},
            {'username': 'dr_carlos', 'email': 'carlos@teste.com', 'first_name': 'Carlos', 'last_name': 'Oliveira', 'perfil': 'PROFESSOR', 'instituicao_ensino': 'UniCEUB'},
        ]
        
        for user_data in extra_users:
            user, created = CustomUser.objects.get_or_create(
                username=user_data['username'],
                defaults={**user_data, 'email_confirmed': True}
            )
            if created:
                user.set_password('Teste@123')
                user.save()
                self.stdout.write(f'  ✓ Usuário extra criado: {user_data["email"]}')
    
    def create_events(self):
        try:
            organizador = CustomUser.objects.get(username='organizador')
            professor = CustomUser.objects.get(username='professor')
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR('  ✗ Erro: Usuários base não encontrados'))
            return
        
        today = timezone.now().date()
        
        events_data = [
            {
                'titulo': 'Seminário de Inteligência Artificial',
                'descricao': 'Seminário sobre avanços recentes em IA, Machine Learning e Deep Learning. Evento aberto a todos os interessados em tecnologia e inovação.',
                'tipo_evento': 'SEMINARIO',
                'data_inicio': today + timedelta(days=7),
                'data_fim': today + timedelta(days=7),
                'horario_inicio': '09:00',
                'horario_fim': '17:00',
                'local': 'Auditório Principal - Bloco A',
                'vagas': 100,
            },
            {
                'titulo': 'Palestra: Carreira em Desenvolvimento de Software',
                'descricao': 'Palestra com profissionais de mercado sobre oportunidades e desafios na carreira de desenvolvedor de software.',
                'tipo_evento': 'PALESTRA',
                'data_inicio': today + timedelta(days=14),
                'data_fim': today + timedelta(days=14),
                'horario_inicio': '19:00',
                'horario_fim': '21:00',
                'local': 'Sala de Conferências - Bloco B',
                'vagas': 50,
            },
            {
                'titulo': 'Minicurso de Python para Iniciantes',
                'descricao': 'Minicurso introdutório de Python abordando conceitos básicos de programação, estruturas de dados e desenvolvimento de pequenos projetos.',
                'tipo_evento': 'MINICURSO',
                'data_inicio': today + timedelta(days=21),
                'data_fim': today + timedelta(days=23),
                'horario_inicio': '14:00',
                'horario_fim': '18:00',
                'local': 'Laboratório de Informática 3',
                'vagas': 30,
            },
            {
                'titulo': 'Semana Acadêmica de Computação 2025',
                'descricao': 'Evento anual com palestras, workshops, minicursos e competições para estudantes e profissionais da área de computação.',
                'tipo_evento': 'SEMANA_ACADEMICA',
                'data_inicio': today + timedelta(days=30),
                'data_fim': today + timedelta(days=34),
                'horario_inicio': '08:00',
                'horario_fim': '22:00',
                'local': 'Campus UniCEUB',
                'vagas': 500,
            },
            {
                'titulo': 'Palestra: Segurança da Informação',
                'descricao': 'Discussão sobre as principais ameaças cibernéticas e como proteger sistemas e dados pessoais.',
                'tipo_evento': 'PALESTRA',
                'data_inicio': today + timedelta(days=10),
                'data_fim': today + timedelta(days=10),
                'horario_inicio': '10:00',
                'horario_fim': '12:00',
                'local': 'Auditório - Bloco C',
                'vagas': 80,
            },
        ]
        
        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                titulo=event_data['titulo'],
                defaults={**event_data, 'organizador': organizador, 'professor_responsavel': professor}
            )
            if created:
                self.stdout.write(f'  ✓ Evento criado: {event_data["titulo"]}')
            else:
                self.stdout.write(f'  ⚠ Evento já existe: {event_data["titulo"]}')
