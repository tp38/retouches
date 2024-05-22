# Retouches

This web application is used to monitor of Nat's retouching activity. 
You can save all sells and purchases for day. And day after days, you can display some reports like :
1. sells and purchases for a day, a week, a month
2. salary of the month

## Installation

Frontend is based on Django framework and backend is a CouchDb server. This document describe how to install them on Docker containers :
- Configuration of each container are in **Dockerfile** and **docker-compose.yml** files. read this files and docker documentation to customize them according to your needs.
- run : docker compose up 
- **entrypoint.sh** : launch Django developpement web server 

With this configuration :
- CouchDb/Fauxton can be access by the url http://localhost:5984/_utils
- Application can be access by the url http://localhost:8000/compta/

## Admin_tools

In this directory, there's some python scripts to import or export data.
We must create a file named credential.py and put in it a valid login/password :
1. cp credential.py.example credential.py
2. vim (or your prefered editor) credential.py 


### importFromCsv.py 

Once they are installed, you can use admin_tools to initialize the database. importFromCsv.py provide all need operations :

1. inserting data in the database : there must be locate in the file name **retouches.csv**. An example can be found in retouches.csv.example :
    - separator is ;
    - field delimiter is |
    - 1st field : doc type = transaction
    - 2nd field : a comment
    - 3rd field : paiement mode (eg in : esp, chq, cb_ca22, cb_sumup, vrt)
    - 4th field : amount
    - 5th field : year
    - 6th field : month
    - 7th field : day
    - 8th field : week number
2. creating views :
    - charges : get payload like *urssaf* or *Le Boudec*
    - paiemnt_ca : get yearly vacancy (CA) transactions (provisions or expenses)
    - paiement_rmb : get credit transactions (provisions or expenses)
    - paies : get salaries
    - recettes-depenses : get sells and purchases
    - transactions : get all transactions

### export2csv.py

extract all transactions in the format describe above