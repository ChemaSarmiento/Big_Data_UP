#!/usr/bin/env python3
"""Controles locales de fixtures y SQL común. No sustituye ejecución MariaDB/BigQuery."""
from pathlib import Path
from decimal import Decimal, InvalidOperation
import csv, hashlib, json, re, sqlite3

root=Path(__file__).resolve().parents[1]
r=root/'recursos'
m=json.loads((r/'manifiesto-fixture.json').read_text())
assert hashlib.sha256((r/m['archivo']).read_bytes()).hexdigest()==m['sha256']
rows=list(csv.DictReader((r/m['archivo']).open()))
assert len(rows)==16
unique={tuple(row.values()):row for row in rows}
assert len(unique)==15
accepted=[];rejected=[]
from datetime import date
for row in unique.values():
 try:
  date.fromisoformat(row['fecha_texto'])
  value=Decimal(row['precio_texto'])
  assert value>0
  accepted.append((row,value))
 except (ValueError,InvalidOperation,AssertionError):rejected.append(row)
assert len(accepted)==13 and len(rejected)==2
assert {row['id'] for row in rejected}=={'C4','C5'}
expected=list(csv.DictReader((r/'gold-esperado.csv').open()))
for row in expected:
 found=[v for data,v in accepted if data['establecimiento']==row['establecimiento']]
 assert len(found)==int(row['productos_encontrados'])
 assert sum(found)==Decimal(row['subtotal_mxn'])
 assert Decimal(len(found))/5==Decimal(row['cobertura'])
 assert bool(row['costo_completo_mxn'])==(len(found)==5)
assert expected[2]['costo_completo_mxn']==''

# Ejecutar el archivo de consultas sobre un fixture relacional reducido, con SQL común.
# sqlite valida resultados de estas SELECT; no demuestra dialecto/servidor MariaDB real.
db=sqlite3.connect(':memory:')
db.executescript('''
CREATE TABLE employees(emp_no INTEGER,first_name TEXT,last_name TEXT,hire_date TEXT);
CREATE TABLE departments(dept_no TEXT,dept_name TEXT);
CREATE TABLE dept_emp(emp_no INTEGER,dept_no TEXT,from_date TEXT,to_date TEXT);
CREATE TABLE salaries(emp_no INTEGER,salary INTEGER,from_date TEXT,to_date TEXT);
INSERT INTO employees VALUES (10001,'Ana','Uno','1990-05-01'),(10002,'Ana','Uno','1992-01-01'),(10003,'Luis','Dos','1988-01-01');
INSERT INTO departments VALUES ('d1','Ventas'),('d2','Ingenieria'),('d3','Sin asignados');
INSERT INTO dept_emp VALUES (10001,'d1','1990-05-01','9999-01-01'),(10002,'d2','1992-01-01','9999-01-01');
INSERT INTO salaries VALUES (10001,40000,'1990-05-01','1996-01-01'),(10001,60000,'1996-01-01','9999-01-01'),(10002,70000,'1992-01-01','9999-01-01');
''')
sql=re.sub(r'--[^\n]*','',(r/'employees-fast-track.sql').read_text())
queries=[q.strip() for q in sql.split(';') if q.strip() and not q.strip().upper().startswith('USE ')]
results=[db.execute(q).fetchall() for q in queries]
assert len(results)==10
assert results[3]==[('d1','Ventas',1),('d2','Ingenieria',1),('d3','Sin asignados',0)]
assert len(results[6])==2 and len(results[7])==1
assert results[7][0][1]==60000
assert results[8]==[(3,3)] and results[9]==[]
assert sum(int(row['puntos_maximos']) for row in csv.DictReader((r/'rubrica.csv').open()))==100
for p in root.glob('especialidad-*/contenido.json'):
 data=json.loads(p.read_text());n=data['session']
 assert len(data['slides'])==(28 if n<8 else 14)
 for s in data['slides']:assert len(s['items'])>=2 and all(len(i['text'])>20 for i in s['items'])
 if n<8:assert sum(step['minutes'] for step in data['lab']['steps'])==55
print('OK: checksum, 16/1/2/13, Gold A150 B160 C54/0.6, SQL employees en fixture SQLite, rúbrica100 y fuentes S2–S8.')
print('Límite: consultas cloud y ejecución MariaDB real pendientes; no se validan por inferencia.')
