"""
apartman/models.py - Modeli za apartman
"""
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Apartman(models.Model):
    naziv = models.CharField(max_length=200, verbose_name="Naziv")
    podnaslov = models.CharField(max_length=300, blank=True, verbose_name="Podnaslov")
    opis = models.TextField(verbose_name="Opis")
    kapacitet = models.IntegerField(verbose_name="Broj gostiju")
    spavace_sobe = models.IntegerField(default=1, verbose_name="Spavaće sobe")
    kupaonice = models.IntegerField(default=1, verbose_name="Kupaonice")
    cijena_po_noci = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Cijena po noći (€)"
    )
    minimalni_boravak = models.IntegerField(default=2, verbose_name="Min. noći")
    adresa = models.CharField(max_length=300, verbose_name="Adresa")
    grad = models.CharField(max_length=100, verbose_name="Grad")
    lat = models.FloatField(verbose_name="Geografska širina")
    lng = models.FloatField(verbose_name="Geografska dužina")
    wifi_lozinka = models.CharField(max_length=100, blank=True, verbose_name="WiFi lozinka")
    pravila_kuce = models.TextField(blank=True, verbose_name="Pravila kuće")
    check_in = models.TimeField(default='15:00', verbose_name="Check-in od")
    check_out = models.TimeField(default='11:00', verbose_name="Check-out do")
    aktivan = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Apartman"
        verbose_name_plural = "Apartmani"

    def __str__(self):
        return self.naziv

    def get_naslovna_slika(self):
        slika = self.slike.filter(naslovna=True).first()
        if not slika:
            slika = self.slike.first()
        return slika


class Slika(models.Model):
    apartman = models.ForeignKey(
        Apartman, on_delete=models.CASCADE,
        related_name='slike', verbose_name="Apartman"
    )
    slika = models.ImageField(upload_to='slike/', verbose_name="Slika")
    thumbnail = ImageSpecField(
        source='slika',
        processors=[ResizeToFill(400, 300)],
        format='JPEG',
        options={'quality': 85}
    )
    naslov = models.CharField(max_length=100, blank=True, verbose_name="Opis slike")
    naslovna = models.BooleanField(default=False, verbose_name="Naslovna slika")
    redoslijed = models.IntegerField(default=0, verbose_name="Redoslijed")

    class Meta:
        verbose_name = "Slika"
        verbose_name_plural = "Slike"
        ordering = ['redoslijed']

    def __str__(self):
        return f"Slika {self.id} - {self.apartman.naziv}"


class Amenity(models.Model):
    """Sadržaji/pogodnosti apartmana"""
    IKONE = [
        ('wifi', '📶 WiFi'),
        ('parking', '🅿️ Parking'),
        ('klima', '❄️ Klima'),
        ('bazen', '🏊 Bazen'),
        ('tv', '📺 TV'),
        ('kuhinja', '🍳 Kuhinja'),
        ('masina_rublje', '👕 Mašina za rublje'),
        ('terasa', '🌿 Terasa'),
        ('roštilj', '🔥 Roštilj'),
        ('kucni_ljubimci', '🐾 Kućni ljubimci OK'),
        ('more', '🌊 Pogled na more'),
        ('planine', '⛰️ Pogled na planine'),
    ]
    naziv = models.CharField(max_length=100, verbose_name="Naziv")
    ikona = models.CharField(max_length=20, choices=IKONE, verbose_name="Ikona")
    apartman = models.ManyToManyField(Apartman, related_name='amenities')

    class Meta:
        verbose_name = "Sadržaj"
        verbose_name_plural = "Sadržaji"

    def __str__(self):
        return self.naziv


class Recenzija(models.Model):
    apartman = models.ForeignKey(
        Apartman, on_delete=models.CASCADE,
        related_name='recenzije', verbose_name="Apartman"
    )
    ime_gosta = models.CharField(max_length=100, verbose_name="Ime gosta")
    drzava = models.CharField(max_length=50, blank=True, verbose_name="Država")
    ocjena = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name="Ocjena (1-5)"
    )
    komentar = models.TextField(verbose_name="Komentar")
    datum = models.DateField(verbose_name="Datum posjeta")
    odobreno = models.BooleanField(default=False, verbose_name="Odobreno za prikaz")
    kreirano = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Recenzija"
        verbose_name_plural = "Recenzije"
        ordering = ['-kreirano']

    def __str__(self):
        return f"{self.ime_gosta} - {self.ocjena}⭐"
