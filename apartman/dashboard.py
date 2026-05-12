"""
apartman/dashboard.py - Dashboard za vlasnika
"""
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rezervacije.models import Rezervacija, ZauzetTermin
from apartman.models import Apartman, Recenzija
from izleti.models import Lokacija
import json
from datetime import date, timedelta


@staff_member_required
def dashboard(request):
    apartman = Apartman.objects.filter(aktivan=True).first()
    danas = date.today()
    pocetak_godine = danas.replace(month=1, day=1)

    # Statistike rezervacija
    sve_rezervacije = Rezervacija.objects.filter(apartman=apartman)
    aktivne = sve_rezervacije.filter(
        status__in=['potvrdjeno', 'placeno'],
        datum_odlaska__gte=danas
    )
    cekaju = sve_rezervacije.filter(status='cekanje')

    # Prihodi ove godine
    prihodi_godina = sve_rezervacije.filter(
        status__in=['potvrdjeno', 'placeno', 'zavrseno'],
        datum_dolaska__gte=pocetak_godine
    ).aggregate(ukupno=Sum('ukupno'))['ukupno'] or 0

    # Prihodi po mjesecima (zadnjih 6)
    prihodi_mjeseci = []
    for i in range(5, -1, -1):
        mjesec_datum = danas.replace(day=1) - timedelta(days=i*30)
        prihod = sve_rezervacije.filter(
            status__in=['potvrdjeno', 'placeno', 'zavrseno'],
            datum_dolaska__year=mjesec_datum.year,
            datum_dolaska__month=mjesec_datum.month,
        ).aggregate(ukupno=Sum('ukupno'))['ukupno'] or 0
        prihodi_mjeseci.append({
            'mjesec': mjesec_datum.strftime('%b %Y'),
            'prihod': float(prihod)
        })

    # Nadolazeće rezervacije (sljedećih 30 dana)
    nadolazece = sve_rezervacije.filter(
        datum_dolaska__gte=danas,
        datum_dolaska__lte=danas + timedelta(days=30),
        status__in=['potvrdjeno', 'placeno', 'cekanje']
    ).order_by('datum_dolaska')

    # Popunjenost ovog mjeseca
    dani_u_mjesecu = 30
    zauzeti_dani = ZauzetTermin.objects.filter(
        apartman=apartman,
        datum_od__month=danas.month
    ).count()
    popunjenost = round((zauzeti_dani / dani_u_mjesecu) * 100)

    # Recenzije
    prosjecna_ocjena = Recenzija.objects.filter(
        apartman=apartman, odobreno=True
    ).aggregate(avg=Sum('ocjena'))

    context = {
        'apartman': apartman,
        'aktivne_rezervacije': aktivne.count(),
        'cekaju_potvrdu': cekaju.count(),
        'prihodi_godina': prihodi_godina,
        'nadolazece': nadolazece,
        'popunjenost': popunjenost,
        'prihodi_json': json.dumps(prihodi_mjeseci),
        'ukupno_rezervacija': sve_rezervacije.count(),
    }
    return render(request, 'dashboard/dashboard.html', context)


@staff_member_required
def kalendar_vlasnika(request):
    """Kalendar svih rezervacija za vlasnika"""
    apartman = Apartman.objects.filter(aktivan=True).first()
    rezervacije = Rezervacija.objects.filter(
        apartman=apartman,
        datum_odlaska__gte=date.today()
    ).order_by('datum_dolaska')

    rezervacije_json = json.dumps([{
        'id': str(r.uuid),
        'title': f"{r.ime} {r.prezime}",
        'start': str(r.datum_dolaska),
        'end': str(r.datum_odlaska),
        'color': {
            'cekanje': '#f59e0b',
            'potvrdjeno': '#3b82f6',
            'placeno': '#10b981',
            'otkazano': '#ef4444',
            'zavrseno': '#6b7280',
        }.get(r.status, '#3b82f6'),
        'extendedProps': {
            'status': r.get_status_display(),
            'email': r.email,
            'telefon': r.telefon,
            'gostiju': r.broj_gostiju,
            'ukupno': str(r.ukupno),
        }
    } for r in rezervacije])

    return render(request, 'dashboard/kalendar.html', {
        'apartman': apartman,
        'rezervacije_json': rezervacije_json,
    })
