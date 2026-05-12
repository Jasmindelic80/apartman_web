"""
apartman/views.py - Multi-listing verzija
Više apartmana, gost bira između njih.
"""
import json
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Apartman, Recenzija
from izleti.models import Lokacija, Kategorija


def pocetna(request):
    """Početna — prikazuje SVE aktivne apartmane."""
    apartmani = Apartman.objects.filter(aktivan=True).prefetch_related('slike', 'amenities')
    recenzije = Recenzija.objects.filter(odobreno=True)[:6]

    context = {
        'apartmani': apartmani,
        'recenzije': recenzije,
        'maps_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'apartman/pocetna.html', context)


def detalji(request, slug=None):
    """Detalji jednog apartmana — preko ID-a."""
    if slug:
        apartman = get_object_or_404(Apartman, pk=slug, aktivan=True)
    else:
        # Backward compatibility — ako pristupi /apartman/ bez ID-a
        apartman = Apartman.objects.filter(aktivan=True).first()

    slike = apartman.slike.all()
    amenities = apartman.amenities.all()

    context = {
        'apartman': apartman,
        'slike': slike,
        'amenities': amenities,
        'maps_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'apartman/detalji.html', context)


def mapa_okolice(request):
    """Mapa — prikazuje SVE apartmane + sve lokacije."""
    apartmani = Apartman.objects.filter(aktivan=True)
    kategorije = Kategorija.objects.all()

    kategorija_filter = request.GET.get('kategorija', '')
    lokacije = Lokacija.objects.filter(aktivno=True)
    if kategorija_filter:
        lokacije = lokacije.filter(kategorija__id=kategorija_filter)

    apartmani_json = json.dumps([{
        'id': a.id,
        'naziv': a.naziv,
        'lat': a.lat,
        'lng': a.lng,
        'cijena': float(a.cijena_po_noci),
    } for a in apartmani])

    lokacije_json = json.dumps([{
        'id': lok.id,
        'naziv': lok.naziv,
        'kratki_opis': lok.kratki_opis,
        'lat': lok.lat,
        'lng': lok.lng,
        'kategorija': lok.kategorija.naziv if lok.kategorija else '',
        'ikona': lok.kategorija.ikona if lok.kategorija else '📍',
        'boja': lok.kategorija.boja if lok.kategorija else '#3b82f6',
        'udaljenost': lok.udaljenost_km,
        'preporuceno': lok.preporuceno,
        'link': lok.google_maps_link or '',
    } for lok in lokacije])

    context = {
        'apartmani': apartmani,
        'apartmani_json': apartmani_json,
        'kategorije': kategorije,
        'lokacije': lokacije,
        'lokacije_json': lokacije_json,
        'maps_key': settings.GOOGLE_MAPS_API_KEY,
        'odabrana_kategorija': kategorija_filter,
    }
    return render(request, 'izleti/mapa.html', context)
