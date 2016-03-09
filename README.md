- [Flurry - Final Project B.sc Computer Science](#sec-1)
- [Requirements](#sec-2)
  - [sudo apt-get install python-psycopg2](#sec-2-1)
  - [install postgres](#sec-2-2)
  - [create db in postgres.](#sec-2-3)
  - [Data.objects.filter(data\_<sub>dates</sub>\_<sub>0</sub>\_<sub>gt</sub>=unicode(dt.datetime.today()))](#sec-2-4)
- [DB start :](#sec-3)
    - [CREATE DATABASE "flurryDB";](#sec-3-0-1)
    - [CREATE CREATE USER admin WITH PASSWORD 'admin';](#sec-3-0-2)
    - [ALTER USER admin WITH SUPERUSER CREATEROLE CREATEDB REPLICATION ;](#sec-3-0-3)
    - [GRANT ALL PRIVILEGES ON DATABASE "flurryDB" to admin;](#sec-3-0-4)

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
