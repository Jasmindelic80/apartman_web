"""apartman/urls.py - Multi-listing URLs"""
from django.urls import path
from . import views
from .seo import robots_txt, sitemap_xml

app_name = 'apartman'

urlpatterns = [
    path('', views.pocetna, name='pocetna'),
    path('apartman/<int:slug>/', views.detalji, name='detalji'),
    path('apartman/', views.detalji, name='detalji_default'),  # za stari link
    path('okolica/', views.mapa_okolice, name='okolica'),
    path('robots.txt', robots_txt, name='robots'),
    path('sitemap.xml', sitemap_xml, name='sitemap'),
]
