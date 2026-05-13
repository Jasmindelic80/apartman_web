"""korisnik_urls.py"""
from django.urls import path
from apartman import korisnik

app_name = 'korisnik'

urlpatterns = [
    path('profil/', korisnik.profil, name='profil'),
    path('recenzija/<uuid:rezervacija_uuid>/', korisnik.ostavi_recenziju, name='recenzija'),
]
