"""marketing/urls.py"""
from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [
    path('ai-generator/', views.ai_generator_post, name='ai_generator'),
    path('pretplati-se/', views.pretplati_se, name='pretplati_se'),
    path('newsletter/posalji/<int:newsletter_id>/', views.posalji_newsletter, name='posalji_newsletter'),
    path('zahtjevi-recenzije/', views.posalji_zahtjeve_za_recenzije, name='zahtjevi_recenzije'),
]
