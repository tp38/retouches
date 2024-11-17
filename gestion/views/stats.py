from django.shortcuts import render, redirect
from couchdb import Server
from couchdb.http import ResourceNotFound

from django.conf import settings

from datetime import datetime, date
import calendar


def inOutByDay(request):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )

    db = s[settings.DB_GESTION]

    weekdays = [ 
        ['Dimanche', 0, 0],
        ['Lundi', 0, 0],
        ['Mardi', 0, 0],
        ['Mercredi', 0, 0],
        ['Jeudi', 0, 0],
        ['Vendredi', 0, 0],
        ['Samedi', 0, 0]
    ]
    for r in db.view( 'stats/retraitsDepotsByDay', group_level=1  ) :
        weekdays[r.key][1] = r.value[0]
        weekdays[r.key][2] = r.value[1]
            
    return render( request,'gestion/inOutByDay.html', {'report': weekdays } )



def getTowns(request):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )

    db = s[settings.DB_GESTION]


    rows = []
    for r in db.view( 'stats/towns', group_level=1  ) :
        rows.append( { "ville": r.key, "nb": r.value } )
            
    rows.sort( key= lambda x: x.get('nb'), reverse=True )
    
    return render( request,'gestion/liste_villes.html', {'rows': rows} )

