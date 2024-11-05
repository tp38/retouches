from django.urls import path
from . import views

urlpatterns = [
    path( '', views.login ),
    path( 'logout/', views.logout ),

    path( 'synthese/', views.synthese, name='synthese' ),
    path( 'recettes/', views.recettes_liste, name='recettes-list' ),
    path( 'recette/<str:uuid>/', views.recette_detail, name='recette-detail' ),
    path( 'depenses/', views.depenses_liste, name='depenses-list' ),
    path( 'depense/<str:uuid>/', views.depense_detail, name='depense-detail' ),
    path( 'provisions/', views.provisions_liste, name='provision-list' ),
    path( 'provision/<str:uuid>/', views.provision_detail, name='provision-detail' ),
    path( 'provision/<str:uuid>/delete', views.provision_delete, name='provision_delete' ),
    path( 'stats/inoutbyday', views.inOutByDay, name='in_out_by_day' ),
]
