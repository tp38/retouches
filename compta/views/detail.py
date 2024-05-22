from django.shortcuts import render, redirect
from couchdb import Server
from couchdb.http import ResourceNotFound
from django.conf import settings
from uuid import uuid4
from datetime import datetime, date
import calendar


def detail(request, uuid):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )
    db = s[settings.DB_NAME]

    if request.method == "POST":
        try:
            doc = db[uuid]
        except ResourceNotFound:
            doc = { '_id': uuid, 'doc': 'transaction' }
        # doc['date'] = request.POST['date']
        doc['comment'] = request.POST['comment']
        doc['type'] = request.POST['type']
        doc['montant'] = float( request.POST['montant'] )
        sd = datetime.strptime( request.POST['date'], "%Y-%m-%d")
        doc['full_date'] = { 'year': sd.year, 'month': sd.month, 'day': sd.day, 'week': sd.isocalendar().week }
        db.save( doc )
        return redirect( '/compta/month_list/' )
    else:
        if uuid == '-1' :
            uuid = uuid4().hex
            dd = date.today().strftime("%Y-%m-%d")
            sd = datetime.strptime(dd, "%Y-%m-%d")
            fd = { 'year': sd.year, 'month': sd.month, 'day': sd.day, 'week': sd.isocalendar().week }
            # doc = {"date": dd, "comment": "to change", "type": "cb", "montant": 0.0, "full_date": fd}
            doc = {"doc": 'transaction', "comment": "to change", "type": "cb", "montant": 0.0, "full_date": fd}
        else:
            doc = db[uuid]
        return render( request,'compta/detail.html',{'row': doc, 'id': uuid } )
