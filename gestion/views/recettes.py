from django.shortcuts import render, redirect
from couchdb import Server
from couchdb.http import ResourceNotFound

from django.conf import settings

from datetime import datetime, date
import calendar
from uuid import uuid4


def recette_detail(request, uuid):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )
    db = s[settings.DB_GESTION]

    if request.method == "POST":
        try:
            doc = db[uuid]
        except ResourceNotFound:
            doc = { '_id': uuid, 'class': 'recette' }

        # save carnet - numero if exists
        if request.POST.__contains__( 'carnet' ) :
            doc['carnet'] = int(request.POST.get('carnet'))
        if request.POST.__contains__( 'numero' ) :
            doc['numero'] = int(request.POST.get('numero'))

        # save price if exists
        if request.POST.__contains__( 'montant_du' ) :
            try:
                doc['cout'] = float(request.POST.get( 'montant_du' ))
            except:
                doc['cout'] = 0.0

        # save description if exists 
        if request.POST.__contains__( 'description' ) :
            doc['description'] = request.POST.get('description')

        # save client if exists
        client = {}
        if request.POST.__contains__( 'nom' ) :
            client['nom'] = request.POST.get('nom')
        if request.POST.__contains__( 'ville' ) :
            client['ville'] = request.POST.get('ville')
        if request.POST.__contains__( 'tel' ) :
            client['tel'] = request.POST.get('tel')

        # save dates if exists
        dates = {}
        if request.POST.__contains__('prevu') and request.POST.get('prevu') != "" :
            dates['prevu'] = DateStringToArray( request.POST.get('prevu') )
        if request.POST.__contains__('sms') and request.POST.get('sms') != "" :
            dates['sms'] = DateStringToArray( request.POST.get('sms') )

        # save reglements if exists
        commande = { 'montant': 0.0, 'date': [0,0,0,0], 'mode': 'esp', 'frais': 0.0, 'bank': False, 'forgot': False }
        if request.POST.__contains__('acp_montant') and request.POST.get('acp_montant') != '' :
            commande['montant'] = float(request.POST.get('acp_montant'))

        if request.POST.__contains__('acp_date') and request.POST.get('acp_date') != '' :
            commande['date'] = DateStringToArray( request.POST.get('acp_date') )
            dates['depot'] = DateStringToArray( request.POST.get('acp_date') )
           
        if request.POST.__contains__('acp_mode') :
            commande['mode'] = request.POST.get('acp_mode')
            if commande['mode'] == 'cb_sumup' :
                commande['frais'] = -1 * round(commande['montant'] * (1 - 0.9825),2)
            elif commande['mode'] == 'cb_ca22' :
                commande['frais'] = -1 * round(commande['montant'] * (1 - 0.9827),2)
            else :
                commande['frais'] = 0

        if request.POST.__contains__('acp_bank') :
            commande['bank'] = True
        else :
            commande['bank'] = False

        if request.POST.__contains__('acp_forgot') :
            commande['forgot'] = True
        else :
            commande['forgot'] = False


        livraison = { 'montant': 0.0, 'date': [0,0,0,0], 'mode': 'esp', 'frais': 0.0, 'bank': False, 'forgot': False }
        if request.POST.__contains__('livraison_montant') and request.POST.get('livraison_montant') != '':
            livraison['montant'] = float(request.POST.get('livraison_montant'))

        if request.POST.__contains__('livraison_date') and request.POST.get('livraison_date') != "" :
            livraison['date'] = DateStringToArray( request.POST.get('livraison_date') )
            dates['retrait'] = DateStringToArray( request.POST.get('livraison_date') )

        if request.POST.__contains__('livraison_mode') :
            livraison['mode'] = request.POST.get('livraison_mode')
            if livraison['mode'] == 'cb_sumup' :
                livraison['frais'] = -1 * round(livraison['montant'] * (1 - 0.9825),2)
            elif livraison['mode'] == 'cb_ca22' :
                livraison['frais'] = -1 * round(livraison['montant'] * (1 - 0.9827),2)
            else :
                livraison['frais'] = 0

        if request.POST.__contains__('livraison_bank') :
            livraison['bank'] = True
        else :
            livraison['bank'] = False

        if request.POST.__contains__('livraison_forgot') :
            livraison['forgot'] = True
        else :
            livraison['forgot'] = False

        reglements = {}
        if len( commande ) != 0 :
            reglements['commande'] = commande
        if len( livraison ) != 0 :
            reglements['livraison'] = livraison

        if len(client) != 0 :
            doc['client'] = client

        if len(dates) != 0 :
            doc['dates'] = dates

        if len(reglements) != 0 :
            doc['reglements'] = reglements

        db.save( doc )        
        return redirect( '/gestion/recettes/' )
    else :
        if uuid == "new" :
            uuid = uuid4()
            carnet = 0
            numero = 0
            for r in db.view( 'recettes/FichesByCarnetNumero',  descending=True, limit=1 ):
                doc = db[r.id]
                carnet = doc['carnet']
                numero = doc['numero']
            numero += 1
            if numero == 100 :
                carnet += 1
                numero = 1
            doc = {
                "class": 'recette', 
                "carnet": carnet, 
                "numero" : numero, 
                "dates" : { "depot" : DateStringToArray( date.today().strftime("%Y-%m-%d") ) },
                "reglements" : {
                    "commande" : {
                        "montant" : 0,
                        "date" : [0,0,0,0],
                        "mode" : "chq",
                        "frais" : 0,
                        "bank" : False,
                        "forgot": False
                    },
                    "livraison" : {
                        "montant" : 0,
                        "date" : [0,0,0,0],
                        "mode" : "chq",
                        "frais" : 0,
                        "bank" : False,
                        "forgot": False
                    }                
                },
                "description" : "",
                "client" : {
                    "nom" : "",
                    "ville" : "",
                    "tel" : ""
                }
            }
            phase = "depot"
        else:
            doc = db[uuid]
            phase = "retrait"

        return render( request,'gestion/detail_recette.html',{'row': doc, 'id': uuid, 'phase': phase } )

