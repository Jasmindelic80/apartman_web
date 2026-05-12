#!/bin/bash
# ================================================
# SETUP SKRIPTA — Pokretanje Django apartman web
# ================================================

echo "=== 1. Provjeri Python verziju (treba 3.10+) ==="
python --version

echo ""
echo "=== 2. Kreiraj virtualno okruženje ==="
python -m venv venv

echo ""
echo "=== 3. Aktiviraj venv ==="
echo "    Windows:  venv\\Scripts\\activate"
echo "    Mac/Linux: source venv/bin/activate"

echo ""
echo "=== 4. Instaliraj pakete ==="
pip install -r requirements.txt

echo ""
echo "=== 5. Kopiraj .env fajl ==="
cp .env.example .env
echo "    VAŽNO: Uredi .env fajl i unesi svoje podatke!"

echo ""
echo "=== 6. Kreiraj __init__.py fajlove ==="
touch apartman_web/__init__.py
touch apartman/__init__.py
touch rezervacije/__init__.py
touch izleti/__init__.py

echo ""
echo "=== 7. Kreiraj migrations ==="
python manage.py makemigrations apartman
python manage.py makemigrations rezervacije
python manage.py makemigrations izleti
python manage.py migrate

echo ""
echo "=== 8. Kreiraj admin korisnika ==="
python manage.py createsuperuser

echo ""
echo "=== 9. Pokreni server ==="
python manage.py runserver

echo ""
echo "✅ Otvori browser: http://127.0.0.1:8000"
echo "✅ Admin panel:    http://127.0.0.1:8000/admin"
