"""chatbot/admin.py"""
from django.contrib import admin
from django.utils.html import format_html
from .models import ChatPoruka, ChatPostavke


@admin.register(ChatPoruka)
class ChatPorukaAdmin(admin.ModelAdmin):
    list_display = ['kreirano', 'pitanje_kratko', 'odgovor_kratko', 'jezik', 'sesija']
    list_filter = ['kreirano', 'jezik']
    search_fields = ['pitanje', 'odgovor']
    readonly_fields = ['kreirano', 'sesija', 'pitanje', 'odgovor', 'jezik']

    def pitanje_kratko(self, obj):
        return obj.pitanje[:60] + '...' if len(obj.pitanje) > 60 else obj.pitanje
    pitanje_kratko.short_description = "Pitanje"

    def odgovor_kratko(self, obj):
        return obj.odgovor[:60] + '...' if len(obj.odgovor) > 60 else obj.odgovor
    odgovor_kratko.short_description = "Odgovor"


@admin.register(ChatPostavke)
class ChatPostavkeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'nacin_prikaza_badge', 'pokazi_na_strankama']

    def has_add_permission(self, request):
        # Dozvoli dodavanje samo ako još nema postavki
        return not ChatPostavke.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Ne dozvoli brisanje
        return False

    fieldsets = (
        ('🎨 GLAVNI IZBOR — Kako prikazati chatbot?', {
            'fields': ('nacin_prikaza',),
            'description': '<p style="background:#fff9eb;padding:1rem;border-left:4px solid #c9a84c;font-size:1rem">'
                          'Odaberi način prikaza i sačuvaj. Promjena se odmah vidi na stranici!</p>',
        }),
        ('💬 Tekst i poruke', {
            'fields': ('naslov', 'podnaslov', 'pozdravna_poruka'),
        }),
        ('💡 Sugerirana pitanja', {
            'fields': ('pokazi_sugerirana', 'sugerirana_pitanja'),
            'description': 'Pitanja koja se pojavljuju kao klikabilna dugmad ispod chata.',
        }),
        ('⚙️ Napredne postavke', {
            'fields': ('pokazi_na_strankama', 'auto_otvori_sekunde', 'boja_dugmeta', 'aktivni_jezici'),
            'classes': ('collapse',),
        }),
    )

    def nacin_prikaza_badge(self, obj):
        boje = {
            'floating': '#3b82f6',
            'uvijek_otvoren': '#10b981',
            'sekcija_pocetna': '#c9a84c',
            'kombinacija': '#9b59b6',
            'auto_otvori': '#f59e0b',
            'iskljucen': '#6b7280',
        }
        boja = boje.get(obj.nacin_prikaza, '#6b7280')
        return format_html(
            '<span style="background:{};color:white;padding:4px 12px;border-radius:4px;font-size:0.85rem">{}</span>',
            boja, obj.get_nacin_prikaza_display()
        )
    nacin_prikaza_badge.short_description = "Trenutni način"
