import csv
from couchdb import Server
from uuid import uuid4



DB_STRING = "http://couchdb:couchdb@db:5984"
DB_NAME = "nat"

couch = Server(DB_STRING)
try:
    db = couch.create(DB_NAME)
except:
    del couch[DB_NAME]
    db = couch.create(DB_NAME)

with open("retouches.csv") as csvfile:
    reader= csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in reader:
        uuid = uuid4().hex
        db[uuid] = {'doc': row[0], 'comment': row[1], 'type': row[2], 'montant': float(row[3]), 'full_date': { 'year': int(row[4]), 'month': int(row[5]), 'week': int(row[6]), 'day': int(row[7]) } }


ing_view = {
    "_id": "_design/compta",
    "views": {
        "charges": {
            "map": "function (doc) {\n  if( doc.doc == 'transaction' && ( doc.comment.includes( 'Urssaf') | doc.comment.includes( 'Boudec') ) ) {\n    emit( [doc.full_date.year, doc.full_date.month, doc.full_date.week, doc.full_date.day], doc.montant )\n  }\n}",
            "reduce": "_sum"
        },
        "paiement_ca": {
            "map": "function (doc) {\n  if( doc.doc == 'transaction' && doc.comment.includes( 'provision CA') ) {\n    emit( [doc.full_date.year, doc.full_date.month, doc.full_date.week, doc.full_date.day], doc.montant )\n  }\n}",
            "reduce": "_sum"
        },
        "paiement_rmb": {
            "map": "function (doc) {\n  if( doc.doc == 'transaction' && doc.comment.includes( 'provision rmb') ) {\n    emit( [doc.full_date.year, doc.full_date.month, doc.full_date.week, doc.full_date.day], doc.montant )\n  }\n}",
            "reduce": "_sum"
        },
        "paies": {
            "map": "function (doc) {\n  if( doc.doc == 'transaction' && doc.comment.includes( 'paie @Nat') ) {\n    emit( [doc.full_date.year, doc.full_date.month, doc.full_date.week, doc.full_date.day], doc.montant )\n  }\n}",
            "reduce": "_sum"
        },
        "recettes-depenses": {
            "map": "function (doc) {\n  if( doc.doc == 'transaction' && !doc.comment.includes( 'provision rmb' ) && !doc.comment.includes( 'provision CA' ) ) {\n    emit([doc.full_date.year, doc.full_date.month, doc.full_date.week, doc.full_date.day], [doc.montant,0]);\n  } else {\n    emit([doc.full_date.year, doc.full_date.month, doc.full_date.week, doc.full_date.day], [0,doc.montant]);\n  }\n}",
            "reduce": "_sum"
        },
        "transactions": {
            "map": "function (doc) {\n  if( doc.doc == 'transaction' ) { \n    emit(`${doc.full_date.year}-${doc.full_date.month < 10 ? '0'+doc.full_date.month : doc.full_date.month}-${doc.full_date.day < 10 ? '0'+doc.full_date.day : doc.full_date.day}`, doc._id);\n  }\n}"
            }
        },
         "language": "javascript"
    }

db.save( ing_view )
