from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Transakcja, Kategoria
from .forms import TransakcjaForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    przychody_suma = sum(item.kwota for item in przychody)

    wydatki = Transakcja.objects.filter(user=request.user, typ='wydatek')
    wydatki_suma = sum(item.kwota for item in wydatki)

    saldo = przychody_suma - wydatki_suma

    context = {
        'transakcje': transakcje,
        'przychody_suma': przychody_suma,
        'wydatki_suma': wydatki_suma,
        'saldo': saldo,
    }
    return render(request, 'finanse/dashboard.html', context)

def lista_transakcji(request):
    transakcje = Transakcja.objects.filter(user=request.user).order_by('-data')
    return render(request, 'finanse/lista.html', {'transakcje': transakcje})
