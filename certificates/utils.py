from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from io import BytesIO
from datetime import datetime

def generate_certificate_pdf(certificate):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    primary_color = HexColor('#1a5490')
    secondary_color = HexColor('#2c3e50')
    gold_color = HexColor('#d4af37')
    
    p.setStrokeColor(gold_color)
    p.setLineWidth(3)
    p.rect(1*cm, 1*cm, width-2*cm, height-2*cm)
    
    p.setLineWidth(1)
    p.rect(1.2*cm, 1.2*cm, width-2.4*cm, height-2.4*cm)
    
    p.setFont("Helvetica-Bold", 40)
    p.setFillColor(primary_color)
    title = "CERTIFICADO"
    title_width = p.stringWidth(title, "Helvetica-Bold", 40)
    p.drawString((width - title_width) / 2, height - 4*cm, title)
    
    p.setFont("Helvetica", 16)
    p.setFillColor(secondary_color)
    subtitle = "de Participação"
    subtitle_width = p.stringWidth(subtitle, "Helvetica", 16)
    p.drawString((width - subtitle_width) / 2, height - 5*cm, subtitle)
    
    p.setStrokeColor(gold_color)
    p.setLineWidth(2)
    p.line(width/2 - 8*cm, height - 5.5*cm, width/2 + 8*cm, height - 5.5*cm)
    
    p.setFont("Helvetica", 14)
    p.setFillColor(secondary_color)
    
    text1 = "Certificamos que"
    text1_width = p.stringWidth(text1, "Helvetica", 14)
    p.drawString((width - text1_width) / 2, height - 7*cm, text1)
    
    p.setFont("Helvetica-Bold", 22)
    p.setFillColor(primary_color)
    participant_name = certificate.participante.get_full_name().upper()
    name_width = p.stringWidth(participant_name, "Helvetica-Bold", 22)
    p.drawString((width - name_width) / 2, height - 8.5*cm, participant_name)
    
    p.setStrokeColor(gold_color)
    p.setLineWidth(1)
    p.line(width/2 - 10*cm, height - 9*cm, width/2 + 10*cm, height - 9*cm)
    
    p.setFont("Helvetica", 14)
    p.setFillColor(secondary_color)
    
    text2 = f"participou do {certificate.evento.get_tipo_evento_display()}"
    text2_width = p.stringWidth(text2, "Helvetica", 14)
    p.drawString((width - text2_width) / 2, height - 10.5*cm, text2)
    
    p.setFont("Helvetica-Bold", 18)
    p.setFillColor(primary_color)
    event_title = f'"{certificate.evento.titulo}"'
    event_width = p.stringWidth(event_title, "Helvetica-Bold", 18)
    p.drawString((width - event_width) / 2, height - 12*cm, event_title)
    
    p.setFont("Helvetica", 12)
    p.setFillColor(secondary_color)
    
    data_inicio = certificate.evento.data_inicio.strftime('%d/%m/%Y')
    data_fim = certificate.evento.data_fim.strftime('%d/%m/%Y')
    if data_inicio == data_fim:
        event_date = f"realizado em {data_inicio}"
    else:
        event_date = f"realizado no período de {data_inicio} a {data_fim}"
    
    event_date_width = p.stringWidth(event_date, "Helvetica", 12)
    p.drawString((width - event_date_width) / 2, height - 13.5*cm, event_date)
    
    event_location = f"no(a) {certificate.evento.local}"
    location_width = p.stringWidth(event_location, "Helvetica", 12)
    p.drawString((width - location_width) / 2, height - 14.5*cm, event_location)
    
    workload = f"com carga horária de {certificate.carga_horaria} hora(s)"
    workload_width = p.stringWidth(workload, "Helvetica", 12)
    p.drawString((width - workload_width) / 2, height - 15.5*cm, workload)
    
    p.setFont("Helvetica", 10)
    p.setFillColor(HexColor('#666666'))
    
    emission_date = f"Data de Emissão: {certificate.data_emissao.strftime('%d/%m/%Y')}"
    p.drawString(2*cm, 2.5*cm, emission_date)
    
    verification_code = f"Código de Verificação: {certificate.codigo_verificacao}"
    p.drawString(2*cm, 2*cm, verification_code)
    
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(secondary_color)
    
    organizer_name = certificate.emitido_por.get_full_name()
    organizer_width = p.stringWidth(organizer_name, "Helvetica-Bold", 12)
    p.drawString((width - organizer_width) / 2, 4*cm, organizer_name)
    
    p.setStrokeColor(secondary_color)
    p.line(width/2 - 6*cm, 3.8*cm, width/2 + 6*cm, 3.8*cm)
    
    p.setFont("Helvetica", 10)
    organizer_title = "Organizador(a) do Evento"
    title_width = p.stringWidth(organizer_title, "Helvetica", 10)
    p.drawString((width - title_width) / 2, 3.5*cm, organizer_title)
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer.getvalue()
