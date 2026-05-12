"""
marketing/models.py - Marketing automatika
"""
from django.db import models
from django.utils import timezone


class Pretplatnik(models.Model):
    """Newsletter pretplatnici."""
    email = models.EmailField(unique=True, verbose_name="Email")
    ime = models.CharField(max_length=100, blank=True, verbose_name="Ime")
    aktivan = models.BooleanField(default=True, verbose_name="Aktivan")
    izvor = models.CharField(
        max_length=50, default='website',
        verbose_name="Izvor (website, rezervacija...)"
    )
    pretplaceno = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pretplatnik"
        verbose_name_plural = "Pretplatnici newslettera"
        ordering = ['-pretplaceno']

    def __str__(self):
        return f"{self.ime or 'Anoniman'} ({self.email})"


class Newsletter(models.Model):
    """Newsletter kampanja."""
    naslov = models.CharField(max_length=200, verbose_name="Naslov")
    sadrzaj = models.TextField(
        verbose_name="Sadržaj (HTML ili tekst)",
        help_text="Možeš koristiti HTML ili AI generator"
    )
    poslano = models.BooleanField(default=False, verbose_name="Poslano")
    datum_slanja = models.DateTimeField(null=True, blank=True)
    primatelji = models.IntegerField(default=0, verbose_name="Broj primatelja")
    kreirano = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletteri"
        ordering = ['-kreirano']

    def __str__(self):
        return self.naslov


class SocialPost(models.Model):
    """Sadržaj za društvene mreže."""
    PLATFORME = [
        ('instagram', '📷 Instagram'),
        ('facebook', '👥 Facebook'),
        ('tiktok', '🎵 TikTok'),
        ('twitter', '🐦 X / Twitter'),
        ('all', '🌍 Sve platforme'),
    ]
    STATUS = [
        ('nacrt', '📝 Nacrt'),
        ('zakazano', '⏰ Zakazano'),
        ('objavljeno', '✅ Objavljeno'),
    ]

    naslov = models.CharField(max_length=200, verbose_name="Interni naslov")
    platforma = models.CharField(max_length=20, choices=PLATFORME, default='all')
    tekst = models.TextField(verbose_name="Tekst posta")
    hashtagovi = models.TextField(blank=True, verbose_name="Hashtagovi")
    slika = models.ImageField(upload_to='social/', blank=True, null=True)
    datum_objave = models.DateTimeField(null=True, blank=True, verbose_name="Datum objave")
    status = models.CharField(max_length=20, choices=STATUS, default='nacrt')
    kreirano = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Post za društvene mreže"
        verbose_name_plural = "Postovi za društvene mreže"
        ordering = ['-kreirano']

    def __str__(self):
        return f"[{self.get_platforma_display()}] {self.naslov}"


class StatistikaPosjete(models.Model):
    """Tracking posjeta stranice."""
    datum = models.DateField(unique=True, default=timezone.now)
    broj_posjeta = models.IntegerField(default=0)
    broj_jedinstvenih = models.IntegerField(default=0)
    najposjecenija_stranica = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Statistika"
        verbose_name_plural = "Statistike posjeta"
        ordering = ['-datum']
