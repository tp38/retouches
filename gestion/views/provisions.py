from django.shortcuts import render, redirect
from couchdb import Server
from couchdb.http import ResourceNotFound

from django.conf import settings

from datetime import datetime, date
import calendar
from uuid import uuid4

from .recettes import DateStringToArray, datetimeToArray

def provision_detail(request, uuid):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )
    db = s[settings.DB_GESTION]

    if request.method == "POST":
        try:
            doc = db[uuid]
        except ResourceNotFound:
            doc = { '_id': uuid, 'class': 'provision' }

        # save date if exists
        if request.POST.__contains__('date') and request.POST.get('date') != "" :
            doc['date'] = DateStringToArray( request.POST.get('date') )

        # save bénéficiare if exists
        if request.POST.__contains__( 'type' ) :
            doc['type'] = request.POST.get('type')

        # save description if exists 
        if request.POST.__contains__( 'description' ) :
            doc['description'] = request.POST.get('description')

        # save price if exists
        if request.POST.__contains__( 'montant' ) :
            doc['montant'] = float(request.POST.get( 'montant' ))

        db.save( doc )        
        return redirect( '/gestion/provisions/' )
    else :
        if uuid == "new" :
            uuid = uuid4()
            doc = {"class": 'provision', "date" : DateStringToArray( date.today().strftime("%Y-%m-%d") ), "montant": "0" }
        else:
            doc = db[uuid]
        return render( request,'gestion/detail_provision.html',{'row': doc, 'id': uuid } )


def provisions_liste(request):
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

    for r in db.view( "gestion/provisionsFiches", startkey=end, endkey=start, descending=True ):
        doc = db[r.id]
        rows.append( doc )

    reqday = datetimeToArray( reqday )
    month = 0
    for r in db.view( 'gestion/provisionsResultat', startkey=end, endkey=start, descending=True, group=True, group_level=2  ) :
        if r.key[1] == reqday[1] :
            month = round( r.value, 2 )
            break

    start = DateStringToArray( f"{reqday[0]}-01-01" )
    end = DateStringToArray( f"{reqday[0]}-12-31" )
    year = 0
    for r in db.view( 'gestion/provisionsResultat', startkey=end, endkey=start, descending=True, group=True, group_level=1  ) :
        if r.key[0] == reqday[0] :
            year = round( r.value, 2 )
            break
            
    report = { 'month': month, 'year': year }

    return render( request,'gestion/liste_provisions.html', {'rows': rows, 'day': dd, 'report': report } )


def provision_delete(request,uuid) :
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )
    db = s[settings.DB_GESTION]

    if request.method == "POST" :
        doc = db[uuid]
        db.delete( doc )
        return redirect( '/gestion/provisions/' )
    else :
        doc = db[uuid]
        return render( request,'gestion/delete_provision.html',{'row': doc, 'id': uuid } )

