 
# Użyj obrazu Pythona 3.10
FROM python:3.10

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki projektu do kontenera
COPY . .

# Zainstaluj zależności
RUN pip install -r requirements.txt

# Uruchom aplikację Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
