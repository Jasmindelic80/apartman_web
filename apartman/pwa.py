"""
apartman/pwa.py - PWA pomoćne rute (opcionalno, ako želimo dinamički manifest)
"""
from django.http import JsonResponse
from .models import Apartman


def manifest_dinamicki(request):
    """Dinamički manifest s podacima iz baze."""
    apartman = Apartman.objects.filter(aktivan=True).first()
    naziv = apartman.naziv if apartman else "Apartman"

    data = {
        "name": naziv,
        "short_name": naziv[:12],
        "description": apartman.podnaslov if apartman else "Vaš odmor",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#1a1a2e",
        "theme_color": "#c9a84c",
        "orientation": "portrait-primary",
        "scope": "/",
        "icons": [
            {
                "src": "/static/icons/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/icons/icon-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ]
    }
    return JsonResponse(data)
