from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dados-dashboard/', views.dados_dashboard, name='dados_dashboard'),
]
