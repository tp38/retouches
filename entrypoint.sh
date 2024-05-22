#!/bin/bash

#apt-get update && apt-get -y install gettext

# Collect static files
#echo "Collect static files"
#python manage.py collectstatic --noinput

# Apply database migrations
#echo "Apply database migrations"
#python manage.py makemigrations
#python manage.py migrate

# Start server
#echo "Update data"
#python manage.py flush --noinput
#python manage.py loaddata db.json

#echo "Start server"
#django-admin startproject retouches
python manage.py runserver 0.0.0.0:8000
