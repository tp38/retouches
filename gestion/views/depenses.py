from django.shortcuts import render, redirect
from couchdb import Server
from couchdb.http import ResourceNotFound

from django.conf import settings

from datetime import datetime, date
import calendar
from uuid import uuid4

from .recettes import DateStringToArray, datetimeToArray

def depense_detail(request, uuid):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )
    db = s[settings.DB_GESTION]

    if request.method == "POST":
        try:
            doc = db[uuid]
        except ResourceNotFound:
            doc = { '_id': uuid, 'class': 'depense' }

        # save date if exists
        if request.POST.__contains__('date') and request.POST.get('date') != "" :
            doc['date'] = DateStringToArray( request.POST.get('date') )

        # save bénéficiare if exists
        if request.POST.__contains__( 'beneficiaire' ) :
            doc['beneficiaire'] = request.POST.get('beneficiaire')

        # save description if exists 
        if request.POST.__contains__( 'description' ) :
            doc['description'] = request.POST.get('description')

        # save price if exists
        if request.POST.__contains__( 'montant' ) :
            try:
                doc['montant'] = float(request.POST.get( 'montant' ))
            except:
                doc[''] = 0.0

        # save bank_state if exists
        if request.POST.__contains__('bank') :
            doc['bank'] = request.POST.get('bank')

        db.save( doc )        
        return redirect( '/gestion/depenses/' )
    else :
        if uuid == "new" :
            uuid = uuid4()
            doc = {"class": 'depense', "date" : DateStringToArray( date.today().strftime("%Y-%m-%d") ), "montant": "0,0" }
        else:
            doc = db[uuid]
        return render( request,'gestion/detail_depense.html',{'row': doc, 'id': uuid } )


def depenses_liste(request):
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

    for r in db.view( "gestion/depensesFiches", startkey=end, endkey=start, descending=True ):
        doc = db[r.id]
        rows.append( doc )

    reqday = datetimeToArray( reqday )
    day = 0
    for r in db.view( 'gestion/depensesResultat', startkey=end, endkey=start, descending=True, group=True, group_level=4  ) :
        if r.key[3] == reqday[3] :
            day = r.value
            break

    week = 0
    for r in db.view( 'gestion/depensesResultat', startkey=end, endkey=start, descending=True, group=True, group_level=3  ) :
        if r.key[2] == reqday[2] :
            week = r.value
            break

    month = 0
    for r in db.view( 'gestion/depensesResultat', startkey=end, endkey=start, descending=True, group=True, group_level=2  ) :
        if r.key[1] == reqday[1] :
            month = r.value
            break

    report = { 'day': day, 'week': week, 'month': month }

    return render( request,'gestion/liste_depenses.html', {'rows': rows, 'day': dd, 'report': report } )



