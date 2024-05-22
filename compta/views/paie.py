from django.shortcuts import render
from couchdb import Server
from django.conf import settings
from datetime import date, datetime


CHARGES = 180
ASSURANCE = 25
CA = 200
RMB = 120



class Bilan():
    def __init__(self, db, year, month, day=10):
        self.db = db
        self.year = year
        self.month = month
        self.day = day
        self.paie = self.get_paie()
        self.charges_m = self.get_charges()
        self.recette, self.depense = self.get_recette_depense()
        self.urssaf_prev = self.get_urssaf_prev()
        self.charges_prev = self.get_charges_prev()
        self.provision_ca = self.get_provision_ca()
        self.provision_rmb = self.get_provision_rmb()
        self.reste = self.get_dispo_net()

    def get_recette_depense(self):
        recette = 0
        depense = 0
        for r in self.db.view( 'compta/recettes-depenses', group=True, group_level=2  ):
            if r.key == [self.year, self.month ] :
                recette = r.value[0]
                depense = r.value[1] * -1
                break
        return  recette, (depense - self.paie - self.charges_m)

    def get_charges(self):
        old_ch = 0
        for v in self.db.view( 'compta/charges', group=True, group_level=2 ):
            if v.key == [self.year, self.month ] :
                old_ch = v.value * -1
                break
        return old_ch

    def get_paie(self):
        paie = 0
        for s in self.db.view( 'compta/paies', group=True, group_level=2 ):
            if s.key == [self.year, self.month ] :
                paie = s.value * -1
                break
        return paie

    def get_recette(self):
        return self.recette

    def get_depense(self):
        return self.depense

    def get_urssaf_prev(self):
        return self.recette * 0.215

    def get_charges_prev(self):
    	if self.year == 2024 and self.month < 4:
    		return CHARGES
    	else:
#    		return CHARGES
        	return CHARGES + ASSURANCE

    def get_dispo_brut(self):
        return self.recette - self.depense - self.paie - self.urssaf_prev - self.charges_prev

    def get_provision_ca(self):
        ca = 0
        for s in self.db.view( 'compta/paiement_ca', group=True, group_level=2 ):
            if s.key == [self.year, self.month ] :
                ca = s.value
                break
        return ca

    def get_provision_rmb(self):
        rmb = 0
        for s in self.db.view( 'compta/paiement_rmb', group=True, group_level=2 ):
            if s.key == [self.year, self.month ] :
                rmb = s.value
                break
        return rmb

    def get_dispo_net(self):
        return self.get_dispo_brut() + self.get_provision_ca() + self.get_provision_rmb()
        # return self.get_dispo_brut()


    def get_bilan(self):
        return {'year': self.year,
                'month': self.month,
                'day': self.day,
                'recette': self.recette,
                'depense': self.depense,
                'paie': self.paie,
                'urssaf': self.urssaf_prev,
                'charges': self.charges_prev,
                'ca': -1 * self.provision_ca,
                'rmb': -1 * self.provision_rmb,
                'reste': self.reste }


def paie(request):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )
    db = s[settings.DB_NAME]

    if not request.method == "POST" :
        try:
            dd = request.GET['date']
        except:
            dd = date.today().strftime("%Y-%m-%d")
        sd = datetime.strptime(dd, "%Y-%m-%d")

        b = Bilan( db, sd.year, sd.month, sd.day )
        return render( request,'compta/paie.html', b.get_bilan() )
    else:

        return render( request,'compta/index.html' )


def synthese_paie(request):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )
    db = s[settings.DB_NAME]

    periods = []
    for r in db.view( 'compta/recettes-depenses', group=True, group_level=2  ):
        periods.append( r.key )

    total_ca = 0.0
    total_rmb = 0.0
    bilans = []
    for p in periods :
        b = Bilan( db, p[0], p[1] )
        bilans.append( b.get_bilan() )
        total_ca += -1 * b.get_provision_ca()
        total_rmb +=  -1 * b.get_provision_rmb()

    return render( request, 'compta/synthese_paie.html', { 'rows': reversed(bilans), 'total_ca': total_ca, 'total_rmb': total_rmb } )
