"""
izleti/models.py - Modeli za izlete, restorane i atrakcije
"""
from django.db import models


class Kategorija(models.Model):
    naziv = models.CharField(max_length=100)
    ikona = models.CharField(max_length=10, default='📍')
    boja = models.CharField(max_length=7, default='#3b82f6')  # hex boja za mapu

    class Meta:
        verbose_name = "Kategorija"
        verbose_name_plural = "Kategorije"

    def __str__(self):
        return self.naziv


class Lokacija(models.Model):
    """Izleti, restorani, atrakcije u okolini"""
    naziv = models.CharField(max_length=200, verbose_name="Naziv")
    kategorija = models.ForeignKey(
        Kategorija, on_delete=models.SET_NULL,
        null=True, related_name='lokacije'
    )
    opis = models.TextField(verbose_name="Opis")
    kratki_opis = models.CharField(max_length=200, verbose_name="Kratki opis")
    udaljenost_km = models.FloatField(verbose_name="Udaljenost (km)")
    trajanje_min = models.IntegerField(
        null=True, blank=True, verbose_name="Trajanje vožnje (min)"
    )
    adresa = models.CharField(max_length=300, blank=True)
    lat = models.FloatField(verbose_name="Geografska širina")
    lng = models.FloatField(verbose_name="Geografska dužina")
    slika = models.ImageField(
        upload_to='izleti/', blank=True, verbose_name="Slika"
    )
    web_link = models.URLField(blank=True, verbose_name="Web stranica")
    google_maps_link = models.URLField(blank=True, verbose_name="Google Maps link")
    cijena = models.CharField(
        max_length=50, blank=True,
        verbose_name="Cijena (npr. 'Besplatno' ili '10€')"
    )
    radno_vrijeme = models.CharField(max_length=200, blank=True, verbose_name="Radno vrijeme")
    preporuceno = models.BooleanField(default=False, verbose_name="Naš prijedlog ⭐")
    redoslijed = models.IntegerField(default=0)
    aktivno = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Lokacija"
        verbose_name_plural = "Lokacije"
        ordering = ['redoslijed', 'udaljenost_km']

    def __str__(self):
        return f"{self.naziv} ({self.kategorija})"
