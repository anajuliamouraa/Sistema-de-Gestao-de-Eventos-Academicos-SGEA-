from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_welcome_email(user):
    subject = 'Bem-vindo ao SGEA - Confirme seu cadastro'
    activation_code = user.generate_activation_code()
    activation_url = f"{settings.SITE_URL}/users/activate/{activation_code}/"
    
    context = {
        'user': user,
        'activation_code': activation_code,
        'activation_url': activation_url,
        'site_url': settings.SITE_URL,
    }
    
    html_content = render_to_string('users/emails/welcome_email.html', context)
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False


def send_inscription_confirmation_email(inscription):
    subject = f'Inscrição confirmada - {inscription.evento.titulo}'
    
    context = {
        'user': inscription.usuario,
        'inscription': inscription,
        'evento': inscription.evento,
        'site_url': settings.SITE_URL,
    }
    
    html_content = render_to_string('users/emails/inscription_confirmation.html', context)
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[inscription.usuario.email],
    )
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False


def send_certificate_available_email(certificate):
    subject = f'Seu certificado está disponível - {certificate.evento.titulo}'
    
    context = {
        'user': certificate.participante,
        'certificate': certificate,
        'evento': certificate.evento,
        'site_url': settings.SITE_URL,
        'certificate_url': f"{settings.SITE_URL}/certificates/view/{certificate.codigo_verificacao}/",
    }
    
    html_content = render_to_string('users/emails/certificate_available.html', context)
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[certificate.participante.email],
    )
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False
