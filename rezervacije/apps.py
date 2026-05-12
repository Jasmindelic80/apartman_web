"""rezervacije/apps.py"""
from django.apps import AppConfig


class RezervacijeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rezervacije'
    verbose_name = 'Rezervacije'

    def ready(self):
        # Učitaj signale kad se app pokrene
        import rezervacije.signals
