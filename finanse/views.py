from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Transakcja, Kategoria
from .forms import TransakcjaForm, KategoriaForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv
from django.http import HttpResponse

def dodaj_transakcje(request):
    if request.method == "POST":
        form = TransakcjaForm(request.POST)
        if form.is_valid():
            transakcja = form.save(commit=False)
            transakcja.user = request.user
            transakcja.save()
            return redirect("lista_transakcji")
    else:
        form = TransakcjaForm()
    return render(request, "finanse/dodaj.html", {"form": form})

def rejestracja(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Konto dla {username} zostało utworzone! Możesz się teraz zalogować.')
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "finanse/registration/rejestracja.html", {"form": form})

@login_required()
def dashboard(request):
    transakcje = Transakcja.objects.filter(user=request.user).order_by('-data')[:5]

    przychody = Transakcja.objects.filter(user=request.user, typ='przychód')
    suma_przychodow = sum(item.kwota for item in przychody)

    wydatki = Transakcja.objects.filter(user=request.user, typ='wydatek')
    suma_wydatkow = sum(item.kwota for item in wydatki)

    saldo = suma_przychodow - suma_wydatkow

    # Dane do wykresu
    kategorie = Kategoria.objects.all()
    nazwy_kategorii = [k.nazwa for k in kategorie]
    wartosci_kategorii = [sum(t.kwota for t in Transakcja.objects.filter(user=request.user, typ='wydatek', kategoria=k)) for k in kategorie]

    przekroczenia = []
    for kategoria in kategorie:
        suma_wydatkow = sum(t.kwota for t in Transakcja.objects.filter(user=request.user, typ='wydatek', kategoria=kategoria))
        if suma_wydatkow > kategoria.budzet:
            przekroczenia.append(f"Przekroczyłeś budżet dla kategorii {kategoria.nazwa}!")

    context = {
        'transakcje': transakcje,
        'suma_przychodow': suma_przychodow,
        'suma_wydatkow': suma_wydatkow,
        'saldo': saldo,
        'nazwy_kategorii': nazwy_kategorii,
        'wartosci_kategorii': wartosci_kategorii,
        'przekroczenia': przekroczenia,
    }
    return render(request, 'finanse/dashboard.html', context)

def lista_transakcji(request):
    transakcje = Transakcja.objects.filter(user=request.user).order_by('-data')
    return render(request, 'finanse/lista.html', {'transakcje': transakcje})

@login_required
def edytuj_budzet(request, pk):
    kategoria = Kategoria.objects.get(pk=pk)
    if request.method == "POST":
        form = KategoriaForm(request.POST, instance=kategoria)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = KategoriaForm(instance=kategoria)
    return render(request, "finanse/edytuj_budzet.html", {"form": form})

@login_required
def eksport_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transakcje.csv"'

    writer = csv.writer(response)
    writer.writerow(["Data", "Opis", "Kategoria", "Typ", "Kwota"])

    transakcje = Transakcja.objects.filter(user=request.user)
    for t in transakcje:
        writer.writerow([t.data, t.opis, t.kategoria, t.typ, t.kwota])

    return response

@login_required
def import_csv(request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.reader(decoded_file)

        for row in reader:
            if len(row) == 5:
                Transakcja.objects.create(
                    user=request.user,
                    data=row[0],
                    opis=row[1],
                    kategoria=Kategoria.objects.get_or_create(nazwa=row[2])[0],
                    typ=row[3],
                    kwota=row[4]
                )
        return redirect("lista_transakcji")

    return render(request, "finanse/import_csv.html")


