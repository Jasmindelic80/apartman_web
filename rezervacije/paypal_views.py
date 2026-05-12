"""
rezervacije/paypal.py - PayPal integracija
Koristi PayPal SDK za web checkout (Smart Buttons)
"""
import os
import json
import base64
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Rezervacija


# PayPal API URL-ovi
PAYPAL_API = {
    'sandbox': 'https://api-m.sandbox.paypal.com',
    'live': 'https://api-m.paypal.com',
}


def _paypal_url():
    """Vrati URL ovisno o modu (sandbox za testiranje, live za produkciju)."""
    mode = os.getenv('PAYPAL_MODE', 'sandbox')
    return PAYPAL_API.get(mode, PAYPAL_API['sandbox'])


def _dohvati_access_token():
    """Autentifikacija s PayPal-om."""
    client_id = os.getenv('PAYPAL_CLIENT_ID', '')
    secret = os.getenv('PAYPAL_SECRET', '')

    if not client_id or not secret:
        return None

    auth = base64.b64encode(f"{client_id}:{secret}".encode()).decode()

    response = requests.post(
        f"{_paypal_url()}/v1/oauth2/token",
        headers={
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data='grant_type=client_credentials',
    )

    if response.status_code == 200:
        return response.json().get('access_token')
    return None


@csrf_exempt
@require_http_methods(["POST"])
def kreiraj_paypal_order(request, uuid):
    """Kreiraj PayPal order za rezervaciju."""
    rezervacija = get_object_or_404(Rezervacija, uuid=uuid)

    token = _dohvati_access_token()
    if not token:
        return JsonResponse({'error': 'PayPal nije konfiguriran'}, status=500)

    # Akontacija ili puni iznos
    iznos = float(rezervacija.ukupno)

    response = requests.post(
        f"{_paypal_url()}/v2/checkout/orders",
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        },
        json={
            "intent": "CAPTURE",
            "purchase_units": [{
                "reference_id": str(rezervacija.uuid),
                "description": f"Rezervacija {rezervacija.apartman.naziv} ({rezervacija.broj_noci} noći)",
                "amount": {
                    "currency_code": "EUR",
                    "value": f"{iznos:.2f}",
                },
            }],
            "application_context": {
                "brand_name": rezervacija.apartman.naziv,
                "landing_page": "NO_PREFERENCE",
                "user_action": "PAY_NOW",
                "return_url": request.build_absolute_uri(f'/rezervacije/paypal/uspjeh/{uuid}/'),
                "cancel_url": request.build_absolute_uri(f'/rezervacije/paypal/odustani/{uuid}/'),
            }
        }
    )

    if response.status_code == 201:
        order = response.json()
        return JsonResponse({'orderID': order['id']})

    return JsonResponse({'error': 'PayPal greška', 'detalji': response.text}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def potvrdi_paypal_order(request, uuid):
    """Capture (naplati) PayPal narudžbu nakon što gost odobri."""
    rezervacija = get_object_or_404(Rezervacija, uuid=uuid)
    data = json.loads(request.body)
    order_id = data.get('orderID')

    token = _dohvati_access_token()
    if not token:
        return JsonResponse({'error': 'PayPal greška'}, status=500)

    response = requests.post(
        f"{_paypal_url()}/v2/checkout/orders/{order_id}/capture",
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        },
    )

    if response.status_code == 201:
        result = response.json()
        if result.get('status') == 'COMPLETED':
            # Ažuriraj status rezervacije
            rezervacija.status = 'placeno'
            rezervacija.save()  # Ovo automatski šalje email!

            return JsonResponse({
                'status': 'success',
                'message': 'Plaćanje je uspješno!',
                'transaction_id': result['purchase_units'][0]['payments']['captures'][0]['id'],
            })

    return JsonResponse({'error': 'Plaćanje nije uspjelo'}, status=500)
