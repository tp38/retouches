from django.shortcuts import render, redirect
from couchdb import Server

from django.conf import settings



def recettes_jour(request):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )
    db = s[settings.DB_NAME]
    if not request.method == "GET" :
        return redirect( '/compta/' )
    else:
        rows = []
        for r in db.view( 'compta/recettes-depenses', group=True, group_level=4, descending=True ):
            rows.append( r )
        # rows = sorted(rows, key=lambda row: row['key'], reverse=True)
        return render( request,'compta/recettes_jour.html', {'rows': rows } )


def recettes_semaine(request):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )
    db = s[settings.DB_NAME]
    if not request.method == "GET" :
        return redirect( '/compta/' )
    else:
        rows = []
        for r in db.view( 'compta/recettes-depenses', group=True, group_level=3, descending=True  ):
            rows.append( r )
        # rows = sorted(rows, key=lambda row: row['key'], reverse=True)
        return render( request,'compta/recettes_semaine.html', {'rows': rows } )

def recettes_mois(request):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )
    db = s[settings.DB_NAME]
    if not request.method == "GET" :
        return redirect( '/compta/' )
    else:
        rows = []
        for r in db.view( 'compta/recettes-depenses', group=True, group_level=2, descending=True  ):
            rows.append( r )
        # rows = sorted(rows, key=lambda row: row['key'], reverse=True)
        return render( request,'compta/recettes_mois.html', {'rows': rows } )
