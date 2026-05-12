"""chatbot/admin.py"""
from django.contrib import admin
from .models import ChatPoruka


@admin.register(ChatPoruka)
class ChatPorukaAdmin(admin.ModelAdmin):
    list_display = ['kreirano', 'pitanje_kratko', 'odgovor_kratko', 'sesija']
    list_filter = ['kreirano']
    search_fields = ['pitanje', 'odgovor']
    readonly_fields = ['kreirano', 'sesija', 'pitanje', 'odgovor']

    def pitanje_kratko(self, obj):
        return obj.pitanje[:60] + '...' if len(obj.pitanje) > 60 else obj.pitanje
    pitanje_kratko.short_description = "Pitanje"

    def odgovor_kratko(self, obj):
        return obj.odgovor[:60] + '...' if len(obj.odgovor) > 60 else obj.odgovor
    odgovor_kratko.short_description = "Odgovor"
