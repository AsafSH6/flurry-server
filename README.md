

# Flurry - Final Project B.sc Computer Science<a id="orgheadline1"></a>

# Requirements<a id="orgheadline6"></a>

## sudo apt-get install python-psycopg2<a id="orgheadline2"></a>

## install postgres<a id="orgheadline3"></a>

## create db in postgres.<a id="orgheadline4"></a>

## Data.objects.filter(data\_<sub>dates</sub>\_<sub>0</sub>\_<sub>gt</sub>=unicode(dt.datetime.today()))<a id="orgheadline5"></a>

# DB start :<a id="orgheadline11"></a>

### CREATE DATABASE "flurryDB";<a id="orgheadline7"></a>

### CREATE CREATE USER admin WITH PASSWORD 'admin';<a id="orgheadline8"></a>

### ALTER USER admin WITH SUPERUSER CREATEROLE CREATEDB REPLICATION ;<a id="orgheadline9"></a>

### GRANT ALL PRIVILEGES ON DATABASE "flurryDB" to admin;<a id="orgheadline10"></a>
