from django.test import TestCase
from .models import Transakcja, Kategoria
from django.contrib.auth.models import User

class TransakcjaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.kategoria = Kategoria.objects.create(nazwa="Pensja")  # Tworzymy kategorię

        self.transakcja = Transakcja.objects.create(
            user=self.user,
            typ="przychód",
            kwota=100.00,
            kategoria=self.kategoria,  # Przypisujemy instancję Kategoria, a nie tekst
            opis="Wynagrodzenie za pracę"
        )

    def test_transakcja_str(self):
        """Testuje metodę __str__ w modelu Transakcja"""
        self.assertEqual(str(self.transakcja), "przychód: 100.00 (Pensja)")

    def test_transakcja_kwota(self):
        """Sprawdza, czy kwota transakcji jest poprawna"""
        self.assertEqual(self.transakcja.kwota, 100.00)