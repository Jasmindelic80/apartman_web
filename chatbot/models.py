"""
chatbot/models.py
"""
from django.db import models


class ChatPoruka(models.Model):
    sesija = models.CharField(max_length=100, db_index=True)
    pitanje = models.TextField()
    odgovor = models.TextField()
    jezik = models.CharField(max_length=5, default='hr')
    kreirano = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Chat poruka"
        verbose_name_plural = "Chat poruke"
        ordering = ['-kreirano']

    def __str__(self):
        return f"{self.kreirano:%d.%m %H:%M} — {self.pitanje[:50]}"


class ChatPostavke(models.Model):
    """Postavke za prikaz chatbota — može se mijenjati iz admina."""

    NACINI_PRIKAZA = [
        ('floating', '💬 A — Floating dugme (klasično, donji desni ugao)'),
        ('uvijek_otvoren', '🪟 B — Uvijek otvoren u uglu (kao Messenger)'),
        ('sekcija_pocetna', '🎯 C — Velika sekcija na početnoj stranici'),
        ('kombinacija', '⭐ D — Kombinacija: sekcija na početnoj + dugme svuda'),
        ('auto_otvori', '🔔 E — Pojavi se sam nakon X sekundi'),
        ('iskljucen', '🚫 F — Isključen (nigdje se ne prikazuje)'),
    ]

    nacin_prikaza = models.CharField(
        max_length=30,
        choices=NACINI_PRIKAZA,
        default='floating',
        verbose_name="Način prikaza chatbota",
    )

    pozdravna_poruka = models.TextField(
        default="Pozdrav! 👋 Ja sam vaš AI asistent. Pitajte me bilo što o apartmanima, lokaciji ili izletima u okolici!",
        verbose_name="Pozdravna poruka",
        help_text="Prva poruka koju gost vidi"
    )

    naslov = models.CharField(
        max_length=100,
        default="AI Asistent",
        verbose_name="Naslov chatbota"
    )

    podnaslov = models.CharField(
        max_length=200,
        default="Online · Odgovara odmah",
        verbose_name="Podnaslov / status"
    )

    auto_otvori_sekunde = models.IntegerField(
        default=10,
        verbose_name="Sekunde prije auto-otvaranja",
        help_text="Samo za način 'Pojavi se sam'"
    )

    pokazi_sugerirana = models.BooleanField(
        default=True,
        verbose_name="Pokaži sugerirana pitanja",
        help_text="Tagovi sa popularnim pitanjima ispod chata"
    )

    sugerirana_pitanja = models.TextField(
        default="Koliko košta noćenje?\nGdje se nalazi apartman?\nKoji je najbolji restoran u blizini?\nKako daleko je Plitvička jezera?\nImate li parking?",
        verbose_name="Sugerirana pitanja",
        help_text="Jedno pitanje po liniji (max 6)"
    )

    pokazi_na_strankama = models.CharField(
        max_length=100,
        default='sve',
        choices=[
            ('sve', 'Na svim stranicama'),
            ('samo_pocetna', 'Samo na početnoj'),
            ('osim_admin', 'Sve osim admina'),
        ],
        verbose_name="Gdje pokazati"
    )

    boja_dugmeta = models.CharField(
        max_length=20,
        default='#c9a84c',
        verbose_name="Boja dugmeta (hex)"
    )

    aktivni_jezici = models.CharField(
        max_length=100,
        default='bs,en,de,it',
        verbose_name="Aktivni jezici",
        help_text="Razdvoji zarezom: bs,en,de,it"
    )

    class Meta:
        verbose_name = "Postavke chatbota"
        verbose_name_plural = "Postavke chatbota"

    def __str__(self):
        return f"Chatbot postavke ({self.get_nacin_prikaza_display()})"

    def save(self, *args, **kwargs):
        # Osiguraj da postoji samo jedan zapis
        if not self.pk and ChatPostavke.objects.exists():
            ChatPostavke.objects.all().delete()
        super().save(*args, **kwargs)

    @classmethod
    def get_postavke(cls):
        """Vraća postavke ili kreira default."""
        postavke = cls.objects.first()
        if not postavke:
            postavke = cls.objects.create()
        return postavke

    def get_sugerirana_lista(self):
        """Vraća listu pitanja."""
        return [p.strip() for p in self.sugerirana_pitanja.split('\n') if p.strip()][:6]
