from django.urls import path
from .views import rejestracja
from .views import dodaj_transakcje

urlpatterns = [
    path("rejestracja/", rejestracja, name="rejestracja"),
    path("dodaj/", dodaj_transakcje, name="dodaj_transakcje"),
]
