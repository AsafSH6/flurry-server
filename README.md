- [Requirements](#sec-2)
- [DB start :](#sec-3)
- [Admin :](#sec-4)
- [REST API :](#sec-5)

# Flurry - Final Project B.sc Computer Science

# Requirements

## sudo apt-get install python-psycopg2

## install postgres

## create db in postgres.

## Data.objects.filter(data\_<sub>dates</sub>\_<sub>0</sub>\_<sub>gt</sub>=unicode(dt.datetime.today()))

# DB start :

### CREATE DATABASE "flurryDB";

### CREATE USER admin WITH PASSWORD 'admin';

### ALTER USER admin WITH SUPERUSER CREATEROLE CREATEDB REPLICATION ;

### GRANT ALL PRIVILEGES ON DATABASE "flurryDB" to admin;

# Admin:

#### Create super user using the command: python manage.py createsuperuser

#### Run the command: python manage.py runserver

#### Go to: http://127.0.0.1:8000/admin/

#### Log in with your super user credentials

# REST API:

##### python manage.py runserver

##### Go to: http://127.0.0.1/api/v1/flurry/
