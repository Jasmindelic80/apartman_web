"""apartman/korisnik.py - Korisnički portal"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rezervacije.models import Rezervacija
from apartman.models import Recenzija, Apartman
from datetime import date


@login_required
def profil(request):
    moje_rezervacije = Rezervacija.objects.filter(
        gost=request.user
    ).order_by('-datum_dolaska')

    nadolazece = moje_rezervacije.filter(
        datum_dolaska__gte=date.today(),
        status__in=['potvrdjeno', 'placeno', 'cekanje']
    )
    prosle = moje_rezervacije.filter(datum_odlaska__lt=date.today())

    return render(request, 'korisnik/profil.html', {
        'nadolazece': nadolazece,
        'prosle': prosle,
        'ukupno_boravaka': prosle.count(),
    })


@login_required
def ostavi_recenziju(request, rezervacija_uuid):
    from rezervacije.models import Rezervacija
    rezervacija = Rezervacija.objects.get(uuid=rezervacija_uuid, gost=request.user)

    if request.method == 'POST':
        Recenzija.objects.create(
            apartman=rezervacija.apartman,
            ime_gosta=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.email,
            ocjena=request.POST.get('ocjena', 5),
            komentar=request.POST.get('komentar', ''),
            datum=rezervacija.datum_dolaska,
            odobreno=False,
        )
        messages.success(request, 'Hvala na recenziji! Bit će objavljena nakon provjere.')
        return redirect('korisnik:profil')

    return render(request, 'korisnik/recenzija.html', {
        'rezervacija': rezervacija
    })
