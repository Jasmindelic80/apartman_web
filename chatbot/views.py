"""
chatbot/views.py - Auto-detekcija jezika browsera + multi-apartman
"""
import json
import os
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils.translation import get_language
from apartman.models import Apartman
from izleti.models import Lokacija
from .models import ChatPoruka
from .context_processors import detektiraj_jezik_browsera

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def _kreiraj_kontekst(jezik_korisnika='bs'):
    apartmani = Apartman.objects.filter(aktivan=True).prefetch_related('amenities')

    if not apartmani.exists():
        return "No apartment data available."

    jezici = {
        'bs': 'bosanskom', 'hr': 'hrvatskom', 'en': 'English',
        'de': 'German (Deutsch)', 'it': 'Italian (Italiano)',
        'fr': 'French', 'es': 'Spanish', 'sr': 'srpskom',
    }
    naziv_jezika = jezici.get(jezik_korisnika, jezik_korisnika)

    kontekst = f"""
You are an AI assistant helping guests choose between multiple apartments.

LANGUAGE: Detected guest language is {naziv_jezika}.
- ALWAYS respond in SAME language as guest's question
- If guest switches language, switch too
- Default: {naziv_jezika}

WE HAVE {apartmani.count()} APARTMENTS:
"""

    for idx, ap in enumerate(apartmani, 1):
        kontekst += f"""
═══ APARTMENT {idx}: "{ap.naziv}" ═══
- Location: {ap.adresa}, {ap.grad}
- Capacity: {ap.kapacitet} guests
- Bedrooms: {ap.spavace_sobe} | Bathrooms: {ap.kupaonice}
- Price: {ap.cijena_po_noci}€/night | Min stay: {ap.minimalni_boravak} nights
- Check-in: from {ap.check_in} | Check-out: until {ap.check_out}
- Description: {ap.opis}
"""
        if ap.podnaslov:
            kontekst += f"- Tagline: {ap.podnaslov}\n"
        if ap.pravila_kuce:
            kontekst += f"- House rules: {ap.pravila_kuce}\n"

        amenities = ap.amenities.all()
        if amenities:
            kontekst += "- Amenities: " + ", ".join([a.naziv for a in amenities]) + "\n"

    lokacije = Lokacija.objects.filter(aktivno=True)[:15]
    if lokacije:
        kontekst += "\nNEARBY ATTRACTIONS:\n"
        for lok in lokacije:
            kontekst += f"- {lok.naziv} ({lok.kategorija.naziv if lok.kategorija else 'location'}, {lok.udaljenost_km}km): {lok.kratki_opis}\n"

    kontekst += """

RULES:
- Keep responses SHORT (2-4 sentences).
- Be warm, welcoming, like a real host.
- Same language as guest's question.
- For booking → direct to "Book now".
- Don't invent details.
"""
    return kontekst


@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    try:
        data = json.loads(request.body)
        pitanje = data.get('pitanje', '').strip()
        sesija = data.get('sesija') or str(uuid.uuid4())
        jezik_klijent = data.get('jezik', '').strip()

        if not pitanje:
            return JsonResponse({'odgovor': 'Postavite pitanje!', 'sesija': sesija})

        # Hijerarhija detekcije jezika:
        # 1. Jezik klijenta (browser navigator.language)
        # 2. Trenutni jezik stranice
        # 3. Accept-Language header
        # 4. Default 'bs'
        if jezik_klijent and len(jezik_klijent) == 2:
            jezik = jezik_klijent
        else:
            jezik = get_language() or detektiraj_jezik_browsera(request) or 'bs'

        api_key = os.getenv('GEMINI_API_KEY') or getattr(settings, 'GEMINI_API_KEY', '')
        if not api_key or not GEMINI_AVAILABLE:
            return JsonResponse({
                'odgovor': 'Chatbot trenutno nije dostupan.',
                'sesija': sesija,
            })

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')

        prethodne = ChatPoruka.objects.filter(sesija=sesija).order_by('-kreirano')[:5]
        history = []
        for p in reversed(list(prethodne)):
            history.append({'role': 'user', 'parts': [p.pitanje]})
            history.append({'role': 'model', 'parts': [p.odgovor]})

        chat = model.start_chat(history=history)
        kontekst = _kreiraj_kontekst(jezik)
        full_prompt = f"{kontekst}\n\nGUEST QUESTION: {pitanje}"

        response = chat.send_message(full_prompt)
        odgovor = response.text

        ChatPoruka.objects.create(
            sesija=sesija, pitanje=pitanje, odgovor=odgovor, jezik=jezik,
        )

        return JsonResponse({
            'odgovor': odgovor,
            'sesija': sesija,
            'jezik': jezik,
        })

    except Exception as e:
        print(f"Chatbot greška: {e}")
        return JsonResponse({
            'odgovor': 'Oprostite, došlo je do greške. Pokušajte ponovo!',
        }, status=200)
