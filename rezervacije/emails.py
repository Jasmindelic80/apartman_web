"""
rezervacije/emails.py - Višejezični automatski emailovi
Detektira jezik gosta i šalje email na njegovom jeziku.
"""
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags


# === PRIJEVODI ZA SVE EMAILOVE ===

PRIJEVODI = {
    'hr': {
        # Predmeti
        'predmet_upit': '✅ Primili smo vaš upit — {naziv}',
        'predmet_potvrdjeno': '✅ Rezervacija potvrđena — {naziv}',
        'predmet_otkazano': 'Rezervacija otkazana — {naziv}',
        'predmet_placeno': '💳 Plaćanje primljeno — {naziv}',
        'predmet_podsjetnik': '🏠 Vaš dolazak za 3 dana — {naziv}',
        'predmet_zahvala': 'Hvala na posjetu — {naziv}',
        'predmet_vlasnik': '🔔 Novi upit — {ime} {prezime}',
        # Sadržaj
        'pozdrav': 'Dragi/a',
        'upit_primljen': 'Primili smo vaš upit za rezervaciju! Kontaktirat ćemo vas u najkraćem roku.',
        'upit_obrada': '⏳ Vaš upit je u obradi — čeka potvrdu vlasnika.',
        'upit_email_potvrda': '📧 Dobit ćete email čim vaša rezervacija bude potvrđena.',
        'apartman': 'Apartman',
        'dolazak': 'Dolazak',
        'odlazak': 'Odlazak',
        'broj_noci': 'Broj noći',
        'broj_gostiju': 'Broj gostiju',
        'ukupno': 'Ukupno',
        'referentni_broj': 'Referentni broj',
        'rezervacija_potvrdjena': '✅ Vaša rezervacija je POTVRĐENA!',
        'veselimo_se': 'Veselimo se vašem dolasku! Sve je spremno za vaš boravak.',
        'info_dolazak': '📍 Informacije za dolazak',
        'adresa': 'Adresa',
        'check_in': 'Check-in',
        'check_out': 'Check-out',
        'od': 'od',
        'do': 'do',
        'detaljne_upute': 'Detaljne upute (kako doći, gdje parkirati, itd.) poslat ćemo vam 3 dana prije dolaska.',
        'rezervacija_otkazana': '❌ Vaša rezervacija je otkazana',
        'nazalost': 'Nažalost, vaša rezervacija ne može biti potvrđena u ovom terminu.',
        'drugi_termin': 'Ako želite, slobodno se javite za drugi termin — bit će nam drago ugostiti vas!',
        'placanje_primljeno': '💳 Plaćanje primljeno!',
        'hvala_uplata': 'Potvrđujemo primitak uplate u iznosu od',
        'dobrodosli_uskoro': 'Dobrodošli uskoro',
        'dolazak_za_3_dana': 'Vaš dolazak je za <strong>3 dana</strong>',
        'wifi': 'WiFi',
        'hvala_posjeta': 'Hvala',
        'uzivali_boravak': 'Nadamo se da ste uživali u boravku!',
        'misljenje_znaci': 'Vaše mišljenje nam puno znači:',
        'ostavi_recenziju': '⭐ Ostavi recenziju',
    },
    'en': {
        'predmet_upit': '✅ We received your inquiry — {naziv}',
        'predmet_potvrdjeno': '✅ Reservation confirmed — {naziv}',
        'predmet_otkazano': 'Reservation cancelled — {naziv}',
        'predmet_placeno': '💳 Payment received — {naziv}',
        'predmet_podsjetnik': '🏠 Your arrival in 3 days — {naziv}',
        'predmet_zahvala': 'Thank you for your visit — {naziv}',
        'predmet_vlasnik': '🔔 New inquiry — {ime} {prezime}',

        'pozdrav': 'Dear',
        'upit_primljen': 'We have received your reservation request! We will contact you shortly.',
        'upit_obrada': '⏳ Your inquiry is being processed — awaiting owner confirmation.',
        'upit_email_potvrda': '📧 You will receive an email as soon as your reservation is confirmed.',
        'apartman': 'Apartment',
        'dolazak': 'Arrival',
        'odlazak': 'Departure',
        'broj_noci': 'Number of nights',
        'broj_gostiju': 'Number of guests',
        'ukupno': 'Total',
        'referentni_broj': 'Reference number',
        'rezervacija_potvrdjena': '✅ Your reservation is CONFIRMED!',
        'veselimo_se': 'We look forward to your arrival! Everything is ready for your stay.',
        'info_dolazak': '📍 Arrival information',
        'adresa': 'Address',
        'check_in': 'Check-in',
        'check_out': 'Check-out',
        'od': 'from',
        'do': 'until',
        'detaljne_upute': 'Detailed instructions (how to get there, parking, etc.) will be sent 3 days before arrival.',
        'rezervacija_otkazana': '❌ Your reservation has been cancelled',
        'nazalost': 'Unfortunately, your reservation cannot be confirmed for this term.',
        'drugi_termin': 'If you wish, feel free to contact us for another term — we would be glad to host you!',
        'placanje_primljeno': '💳 Payment received!',
        'hvala_uplata': 'We confirm receipt of your payment in the amount of',
        'dobrodosli_uskoro': 'Welcome soon',
        'dolazak_za_3_dana': 'Your arrival is in <strong>3 days</strong>',
        'wifi': 'WiFi',
        'hvala_posjeta': 'Thank you',
        'uzivali_boravak': 'We hope you enjoyed your stay!',
        'misljenje_znaci': 'Your opinion means a lot to us:',
        'ostavi_recenziju': '⭐ Leave a review',
    },
    'de': {
        'predmet_upit': '✅ Wir haben Ihre Anfrage erhalten — {naziv}',
        'predmet_potvrdjeno': '✅ Reservierung bestätigt — {naziv}',
        'predmet_otkazano': 'Reservierung storniert — {naziv}',
        'predmet_placeno': '💳 Zahlung erhalten — {naziv}',
        'predmet_podsjetnik': '🏠 Ihre Ankunft in 3 Tagen — {naziv}',
        'predmet_zahvala': 'Danke für Ihren Besuch — {naziv}',
        'predmet_vlasnik': '🔔 Neue Anfrage — {ime} {prezime}',

        'pozdrav': 'Liebe/r',
        'upit_primljen': 'Wir haben Ihre Reservierungsanfrage erhalten! Wir werden uns in Kürze bei Ihnen melden.',
        'upit_obrada': '⏳ Ihre Anfrage wird bearbeitet — wartet auf Bestätigung des Eigentümers.',
        'upit_email_potvrda': '📧 Sie erhalten eine E-Mail, sobald Ihre Reservierung bestätigt ist.',
        'apartman': 'Apartment',
        'dolazak': 'Anreise',
        'odlazak': 'Abreise',
        'broj_noci': 'Anzahl der Nächte',
        'broj_gostiju': 'Anzahl der Gäste',
        'ukupno': 'Gesamt',
        'referentni_broj': 'Referenznummer',
        'rezervacija_potvrdjena': '✅ Ihre Reservierung ist BESTÄTIGT!',
        'veselimo_se': 'Wir freuen uns auf Ihre Ankunft! Alles ist bereit für Ihren Aufenthalt.',
        'info_dolazak': '📍 Anreiseinformationen',
        'adresa': 'Adresse',
        'check_in': 'Check-in',
        'check_out': 'Check-out',
        'od': 'ab',
        'do': 'bis',
        'detaljne_upute': 'Detaillierte Anweisungen (Anfahrt, Parken usw.) senden wir Ihnen 3 Tage vor Ankunft.',
        'rezervacija_otkazana': '❌ Ihre Reservierung wurde storniert',
        'nazalost': 'Leider kann Ihre Reservierung für diesen Termin nicht bestätigt werden.',
        'drugi_termin': 'Wenn Sie möchten, kontaktieren Sie uns gerne für einen anderen Termin — wir würden uns freuen, Sie willkommen zu heißen!',
        'placanje_primljeno': '💳 Zahlung erhalten!',
        'hvala_uplata': 'Wir bestätigen den Eingang Ihrer Zahlung in Höhe von',
        'dobrodosli_uskoro': 'Bald willkommen',
        'dolazak_za_3_dana': 'Ihre Ankunft ist in <strong>3 Tagen</strong>',
        'wifi': 'WLAN',
        'hvala_posjeta': 'Danke',
        'uzivali_boravak': 'Wir hoffen, Sie haben Ihren Aufenthalt genossen!',
        'misljenje_znaci': 'Ihre Meinung bedeutet uns viel:',
        'ostavi_recenziju': '⭐ Bewertung abgeben',
    },
    'it': {
        'predmet_upit': '✅ Abbiamo ricevuto la sua richiesta — {naziv}',
        'predmet_potvrdjeno': '✅ Prenotazione confermata — {naziv}',
        'predmet_otkazano': 'Prenotazione annullata — {naziv}',
        'predmet_placeno': '💳 Pagamento ricevuto — {naziv}',
        'predmet_podsjetnik': '🏠 Il suo arrivo tra 3 giorni — {naziv}',
        'predmet_zahvala': 'Grazie per la sua visita — {naziv}',
        'predmet_vlasnik': '🔔 Nuova richiesta — {ime} {prezime}',

        'pozdrav': 'Gentile',
        'upit_primljen': 'Abbiamo ricevuto la sua richiesta di prenotazione! La contatteremo al più presto.',
        'upit_obrada': '⏳ La sua richiesta è in elaborazione — in attesa di conferma del proprietario.',
        'upit_email_potvrda': '📧 Riceverà un\'email non appena la sua prenotazione sarà confermata.',
        'apartman': 'Appartamento',
        'dolazak': 'Arrivo',
        'odlazak': 'Partenza',
        'broj_noci': 'Numero di notti',
        'broj_gostiju': 'Numero di ospiti',
        'ukupno': 'Totale',
        'referentni_broj': 'Numero di riferimento',
        'rezervacija_potvrdjena': '✅ La sua prenotazione è CONFERMATA!',
        'veselimo_se': 'Aspettiamo con gioia il suo arrivo! Tutto è pronto per il suo soggiorno.',
        'info_dolazak': '📍 Informazioni per l\'arrivo',
        'adresa': 'Indirizzo',
        'check_in': 'Check-in',
        'check_out': 'Check-out',
        'od': 'dalle',
        'do': 'entro le',
        'detaljne_upute': 'Le istruzioni dettagliate (come arrivare, parcheggio, ecc.) saranno inviate 3 giorni prima dell\'arrivo.',
        'rezervacija_otkazana': '❌ La sua prenotazione è stata annullata',
        'nazalost': 'Purtroppo, la sua prenotazione non può essere confermata per questo periodo.',
        'drugi_termin': 'Se desidera, ci contatti per un altro periodo — saremmo lieti di ospitarla!',
        'placanje_primljeno': '💳 Pagamento ricevuto!',
        'hvala_uplata': 'Confermiamo la ricezione del pagamento di',
        'dobrodosli_uskoro': 'Benvenuti presto',
        'dolazak_za_3_dana': 'Il suo arrivo è tra <strong>3 giorni</strong>',
        'wifi': 'WiFi',
        'hvala_posjeta': 'Grazie',
        'uzivali_boravak': 'Speriamo che abbia goduto del suo soggiorno!',
        'misljenje_znaci': 'La sua opinione conta molto per noi:',
        'ostavi_recenziju': '⭐ Lascia una recensione',
    },
}


