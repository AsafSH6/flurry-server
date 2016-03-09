1 . sudo apt-get install python-psycopg2
2 . install postgres 
3 . create db in postgres.
4 . Data.objects.filter(data__dates__0__gt=unicode(dt.datetime.today()))

DB start :  
 * CREATE DATABASE "flurryDB";
 * CREATE CREATE USER admin WITH PASSWORD 'admin';
 * ALTER USER admin WITH SUPERUSER CREATEROLE CREATEDB REPLICATION ;
 * GRANT ALL PRIVILEGES ON DATABASE "flurryDB" to admin;
