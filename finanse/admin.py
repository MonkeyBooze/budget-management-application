from django.contrib import admin
from .models import Kategoria, Transakcja

@admin.register(Kategoria)
class KategoriaAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'budzet']
    list_editable = ['budzet']

@admin.register(Transakcja)
class TransakcjaAdmin(admin.ModelAdmin):
    list_display = ['user', 'typ', 'kwota', 'kategoria', 'data']
    list_filter = ['typ', 'kategoria', 'data']
    search_fields = ['opis']