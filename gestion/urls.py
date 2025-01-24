from django.urls import path
from . import views

urlpatterns = [
    path( '', views.login, name='login' ),
    path( 'logout/', views.logout, name='logout' ),

    path( 'synthese/', views.synthese, name='synthese' ),
    path( 'unchecked/<str:uuid>/', views.unchecked, name='unchecked' ),
    path( 'recettes/', views.recettes_liste, name='recettes-list' ),
    path( 'recette/<str:uuid>/', views.recette_detail, name='recette-detail' ),
    path( 'depenses/', views.depenses_liste, name='depenses-list' ),
    path( 'depense/<str:uuid>/', views.depense_detail, name='depense-detail' ),
    path( 'provisions/', views.provisions_liste, name='provisions-list' ),
    path( 'provision/<str:uuid>/', views.provision_detail, name='provision-detail' ),
    path( 'provision/<str:uuid>/delete', views.provision_delete, name='provision-delete' ),
    path( 'depots/', views.depots_liste, name='depots-list' ),
    path( 'depot/<str:uuid>/', views.depot_detail, name='depot-detail' ),
    path( 'stats/inoutbyday', views.inOutByDay, name='in_out_by_day' ),
    path( 'stats/towns', views.getTowns, name='town-list' ),
    path( 'stats/recdep/<int:group>/', views.recettes_depenses, name='recettes_depenses' ),
    path( 'stats/especes/<int:group>/', views.especes, name='especes' ),
    path( 'stats/oublis/<int:group>/', views.oublis, name='especes_forgot' ),
    path( 'stats/activitybydate/<str:dd>/', views.activity_by_date, name='activity-by-date' ),
    path( 'stats/nameactivity/<str:name>/', views.name_activity, name='name-activity' ),
    path( 'stats/phoneactivity/<str:phone>/', views.phone_activity, name='phone-activity' ),
]
