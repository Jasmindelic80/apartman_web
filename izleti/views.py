"""izleti/views.py"""
from django.shortcuts import render, get_object_or_404
from .models import Lokacija, Kategorija


def lista_lokacija(request):
    kategorije = Kategorija.objects.all()
    kategorija_filter = request.GET.get('kategorija', '')
    lokacije = Lokacija.objects.filter(aktivno=True)
    if kategorija_filter:
        lokacije = lokacije.filter(kategorija__id=kategorija_filter)
    preporucene = lokacije.filter(preporuceno=True)

    return render(request, 'izleti/lista.html', {
        'lokacije': lokacije,
        'kategorije': kategorije,
        'preporucene': preporucene,
        'odabrana_kategorija': kategorija_filter,
    })


def detalji_lokacije(request, pk):
    lokacija = get_object_or_404(Lokacija, pk=pk, aktivno=True)
    slicne = Lokacija.objects.filter(
        kategorija=lokacija.kategorija, aktivno=True
    ).exclude(pk=pk)[:3]

    return render(request, 'izleti/detalji.html', {
        'lokacija': lokacija,
        'slicne': slicne,
    })
