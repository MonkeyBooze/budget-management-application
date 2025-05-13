from django import forms
from .models import Transakcja, Kategoria

class TransakcjaForm(forms.ModelForm):
    class Meta:
        model = Transakcja
        fields = ["typ", "kwota", "kategoria", "opis"]
class KategoriaForm(forms.ModelForm):
    class Meta:
        model = Kategoria
        fields = ["nazwa", "budzet"]

