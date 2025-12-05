from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserUpdateForm
from .models import CustomUser
from .emails import send_welcome_email
from audit.models import AuditLog


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        send_welcome_email(user)
        AuditLog.log(
            action='USER_CREATED',
            user=user,
            description=f'Novo usuário cadastrado: {user.username} ({user.get_perfil_display()})',
            request=self.request,
            obj=user
        )
        messages.success(
            self.request, 
            'Cadastro realizado com sucesso! Verifique seu email para ativar sua conta.'
        )
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro no cadastro. Verifique os dados informados.')
        return super().form_invalid(form)


def activate_account(request, code):
    try:
        user = CustomUser.objects.get(activation_code=code)
        if user.verify_activation_code(code):
            AuditLog.log(
                action='USER_EMAIL_CONFIRMED',
                user=user,
                description=f'Email confirmado para usuário: {user.username}',
                request=request,
                obj=user
            )
            messages.success(
                request,
                'Email confirmado com sucesso! Agora você pode fazer login e usar todas as funcionalidades.'
            )
            return redirect('users:login')
        else:
            messages.error(
                request,
                'Código de ativação expirado ou inválido. Faça login e solicite um novo código.'
            )
            return redirect('users:login')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Código de ativação inválido.')
        return redirect('users:login')


def resend_activation(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email, email_confirmed=False)
            send_welcome_email(user)
            messages.success(request, 'Email de ativação reenviado com sucesso!')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Email não encontrado ou já confirmado.')
        return redirect('users:login')
    
    return render(request, 'users/resend_activation.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('events:home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.email_confirmed and not user.is_superuser:
                messages.warning(
                    request,
                    'Seu email ainda não foi confirmado. Verifique sua caixa de entrada ou solicite um novo código.'
                )
                return render(request, 'users/login.html', {
                    'form': form,
                    'show_resend': True,
                    'user_email': user.email
                })
            
            login(request, user)
            AuditLog.log(
                action='USER_LOGIN',
                user=user,
                description=f'Login realizado: {user.username}',
                request=request,
                obj=user
            )
            messages.success(request, f'Bem-vindo, {user.get_full_name() or user.username}!')
            next_page = request.GET.get('next', 'events:home')
            return redirect(next_page)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    user = request.user
    AuditLog.log(
        action='USER_LOGOUT',
        user=user,
        description=f'Logout realizado: {user.username}',
        request=request,
        obj=user
    )
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('users:login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Erro ao atualizar perfil.')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'users/profile.html', context)
