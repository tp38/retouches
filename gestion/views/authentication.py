from django.shortcuts import render, redirect
from couchdb import Server, Database

from django.conf import settings


def login(request):
    if request.method == "POST":
        login = request.POST['login']
        pwd = request.POST['pwd']
        s = Server( settings.URL_SERVER % (login, pwd) )
        try:
            db = s[settings.DB_GESTION]
            request.session['login'] = login
            request.session['pwd'] = pwd
            return redirect( '/gestion/synthese/' )
        except:
            return render( request, 'gestion/login.html', { 'error': 'Bad username or password'} )
    else:
        return render( request, 'gestion/login.html' )


def logout(request):
    del request.session['login']
    del request.session['pwd']
    return redirect( '/gestion/' )
