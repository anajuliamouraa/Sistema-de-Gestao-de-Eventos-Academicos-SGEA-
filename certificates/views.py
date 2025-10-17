from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from events.models import Inscription
from .models import Certificate
from .forms import CertificateForm, CertificateVerificationForm
from .utils import generate_certificate_pdf

@login_required
def issue_certificate(request, inscription_pk):
    inscription = get_object_or_404(Inscription, pk=inscription_pk)
    if request.user != inscription.evento.organizador:
        messages.error(request, 'Você não tem permissão para emitir certificados para este evento.')
        return redirect('events:event_detail', pk=inscription.evento.pk)
    if inscription.status != 'CONFIRMADA':
        messages.error(request, 'Não é possível emitir certificado para inscrição não confirmada.')
        return redirect('events:event_inscriptions', pk=inscription.evento.pk)
    if hasattr(inscription, 'certificado'):
        messages.warning(request, 'Já existe um certificado emitido para esta inscrição.')
        return redirect('certificates:view', codigo=inscription.certificado.codigo_verificacao)
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.inscricao = inscription
            certificate.emitido_por = request.user
            certificate.save()
            messages.success(request, 'Certificado emitido com sucesso!')
            return redirect('certificates:view', codigo=certificate.codigo_verificacao)
        else:
            messages.error(request, 'Erro ao emitir certificado. Verifique os dados informados.')
    else:
        form = CertificateForm()
    
    context = {
        'form': form,
        'inscription': inscription,
    }
    return render(request, 'certificates/issue_certificate.html', context)

@login_required
def my_certificates(request):
    certificates = Certificate.objects.filter(
        inscricao__usuario=request.user
    ).order_by('-data_emissao')
    context = {'certificates': certificates}
    return render(request, 'certificates/my_certificates.html', context)

def view_certificate(request, codigo):
    certificate = get_object_or_404(Certificate, codigo_verificacao=codigo)
    context = {'certificate': certificate}
    return render(request, 'certificates/view_certificate.html', context)

def download_certificate(request, codigo):
    certificate = get_object_or_404(Certificate, codigo_verificacao=codigo)
    pdf = generate_certificate_pdf(certificate)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_{certificate.codigo_verificacao}.pdf"'
    return response

def verify_certificate(request):
    certificate = None
    if request.method == 'POST':
        form = CertificateVerificationForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo_verificacao']
            try:
                certificate = Certificate.objects.get(codigo_verificacao=codigo)
                messages.success(request, 'Certificado encontrado e verificado com sucesso!')
            except Certificate.DoesNotExist:
                messages.error(request, 'Certificado não encontrado. Verifique o código informado.')
    else:
        form = CertificateVerificationForm()
    
    context = {
        'form': form,
        'certificate': certificate,
    }
    return render(request, 'certificates/verify_certificate.html', context)
