"""
marketing/views.py - Marketing automatika
"""
import os
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
from .models import Pretplatnik, Newsletter, SocialPost, StatistikaPosjete
from apartman.models import Apartman, Recenzija
from izleti.models import Lokacija
from rezervacije.models import Rezervacija
from datetime import date, timedelta

try:
    import google.generativeai as genai
    GEMINI = True
except ImportError:
    GEMINI = False


# ============= AI GENERATOR ZA POSTOVE =============

@staff_member_required
@csrf_exempt
def ai_generator_post(request):
    """AI generira post za društvene mreže."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    try:
        data = json.loads(request.body)
        tip = data.get('tip', 'opci')  # opci, ponuda, izlet, restoran
        platforma = data.get('platforma', 'instagram')
        tema = data.get('tema', '')
        jezik = data.get('jezik', 'bs')

        api_key = os.getenv('GEMINI_API_KEY', '')
        if not api_key or not GEMINI:
            return JsonResponse({'error': 'Gemini nije konfiguriran'}, status=500)

        apartmani = Apartman.objects.filter(aktivan=True)
        lokacije = Lokacija.objects.filter(aktivno=True)[:8]

        kontekst = "Naši apartmani:\n"
        for ap in apartmani:
            kontekst += f"- {ap.naziv}: {ap.podnaslov or ''}, {ap.cijena_po_noci}€/noć, {ap.grad}\n"

        kontekst += "\nU okolini:\n"
        for lok in lokacije:
            kontekst += f"- {lok.naziv} ({lok.udaljenost_km}km)\n"

        # Različiti promptovi za različite tipove
        promptovi = {
            'opci': f"Napiši privlačan post za {platforma} na {jezik} jeziku o našim apartmanima. Dodaj 5-10 hashtagova.",
            'ponuda': f"Napiši post za {platforma} o trenutnoj posebnoj ponudi/popustu na {jezik} jeziku. Energično i pozivajuće. Dodaj hashtagove.",
            'izlet': f"Napiši post o izletu/atrakciji u okolini ({tema}) na {jezik} jeziku. Inspiruje na rezervaciju. Dodaj hashtagove.",
            'restoran': f"Napiši post o lokalnom restoranu/kuhinji ({tema}) na {jezik} jeziku. Mami na boravak. Dodaj hashtagove.",
            'sezona': f"Napiši sezonski post (proljeće/ljeto/jesen/zima) na {jezik} jeziku - {tema}. Dodaj hashtagove.",
        }

        prompt = f"""
{promptovi.get(tip, promptovi['opci'])}

KONTEKST O NAMA:
{kontekst}

PRAVILA:
- Tekst na {jezik} jeziku
- Za Instagram: emocionalno, slikovito, do 150 riječi
- Za Facebook: informativno, do 200 riječi
- Za TikTok: kratko, energično, do 100 riječi
- DODAJ 8-12 relevantnih hashtagova na kraju
- Koristi emoji da privučeš pažnju
- ZAVRŠI s pozivom na akciju (link na stranicu, rezervaciju)
- Tema (ako je data): {tema}

Format odgovora:
TEKST:
[ovdje glavni tekst posta]

HASHTAGOVI:
[ovdje hashtagovi razdvojeni razmacima]
"""

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content(prompt)

        odgovor = response.text

        # Razdvoji tekst i hashtagove
        if 'HASHTAGOVI:' in odgovor:
            tekst_dio, hashtagovi_dio = odgovor.split('HASHTAGOVI:', 1)
            tekst_dio = tekst_dio.replace('TEKST:', '').strip()
            hashtagovi_dio = hashtagovi_dio.strip()
        else:
            tekst_dio = odgovor
            hashtagovi_dio = ''

        return JsonResponse({
            'tekst': tekst_dio,
            'hashtagovi': hashtagovi_dio,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============= NEWSLETTER =============

def pretplati_se(request):
    """Forma za pretplatu na newsletter."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        ime = request.POST.get('ime', '').strip()

        if email:
            pretplatnik, created = Pretplatnik.objects.get_or_create(
                email=email,
                defaults={'ime': ime}
            )
            if created:
                messages.success(request, '✅ Hvala! Pretplaćeni ste na newsletter.')
            else:
                messages.info(request, 'Već ste pretplaćeni na newsletter.')

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'ok', 'created': created})

            return redirect(request.META.get('HTTP_REFERER', '/'))

    return JsonResponse({'error': 'POST required'}, status=405)


