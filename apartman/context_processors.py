
from django.conf import settings
from .models import Apartman


def globalne_postavke(request):
    apartman = Apartman.objects.filter(aktivan=True).first()
    return {
        'apartman': apartman,
        'maps_key': settings.GOOGLE_MAPS_API_KEY,
        'GA_ID': getattr(settings, 'GA_ID', ''),
        'FACEBOOK_PIXEL': getattr(settings, 'FACEBOOK_PIXEL', ''),
    }
