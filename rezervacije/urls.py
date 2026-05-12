"""rezervacije/urls.py - Multi-apartman"""
from django.urls import path
from . import views, paypal_views

app_name = 'rezervacije'

urlpatterns = [
    path('', views.rezerviraj, name='rezerviraj'),
    path('<int:apartman_id>/', views.rezerviraj, name='rezerviraj_apartman'),
    path('potvrda/<uuid:uuid>/', views.potvrda_rezervacije, name='potvrda'),

    # PayPal
    path('paypal/<uuid:uuid>/', views.paypal_placanje, name='paypal'),
    path('paypal/kreiraj/<uuid:uuid>/', paypal_views.kreiraj_paypal_order, name='paypal_kreiraj'),
    path('paypal/potvrdi/<uuid:uuid>/', paypal_views.potvrdi_paypal_order, name='paypal_potvrdi'),

    # API
    path('api/dostupnost/', views.dostupnost_api, name='dostupnost_api'),
    path('api/dostupnost/<int:apartman_id>/', views.dostupnost_api, name='dostupnost_apartman'),
    path('api/sinkroniziraj/', views.sinkroniziraj_ical, name='sinkroniziraj'),
]