def t(jezik, kljuc, **kwargs):
    """Helper za prijevod."""
    rj = PRIJEVODI.get(jezik, PRIJEVODI['hr'])
    tekst = rj.get(kljuc, PRIJEVODI['hr'].get(kljuc, kljuc))
    return tekst.format(**kwargs) if kwargs else tekst


def _detektiraj_jezik(rezervacija):
    """
    Pokuša detektirati jezik gosta iz polja `drzava` ili default 'hr'.
    Možeš ovo proširiti — npr. spremiti jezik iz forme.
    """
    drzava = (rezervacija.drzava or '').lower().strip()

    mapa = {
        # English
        'uk': 'en', 'usa': 'en', 'us': 'en', 'ireland': 'en', 'australia': 'en',
        'united kingdom': 'en', 'united states': 'en', 'england': 'en',
        # German
        'germany': 'de', 'austria': 'de', 'switzerland': 'de',
        'deutschland': 'de', 'österreich': 'de', 'schweiz': 'de',
        'njemačka': 'de', 'austrija': 'de', 'švicarska': 'de',
        # Italian
        'italy': 'it', 'italia': 'it', 'italija': 'it',
        # Croatian (default)
        'croatia': 'hr', 'hrvatska': 'hr', 'bosna': 'hr',
        'serbia': 'hr', 'montenegro': 'hr',
    }
    return mapa.get(drzava, 'hr')


