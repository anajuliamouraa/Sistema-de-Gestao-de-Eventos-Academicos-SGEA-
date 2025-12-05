from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Event, Inscription
from .forms import EventForm, InscriptionForm, EventSearchForm, PresenceForm
from audit.models import AuditLog
from users.emails import send_inscription_confirmation_email


def home(request):
    events = Event.objects.filter(ativo=True).select_related(
        'organizador', 'professor_responsavel'
    ).order_by('-data_inicio')
    
    search_form = EventSearchForm(request.GET)
    if search_form.is_valid():
        busca = search_form.cleaned_data.get('busca')
        tipo_evento = search_form.cleaned_data.get('tipo_evento')
        apenas_com_vagas = search_form.cleaned_data.get('apenas_com_vagas')
        
        if busca:
            events = events.filter(
                Q(titulo__icontains=busca) |
                Q(descricao__icontains=busca) |
                Q(local__icontains=busca)
            )
        
        if tipo_evento:
            events = events.filter(tipo_evento=tipo_evento)
        
        if apenas_com_vagas:
            events = events.filter(vagas_disponiveis__gt=0)
    
    paginator = Paginator(events, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'events': page_obj,
        'search_form': search_form,
    }
    return render(request, 'events/home.html', context)


@login_required
def event_detail(request, pk):
    event = get_object_or_404(
        Event.objects.select_related('organizador', 'professor_responsavel'),
        pk=pk
    )
    
    is_inscrito = False
    inscricao = None
    can_inscribe = False
    
    if request.user.is_authenticated:
        try:
            inscricao = Inscription.objects.get(evento=event, usuario=request.user)
            is_inscrito = inscricao.status == 'CONFIRMADA'
        except Inscription.DoesNotExist:
            pass
        
        can_inscribe = (
            request.user.can_inscribe_events() and 
            not is_inscrito and 
            event.tem_vagas() and 
            event.ativo and
            not event.is_passado()
        )
    
    context = {
        'event': event,
        'is_inscrito': is_inscrito,
        'inscricao': inscricao,
        'is_organizador': request.user == event.organizador,
        'can_inscribe': can_inscribe,
    }
    return render(request, 'events/event_detail.html', context)


@login_required
def event_create(request):
    if not request.user.is_organizador():
        messages.error(request, 'Apenas organizadores podem criar eventos.')
        return redirect('events:home')
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizador = request.user
            event.save()
            
            AuditLog.log(
                action='EVENT_CREATED',
                user=request.user,
                description=f'Evento criado: {event.titulo}',
                request=request,
                obj=event,
                extra_data={
                    'titulo': event.titulo,
                    'tipo_evento': event.tipo_evento,
                    'data_inicio': str(event.data_inicio),
                    'vagas': event.vagas
                }
            )
            
            messages.success(request, 'Evento criado com sucesso!')
            return redirect('events:event_detail', pk=event.pk)
        else:
            messages.error(request, 'Erro ao criar evento. Verifique os dados informados.')
    else:
        form = EventForm()
    
    context = {'form': form, 'action': 'Criar'}
    return render(request, 'events/event_form.html', context)


