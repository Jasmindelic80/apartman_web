"""dashboard/urls.py"""
from django.urls import path
from apartman import dashboard

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard.dashboard, name='glavna'),
    path('kalendar/', dashboard.kalendar_vlasnika, name='kalendar'),
]
