"""
marketing/admin.py
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Pretplatnik, Newsletter, SocialPost, StatistikaPosjete


@admin.register(Pretplatnik)
class PretplatnikAdmin(admin.ModelAdmin):
    list_display = ['email', 'ime', 'aktivan', 'izvor', 'pretplaceno']
    list_filter = ['aktivan', 'izvor']
    search_fields = ['email', 'ime']
    list_editable = ['aktivan']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['naslov', 'poslano', 'primatelji', 'datum_slanja', 'akcije']
    list_filter = ['poslano']
    readonly_fields = ['poslano', 'datum_slanja', 'primatelji']
    search_fields = ['naslov']

    def akcije(self, obj):
        if not obj.poslano:
            url = reverse('marketing:posalji_newsletter', args=[obj.pk])
            return format_html(
                '<a href="{}" class="button" style="background:#c9a84c;color:#1a1a2e;padding:5px 12px;text-decoration:none">📧 Pošalji</a>',
                url
            )
        return format_html('<span style="color:#10b981">✅ Poslan</span>')
    akcije.short_description = "Akcije"


@admin.register(SocialPost)
class SocialPostAdmin(admin.ModelAdmin):
    list_display = ['naslov', 'platforma', 'status', 'datum_objave', 'kreirano']
    list_filter = ['platforma', 'status']
    list_editable = ['status']
    search_fields = ['naslov', 'tekst']

    fieldsets = (
        ('Osnovno', {
            'fields': ('naslov', 'platforma', 'status', 'datum_objave')
        }),
        ('Sadržaj', {
            'fields': ('tekst', 'hashtagovi', 'slika'),
            'description': 'Tip "Save and continue editing" da koristiš AI generator'
        }),
    )

    class Media:
        js = ('marketing/ai_generator.js',)


@admin.register(StatistikaPosjete)
class StatistikaPosjeteAdmin(admin.ModelAdmin):
    list_display = ['datum', 'broj_posjeta', 'broj_jedinstvenih', 'najposjecenija_stranica']
    readonly_fields = ['datum', 'broj_posjeta', 'broj_jedinstvenih', 'najposjecenija_stranica']
