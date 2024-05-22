from django.urls import path
from . import views

urlpatterns = [
    path( '', views.login ),
    path( 'logout/', views.logout ),
    path( 'month_list/', views.month_list ),
    path( 'recettes_jour/', views.recettes_jour ),
    path( 'recettes_semaine/', views.recettes_semaine ),
    path( 'recettes_mois/', views.recettes_mois ),
    path( 'synthese_paie/', views.synthese_paie ),
    path( 'paie/', views.paie ),
    path( 'process/', views.process ),
    path( 'doc/<str:uuid>/', views.detail ),
]
