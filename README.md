# budget-management-application
Technologie użyte:
- Python 3.x
- Django – framework webowy
- SQLite3 – domyślna baza danych Django
- Docker – opcjonalna konteneryzacja aplikacji
- HTML/CSS – szablony front-endowe (jeśli występują)

Wymagania systemowe
- Python 3.9+
- pip / venv
- Docker (opcjonalnie)

⚙️ Konfiguracja środowiska (lokalnie)
W bashu wpisujemy:
# 1. Stwórzenie i aktywowanie środowiska wirtualnego
python -m venv venv
venv\Scripts\activate na Windows

# 2. Zainstalowanie zależności
pip install -r requirements.txt

# 3. Uruchomienie migracji
python manage.py migrate

# 4. Uruchomienie serwera
python manage.py runserver
Alternatywnie: uruchomienie z Dockerem

# Budowanie obrazu
docker build -t budget-app .

# Uruchamianie kontenera
docker run -p 8000:8000 budget-app

models.py
Zawiera definicje modeli danych np. Budget, Transaction, Category. To one określają strukturę bazy danych.

views.py
Logika odpowiedzialna za przetwarzanie żądań użytkownika, np. wyświetlanie budżetów, dodawanie transakcji.

templates/
Szablony HTML, które są renderowane przez widoki. Znajdziesz tu interfejs użytkownika.

urls.py
Definicje tras URL – mapują ścieżki na konkretne widoki.

admin.py
Konfiguracja panelu administracyjnego Django dla zarządzania danymi.

manage.py
Narzędzie CLI do zarządzania projektem – uruchamianie serwera, migracji, tworzenie użytkowników itd.
