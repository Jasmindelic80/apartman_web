"""izleti/urls.py"""
from django.urls import path
from . import views

app_name = 'izleti'

urlpatterns = [
    path('', views.lista_lokacija, name='lista'),
    path('<int:pk>/', views.detalji_lokacije, name='detalji'),
]
