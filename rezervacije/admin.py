from django.contrib import admin
from django.utils.html import format_html
from .models import Rezervacija, ZauzetTermin


@admin.register(Rezervacija)
class RezervacijaAdmin(admin.ModelAdmin):
    list_display = [
        'ime', 'prezime', 'email', 'datum_dolaska',
        'datum_odlaska', 'broj_noci_prikaz', 'ukupno', 'status', 'izvor'
    ]
    list_filter = ['status', 'izvor', 'datum_dolaska']
    search_fields = ['ime', 'prezime', 'email']
    readonly_fields = ['uuid', 'kreirano', 'azurirano']

    def broj_noci_prikaz(self, obj):
        return f"{obj.broj_noci} noći"
    broj_noci_prikaz.short_description = "Noći"

    fieldsets = (
        ('Gost', {
            'fields': ('ime', 'prezime', 'email', 'telefon', 'drzava', 'gost')
        }),
        ('Rezervacija', {
            'fields': ('apartman', 'datum_dolaska', 'datum_odlaska',
                      'broj_gostiju', 'cijena_po_noci', 'ukupno')
        }),
        ('Status', {
            'fields': ('status', 'izvor', 'napomene_gosta', 'napomene_vlasnika')
        }),
        ('Sistem', {
            'fields': ('uuid', 'kreirano', 'azurirano'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ZauzetTermin)
class ZauzetTerminAdmin(admin.ModelAdmin):
    list_display = ['apartman', 'datum_od', 'datum_do', 'izvor']
    list_filter = ['izvor', 'apartman']