from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from events.models import Event, Inscription
from audit.models import AuditLog
from .serializers import (
    EventListSerializer, EventDetailSerializer,
    InscriptionSerializer, InscriptionCreateSerializer
)
from .throttling import EventQueryThrottle, InscriptionThrottle


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            AuditLog.log(
                action='USER_LOGIN',
                user=user,
                description=f'Login via API - Token {"criado" if created else "reutilizado"}',
                request=request
            )
            
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'username': user.username,
                'perfil': user.perfil,
                'email_confirmed': user.email_confirmed
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventListView(generics.ListAPIView):
    serializer_class = EventListSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [EventQueryThrottle]
    
    def get_queryset(self):
        queryset = Event.objects.filter(ativo=True).select_related(
            'organizador', 'professor_responsavel'
        ).order_by('-data_inicio')
        
        tipo = self.request.query_params.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo_evento=tipo)
        
        ativo = self.request.query_params.get('ativo')
        if ativo is not None:
            queryset = queryset.filter(ativo=ativo.lower() == 'true')
        
        com_vagas = self.request.query_params.get('com_vagas')
        if com_vagas and com_vagas.lower() == 'true':
            queryset = queryset.filter(vagas_disponiveis__gt=0)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        AuditLog.log(
            action='EVENT_API_QUERY',
            user=request.user,
            description=f'Consulta de eventos via API - {len(response.data)} resultados',
            request=request,
            extra_data={
                'query_params': dict(request.query_params),
                'results_count': len(response.data)
            }
        )
        
        return response


class EventDetailView(generics.RetrieveAPIView):
    serializer_class = EventDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [EventQueryThrottle]
    queryset = Event.objects.select_related('organizador', 'professor_responsavel')
    
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        
        AuditLog.log(
            action='EVENT_API_QUERY',
            user=request.user,
            description=f'Consulta de evento via API: {self.get_object().titulo}',
            request=request,
            obj=self.get_object()
        )
        
        return response


class InscriptionCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [InscriptionThrottle]
    
    def post(self, request):
        serializer = InscriptionCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            inscription = serializer.save()
            
            AuditLog.log(
                action='INSCRIPTION_API',
                user=request.user,
                description=f'Inscrição via API no evento: {inscription.evento.titulo}',
                request=request,
                obj=inscription,
                extra_data={
                    'evento_id': inscription.evento.pk,
                    'evento_titulo': inscription.evento.titulo
                }
            )
            
            return Response(
                InscriptionSerializer(inscription).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyInscriptionsView(generics.ListAPIView):
    serializer_class = InscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [InscriptionThrottle]
    
    def get_queryset(self):
        return Inscription.objects.filter(
            usuario=self.request.user,
            status='CONFIRMADA'
        ).select_related('evento').order_by('-data_inscricao')


class InscriptionCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [InscriptionThrottle]
    
    def delete(self, request, pk):
        try:
            inscription = Inscription.objects.get(pk=pk, usuario=request.user)
        except Inscription.DoesNotExist:
            return Response(
                {'error': 'Inscrição não encontrada.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if inscription.status == 'CANCELADA':
            return Response(
                {'error': 'Esta inscrição já foi cancelada.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        evento_titulo = inscription.evento.titulo
        inscription.status = 'CANCELADA'
        inscription.save()
        
        AuditLog.log(
            action='INSCRIPTION_CANCELLED',
            user=request.user,
            description=f'Cancelamento de inscrição via API: {evento_titulo}',
            request=request,
            obj=inscription
        )
        
        return Response(
            {'message': 'Inscrição cancelada com sucesso.'},
            status=status.HTTP_200_OK
        )


class APIRootView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            'message': 'Bem-vindo à API do SGEA - Sistema de Gestão de Eventos Acadêmicos',
            'version': '2.0',
            'endpoints': {
                'auth': {
                    'token': '/api/auth/token/',
                    'description': 'POST - Obter token de autenticação'
                },
                'events': {
                    'list': '/api/events/',
                    'detail': '/api/events/<id>/',
                    'description': 'GET - Listar e consultar eventos'
                },
                'inscriptions': {
                    'create': '/api/inscriptions/',
                    'my_inscriptions': '/api/inscriptions/me/',
                    'cancel': '/api/inscriptions/<id>/',
                    'description': 'Gerenciar inscrições'
                }
            },
            'rate_limits': {
                'events': '20 requisições/dia',
                'inscriptions': '50 requisições/dia'
            },
            'authentication': 'Token-based. Header: Authorization: Token <token>'
        })
