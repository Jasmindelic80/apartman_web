"""
rezervacije/management/commands/posalji_emailove.py

Pokretanje: python manage.py posalji_emailove
Dodaj u cron job da se izvršava svaki dan u 09:00
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from rezervacije.models import Rezervacija
from rezervacije.emails import posalji_podsjetnik, posalji_zahvalu
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Šalje automatske emailove — podsjetnik 3 dana prije i zahvalu nakon odlaska'

    def handle(self, *args, **kwargs):
        danas = date.today()
        za_3_dana = danas + timedelta(days=3)

        # Podsjetnici — dolazak za 3 dana
        podsjetnici = Rezervacija.objects.filter(
            datum_dolaska=za_3_dana,
            status__in=['potvrdjeno', 'placeno'],
        )
        for r in podsjetnici:
            posalji_podsjetnik(r)
            self.stdout.write(f'✅ Podsjetnik → {r.email}')

        # Zahvale — odlazak bio jučer
        jucer = danas - timedelta(days=1)
        zahvale = Rezervacija.objects.filter(
            datum_odlaska=jucer,
            status__in=['potvrdjeno', 'placeno', 'zavrseno'],
        )
        for r in zahvale:
            posalji_zahvalu(r)
            # Automatski promijeni status na "završeno"
            r.status = 'zavrseno'
            r.save()
            self.stdout.write(f'✅ Zahvala → {r.email}')

        self.stdout.write(self.style.SUCCESS(
            f'Gotovo! Poslano {podsjetnici.count()} podsjetnika i {zahvale.count()} zahvala.'
        ))
