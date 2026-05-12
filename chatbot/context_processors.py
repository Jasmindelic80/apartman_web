"""
chatbot/context_processors.py
Auto-detekcija jezika browsera za chatbot
"""
from django.utils import translation
from .models import ChatPostavke


# Pozdravne poruke na 4 jezika
POZDRAVI = {
    'bs': "Zdravo! 👋 Ja sam vaš AI asistent. Pitajte me bilo šta o apartmanima, lokaciji ili izletima u okolini!",
    'hr': "Pozdrav! 👋 Ja sam vaš AI asistent. Pitajte me bilo što o apartmanima, lokaciji ili izletima u okolici!",
    'en': "Hello! 👋 I'm your AI assistant. Ask me anything about the apartments, location, or trips in the area!",
    'de': "Hallo! 👋 Ich bin Ihr KI-Assistent. Fragen Sie mich alles über die Apartments, den Standort oder Ausflüge in der Umgebung!",
    'it': "Ciao! 👋 Sono il vostro assistente AI. Chiedetemi qualsiasi cosa sugli appartamenti, sulla posizione o sulle escursioni nella zona!",
    'fr': "Bonjour! 👋 Je suis votre assistant IA. Demandez-moi tout sur les appartements, l'emplacement ou les excursions dans la région!",
    'es': "¡Hola! 👋 Soy tu asistente de IA. ¡Pregúntame cualquier cosa sobre los apartamentos, la ubicación o las excursiones en la zona!",
    'sr': "Здраво! 👋 Ја сам ваш AI асистент. Питајте ме било шта о апартманима, локацији или излетима у околини!",
}

# Sugerirana pitanja po jezicima
SUGERIRANA = {
    'bs': [
        "Koliko košta noćenje?",
        "Gdje se nalazi apartman?",
        "Koji je najbolji restoran u blizini?",
        "Kako daleko je Štrbački buk?",
        "Imate li parking?",
        "Šta posjetiti za vikend?",
    ],
    'hr': [
        "Koliko košta noćenje?",
        "Gdje se nalazi apartman?",
        "Koji je najbolji restoran u blizini?",
        "Kako daleko su Plitvička jezera?",
        "Imate li parking?",
        "Što posjetiti za vikend?",
    ],
    'en': [
        "How much is a night?",
        "Where is the apartment located?",
        "What's the best nearby restaurant?",
        "How far is Plitvice Lakes?",
        "Is there parking?",
        "What to visit for a weekend?",
    ],
    'de': [
        "Wie viel kostet eine Nacht?",
        "Wo befindet sich das Apartment?",
        "Welches ist das beste Restaurant in der Nähe?",
        "Wie weit sind die Plitvicer Seen?",
        "Gibt es einen Parkplatz?",
        "Was kann man am Wochenende besuchen?",
    ],
    'it': [
        "Quanto costa una notte?",
        "Dove si trova l'appartamento?",
        "Qual è il miglior ristorante vicino?",
        "Quanto distano i Laghi di Plitvice?",
        "C'è il parcheggio?",
        "Cosa visitare per un fine settimana?",
    ],
    'fr': [
        "Combien coûte une nuit?",
        "Où se trouve l'appartement?",
        "Quel est le meilleur restaurant à proximité?",
        "À quelle distance sont les lacs de Plitvice?",
        "Y a-t-il un parking?",
        "Que visiter pour un week-end?",
    ],
}

# Naslovi i statusi po jezicima
NASLOVI = {
    'bs': {'naslov': 'AI Asistent', 'status': 'Online · Odgovara odmah'},
    'hr': {'naslov': 'AI Asistent', 'status': 'Online · Odgovara odmah'},
    'en': {'naslov': 'AI Assistant', 'status': 'Online · Responds instantly'},
    'de': {'naslov': 'KI-Assistent', 'status': 'Online · Antwortet sofort'},
    'it': {'naslov': 'Assistente AI', 'status': 'Online · Risponde subito'},
    'fr': {'naslov': 'Assistant IA', 'status': 'En ligne · Répond immédiatement'},
}

