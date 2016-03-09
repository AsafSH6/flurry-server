<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#orgheadline1">1. Flurry - Final Project B.sc Computer Science</a></li>
<li><a href="#orgheadline6">2. Requirements</a>
<ul>
<li><a href="#orgheadline2">2.1. sudo apt-get install python-psycopg2</a></li>
<li><a href="#orgheadline3">2.2. install postgres</a></li>
<li><a href="#orgheadline4">2.3. create db in postgres.</a></li>
<li><a href="#orgheadline5">2.4. Data.objects.filter(data_<sub>dates</sub>_<sub>0</sub>_<sub>gt</sub>=unicode(dt.datetime.today()))</a></li>
</ul>
</li>
<li><a href="#orgheadline11">3. DB start :</a>
<ul>
<li>
<ul>
<li><a href="#orgheadline7">3.0.1. CREATE DATABASE "flurryDB";</a></li>
<li><a href="#orgheadline8">3.0.2. CREATE CREATE USER admin WITH PASSWORD 'admin';</a></li>
<li><a href="#orgheadline9">3.0.3. ALTER USER admin WITH SUPERUSER CREATEROLE CREATEDB REPLICATION ;</a></li>
<li><a href="#orgheadline10">3.0.4. GRANT ALL PRIVILEGES ON DATABASE "flurryDB" to admin;</a></li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
</div>

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