def _posalji(predmet, html, primatelji):
    try:
        msg = EmailMultiAlternatives(
            subject=predmet,
            body=strip_tags(html),
            from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
            to=primatelji,
        )
        msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"❌ Email greška: {e}")
        return False


def _zaglavlje(apartman):
    return f"""
    <div style="background:#1a1a2e;padding:2rem;text-align:center">
        <h1 style="color:#c9a84c;font-size:1.5rem;margin:0;font-family:Georgia,serif">{apartman.naziv}</h1>
    </div>
    """


def _podnozje(apartman):
    return f"""
    <div style="background:#1a1a2e;padding:1.5rem;text-align:center;color:rgba(255,255,255,0.5);font-size:0.8rem">
        {apartman.naziv} · {apartman.adresa}
    </div>
    """


def _detalji_tabela(rezervacija, jezik):
    return f"""
    <div style="background:white;border-left:3px solid #c9a84c;padding:1.5rem;margin:1.5rem 0">
        <table style="width:100%;font-size:0.9rem">
            <tr><td style="color:#999;padding:0.3rem 0">{t(jezik, 'apartman')}</td><td><strong>{rezervacija.apartman.naziv}</strong></td></tr>
            <tr><td style="color:#999;padding:0.3rem 0">{t(jezik, 'dolazak')}</td><td><strong>{rezervacija.datum_dolaska.strftime('%d.%m.%Y')}</strong></td></tr>
            <tr><td style="color:#999;padding:0.3rem 0">{t(jezik, 'odlazak')}</td><td><strong>{rezervacija.datum_odlaska.strftime('%d.%m.%Y')}</strong></td></tr>
            <tr><td style="color:#999;padding:0.3rem 0">{t(jezik, 'broj_noci')}</td><td><strong>{rezervacija.broj_noci}</strong></td></tr>
            <tr><td style="color:#999;padding:0.3rem 0">{t(jezik, 'broj_gostiju')}</td><td><strong>{rezervacija.broj_gostiju}</strong></td></tr>
            <tr style="border-top:1px solid #eee">
                <td style="color:#999;padding:0.5rem 0"><strong>{t(jezik, 'ukupno')}</strong></td>
                <td><strong style="color:#c9a84c;font-size:1.1rem">{rezervacija.ukupno}€</strong></td>
            </tr>
        </table>
    </div>
    """


