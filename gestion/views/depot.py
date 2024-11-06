from django.shortcuts import render, redirect
from couchdb import Server
from couchdb.http import ResourceNotFound

from django.conf import settings

from datetime import datetime, date
import calendar
from uuid import uuid4

from .recettes import DateStringToArray, datetimeToArray

def depot_detail(request, uuid):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )
    db = s[settings.DB_GESTION]

    if request.method == "POST":
        try:
            doc = db[uuid]
        except ResourceNotFound:
            doc = { '_id': uuid, 'class': 'depot' }

        # save date if exists
        if request.POST.__contains__('date') and request.POST.get('date') != "" :
            doc['date'] = DateStringToArray( request.POST.get('date') )

        # save description if exists 
        if request.POST.__contains__( 'description' ) :
            doc['description'] = request.POST.get('description')

        # save price if exists
        if request.POST.__contains__( 'montant' ) :
            doc['montant'] = float(request.POST.get( 'montant' ))

        # save bank_state if exists
        if request.POST.__contains__('bank') :
            doc['bank'] = request.POST.get('bank')

        db.save( doc )        
        return redirect( '/gestion/depots/' )
    else :
        if uuid == "new" :
            uuid = uuid4()
            doc = {"class": 'depot', "date" : DateStringToArray( date.today().strftime("%Y-%m-%d") ), "montant": "0" }
        else:
            doc = db[uuid]
        return render( request,'gestion/detail_depot.html',{'row': doc, 'id': uuid } )


def depots_liste(request):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )

    db = s[settings.DB_GESTION]
    rows = []

    if request.method == "POST":
        dd = request.POST.get('dd')
    else:
        dd = date.today().strftime("%Y-%m-%d")

    reqday = datetime.strptime(dd, "%Y-%m-%d")
    start = DateStringToArray( f"{reqday.year}-{reqday.month:02d}-01" )
    end = DateStringToArray( f"{reqday.year}-{reqday.month:02d}-{calendar.monthrange(reqday.year, reqday.month)[1]:02d}" )

    for r in db.view( "gestion/depotsFiches", startkey=end, endkey=start, descending=True ):
        doc = db[r.id]
        rows.append( doc )

    reqday = datetimeToArray( reqday )
    month = 0
    for r in db.view( 'gestion/depotsResultat', startkey=end, endkey=start, descending=True, group=True, group_level=2  ) :
        if r.key[1] == reqday[1] :
            month = r.value
            break

    start = DateStringToArray( f"{reqday[0]}-01-01" )
    end = DateStringToArray( f"{reqday[0]}-12-31" )
    year = 0
    for r in db.view( 'gestion/depotsResultat', startkey=end, endkey=start, descending=True, group=True, group_level=1  ) :
        if r.key[0] == reqday[0] :
            year = r.value
            break

    report = { 'month': month, 'year': year }

    return render( request,'gestion/liste_depots.html', {'rows': rows, 'day': dd, 'report': report } )

