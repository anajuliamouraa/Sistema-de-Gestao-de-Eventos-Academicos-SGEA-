from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.APIRootView.as_view(), name='root'),
    path('auth/token/', views.CustomObtainAuthToken.as_view(), name='token'),
    path('events/', views.EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('inscriptions/', views.InscriptionCreateView.as_view(), name='inscription-create'),
    path('inscriptions/me/', views.MyInscriptionsView.as_view(), name='my-inscriptions'),
    path('inscriptions/<int:pk>/', views.InscriptionCancelView.as_view(), name='inscription-cancel'),
]
