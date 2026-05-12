"""
izleti/admin.py
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Kategorija, Lokacija


@admin.register(Kategorija)
class KategorijaAdmin(admin.ModelAdmin):
    list_display = ['naziv', 'ikona', 'boja_preview']

    def boja_preview(self, obj):
        return format_html(
            '<span style="background:{};padding:3px 12px;border-radius:4px;color:white">{}</span>',
            obj.boja, obj.boja
        )
    boja_preview.short_description = "Boja"


@admin.register(Lokacija)
class LokacijaAdmin(admin.ModelAdmin):
    list_display = ['naziv', 'kategorija', 'udaljenost_km', 'preporuceno', 'aktivno']
    list_editable = ['preporuceno', 'aktivno']
    list_filter = ['kategorija', 'preporuceno']
    search_fields = ['naziv', 'opis']

    fieldsets = (
        ('Osnovne informacije', {
            'fields': ('naziv', 'kategorija', 'kratki_opis', 'opis', 'slika')
        }),
        ('Lokacija', {
            'fields': ('adresa', 'lat', 'lng', 'udaljenost_km', 'trajanje_min')
        }),
        ('Detalji', {
            'fields': ('cijena', 'radno_vrijeme', 'web_link', 'google_maps_link')
        }),
        ('Prikaz', {
            'fields': ('preporuceno', 'redoslijed', 'aktivno')
        }),
    )
