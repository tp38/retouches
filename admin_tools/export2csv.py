from couchdb import Server
#import json


DB_STRING = "http://couchdb:couchdb@db:5984"
DB_NAME = "retouches"

SERVER = Server(DB_STRING)
db = SERVER[DB_NAME]

with open("retouches.csv", 'w', encoding="utf-8") as csvfile:
    for r in db.view( 'compta/transactions' ):
        doc = db.get(r.id)
        # csvfile.write( f"\"{doc['date']}\";\"{doc['comment']}\";\"{doc['type']}\";\"{doc['montant']}\";\"{doc['full_date']['year']}\";\"{doc['full_date']['month']}\";\"{doc['full_date']['week']}\";\"{doc['full_date']['day']}\"\n" )
        csvfile.write( f"|{doc['doc']}|;|{doc['comment']}|;|{doc['type']}|;|{doc['montant']}|;|{doc['full_date']['year']}|;|{doc['full_date']['month']}|;|{doc['full_date']['week']}|;|{doc['full_date']['day']}|\n" )
