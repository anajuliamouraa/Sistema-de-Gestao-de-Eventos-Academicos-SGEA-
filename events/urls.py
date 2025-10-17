from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.home, name='home'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/create/', views.event_create, name='event_create'),
    path('event/<int:pk>/update/', views.event_update, name='event_update'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('my-events/', views.my_events, name='my_events'),
    path('event/<int:pk>/inscriptions/', views.event_inscriptions, name='event_inscriptions'),
    path('event/<int:event_pk>/inscribe/', views.inscription_create, name='inscription_create'),
    path('inscription/<int:pk>/cancel/', views.inscription_cancel, name='inscription_cancel'),
    path('my-inscriptions/', views.my_inscriptions, name='my_inscriptions'),
]
