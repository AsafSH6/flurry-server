- [Flurry - Final Project B.sc Computer Science](#sec-1)
- [Requirements](#sec-2)
- [DB start :](#sec-3)
- [Articles :](#sec-4)
- [Compability to the OBD-II:](#sec-5)

# Flurry - Final Project B.sc Computer Science

# Requirements

1.  sudo apt-get install python-psycopg2

2.  install postgres

3.  create db in postgres.

4.  Data.objects.filter(data\_<sub>dates</sub>\_<sub>0</sub>\_<sub>gt</sub>=unicode(dt.datetime.today()))

# DB start :

1.  CREATE DATABASE "flurryDB";

2.  CREATE CREATE USER admin WITH PASSWORD 'admin';

3.  ALTER USER admin WITH SUPERUSER CREATEROLE CREATEDB REPLICATION ;

4.  GRANT ALL PRIVILEGES ON DATABASE "flurryDB" to admin;

# Articles :

# Compability to the OBD-II:

1.  If your vehicle (any brand) is made/imported AFTER 1 Jan, 2003 — then it's 100% OBD-2 compliant. TOAD will work!
