from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta
from .models import AuditLog
from users.models import CustomUser


@login_required
def audit_list(request):
    if not request.user.is_organizador():
        messages.error(request, 'Apenas organizadores podem acessar os registros de auditoria.')
        return render(request, 'audit/access_denied.html')
    
    logs = AuditLog.objects.all().select_related('user')
    
    date_filter = request.GET.get('date')
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            logs = logs.filter(timestamp__date=filter_date)
        except ValueError:
            pass
    
    period = request.GET.get('period')
    if period:
        today = datetime.now().date()
        if period == 'today':
            logs = logs.filter(timestamp__date=today)
        elif period == 'week':
            start_date = today - timedelta(days=7)
            logs = logs.filter(timestamp__date__gte=start_date)
        elif period == 'month':
            start_date = today - timedelta(days=30)
            logs = logs.filter(timestamp__date__gte=start_date)
    
    user_id = request.GET.get('user')
    if user_id:
        try:
            logs = logs.filter(user_id=int(user_id))
        except (ValueError, TypeError):
            pass
    
    action = request.GET.get('action')
    if action:
        logs = logs.filter(action=action)
    
    search = request.GET.get('search')
    if search:
        logs = logs.filter(
            Q(description__icontains=search) |
            Q(object_repr__icontains=search) |
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search)
        )
    
    paginator = Paginator(logs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    users = CustomUser.objects.filter(audit_logs__isnull=False).distinct().order_by('username')
    actions = AuditLog.ACTION_CHOICES
    
    context = {
        'page_obj': page_obj,
        'users': users,
        'actions': actions,
        'filters': {
            'date': date_filter,
            'period': period,
            'user': user_id,
            'action': action,
            'search': search,
        }
    }
    
    AuditLog.log(
        action='EVENT_API_QUERY',
        user=request.user,
        description='Consulta aos registros de auditoria',
        request=request
    )
    
    return render(request, 'audit/audit_list.html', context)


@login_required
def audit_detail(request, pk):
    if not request.user.is_organizador():
        messages.error(request, 'Apenas organizadores podem acessar os registros de auditoria.')
        return render(request, 'audit/access_denied.html')
    
    try:
        log = AuditLog.objects.select_related('user').get(pk=pk)
    except AuditLog.DoesNotExist:
        messages.error(request, 'Registro de auditoria não encontrado.')
        return render(request, 'audit/audit_list.html')
    
    context = {'log': log}
    return render(request, 'audit/audit_detail.html', context)
