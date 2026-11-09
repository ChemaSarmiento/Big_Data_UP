#!/usr/bin/env python3
"""Publica HTML estático S1–S7 desde editorial/guion.py, sin tocar S8 ni labs."""
from pathlib import Path
import sys,html,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'editorial'))
from guion import SESSIONS
E=html.escape
for n,data in SESSIONS.items():
 path=ROOT/f'especialidad-{n:02d}'
 rendered=[]
 for i,s in enumerate(data['slides'],1):
  title='' if 'cover' in s['layout'].split() else f'<h1>{s["title"]}</h1>'
  classes=' '.join(x if x in ('cover','dark','statement') else 'kind-'+x for x in s['layout'].split())
  rendered.append(f'''<section class="slide {classes}" data-id="E{n:02d}-{i:02d}" data-title="{E(s['title'],quote=True)}" data-note="{E(s['note'],quote=True)}" data-layout="{s['layout']}">
<div class="eyebrow"><span>Especialidad / {n:02d} · {s['phase']}</span><span>Chema Sarmiento</span></div>{title}<div class="content">{s['body']}</div><div class="source"><span>{s['source']}</span><span>{n:02d} / {i:02d}</span></div></section>''')
 title=data['title']
 extra_script='<script src="../editorial/silver.js" defer></script>' if n==4 else '<script src="../editorial/gold.js" defer></script>' if n==5 else '<link rel="stylesheet" href="../editorial/bi.css"><script src="../editorial/bi.js" defer></script>' if n==6 else '<link rel="stylesheet" href="../editorial/ai.css"><script src="../editorial/ai.js" defer></script>' if n==7 else ''
 page=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} · Especialidad</title><meta name="description" content="Sesión {n}: {E(data['bigidea'],quote=True)}"><link rel="stylesheet" href="../editorial/editorial.css"><script src="../compartido/deck.js" defer></script><script src="../editorial/interacciones.js" defer></script>{extra_script}</head><body data-session="{n}"><div id="viewport"><main id="stage" aria-label="Presentación: clic en espacio libre o flechas para revelar">{''.join(rendered)}</main></div><footer class="toolbar"><div class="left"><a href="../" aria-label="Volver al curso">Curso</a><button id="previous" aria-label="Paso anterior">←</button><span id="counter" class="counter"></span><button id="next" aria-label="Paso siguiente">→</button><span id="step-counter" class="step-counter" aria-live="polite"></span><span id="section-label"></span></div><div class="controls"><button id="show-all">Mostrar todo</button><button id="index-button">Índice</button><button id="lab-button">Laboratorio</button><button id="notes-button">Notas</button><button id="fullscreen" aria-label="Pantalla completa">⛶</button></div></footer><div class="progress" aria-hidden="true"><div id="progress"></div></div><dialog id="overview"><div class="dialog-heading"><h2>Ruta de la sesión {n}</h2><button data-close>Cerrar ×</button></div><ol id="slide-list"></ol><button id="print-button">Imprimir / guardar PDF</button></dialog><dialog id="notes"><div class="dialog-heading"><h2>Guion de facilitación</h2><button data-close>Cerrar ×</button></div><p id="notes-text"></p></dialog><dialog id="lab"><div class="dialog-heading"><h2>Laboratorio · sesión {n}</h2><button data-close>Cerrar ×</button></div><p>Abre la guía en otra pestaña para conservar tu lugar.</p><p><a href="laboratorio.html" target="_blank" rel="noopener">Instrucciones completas, código y comprobación ↗</a></p><p><a href="notas-docente.md">Guion docente</a></p></dialog><noscript>Se requiere JavaScript para la navegación. Puedes leer la guía de laboratorio y las notas.</noscript></body></html>'''
 (path/'index.html').write_text(page)
 notes=f'# Sesión {n} · {title}\n\nGran idea: {data["bigidea"]}\n\nGuion para presentar en vivo. [pausa 3 s] indica silencio deliberado. Los controles se activan por el docente; no hay avance automático.\n\n'
 notes+='\n\n'.join(f'## {i:02d}. {s["title"]}\n\n{s["note"]}' for i,s in enumerate(data['slides'],1))
 (path/'notas-docente.md').write_text(notes+'\n')
 (path/'README.md').write_text(f'''# S{n} · {title}

{len(data['slides'])} slides, rediseño editorial con el kit de Chema. Fuente: `../editorial/guion.py` (SESSIONS[{n}]); presentación generada por `python3 presentaciones-v2/scripts/build-editorial.py` desde raíz.

Abrir `/especialidad-{n:02d}/` desde el servidor sobre `presentaciones-v2`. Teclado ←/→, clic en espacio libre para revelar, O índice, L laboratorio, F pantalla completa. Imprimir desde Índice, con todos los pasos revelados. Mobile usa flujo vertical.

Guía extensa: `laboratorio.html`. Fuente de las slides y notas: guion.py, no contenido.json. El contenido.json anterior de S2–S7 queda como referencia de la guía; build.py ya no regenera estas sesiones. No editar index.html a mano.

Ensayo cloud/MariaDB pendiente. Simulaciones locales etiquetadas como ejemplos, sin ejecutar SQL remoto. Datos distintos por equipo para el proyecto. Solo Especialidad.
''')
 print(f'S{n}: {len(data["slides"])} slides')
(ROOT/'editorial/manifest.json').write_text(json.dumps({str(n):{'title':d['title'],'slides':len(d['slides']),'source':'editorial/guion.py'} for n,d in SESSIONS.items()},ensure_ascii=False,indent=2)+'\n')

if 6 in SESSIONS:
 from guion import dashboard
 (ROOT/'especialidad-06/practica.html').write_text('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Práctica de dashboard · Especialidad</title><link rel="stylesheet" href="../compartido/curso.css"><link rel="stylesheet" href="../editorial/bi.css"><script src="../editorial/bi.js" defer></script></head><body><article class="guide"><a href="index.html#4/0">← Volver al deck</a><h1>Comprueba qué cambia al filtrar.</h1><p>Simulación local sobre datos ficticios. Sin conexión a BigQuery ni al archivo real de PROFECO. El filtro cambia las tiendas visibles dentro del mismo escenario histórico.</p>'+dashboard()+'<h2>Prueba de lectura</h2><p>Elige Solo C y explica por qué el costo completo es desconocido. Elige Solo B y comprueba el alcance de la conclusión. Vuelve a Todas y contrasta con gold-esperado.csv.</p><p><a href="../recursos/gold-esperado.csv" download>Resultados de referencia ↓</a> · <a href="laboratorio.html">Laboratorio BI</a></p></article></body></html>')
