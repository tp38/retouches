from django.shortcuts import render, redirect
from couchdb import Server
from django.conf import settings



# Create your views here.

def process(request):
    login = request.session['login']
    pwd = request.session['pwd']
    s = Server( settings.URL_SERVER % (login, pwd) )
    db = s[settings.DB_NAME]
    
    return redirect( '/compta/' )
