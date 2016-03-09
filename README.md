- [Requirements](#sec-2)
- [DB start :](#sec-3)

# Flurry - Final Project B.sc Computer Science

# Requirements

## sudo apt-get install python-psycopg2

## install postgres

## create db in postgres.

## Data.objects.filter(data\_<sub>dates</sub>\_<sub>0</sub>\_<sub>gt</sub>=unicode(dt.datetime.today()))

# DB start :

### CREATE DATABASE "flurryDB";

### CREATE CREATE USER admin WITH PASSWORD 'admin';

### ALTER USER admin WITH SUPERUSER CREATEROLE CREATEDB REPLICATION ;

### GRANT ALL PRIVILEGES ON DATABASE "flurryDB" to admin;
