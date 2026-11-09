#!/usr/bin/env python3
"""Inspección docente reproducible: requiere red; no se ejecuta en build ni en clase.
Ejecutar desde raíz. Si cambia el origen, revisar resultados antes de guardar la muestra.
"""
import urllib.request,urllib.parse,json,csv,io,hashlib
from pathlib import Path
from html.parser import HTMLParser
class P(HTMLParser):
 def __init__(self):super().__init__();self.params={}
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='form':self.url=a['action']
  if t=='input' and a.get('type')=='hidden':self.params[a['name']]=a['value']
with urllib.request.urlopen('https://drive.google.com/uc?export=download&id=1dLxKFxawXTTaqCDr9Y9YpYdWTpOhol42',timeout=60) as r:
 warning=r.read(65536).decode('utf-8')
p=P();p.feed(warning);url=p.url+'?'+urllib.parse.urlencode(p.params)
size=20663702126
windows=[]
for label,start in [('inicio',0),('medio',size//2),('final',size-2097152)]:
 with urllib.request.urlopen(urllib.request.Request(url,headers={'Range':f'bytes={start}-{start+2097151}'}),timeout=90) as r:
  assert r.status==206,r.status
  assert r.headers['Content-Range'].endswith('/'+str(size)), 'El tamaño cambió: volver a perfilar antes de sobrescribir muestra'
  assert r.headers['Content-Range'].startswith(f'bytes {start}-'),r.headers['Content-Range']
  data=r.read(2097152)
 windows.append((label,start,data))
header=next(csv.reader(io.StringIO(windows[0][2].decode('utf-8').splitlines()[0])))
rows=[];info=[]
for label,start,data in windows:
 # CSV quotes may contain newlines; keep only records that parse strictly with all15 fields.
 text=data.decode('utf-8',errors='replace');text=text[text.find('\n')+1:];text=text[:text.rfind('\n')]
 parsed=list(csv.reader(io.StringIO(text),strict=True));valid=[r for r in parsed if len(r)==15 and len(r[6])>=10 and r[6][:4].isdigit()]
 selected=valid[:1500];rows+=selected
 info.append({'window':label,'byte_start':start,'bytes_read':len(data),'sha256_window':hashlib.sha256(data).hexdigest(),'complete_15_field_records':len(valid),'sample_rows':len(selected),'sample_min_date':min(r[6] for r in selected),'sample_max_date':max(r[6] for r in selected)})
out=Path('presentaciones-v2/clase-bigquery/recursos');out.mkdir(parents=True,exist_ok=True)
with (out/'all_data_muestra.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(header);w.writerows(rows)
meta={'source_file_id':'1dLxKFxawXTTaqCDr9Y9YpYdWTpOhol42','source_bytes':size,'inspected_at':'2026-11-09','method':'Tres ventanas contiguas de2MiB; primeras1500 filas completas de15 campos por ventana. No aleatoria ni representativa. Se omiten líneas parciales de borde. Valores sin normalizar.','columns':header,'windows':info,'sample_rows':len(rows),'sample_sha256':hashlib.sha256((out/'all_data_muestra.csv').read_bytes()).hexdigest()}
(out/'perfil-muestra.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');print(json.dumps(meta,ensure_ascii=False,indent=2))
from collections import Counter
print('TOP',Counter((r[0],r[1],r[2],r[6][:10],r[11],r[12].strip()) for r in rows).most_common(5))
print('blank prices',sum(not r[5].strip() for r in rows),'duplicates',len(rows)-len(set(map(tuple,rows))))
