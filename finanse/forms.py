from django import forms
from .models import Transakcja

class TransakcjaForm(forms.ModelForm):
    class Meta:
        model = Transakcja
        fields = ["typ", "kwota", "kategoria", "opis"]

