from django.db import models
from django.contrib.auth.models import User

class Kategoria(models.Model):
    nazwa = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nazwa

class Transakcja(models.Model):
    TYPY_TRANSAKCJI = [
        ('przychód', 'Przychód'),
        ('wydatek', 'Wydatek'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    typ = models.CharField(max_length=10, choices=TYPY_TRANSAKCJI)
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    kategoria = models.ForeignKey(Kategoria, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    opis = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.typ}: {self.kwota:.2f} ({self.kategoria})"  # Wymusza dwa miejsca po przecinku
