from django.contrib import admin
from django.utils.html import format_html
from .models import Apartman, Slika, Amenity, Recenzija


class SlikaInline(admin.TabularInline):
    model = Slika
    extra = 3
    fields = ['slika', 'naslov', 'naslovna', 'redoslijed']


@admin.register(Apartman)
class ApartmanAdmin(admin.ModelAdmin):
    list_display = ['naziv', 'grad', 'kapacitet', 'cijena_po_noci', 'aktivan']
    list_editable = ['aktivan', 'cijena_po_noci']
    search_fields = ['naziv', 'grad', 'adresa']
    inlines = [SlikaInline]

    fieldsets = (
        ('Osnovne informacije', {
            'fields': ('naziv', 'podnaslov', 'opis', 'aktivan')
        }),
        ('Detalji', {
            'fields': ('kapacitet', 'spavace_sobe', 'kupaonice',
                      'cijena_po_noci', 'minimalni_boravak')
        }),
        ('Lokacija', {
            'fields': ('adresa', 'grad', 'lat', 'lng')
        }),
        ('Check-in / Check-out', {
            'fields': ('check_in', 'check_out', 'wifi_lozinka', 'pravila_kuce')
        }),
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['naziv', 'ikona']


@admin.register(Recenzija)
class RecenzijaAdmin(admin.ModelAdmin):
    list_display = ['ime_gosta', 'drzava', 'ocjena', 'datum', 'odobreno']
    list_editable = ['odobreno']
    list_filter = ['odobreno', 'ocjena']