"""
chatbot/models.py
"""
from django.db import models


class ChatPoruka(models.Model):
    sesija = models.CharField(max_length=100, db_index=True)
    pitanje = models.TextField()
    odgovor = models.TextField()
    jezik = models.CharField(max_length=5, default='hr')
    kreirano = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Chat poruka"
        verbose_name_plural = "Chat poruke"
        ordering = ['-kreirano']

    def __str__(self):
        return f"{self.kreirano:%d.%m %H:%M} — {self.pitanje[:50]}"
