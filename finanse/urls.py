from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from finanse import views as finanse_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('rejestracja/', finanse_views.rejestracja, name='rejestracja'),
    path('dodaj/', finanse_views.dodaj_transakcje, name='dodaj_transakcje'),
    path('', finanse_views.dashboard, name='dashboard'),
    path('lista/', finanse_views.lista_transakcji, name='lista_transakcji'),
    path('budzet/<int:pk>/', finanse_views.edytuj_budzet, name='edytuj_budzet'),
    path('eksport/', finanse_views.eksport_csv, name='eksport_csv'),
    path('import/', finanse_views.import_csv, name='import_csv'),
    ]