@staff_member_required
def posalji_newsletter(request, newsletter_id):
    """Pošalji newsletter svim pretplatnicima."""
    newsletter = Newsletter.objects.get(pk=newsletter_id)

    if newsletter.poslano:
        messages.warning(request, 'Newsletter je već poslan!')
        return redirect('admin:marketing_newsletter_changelist')

    pretplatnici = Pretplatnik.objects.filter(aktivan=True)
    poslano = 0

    for p in pretplatnici:
        try:
            html = f"""
            <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
                <div style="background:#1a1a2e;padding:2rem;text-align:center">
                    <h1 style="color:#c9a84c;font-size:1.5rem;margin:0">Apartmani Dalija</h1>
                </div>
                <div style="padding:2rem;background:#f9f9f9">
                    <h2>{newsletter.naslov}</h2>
                    <div>{newsletter.sadrzaj}</div>
                </div>
                <div style="background:#1a1a2e;padding:1.5rem;text-align:center;color:rgba(255,255,255,0.5);font-size:0.8rem">
                    Primaš ovaj email jer si pretplaćen na naš newsletter.<br>
                    <a href="#" style="color:#c9a84c">Otpiši se</a>
                </div>
            </div>
            """

            msg = EmailMultiAlternatives(
                subject=newsletter.naslov,
                body=strip_tags(html),
                from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                to=[p.email],
            )
            msg.attach_alternative(html, "text/html")
            msg.send(fail_silently=True)
            poslano += 1
        except Exception as e:
            print(f"Greška: {e}")

    newsletter.poslano = True
    newsletter.datum_slanja = date.today()
    newsletter.primatelji = poslano
    newsletter.save()

    messages.success(request, f'✅ Newsletter poslan na {poslano} adresa!')
    return redirect('admin:marketing_newsletter_changelist')


# ============= AUTO TRAŽENJE RECENZIJA =============

@staff_member_required
def posalji_zahtjeve_za_recenzije(request):
    """Šalje email gostima koji su otišli u zadnjih 7 dana."""
    od = date.today() - timedelta(days=7)
    do = date.today() - timedelta(days=1)

    rezervacije = Rezervacija.objects.filter(
        datum_odlaska__gte=od,
        datum_odlaska__lte=do,
        status__in=['placeno', 'zavrseno'],
    )

    poslano = 0
    for r in rezervacije:
        # Provjeri da nije već ostavio recenziju
        ima_rec = Recenzija.objects.filter(
            apartman=r.apartman,
            ime_gosta__icontains=r.ime,
        ).exists()

        if not ima_rec:
            posalji_zahtjev_recenzija(r)
            poslano += 1

    messages.success(request, f'📧 Poslano {poslano} zahtjeva za recenzije.')
    return redirect('admin:index')


def posalji_zahtjev_recenzija(rezervacija):
    """Email s linkovima na sve platforme za recenzije."""
    apartman = rezervacija.apartman

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
        <div style="background:#1a1a2e;padding:2rem;text-align:center">
            <h1 style="color:#c9a84c;font-size:1.5rem;margin:0">{apartman.naziv}</h1>
        </div>
        <div style="padding:2rem;background:#f9f9f9">
            <h2>Hvala, {rezervacija.ime}! 🙏</h2>
            <p>Nadamo se da si uživao u boravku u Bihaću!</p>
            <p>Tvoje mišljenje nam puno znači — molim te ostavi recenziju
            na jednoj od platformi:</p>

            <div style="margin:2rem 0">
                <!-- GOOGLE -->
                <a href="https://search.google.com/local/writereview?placeid=TVOJ_PLACE_ID"
                   style="display:block;background:#4285F4;color:white;padding:1rem;text-align:center;text-decoration:none;margin-bottom:0.5rem;font-weight:600">
                   ⭐ Recenzija na Googleu
                </a>

                <!-- BOOKING -->
                <a href="https://www.booking.com/hotel/ba/TVOJ-APARTMAN.html"
                   style="display:block;background:#003580;color:white;padding:1rem;text-align:center;text-decoration:none;margin-bottom:0.5rem;font-weight:600">
                   🔵 Recenzija na Booking.com
                </a>

                <!-- AIRBNB -->
                <a href="https://www.airbnb.com/rooms/TVOJ_ID/reviews"
                   style="display:block;background:#ff5a5f;color:white;padding:1rem;text-align:center;text-decoration:none;margin-bottom:0.5rem;font-weight:600">
                   🏠 Recenzija na Airbnb
                </a>

                <!-- NAŠA STRANICA -->
                <a href="http://127.0.0.1:8000/moj-racun/recenzija/{rezervacija.uuid}/"
                   style="display:block;background:#c9a84c;color:#1a1a2e;padding:1rem;text-align:center;text-decoration:none;font-weight:600">
                   📝 Recenzija na našoj stranici
                </a>
            </div>

            <p style="color:#666;font-size:0.9rem">
                Hvala unaprijed na izdvojenom vremenu! Tvoje iskustvo pomaže drugim gostima da pronađu nas.
            </p>
        </div>
        <div style="background:#1a1a2e;padding:1rem;text-align:center;color:rgba(255,255,255,0.5);font-size:0.8rem">
            {apartman.naziv}
        </div>
    </div>
    """

    try:
        msg = EmailMultiAlternatives(
            subject=f'Hvala na posjetu! Ostavi recenziju 🌟',
            body=strip_tags(html),
            from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
            to=[rezervacija.email],
        )
        msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=True)
        return True
    except Exception as e:
        print(f"Greška: {e}")
        return False
