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
    for r in db.view( 'gestion/recettesResultat', startkey=end, endkey=start, descending=True, group=True, group_level=2  ) :
        if r.key[1] == reqday[1] :
            ca = round(r.value,2)
            break

    depenses = 0
    for r in db.view( 'gestion/depensesResultat', startkey=end, endkey=start, descending=True, group=True, group_level=2  ) :
        if r.key[1] == reqday[1] :
            depenses = round(r.value,2)
            break

    provisions = 0
    for r in db.view( 'gestion/provisionsResultat', startkey=end, endkey=start, descending=True, group=True, group_level=2  ) :
        if r.key[1] == reqday[1] :
            provisions = round(r.value,2)
            break

    frais = 0
    for r in db.view( 'gestion/recettesFrais', startkey=end, endkey=start, descending=True, group=True, group_level=2  ) :
        if r.key[1] == reqday[1] :
            frais = round(r.value,2)
            break

    compta = { 'bank': 0.0, 'real': 0.0, 'incomes': 0.0, 'provision': 0.0}
    for r in db.view( 'gestion/compta', startkey=end, endkey=[2024,1,1,1], descending=True, group_level=1 ) :
        compta['bank'] = round(r.value[0],2)
        compta['real'] = round( compta['bank'] - r.value[1], 2)
        compta['incomes'] = round( compta['real'] - r.value[2] - r.value[3], 2)
        compta['provision'] = round(r.value[3],2)

    return render( request,'gestion/synthese.html', { 'compta': compta, 'day': reqday, 'ca': ca, 'depenses': depenses, 'provisions': provisions, 'frais': frais, 'reste': ca + depenses + frais - provisions } )



