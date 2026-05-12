"""
rezervacije/signals.py - Automatski emailovi kod promjene statusa
Koristi spremljeni jezik iz rezervacije.
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Rezervacija
from .emails import (
    posalji_potvrdjenu_rezervaciju,
    posalji_otkazanu_rezervaciju,
    posalji_placeno,
)


@receiver(pre_save, sender=Rezervacija)
def zapamti_stari_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            stara = Rezervacija.objects.get(pk=instance.pk)
            instance._stari_status = stara.status
        except Rezervacija.DoesNotExist:
            instance._stari_status = None
    else:
        instance._stari_status = None


@receiver(post_save, sender=Rezervacija)
def posalji_email_kod_promjene_statusa(sender, instance, created, **kwargs):
    if created:
        return

    stari = getattr(instance, '_stari_status', None)
    novi = instance.status
    if stari == novi:
        return

    # Koristi spremljeni jezik (ako postoji u modelu)
    jezik = getattr(instance, 'jezik', 'hr')

    if novi == 'potvrdjeno':
        posalji_potvrdjenu_rezervaciju(instance, jezik=jezik)
        print(f"✅ Email potvrde [{jezik}] poslan: {instance.email}")
    elif novi == 'otkazano':
        posalji_otkazanu_rezervaciju(instance, jezik=jezik)
        print(f"❌ Email otkazivanja [{jezik}] poslan: {instance.email}")
    elif novi == 'placeno':
        posalji_placeno(instance, jezik=jezik)
        print(f"💳 Email plaćanja [{jezik}] poslan: {instance.email}")
