from django.shortcuts import render, redirect
from couchdb import Server
from couchdb.http import ResourceNotFound

from django.conf import settings

from datetime import datetime, date
import calendar

from .recettes import DateStringToArray, datetimeToArray

def synthese(request):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )

    db = s[settings.DB_GESTION]

    if request.method == "POST":
        dd = request.POST.get('date')
    else:
        dd = date.today().strftime("%Y-%m-%d")

    reqday = datetime.strptime(dd, "%Y-%m-%d")
    start = DateStringToArray( f"{reqday.year}-{reqday.month:02d}-01" )
    end = DateStringToArray( f"{reqday.year}-{reqday.month:02d}-{calendar.monthrange(reqday.year, reqday.month)[1]:02d}" )

    reqday = datetimeToArray( reqday )
    ca = 0
    try :
        for r in db.view( 'recettes/Resultat', startkey=end, endkey=start, descending=True, group=True, group_level=2  ) :
            if r.key[1] == reqday[1] :
                ca = round(r.value,2)
                break
    except:
        pass

    depenses = 0
    try :
        for r in db.view( 'depenses/Resultat', startkey=end, endkey=start, descending=True, group=True, group_level=2  ) :
            if r.key[1] == reqday[1] :
                depenses = round(r.value,2)
                break
    except:
        pass

    provisions = 0
    try :
        for r in db.view( 'provisions/Resultat', startkey=end, endkey=start, descending=True, group=True, group_level=2  ) :
            if r.key[1] == reqday[1] :
                provisions = round(r.value,2)
                break
    except :
        pass

    frais = 0
    try :
        for r in db.view( 'recettes/Frais', startkey=end, endkey=start, descending=True, group=True, group_level=2  ) :
            if r.key[1] == reqday[1] :
                frais = round(r.value,2)
                break
    except :
        pass

    compta = { 'bank': 0.0, 'real': 0.0, 'incomes': 0.0, 'provision': 0.0}
    for r in db.view( 'gestion/soldesBancaire', startkey=end, endkey=[2024,1,1,1], descending=True, group_level=1 ) :
        compta['bank'] = round(r.value[0],2)
        compta['real'] = round( r.value[0] + r.value[1], 2)
        compta['incomes'] = round( r.value[0] + r.value[1] + r.value[2] - r.value[3], 2)
        compta['provision'] = round(r.value[3],2)

    urssaf = round( ca * 0.215, 2)

    pending = 0
    for r in db.view( 'gestion/recettesEnAttente', group_level=1 ) :
        pending += r['value']

    return render( request,'gestion/synthese.html', { 
        'compta': compta, 
        'day': reqday, 
        'ca': ca, 
        'urssaf': urssaf, 
        'depenses': depenses, 
        'provisions': provisions, 
        'frais': frais, 
        'bilan': ca + depenses + frais - provisions,
        'pending': pending } )


def unchecked( request, uuid ) :
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )
    db = s[settings.DB_GESTION]

    if request.method == "GET":
        if uuid == 'none' :
            rows = []
            for r in db.view( 'gestion/unchecked'  ) :
                doc = db[r.key]
                rows.append( doc )
            return render( request,'gestion/unchecked.html', { 'rows': rows } )
        else :
            doc = db[uuid]
            if doc['class'] == 'recette' :
                return redirect( f"/gestion/recette/{uuid}" )
            elif doc['class'] == 'depense' :
                return redirect( f"/gestion/depense/{uuid}")
            elif doc['class'] == 'depot' :
                return redirect( f"/gestion/depot/{uuid}")
            else :
                rows = []
                for r in db.view( 'gestion/unchecked'  ) :
                    doc = db[r.key]
                    rows.append( doc )
                return render( request,'gestion/unchecked.html', { 'rows': rows } )


