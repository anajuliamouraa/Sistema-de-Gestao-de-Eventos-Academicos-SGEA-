from rest_framework import serializers
from events.models import Event, Inscription
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    perfil_display = serializers.CharField(source='get_perfil_display', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 
                  'perfil', 'perfil_display', 'instituicao_ensino']
        read_only_fields = fields


class EventListSerializer(serializers.ModelSerializer):
    tipo_evento_display = serializers.CharField(source='get_tipo_evento_display', read_only=True)
    organizador_nome = serializers.CharField(source='organizador.get_full_name', read_only=True)
    professor_responsavel_nome = serializers.CharField(
        source='professor_responsavel.get_full_name', read_only=True
    )
    vagas_ocupadas = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    banner_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'titulo', 'descricao', 'tipo_evento', 'tipo_evento_display',
            'data_inicio', 'data_fim', 'horario_inicio', 'horario_fim',
            'local', 'vagas', 'vagas_disponiveis', 'vagas_ocupadas',
            'organizador_nome', 'professor_responsavel_nome',
            'banner_url', 'ativo', 'status', 'data_criacao'
        ]
        read_only_fields = fields
    
    def get_vagas_ocupadas(self, obj):
        return obj.vagas - obj.vagas_disponiveis
    
    def get_status(self, obj):
        if obj.is_passado():
            return 'finalizado'
        elif obj.is_em_andamento():
            return 'em_andamento'
        else:
            return 'futuro'
    
    def get_banner_url(self, obj):
        request = self.context.get('request')
        banner_url = obj.get_banner_url()
        if banner_url and request:
            return request.build_absolute_uri(banner_url)
        return banner_url


class EventDetailSerializer(EventListSerializer):
    organizador = UserSerializer(read_only=True)
    professor_responsavel = UserSerializer(read_only=True)
    
    class Meta(EventListSerializer.Meta):
        fields = EventListSerializer.Meta.fields + ['organizador', 'professor_responsavel']


class InscriptionSerializer(serializers.ModelSerializer):
    evento_titulo = serializers.CharField(source='evento.titulo', read_only=True)
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Inscription
        fields = [
            'id', 'evento', 'evento_titulo', 'usuario', 'usuario_nome',
            'status', 'status_display', 'presenca_confirmada',
            'data_inscricao', 'observacoes'
        ]
        read_only_fields = ['id', 'evento_titulo', 'usuario', 'usuario_nome', 
                           'status_display', 'data_inscricao', 'presenca_confirmada']


class InscriptionCreateSerializer(serializers.Serializer):
    evento_id = serializers.IntegerField()
    observacoes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_evento_id(self, value):
        try:
            evento = Event.objects.get(pk=value)
        except Event.DoesNotExist:
            raise serializers.ValidationError('Evento não encontrado.')
        
        if not evento.ativo:
            raise serializers.ValidationError('Este evento não está aceitando inscrições.')
        
        if not evento.tem_vagas():
            raise serializers.ValidationError('Não há vagas disponíveis para este evento.')
        
        if evento.is_passado():
            raise serializers.ValidationError('Este evento já foi encerrado.')
        
        return value
    
    def validate(self, attrs):
        user = self.context['request'].user
        evento_id = attrs['evento_id']
        
        if user.is_organizador():
            raise serializers.ValidationError({
                'non_field_errors': ['Organizadores não podem se inscrever em eventos.']
            })
        
        if not user.email_confirmed:
            raise serializers.ValidationError({
                'non_field_errors': ['Você precisa confirmar seu email antes de se inscrever em eventos.']
            })
        
        if Inscription.objects.filter(evento_id=evento_id, usuario=user).exists():
            raise serializers.ValidationError({
                'evento_id': ['Você já está inscrito neste evento.']
            })
        
        return attrs
    
    def create(self, validated_data):
        user = self.context['request'].user
        evento = Event.objects.get(pk=validated_data['evento_id'])
        
        inscription = Inscription.objects.create(
            evento=evento,
            usuario=user,
            observacoes=validated_data.get('observacoes', ''),
            status='CONFIRMADA'
        )
        
        return inscription


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
