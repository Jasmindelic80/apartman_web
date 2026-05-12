"""
rezervacije/utils.py - iCal sinkronizacija s Booking.com i Airbnb
"""
import requests
from django.conf import settings

try:
    from icalendar import Calendar
    ICAL_AVAILABLE = True
except ImportError:
    ICAL_AVAILABLE = False


def dohvati_zauzete_termine():
    # TESTNI PODACI - obrisi kad dobijes pravi iCal
    from datetime import date
    return [
        {'od': date(2025, 6, 10), 'do': date(2025, 6, 15), 'izvor': 'booking'},
        {'od': date(2025, 6, 20), 'do': date(2025, 6, 25), 'izvor': 'airbnb'},
        {'od': date(2025, 7, 1),  'do': date(2025, 7, 7),  'izvor': 'booking'},
    ]
