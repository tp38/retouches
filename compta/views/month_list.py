from django.shortcuts import render
from couchdb import Server, ResourceNotFound
from django.conf import settings

from datetime import datetime, date
import calendar



def month_list(request):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )

    db = s[settings.DB_NAME]
    rows = []

    if request.method == "POST":
        dd = request.POST['date']
    else:
        dd = date.today().strftime("%Y-%m-%d")

    sd = datetime.strptime(dd, "%Y-%m-%d")
    start = f"{sd.year}-{sd.month:02d}-01"
    end = f"{sd.year}-{sd.month:02d}-{calendar.monthrange(sd.year, sd.month)[1]:02d}"

    for r in db.view( 'compta/transactions',  startkey=end, endkey=start, descending=True ):
        doc = db[r.id]
        if doc['type'] == 'cb_sumup' and doc['montant'] > 0 :
            doc['m_bank'] = 0.9825 * doc['montant']
        if doc['type'] == 'cb_ca22' and doc['montant'] > 0 :
            doc['m_bank'] = 0.9827 * doc['montant']
        rows.append( doc )

    return render( request,'compta/month_list.html', {'rows': rows, 'day': dd } )
