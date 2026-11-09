#!/usr/bin/env python3
"""Controles locales independientes sobre la muestra; NO ejecuta GoogleSQL."""
from pathlib import Path
import csv,json,hashlib,datetime,re
from decimal import Decimal
from collections import defaultdict
root=Path(__file__).resolve().parents[1]/'clase-bigquery/recursos'
meta=json.loads((root/'perfil-muestra.json').read_text());data=(root/'all_data_muestra.csv').read_bytes()
assert hashlib.sha256(data).hexdigest()==meta['sample_sha256']
assert b'\xef\xbf\xbd' not in data, 'No se permiten caracteres de reemplazo en muestra'
with (root/'all_data_muestra.csv').open(newline='') as f:
 reader=csv.DictReader(f);assert reader.fieldnames==meta['columns'];rows=list(reader)
assert len(rows)==4500
assert all(len(r)==15 and None not in r for r in rows)
unique={tuple(r.values()) for r in rows};assert len(unique)==4500
clean=lambda x:re.sub(r'\s+',' ',x.strip().upper())
groups=defaultdict(set);accepted=0;rejected=0;selected=[]
for row in rows:
 try:
  price=Decimal(row['precio']);dt=datetime.datetime.fromisoformat(row['fechaRegistro'])
  required=['producto','marca','presentacion','nombreComercial','direccion','estado','municipio']
  valid=price>0 and all(clean(row[k]) for k in required)
 except (ValueError,ArithmeticError):valid=False
 if not valid:rejected+=1;continue
 accepted+=1
 key=tuple(clean(row[k]) for k in ['producto','marca','presentacion','cadenaComercial','nombreComercial','direccion','estado','municipio'])+(dt.date().isoformat(),)
 groups[key].add(price)
 if clean(row['producto'])=='REFRESCO' and clean(row['marca'])=='SPRITE' and clean(row['presentacion'])=='BOTELLA 2 LT. NO RETORNABLE' and clean(row['estado'])=='DISTRITO FEDERAL' and clean(row['municipio'])=='TLALPAN' and dt.date().isoformat()=='2014-03-19':selected.append((clean(row['nombreComercial']),price))
assert accepted==4500 and rejected==0
assert sum(r['municipio']!=r['municipio'].strip() for r in rows)==3000
assert len(selected)==2 and {p for _,p in selected}=={Decimal('15.1'),Decimal('15.5')}
assert max(p for _,p in selected)-min(p for _,p in selected)==Decimal('0.4')
# Repetir registros no cambia el conjunto de firmas lógicas de entrada.
assert len(set(tuple(r.values()) for r in rows+rows))==4500
result={'rows':len(rows),'accepted_local_rules':accepted,'rejected_local_rules':rejected,'trailing_municipio':3000,'distinct_input_rows':len(unique),'product_store_day_groups':len(groups),'groups_with_price_conflicts':sum(len(x)>1 for x in groups.values()),'comparison':[{'store':s,'price_mxn':str(p)} for s,p in selected],'scope':'Muestra únicamente. Controles Python, no ejecución BigQuery.'}
print(json.dumps(result,ensure_ascii=False,indent=2))
