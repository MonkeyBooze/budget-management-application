from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import Transakcja, Kategoria
from .forms import TransakcjaForm, KategoriaForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv
from django.http import HttpResponse
from django.contrib.auth import logout


def dodaj_transakcje(request):
    if request.method == "POST":
        form = TransakcjaForm(request.POST)
        if form.is_valid():
            transakcja = form.save(commit=False)
            transakcja.user = request.user

            # Obsługa kategorii - znajdź lub utwórz
            kategoria_nazwa = request.POST.get('kategoria_nazwa', '').strip()
            if kategoria_nazwa:
                kategoria, created = Kategoria.objects.get_or_create(
                    nazwa=kategoria_nazwa,
                    defaults={'budzet': 0.00}
                )
                transakcja.kategoria = kategoria

                if created:
                    messages.success(request, f'Utworzono nową kategorię: {kategoria_nazwa}')

            transakcja.save()
            messages.success(request, 'Transakcja została dodana!')
            return redirect("lista_transakcji")
    else:
        form = TransakcjaForm()

    # Przekaż istniejące kategorie do template
    existing_categories = list(Kategoria.objects.values_list('nazwa', flat=True))
    return render(request, "finanse/dodaj.html", {
        "form": form,
        "existing_categories": existing_categories
    })


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
    wartosci_kategorii = [sum(t.kwota for t in Transakcja.objects.filter(user=request.user, typ='wydatek', kategoria=k))
                          for k in kategorie]

    przekroczenia = []
    for kategoria in kategorie:
        suma_wydatkow_kat = sum(
            t.kwota for t in Transakcja.objects.filter(user=request.user, typ='wydatek', kategoria=kategoria))
        if suma_wydatkow_kat > kategoria.budzet:
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

    # Dodaj podsumowania dla template
    przychody = Transakcja.objects.filter(user=request.user, typ='przychód')
    suma_przychodow = sum(item.kwota for item in przychody)

    wydatki = Transakcja.objects.filter(user=request.user, typ='wydatek')
    suma_wydatkow = sum(item.kwota for item in wydatki)

    saldo = suma_przychodow - suma_wydatkow

    return render(request, 'finanse/lista.html', {
        'transakcje': transakcje,
        'suma_przychodow': suma_przychodow,
        'suma_wydatkow': suma_wydatkow,
        'saldo': saldo,
    })


@login_required
def edytuj_transakcje(request, pk):
    transakcja = get_object_or_404(Transakcja, pk=pk, user=request.user)

    if request.method == "POST":
        form = TransakcjaForm(request.POST, instance=transakcja)
        if form.is_valid():
            transakcja = form.save(commit=False)

            # Obsługa kategorii
            kategoria_nazwa = request.POST.get('kategoria_nazwa', '').strip()
            if kategoria_nazwa:
                kategoria, created = Kategoria.objects.get_or_create(
                    nazwa=kategoria_nazwa,
                    defaults={'budzet': 0.00}
                )
                transakcja.kategoria = kategoria

                if created:
                    messages.success(request, f'Utworzono nową kategorię: {kategoria_nazwa}')

            transakcja.save()
            messages.success(request, 'Transakcja została zaktualizowana!')
            return redirect("lista_transakcji")
    else:
        form = TransakcjaForm(instance=transakcja)

    # Przekaż istniejące kategorie i aktualną kategorię
    existing_categories = list(Kategoria.objects.values_list('nazwa', flat=True))
    current_category = transakcja.kategoria.nazwa if transakcja.kategoria else ''

    return render(request, "finanse/edytuj_transakcje.html", {
        "form": form,
        "transakcja": transakcja,
        "existing_categories": existing_categories,
        "current_category": current_category
    })


@login_required
def usun_transakcje(request, pk):
    transakcja = get_object_or_404(Transakcja, pk=pk, user=request.user)

    if request.method == "POST":
        transakcja.delete()
        messages.success(request, 'Transakcja została usunięta!')
        return redirect("lista_transakcji")

    return render(request, "finanse/usun_transakcje.html", {"transakcja": transakcja})


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


def logout_view(request):
    logout(request)
    messages.success(request, 'Zostałeś pomyślnie wylogowany.')
    return redirect('login')