@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if request.user != event.organizador:
        messages.error(request, 'Você não tem permissão para editar este evento.')
        return redirect('events:event_detail', pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            
            AuditLog.log(
                action='EVENT_UPDATED',
                user=request.user,
                description=f'Evento atualizado: {event.titulo}',
                request=request,
                obj=event,
                extra_data={'campos_alterados': list(form.changed_data)}
            )
            
            messages.success(request, 'Evento atualizado com sucesso!')
            return redirect('events:event_detail', pk=event.pk)
        else:
            messages.error(request, 'Erro ao atualizar evento. Verifique os dados informados.')
    else:
        form = EventForm(instance=event)
    
    context = {'form': form, 'event': event, 'action': 'Editar'}
    return render(request, 'events/event_form.html', context)


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if request.user != event.organizador:
        messages.error(request, 'Você não tem permissão para excluir este evento.')
        return redirect('events:event_detail', pk=pk)
    
    if request.method == 'POST':
        titulo = event.titulo
        
        AuditLog.log(
            action='EVENT_DELETED',
            user=request.user,
            description=f'Evento excluído: {titulo}',
            request=request,
            extra_data={
                'evento_id': event.pk,
                'titulo': titulo,
                'tipo_evento': event.tipo_evento
            }
        )
        
        event.delete()
        messages.success(request, 'Evento excluído com sucesso!')
        return redirect('events:home')
    
    context = {'event': event}
    return render(request, 'events/event_confirm_delete.html', context)


@login_required
def inscription_create(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    
    if request.user.is_organizador():
        messages.error(request, 'Organizadores não podem se inscrever em eventos.')
        return redirect('events:event_detail', pk=event_pk)
    
    if not request.user.email_confirmed:
        messages.warning(request, 'Você precisa confirmar seu email antes de se inscrever em eventos.')
        return redirect('events:event_detail', pk=event_pk)
    
    if Inscription.objects.filter(evento=event, usuario=request.user).exists():
        messages.warning(request, 'Você já está inscrito neste evento.')
        return redirect('events:event_detail', pk=event_pk)
    
    if not event.tem_vagas():
        messages.error(request, 'Não há mais vagas disponíveis para este evento.')
        return redirect('events:event_detail', pk=event_pk)
    
    if not event.ativo:
        messages.error(request, 'Este evento não está aceitando inscrições.')
        return redirect('events:event_detail', pk=event_pk)
    
    if event.is_passado():
        messages.error(request, 'Este evento já foi encerrado.')
        return redirect('events:event_detail', pk=event_pk)
    
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            inscription = form.save(commit=False)
            inscription.evento = event
            inscription.usuario = request.user
            inscription.status = 'CONFIRMADA'
            
            try:
                inscription.save()
                
                AuditLog.log(
                    action='INSCRIPTION_CREATED',
                    user=request.user,
                    description=f'Inscrição no evento: {event.titulo}',
                    request=request,
                    obj=inscription,
                    extra_data={
                        'evento_id': event.pk,
                        'evento_titulo': event.titulo
                    }
                )
                
                send_inscription_confirmation_email(inscription)
                
                messages.success(request, 'Inscrição realizada com sucesso!')
                return redirect('events:event_detail', pk=event_pk)
            except Exception as e:
                messages.error(request, f'Erro ao realizar inscrição: {str(e)}')
        else:
            messages.error(request, 'Erro ao realizar inscrição.')
    else:
        form = InscriptionForm()
    
    context = {'form': form, 'event': event}
    return render(request, 'events/inscription_form.html', context)


@login_required
def inscription_cancel(request, pk):
    inscription = get_object_or_404(Inscription, pk=pk)
    
    if request.user != inscription.usuario:
        messages.error(request, 'Você não tem permissão para cancelar esta inscrição.')
        return redirect('events:event_detail', pk=inscription.evento.pk)
    
    if request.method == 'POST':
        evento_titulo = inscription.evento.titulo
        inscription.status = 'CANCELADA'
        inscription.save()
        
        AuditLog.log(
            action='INSCRIPTION_CANCELLED',
            user=request.user,
            description=f'Inscrição cancelada: {evento_titulo}',
            request=request,
            obj=inscription,
            extra_data={
                'evento_id': inscription.evento.pk,
                'evento_titulo': evento_titulo
            }
        )
        
        messages.success(request, 'Inscrição cancelada com sucesso!')
        return redirect('events:event_detail', pk=inscription.evento.pk)
    
    context = {'inscription': inscription}
    return render(request, 'events/inscription_confirm_cancel.html', context)


@login_required
def my_inscriptions(request):
    inscriptions = Inscription.objects.filter(
        usuario=request.user,
        status='CONFIRMADA'
    ).select_related('evento').order_by('-data_inscricao')
    
    context = {'inscriptions': inscriptions}
    return render(request, 'events/my_inscriptions.html', context)


@login_required
def my_events(request):
    if not request.user.is_organizador():
        messages.error(request, 'Apenas organizadores podem acessar esta página.')
        return redirect('events:home')
    
    events = Event.objects.filter(
        organizador=request.user
    ).select_related('professor_responsavel').order_by('-data_criacao')
    
    context = {'events': events}
    return render(request, 'events/my_events.html', context)


@login_required
def event_inscriptions(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if request.user != event.organizador:
        messages.error(request, 'Você não tem permissão para visualizar as inscrições deste evento.')
        return redirect('events:event_detail', pk=pk)
    
    inscriptions = event.inscricoes.filter(
        status='CONFIRMADA'
    ).select_related('usuario').order_by('-data_inscricao')
    
    context = {
        'event': event,
        'inscriptions': inscriptions,
    }
    return render(request, 'events/event_inscriptions.html', context)


@login_required
def confirm_presence(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if request.user != event.organizador:
        messages.error(request, 'Você não tem permissão para confirmar presenças.')
        return redirect('events:event_detail', pk=pk)
    
    if request.method == 'POST':
        form = PresenceForm(request.POST, event=event)
        if form.is_valid():
            inscricoes_ids = form.cleaned_data.get('inscricoes', [])
            
            Inscription.objects.filter(evento=event).update(presenca_confirmada=False)
            updated = Inscription.objects.filter(
                pk__in=inscricoes_ids
            ).update(presenca_confirmada=True)
            
            AuditLog.log(
                action='PRESENCE_CONFIRMED',
                user=request.user,
                description=f'Presenças confirmadas no evento: {event.titulo}',
                request=request,
                obj=event,
                extra_data={
                    'total_presentes': updated,
                    'inscricoes_ids': list(inscricoes_ids)
                }
            )
            
            messages.success(request, f'{updated} presença(s) confirmada(s) com sucesso!')
            return redirect('events:event_inscriptions', pk=pk)
    else:
        initial_ids = list(
            event.inscricoes.filter(
                status='CONFIRMADA', 
                presenca_confirmada=True
            ).values_list('pk', flat=True)
        )
        form = PresenceForm(event=event, initial={'inscricoes': initial_ids})
    
    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'events/confirm_presence.html', context)
