from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Transakcja
from .forms import TransakcjaForm

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
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "finanse/registration/rejestracja.html", {"form": form})

