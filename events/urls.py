from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.home, name='home'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/edit/', views.event_update, name='event_update'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('events/<int:pk>/inscriptions/', views.event_inscriptions, name='event_inscriptions'),
    path('events/<int:pk>/presence/', views.confirm_presence, name='confirm_presence'),
    path('events/<int:event_pk>/inscribe/', views.inscription_create, name='inscription_create'),
    path('inscriptions/<int:pk>/cancel/', views.inscription_cancel, name='inscription_cancel'),
    path('my-inscriptions/', views.my_inscriptions, name='my_inscriptions'),
    path('my-events/', views.my_events, name='my_events'),
]
