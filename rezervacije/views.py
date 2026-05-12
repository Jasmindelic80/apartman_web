"""rezervacije/views.py - Multi-apartman verzija"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.utils.translation import get_language
from .models import Rezervacija, ZauzetTermin
from apartman.models import Apartman
from .utils import dohvati_zauzete_termine
from .emails import posalji_potvrdu_upita, posalji_potvrdu_vlasnik
from datetime import date


def rezerviraj(request, apartman_id=None):
    """Rezervacija — može za određeni apartman ili izbor."""

    # Dohvati apartman
    if apartman_id:
        apartman = get_object_or_404(Apartman, pk=apartman_id, aktivan=True)
    else:
        # Ako nije specificiran, uzmi prvi (backward compat)
        apartman = Apartman.objects.filter(aktivan=True).first()

    svi_apartmani = Apartman.objects.filter(aktivan=True)

    if request.method == 'POST':
        # Iz forme može doći odabrani apartman
        odabrani_id = request.POST.get('apartman_id')
        if odabrani_id:
            apartman = get_object_or_404(Apartman, pk=odabrani_id, aktivan=True)

        datum_dolaska = request.POST.get('datum_dolaska')
        datum_odlaska = request.POST.get('datum_odlaska')

        from datetime import datetime
        od = datetime.strptime(datum_dolaska, '%Y-%m-%d').date()
        do = datetime.strptime(datum_odlaska, '%Y-%m-%d').date()
        noci = (do - od).days
        ukupno = apartman.cijena_po_noci * noci

        rezervacija_data = {
            'apartman': apartman,
            'ime': request.POST.get('ime'),
            'prezime': request.POST.get('prezime'),
            'email': request.POST.get('email'),
            'telefon': request.POST.get('telefon'),
            'drzava': request.POST.get('drzava', ''),
            'datum_dolaska': od,
            'datum_odlaska': do,
            'broj_gostiju': int(request.POST.get('broj_gostiju', 1)),
            'cijena_po_noci': apartman.cijena_po_noci,
            'ukupno': ukupno,
            'napomene_gosta': request.POST.get('napomene', ''),
        }

        # Dodaj jezik ako polje postoji u modelu
        try:
            rezervacija_data['jezik'] = get_language() or 'hr'
            rezervacija = Rezervacija.objects.create(**rezervacija_data)
        except TypeError:
            # Ako polje 'jezik' još nije u modelu
            rezervacija_data.pop('jezik', None)
            rezervacija = Rezervacija.objects.create(**rezervacija_data)

        jezik_stranice = get_language() or 'hr'
        posalji_potvrdu_upita(rezervacija, jezik=jezik_stranice)
        posalji_potvrdu_vlasnik(rezervacija)

        messages.success(request, f'Hvala {rezervacija.ime}!')
        return redirect('rezervacije:potvrda', uuid=rezervacija.uuid)

    # Zauzeti termini SAMO za odabrani apartman
    zauzeti = ZauzetTermin.objects.filter(apartman=apartman) if apartman else []
    zauzeti_json = json.dumps([{
        'od': str(z.datum_od),
        'do': str(z.datum_do),
    } for z in zauzeti])

    return render(request, 'rezervacije/rezerviraj.html', {
        'apartman': apartman,
        'svi_apartmani': svi_apartmani,
        'zauzeti_json': zauzeti_json,
        'danas': str(date.today()),
    })


def potvrda_rezervacije(request, uuid):
    rezervacija = get_object_or_404(Rezervacija, uuid=uuid)
    return render(request, 'rezervacije/potvrda.html', {'rezervacija': rezervacija})


def dostupnost_api(request, apartman_id=None):
    """API — zauzeti termini za određeni apartman."""
    if apartman_id:
        apartman = get_object_or_404(Apartman, pk=apartman_id)
    else:
        apartman = Apartman.objects.filter(aktivan=True).first()

    zauzeti = ZauzetTermin.objects.filter(apartman=apartman)
    return JsonResponse({
        'zauzeto': [{'od': str(z.datum_od), 'do': str(z.datum_do)} for z in zauzeti]
    })


def sinkroniziraj_ical(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Nedovoljna prava'}, status=403)
    apartman = Apartman.objects.filter(aktivan=True).first()
    termini = dohvati_zauzete_termine()
    ZauzetTermin.objects.filter(apartman=apartman).exclude(izvor='direktno').delete()
    for t in termini:
        ZauzetTermin.objects.create(apartman=apartman, datum_od=t['od'], datum_do=t['do'], izvor=t['izvor'])
    return JsonResponse({'status': 'ok', 'uvezeno': len(termini)})


# ===== PAYPAL VIEW =====
def paypal_placanje(request, uuid):
    """PayPal stranica."""
    import os
    rezervacija = get_object_or_404(Rezervacija, uuid=uuid)
    return render(request, 'rezervacije/paypal_placanje.html', {
        'rezervacija': rezervacija,
        'paypal_client_id': os.getenv('PAYPAL_CLIENT_ID', ''),
    })