# === EMAILOVI ===

def posalji_potvrdu_upita(rezervacija, jezik=None):
    """Email gostu nakon slanja upita."""
    jezik = jezik or _detektiraj_jezik(rezervacija)

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
        {_zaglavlje(rezervacija.apartman)}
        <div style="padding:2rem;background:#f9f9f9">
            <h2 style="color:#1a1a2e">{t(jezik, 'pozdrav')} {rezervacija.ime},</h2>
            <p>{t(jezik, 'upit_primljen')}</p>
            {_detalji_tabela(rezervacija, jezik)}
            <p style="color:#666;font-size:0.85rem">
                {t(jezik, 'upit_obrada')}<br>
                {t(jezik, 'upit_email_potvrda')}
            </p>
            <p style="color:#999;font-size:0.8rem">{t(jezik, 'referentni_broj')}: <strong>{rezervacija.uuid}</strong></p>
        </div>
        {_podnozje(rezervacija.apartman)}
    </div>
    """
    predmet = t(jezik, 'predmet_upit', naziv=rezervacija.apartman.naziv)
    return _posalji(predmet, html, [rezervacija.email])


def posalji_potvrdu_vlasnik(rezervacija):
    """Email vlasniku — uvijek na hrvatskom."""
    jezik = 'hr'
    napomena = f'<p style="background:#fef3c7;padding:1rem;border-left:3px solid #f59e0b;margin:1.5rem 0"><strong>Napomena gosta:</strong><br>{rezervacija.napomene_gosta}</p>' if rezervacija.napomene_gosta else ""

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:2rem">
        <h2 style="color:#1a1a2e">🔔 Novi upit za rezervaciju!</h2>
        <table style="width:100%;border-collapse:collapse;font-size:0.9rem">
            <tr style="background:#f5f5f5"><td style="padding:0.7rem;color:#999">Gost</td><td style="padding:0.7rem"><strong>{rezervacija.ime} {rezervacija.prezime}</strong></td></tr>
            <tr><td style="padding:0.7rem;color:#999">Email</td><td style="padding:0.7rem"><a href="mailto:{rezervacija.email}">{rezervacija.email}</a></td></tr>
            <tr style="background:#f5f5f5"><td style="padding:0.7rem;color:#999">Telefon</td><td style="padding:0.7rem">{rezervacija.telefon}</td></tr>
            <tr><td style="padding:0.7rem;color:#999">Država</td><td style="padding:0.7rem">{rezervacija.drzava or '-'} (jezik: {_detektiraj_jezik(rezervacija).upper()})</td></tr>
            <tr style="background:#f5f5f5"><td style="padding:0.7rem;color:#999">Dolazak</td><td style="padding:0.7rem">{rezervacija.datum_dolaska.strftime('%d.%m.%Y')}</td></tr>
            <tr><td style="padding:0.7rem;color:#999">Odlazak</td><td style="padding:0.7rem">{rezervacija.datum_odlaska.strftime('%d.%m.%Y')}</td></tr>
            <tr style="background:#f5f5f5"><td style="padding:0.7rem;color:#999">Noći / Gostiju</td><td style="padding:0.7rem">{rezervacija.broj_noci} / {rezervacija.broj_gostiju}</td></tr>
            <tr style="background:#c9a84c22"><td style="padding:0.7rem"><strong>Ukupno</strong></td><td style="padding:0.7rem"><strong style="color:#c9a84c">{rezervacija.ukupno}€</strong></td></tr>
        </table>
        {napomena}
        <div style="margin-top:1.5rem">
            <a href="http://127.0.0.1:8000/admin/rezervacije/rezervacija/{rezervacija.pk}/change/"
               style="background:#1a1a2e;color:white;padding:0.8rem 1.5rem;text-decoration:none;font-size:0.85rem">
                ⚙️ Upravljaj
            </a>
        </div>
    </div>
    """
    predmet = t(jezik, 'predmet_vlasnik', ime=rezervacija.ime, prezime=rezervacija.prezime)
    if settings.EMAIL_HOST_USER:
        return _posalji(predmet, html, [settings.EMAIL_HOST_USER])


