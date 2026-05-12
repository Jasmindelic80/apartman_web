"""
rezervacije/models.py - Modeli za rezervacije
"""
from django.db import models
from django.contrib.auth.models import User
from apartman.models import Apartman
import uuid


class Rezervacija(models.Model):
    STATUS = [
        ('cekanje', '⏳ Čeka potvrdu'),
        ('potvrdjeno', '✅ Potvrđeno'),
        ('placeno', '💳 Plaćeno'),
        ('otkazano', '❌ Otkazano'),
        ('zavrseno', '🏁 Završeno'),
    ]

    IZVOR = [
        ('direktno', 'Direktna rezervacija'),
        ('booking', 'Booking.com'),
        ('airbnb', 'Airbnb'),
        ('ostalo', 'Ostalo'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    apartman = models.ForeignKey(
        Apartman, on_delete=models.CASCADE,
        related_name='rezervacije'
    )
    gost = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='rezervacije'
    )

    # Podaci gosta (ako nije registriran)
    ime = models.CharField(max_length=100, verbose_name="Ime")
    prezime = models.CharField(max_length=100, verbose_name="Prezime")
    email = models.EmailField(verbose_name="Email")
    telefon = models.CharField(max_length=20, verbose_name="Telefon")
    drzava = models.CharField(max_length=50, blank=True, verbose_name="Država")

    jezik = models.CharField(
        max_length=5,
        default='hr',
        choices=[
            ('hr', 'Hrvatski'),
            ('en', 'English'),
            ('de', 'Deutsch'),
            ('it', 'Italiano'),
        ],
        verbose_name="Jezik gosta"
    )

    # Datumi
    datum_dolaska = models.DateField(verbose_name="Datum dolaska")
    datum_odlaska = models.DateField(verbose_name="Datum odlaska")

    # Financije
    broj_gostiju = models.IntegerField(default=1, verbose_name="Broj gostiju")
    cijena_po_noci = models.DecimalField(max_digits=8, decimal_places=2)
    ukupno = models.DecimalField(max_digits=10, decimal_places=2)

    # Status
    status = models.CharField(max_length=20, choices=STATUS, default='cekanje')
    izvor = models.CharField(max_length=20, choices=IZVOR, default='direktno')

    # Napomene
    napomene_gosta = models.TextField(blank=True, verbose_name="Napomene gosta")
    napomene_vlasnika = models.TextField(blank=True, verbose_name="Privatne napomene")

    # Vremenski zapisi
    kreirano = models.DateTimeField(auto_now_add=True)
    azurirano = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Rezervacija"
        verbose_name_plural = "Rezervacije"
        ordering = ['-datum_dolaska']

    def __str__(self):
        return f"{self.ime} {self.prezime} — {self.datum_dolaska} do {self.datum_odlaska}"

    @property
    def broj_noci(self):
        return (self.datum_odlaska - self.datum_dolaska).days

    def izracunaj_ukupno(self):
        return self.cijena_po_noci * self.broj_noci


class ZauzetTermin(models.Model):
    """Termini povučeni s Booking/Airbnb iCal"""
    apartman = models.ForeignKey(
        Apartman, on_delete=models.CASCADE,
        related_name='zauzeti_termini'
    )
    datum_od = models.DateField()
    datum_do = models.DateField()
    izvor = models.CharField(max_length=20, default='booking')
    napomena = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Zauzet termin"
        verbose_name_plural = "Zauzeti termini"

    def __str__(self):
        return f"{self.izvor}: {self.datum_od} — {self.datum_do}"