POPULARNA_LABEL = {
    'bs': '💡 Popularna pitanja:',
    'hr': '💡 Popularna pitanja:',
    'en': '💡 Popular questions:',
    'de': '💡 Häufige Fragen:',
    'it': '💡 Domande popolari:',
    'fr': '💡 Questions populaires:',
}


def detektiraj_jezik_browsera(request):
    """
    Detektira jezik iz browser headera Accept-Language.
    Vraća kod jezika ('en', 'de', 'it', 'bs', 'hr').
    """
    # 1. Prvi prioritet: trenutni jezik stranice (ako je gost već odabrao)
    trenutni = translation.get_language()
    if trenutni and trenutni[:2] in POZDRAVI:
        return trenutni[:2]

    # 2. Drugi prioritet: browser jezik
    accept_lang = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    if accept_lang:
        # Format: "de-DE,de;q=0.9,en;q=0.8" → uzmi prvi
        prvi = accept_lang.split(',')[0].split(';')[0].strip().lower()

        # Mapiranje varijanti
        mapa = {
            'bs': 'bs', 'hr': 'bs',  # bosanski/hrvatski → bosanski
            'sr': 'bs', 'sr-cyrl': 'bs',  # srpski → bosanski (sličan)
            'en': 'en', 'en-us': 'en', 'en-gb': 'en',
            'de': 'de', 'de-de': 'de', 'de-at': 'de', 'de-ch': 'de',
            'it': 'it', 'it-it': 'it',
            'fr': 'fr', 'fr-fr': 'fr',
            'es': 'en',  # španski → engleski (fallback)
        }

        # Probaj puni kod (npr. "de-de"), pa skraćeni ("de")
        if prvi in mapa:
            return mapa[prvi]
        if prvi[:2] in mapa:
            return mapa[prvi[:2]]

    # 3. Default: bosanski
    return 'bs'


def chatbot_postavke(request):
    """Dostupne u svim templateima."""
    try:
        postavke = ChatPostavke.get_postavke()
    except Exception:
        return {}

    # Detektiraj jezik
    jezik = detektiraj_jezik_browsera(request)

    # Provjera da li pokazati na trenutnoj stranici
    pokazati = True
    putanja = request.path

    if postavke.pokazi_na_strankama == 'samo_pocetna':
        pokazati = putanja in ['/', '/en/', '/de/', '/it/', '/bs/', '/hr/']
    elif postavke.pokazi_na_strankama == 'osim_admin':
        pokazati = '/admin/' not in putanja and '/dashboard/' not in putanja
    elif postavke.pokazi_na_strankama == 'sve':
        pokazati = '/admin/' not in putanja

    if postavke.nacin_prikaza == 'iskljucen':
        pokazati = False

    # Dohvati lokalizovani sadržaj
    pozdrav = POZDRAVI.get(jezik, POZDRAVI['bs'])
    pitanja = SUGERIRANA.get(jezik, SUGERIRANA['bs'])
    naslov_info = NASLOVI.get(jezik, NASLOVI['bs'])
    popularna_label = POPULARNA_LABEL.get(jezik, POPULARNA_LABEL['bs'])

    # Ako je vlasnik definirao vlastiti pozdrav, koristi ga (osim ako je default)
    default_pozdrav = "Pozdrav! 👋 Ja sam vaš AI asistent. Pitajte me bilo što o apartmanima, lokaciji ili izletima u okolici!"
    if postavke.pozdravna_poruka and postavke.pozdravna_poruka.strip() != default_pozdrav.strip():
        pozdrav = postavke.pozdravna_poruka

    return {
        'chatbot_postavke': postavke,
        'pokazi_chatbot': pokazati,
        'sugerirana_pitanja': pitanja if postavke.pokazi_sugerirana else [],
        'chatbot_jezik': jezik,
        'chatbot_pozdrav': pozdrav,
        'chatbot_naslov': naslov_info['naslov'],
        'chatbot_status': naslov_info['status'],
        'chatbot_popularna_label': popularna_label,
    }