def posalji_potvrdjenu_rezervaciju(rezervacija, jezik=None):
    """Kad vlasnik POTVRDI rezervaciju."""
    jezik = jezik or _detektiraj_jezik(rezervacija)
    wifi_red = f'<p>📶 <strong>{t(jezik, "wifi")}:</strong> {rezervacija.apartman.wifi_lozinka}</p>' if rezervacija.apartman.wifi_lozinka else ''

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
        {_zaglavlje(rezervacija.apartman)}
        <div style="padding:2rem;background:#f9f9f9">
            <div style="background:#d1fae5;border-left:3px solid #10b981;padding:1rem;margin-bottom:1.5rem">
                <strong style="color:#065f46;font-size:1.1rem">{t(jezik, 'rezervacija_potvrdjena')}</strong>
            </div>
            <h2 style="color:#1a1a2e">{t(jezik, 'pozdrav')} {rezervacija.ime},</h2>
            <p>{t(jezik, 'veselimo_se')}</p>
            {_detalji_tabela(rezervacija, jezik)}
            <div style="background:white;padding:1.5rem;margin:1.5rem 0">
                <h3 style="margin-top:0;color:#1a1a2e;font-size:1.1rem">{t(jezik, 'info_dolazak')}</h3>
                <p style="font-size:0.9rem;line-height:1.8">
                    <strong>{t(jezik, 'adresa')}:</strong> {rezervacija.apartman.adresa}<br>
                    <strong>{t(jezik, 'check_in')}:</strong> {t(jezik, 'od')} {rezervacija.apartman.check_in}<br>
                    <strong>{t(jezik, 'check_out')}:</strong> {t(jezik, 'do')} {rezervacija.apartman.check_out}
                </p>
                {wifi_red}
            </div>
            <p style="color:#666;font-size:0.9rem">{t(jezik, 'detaljne_upute')}</p>
            <p style="color:#999;font-size:0.8rem">{t(jezik, 'referentni_broj')}: <strong>{rezervacija.uuid}</strong></p>
        </div>
        {_podnozje(rezervacija.apartman)}
    </div>
    """
    predmet = t(jezik, 'predmet_potvrdjeno', naziv=rezervacija.apartman.naziv)
    return _posalji(predmet, html, [rezervacija.email])


def posalji_otkazanu_rezervaciju(rezervacija, jezik=None):
    """Kad vlasnik OTKAŽE rezervaciju."""
    jezik = jezik or _detektiraj_jezik(rezervacija)

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
        {_zaglavlje(rezervacija.apartman)}
        <div style="padding:2rem;background:#f9f9f9">
            <div style="background:#fee2e2;border-left:3px solid #ef4444;padding:1rem;margin-bottom:1.5rem">
                <strong style="color:#991b1b">{t(jezik, 'rezervacija_otkazana')}</strong>
            </div>
            <h2 style="color:#1a1a2e">{t(jezik, 'pozdrav')} {rezervacija.ime},</h2>
            <p>{t(jezik, 'nazalost')}</p>
            {_detalji_tabela(rezervacija, jezik)}
            <p>{t(jezik, 'drugi_termin')}</p>
        </div>
        {_podnozje(rezervacija.apartman)}
    </div>
    """
    predmet = t(jezik, 'predmet_otkazano', naziv=rezervacija.apartman.naziv)
    return _posalji(predmet, html, [rezervacija.email])


