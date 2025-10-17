from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('issue/<int:inscription_pk>/', views.issue_certificate, name='issue'),
    path('my-certificates/', views.my_certificates, name='my_certificates'),
    path('view/<uuid:codigo>/', views.view_certificate, name='view'),
    path('download/<uuid:codigo>/', views.download_certificate, name='download'),
    path('verify/', views.verify_certificate, name='verify'),
]
