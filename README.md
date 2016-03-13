- [Flurry - Final Project B.sc Computer Science](#sec-1)
- [Requirements](#sec-2)
- [DB start :](#sec-3)
- [Admin :](#sec-4)
- [REST API :](#sec-5)
- [Compability to the OBD-II:](#sec-6)

# Flurry - Final Project B.sc Computer Science

# Requirements

1.  sudo apt-get install python-psycopg2

2.  install postgres

3.  create db in postgres.

4.  Data.objects.filter(data\_<sub>dates</sub>\_<sub>0</sub>\_<sub>gt</sub>=unicode(dt.datetime.today()))

# DB start :

1.  CREATE DATABASE "flurryDB";

2.  CREATE USER admin WITH PASSWORD 'admin';

3.  ALTER USER admin WITH SUPERUSER CREATEROLE CREATEDB REPLICATION ;

4.  GRANT ALL PRIVILEGES ON DATABASE "flurryDB" to admin;


# Admin:

#### Create super user using the command: python manage.py createsuperuser

#### Run the command: python manage.py runserver

#### Go to: http://127.0.0.1:8000/admin/

#### Log in with your super user credentials

# REST API:

##### python manage.py runserver

##### Go to: http://127.0.0.1/api/v1/flurry/

# Compability to the OBD-II:

1.  If your vehicle (any brand) is made/imported AFTER 1 Jan, 2003 — then it's 100% OBD-2 compliant. TOAD will work!
