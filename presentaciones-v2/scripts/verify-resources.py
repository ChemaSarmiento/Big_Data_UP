#!/usr/bin/env python3
"""Coherencia local del material de tweets: verdad.json, laboratorios S2–S8 y recursos. No ejecuta nada en la nube."""
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'recursos'
errors=[]
def check(cond,msg):
    if not cond:errors.append(msg)

v=json.loads((REC/'tweets/verdad.json').read_text())
total=v['tablas']['tweets_silver.tweets']['filas']
check(total==v['tablas']['tweets_bronze.entrada']['filas'],'Bronze y Silver deben tener las mismas filas')
check(sum(v['tweets_por_dia'][k] for k in v['tweets_por_dia'] if k.startswith('2022'))==total,'tweets por día no suma el total')
idi=v['idiomas']
check(idi['en']+idi['es']+idi['otro_total_fuera_de_en_es']==total,'idiomas en+es+otros no suma el total')
sanc=v['gold_sanciones_por_idioma']
check(sum(x['base'] for x in sanc.values())==total,'base de sanciones por idioma no suma el total')
check(set(v['gold_temas_total'])-{'_nota'}=={'energia','sanciones','mercados','alimentos','cadena_suministro','aviacion'},'seis temas esperados')
check(v['tablas']['tweets_gold.tema_dia']['filas']==12*6*3,'tema_dia debe tener 12 días x 6 temas x 3 grupos')
check(v['parquet_spark']['partes']==177,'el Parquet tiene 177 partes')
check(v['calidad_silver']['ids_distintos']==total,'ids distintos == filas')
check(v['calidad_silver']['max_repeticiones_de_un_texto'].startswith('421'),'texto más repetido corregido a 421')
for k,pct in v['gold_energia_en_pct_del_dia'].items():
    if k.startswith('2022'):
        n,base,p=pct
        check(abs(round(100*n/base,3)-p)<0.0015,f'energía en {k}: {n}/{base} no da {p}')

sessions=0
for n in range(2,9):
    d=json.loads((ROOT/f'especialidad-{n:02d}/contenido.json').read_text())
    steps=d['lab']['steps']
    check(len(steps)==6,f'S{n}: la guía debe tener 6 pasos')
    if n<8:check(sum(s['minutes'] for s in steps)==70,f'S{n}: los pasos suman {sum(s["minutes"] for s in steps)} y no 70 min')
    for s in steps:
        for f in ('action','check'):check(s.get(f),f'S{n} paso {s["n"]}: falta {f}')
        if n<8:
            for f in ('titulo','donde','error'):check(s.get(f),f'S{n} paso {s["n"]}: falta {f}')
            check(s.get('codigo') or s.get('salida'),f'S{n} paso {s["n"]}: falta código o salida esperada')
    check(d['lab'].get('aviso') and d['lab'].get('prerequisitos'),f'S{n}: faltan aviso/prerrequisitos')
    for a in d.get('assets',[]):check((REC/a).exists(),f'S{n}: el asset {a} no existe')
    guide=(ROOT/f'especialidad-{n:02d}/laboratorio.html').read_text()
    check(len(re.findall(r'<section id="paso-\d"',guide))==6,f'S{n}: laboratorio.html debe tener 6 pasos')
    check('precios-ilustrativos' not in guide and 'curso_bronze' not in guide,f'S{n}: la guía cita el fixture viejo')
    sessions+=1
guide1=(ROOT/'especialidad-01/laboratorio.html').read_text()
check(len(re.findall(r'<section id="paso-\d"',guide1))==6,'S1: laboratorio.html debe tener 6 pasos')

for f in sorted((REC/'tweets').iterdir()):
    if f.suffix in {'.sql','.py','.sh','.md','.csv','.json'}:
        t=f.read_text()
        check(len(t.strip())>20,f'{f.name} está vacío')
        if f.suffix=='.sql':
            code='\n'.join(l for l in t.split('\n') if not l.lstrip().startswith('--'))
            check(code.count('(')==code.count(')'),f'{f.name}: paréntesis desbalanceados')
        check(not re.search(r'TODO:|FIXME',t),f'{f.name} contiene marcas pendientes')

import re as _re
banned={'docente':r'docente','equipo (actividad)':r'trabajo en equipo|por equipos|cada equipo|tu equipo','H1–H8':r'(?-i:(?<![</\w])H[1-8]\b)','fecha de calendario':r'(?<![\d-])202[3-9]|nov(iembre)? de 20|abril de 20','proyecto de referencia':r'big-data-lunes'}
for n in range(1,8):
    for fn in ('index.html','laboratorio.html','notas.md'):
        f=ROOT/f'especialidad-{n:02d}'/fn
        if not f.exists():
            check(False,f'falta {f.name} de S{n}');continue
        txt=f.read_text()
        txt=_re.sub(r'<h1[^>]*>.*?</h1>','',txt)
        txt=_re.sub(r'gs://[^\s<"\']*|[A-Za-z0-9-]*2026[0-9]{4}','',txt)
        for k,pat in banned.items():
            hits=_re.findall(pat,txt,flags=_re.I)
            check(not hits,f'S{n} {fn}: aparece «{k}» ({len(hits)})')
if errors:
    print('FALLOS:');[print(' -',e) for e in errors];sys.exit(1)
print(f'OK: verdad coherente ({total:,} tweets), {sessions} guías S2–S8 con 6 pasos de 70 min, assets presentes. Límite: nada se ejecutó en la nube desde este script.')