def recettes_liste(request):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )

    db = s[settings.DB_GESTION]

    if request.method == "POST":
        dd = request.POST.get('dd')
        mode = request.POST.get('mode')
    else:
        dd = date.today().strftime("%Y-%m-%d")
        mode = "En_cours"

    reqday = datetime.strptime(dd, "%Y-%m-%d")
    start = DateStringToArray( f"{reqday.year}-{reqday.month:02d}-01" )
    end = DateStringToArray( f"{reqday.year}-{reqday.month:02d}-{calendar.monthrange(reqday.year, reqday.month)[1]:02d}" )

    if mode == "En_cours" :
        view = "recettes/FichesEnCours"
    else:
        view = "recettes/Fiches"

    data = []
    try:
        for r in db.view( view, startkey=[end,{}], endkey=[start,{}], descending=True ):
            doc = db[r.id]
            data.append( doc )
    except:
        pass

    reqday = datetimeToArray( reqday )
    day = 0
    try:
        for r in db.view( 'recettes/Resultat', startkey=end, endkey=start, descending=True, group=True, group_level=4  ) :
            if r.key[3] == reqday[3] :
                day = r.value
                break
    except:
        pass

    week = 0
    try:
        for r in db.view( 'recettes/Resultat', startkey=end, endkey=start, descending=True, group=True, group_level=3  ) :
            if r.key[2] == reqday[2] :
                week = r.value
                break
    except:
        pass

    month = 0
    try:
        for r in db.view( 'recettes/Resultat', startkey=end, endkey=start, descending=True, group=True, group_level=2  ) :
            if r.key[1] == reqday[1] :
                month = r.value
                break
    except:
        pass

    report = { 'day': day, 'week': week, 'month': month }

    return render( request,'gestion/liste_recettes.html', {'rows': data, 'day': dd, 'report': report } )

def DateStringToArray( d ) :
    s = datetime.strptime( d, "%Y-%m-%d")
    return datetimeToArray( s )

def datetimeToArray( s ) :
    week = s.isocalendar()[1]
    if s.month == 12 and week == 1 :
        week = 53
    return [ s.year, s.month, week, s.day ]

