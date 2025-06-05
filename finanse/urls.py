from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # Auth URLs
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('rejestracja/', views.rejestracja, name='rejestracja'),

    # App URLs
    path('', login_required(views.dashboard), name='dashboard'),
    path('dodaj/', login_required(views.dodaj_transakcje), name='dodaj_transakcje'),
    path('lista/', login_required(views.lista_transakcji), name='lista_transakcji'),
    path('budzet/<int:pk>/', login_required(views.edytuj_budzet), name='edytuj_budzet'),
    path('eksport/', login_required(views.eksport_csv), name='eksport_csv'),
    path('import/', login_required(views.import_csv), name='import_csv'),
    path('edytuj/<int:pk>/', login_required(views.edytuj_transakcje), name='edytuj_transakcje'),
    path('usun/<int:pk>/', login_required(views.usun_transakcje), name='usun_transakcje'),
]