def posalji_placeno(rezervacija, jezik=None):
    """Kad je plaćanje primljeno."""
    jezik = jezik or _detektiraj_jezik(rezervacija)

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
        {_zaglavlje(rezervacija.apartman)}
        <div style="padding:2rem;background:#f9f9f9">
            <div style="background:#d1fae5;border-left:3px solid #10b981;padding:1rem;margin-bottom:1.5rem">
                <strong style="color:#065f46">{t(jezik, 'placanje_primljeno')}</strong>
            </div>
            <h2>{t(jezik, 'hvala_posjeta')}, {rezervacija.ime}!</h2>
            <p>{t(jezik, 'hvala_uplata')} <strong>{rezervacija.ukupno}€</strong>.</p>
            {_detalji_tabela(rezervacija, jezik)}
        </div>
        {_podnozje(rezervacija.apartman)}
    </div>
    """
    predmet = t(jezik, 'predmet_placeno', naziv=rezervacija.apartman.naziv)
    return _posalji(predmet, html, [rezervacija.email])


def posalji_podsjetnik(rezervacija, jezik=None):
    """3 dana prije dolaska."""
    jezik = jezik or _detektiraj_jezik(rezervacija)
    wifi_red = f'<p>📶 <strong>{t(jezik, "wifi")}:</strong> {rezervacija.apartman.wifi_lozinka}</p>' if rezervacija.apartman.wifi_lozinka else ''

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
        {_zaglavlje(rezervacija.apartman)}
        <div style="padding:2rem">
            <h2>{t(jezik, 'dobrodosli_uskoro')}, {rezervacija.ime}! 🎉</h2>
            <p>{t(jezik, 'dolazak_za_3_dana')} ({rezervacija.datum_dolaska.strftime('%d.%m.%Y')}).</p>
            <div style="background:#f9f9f9;border-left:3px solid #c9a84c;padding:1.5rem;margin:1.5rem 0">
                <h3 style="margin-top:0">{t(jezik, 'info_dolazak')}</h3>
                <p>📍 <strong>{t(jezik, 'adresa')}:</strong> {rezervacija.apartman.adresa}</p>
                <p>🕐 <strong>{t(jezik, 'check_in')}:</strong> {t(jezik, 'od')} {rezervacija.apartman.check_in}</p>
                <p>🕐 <strong>{t(jezik, 'check_out')}:</strong> {t(jezik, 'do')} {rezervacija.apartman.check_out}</p>
                {wifi_red}
            </div>
        </div>
        {_podnozje(rezervacija.apartman)}
    </div>
    """
    predmet = t(jezik, 'predmet_podsjetnik', naziv=rezervacija.apartman.naziv)
    return _posalji(predmet, html, [rezervacija.email])


def posalji_zahvalu(rezervacija, jezik=None):
    """Nakon odlaska — poziv na recenziju."""
    jezik = jezik or _detektiraj_jezik(rezervacija)

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
        {_zaglavlje(rezervacija.apartman)}
        <div style="padding:2rem;text-align:center">
            <h2>{t(jezik, 'hvala_posjeta')}, {rezervacija.ime}! 🙏</h2>
            <p style="color:#666;line-height:1.8">{t(jezik, 'uzivali_boravak')}</p>
            <div style="background:#f9f9f9;padding:2rem;margin:2rem 0">
                <p style="margin:0 0 1rem;color:#666">{t(jezik, 'misljenje_znaci')}</p>
                <a href="http://127.0.0.1:8000/moj-racun/recenzija/{rezervacija.uuid}/"
                   style="background:#c9a84c;color:#1a1a2e;padding:0.9rem 2rem;text-decoration:none;font-weight:600;display:inline-block">
                    {t(jezik, 'ostavi_recenziju')}
                </a>
            </div>
        </div>
        {_podnozje(rezervacija.apartman)}
    </div>
    """
    predmet = t(jezik, 'predmet_zahvala', naziv=rezervacija.apartman.naziv)
    return _posalji(predmet, html, [rezervacija.email])
