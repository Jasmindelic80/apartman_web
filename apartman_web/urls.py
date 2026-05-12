"""
urls.py - Glavne URL rute
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # promjena jezika
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('rezervacije/', include('rezervacije.urls', namespace='rezervacije')),
    path('izleti/', include('izleti.urls', namespace='izleti')),
    path('dashboard/', include('dashboard_urls', namespace='dashboard')),
    path('moj-racun/', include('korisnik_urls', namespace='korisnik')),
    path('', include('apartman.urls', namespace='apartman')),
    path('chatbot/', include('chatbot.urls', namespace='chatbot')),
    path('marketing/', include('marketing.urls', namespace='marketing')),
    prefix_default_language=False,
)

# Media fajlovi u razvoju
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
