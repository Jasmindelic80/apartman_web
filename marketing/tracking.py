"""
marketing/tracking.py - Custom tracking sistema (radi bez GA)
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import StatistikaPosjete
from datetime import date
import json


@csrf_exempt
@require_http_methods(["POST"])
def track_view(request):
    """Snimaj posjetu u bazu."""
    try:
        # Dohvati ili kreiraj zapis za danas
        zapis, created = StatistikaPosjete.objects.get_or_create(
            datum=date.today(),
            defaults={'broj_posjeta': 0, 'broj_jedinstvenih': 0}
        )
        zapis.broj_posjeta += 1
        if created or not request.session.get('vec_brojan'):
            zapis.broj_jedinstvenih += 1
            request.session['vec_brojan'] = True
        zapis.save()

        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False}, status=200)
