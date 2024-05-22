from couchdb import Server, http
from .credential import login_nat, password_nat

DB_ADMIN_STRING = "http://couchdb:couchdb@db:5984"
DB_USER_STRING = "http://db:5984"
DB_NAME = "/retouches"



if __name__ == "__main__" :
    login = "titi"
    pwd = "gmjqsgdmqsdg"
    s = Server( f"http://{login}:{pwd}@db:5984" )
    try:
        db = s['retouches']
        print( "OK" )
    except http.Unauthorized:
        print( "UnAuthorised" )


    s = Server( f"http://{login_nat}:{password_nat}@db:5984" )
    try:
        db = s['retouches']
        print( "OK" )
    except http.Unauthorized:
        print( "UnAuthorised" )
