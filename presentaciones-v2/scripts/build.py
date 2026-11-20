#!/usr/bin/env python3
"""Genera guías S2–S8 y decks S8. S1–S7 usan build-editorial.py."""
from pathlib import Path
import html,json
ROOT=Path(__file__).resolve().parents[1]
esc=lambda s:html.escape(str(s),quote=True)
def links(data):return ' · '.join(f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(t)} ↗</a>' for t,u in data)
def demo(kind):
 if kind=='timer':return '''<div class="demo" data-timer><div class="demo-head"><span>DEFENSA 7 MIN + PREGUNTAS 3 MIN · INICIO MANUAL</span></div><output class="timer-value" aria-live="off">07:00</output><div class="timer-controls"><button data-timer-start>Iniciar / pausar</button><button data-timer-reset>Reiniciar</button><button data-timer-questions>Preguntas · 3 min</button></div></div>'''
 raise ValueError(kind)
def body(s):
 if s['kind']=='raw':return s['html']+s.get('extra','')
 return body0(s)+s.get('extra','')
def body0(s):
 kind=s['kind'];items=s['items']
 if kind=='code':
  return '<div class="code-lesson"><div>'+''.join(f'<p data-step="{i}"><b>{esc(p["label"])}</b><br>{esc(p["text"])}</p>' for i,p in enumerate(items))+'</div><div class="code-panel"><span>FRAGMENTO DOCENTE · ARCHIVO COMPLETO EN LA GUÍA</span><pre tabindex="0"><code id="code-'+s['id']+'">'+esc(s['code'])+'</code></pre><button data-copy="code-'+s['id']+'">Copiar código</button><span class="copy-status" role="status"></span></div></div>'
 if kind=='timer':
  return '<p class="interaction-intro">'+esc(items[0]['text'])+'</p>'+demo(kind)+f'<p class="takeaway" data-step="1"><strong>{esc(items[1]["label"])}:</strong> {esc(items[1]["text"])}</p>'
 if kind=='pause':return '<div class="pause-number">10<span>MINUTOS</span></div>'+''.join(f'<p class="lead" data-step="{i}">{esc(x["text"])}</p>' for i,x in enumerate(items))
 if kind=='cover':return '<p class="lead">'+esc(items[0]['text'])+'</p><div class="session-number" aria-hidden="true">'+s['id'][1:3]+'</div><p class="takeaway" data-step="1"><strong>'+esc(items[1]['label'])+':</strong> '+esc(items[1]['text'])+'</p>'
 raise ValueError(kind)
def shell(title,inner,n):
 return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Especialidad, sesión {n}: {esc(title)}"><title>{esc(title)} · Especialidad</title><link rel="stylesheet" href="../compartido/curso.css"><script src="../compartido/deck.js" defer></script></head><body data-session="{n}"><header><a class="brand" href="../"><span class="mark" aria-hidden="true">∴</span> Big Data <span class="edition">ESPECIALIDAD / {n:02d}</span></a><nav aria-label="Herramientas"><button id="index-button">Índice <kbd>O</kbd></button><button id="lab-button">Guía de laboratorio</button><button id="fullscreen" aria-label="Pantalla completa">⛶</button></nav></header><main id="stage" aria-label="Presentación; clic en espacio libre para avanzar">{inner}</main><footer><div><span id="counter" class="counter"></span><span id="step-counter" class="step-counter" aria-live="polite"></span></div><div class="footer-middle"><span id="section-label"></span><small>Clic o → revela · ← retrocede</small></div><div class="controls"><button id="show-all">Mostrar todo</button><button id="notes-button">Notas</button><button id="previous" aria-label="Paso anterior">←</button><button id="next" aria-label="Paso siguiente">→</button></div></footer><div class="progress" aria-hidden="true"><div id="progress"></div></div><dialog id="overview"><div class="dialog-heading"><h2>Ruta de la sesión {n}</h2><button data-close>Cerrar ×</button></div><ol id="slide-list"></ol><button id="print-button">Imprimir todas las slides</button></dialog><dialog id="notes"><div class="dialog-heading"><h2>Notas de facilitación</h2><button data-close>Cerrar ×</button></div><p id="notes-text"></p></dialog><dialog id="lab"><div class="dialog-heading"><h2>Laboratorio / taller</h2><button data-close>Cerrar ×</button></div><p>Abre las instrucciones sin perder tu lugar.</p><a href="laboratorio.html" target="_blank" rel="noopener">Guía completa y recursos ↗</a></dialog><noscript>Activa JavaScript para las interacciones. El contenido y la guía permanecen legibles.</noscript></body></html>'''
def phase(i):
 return 'COMITÉ · '+('ENCUADRE' if i<=8 else 'DEFENSAS / AUDITORÍA / CIERRE')
def render(data,path):
 n=data['session'];ss=[]
 for i,s in enumerate(data['slides'] if n==8 else [],1):
  resource=''
  paso=s.get('paso')
  if paso:resource='<p class="source"><a href="laboratorio.html#paso-'+str(paso)+'" target="_blank" rel="noopener">Instrucciones, código completo, comprobación y recuperación ↗</a></p>'
  if s.get('sources'):resource='<p class="source">'+links(s['sources'])+'</p>'
  ss.append(f'<section class="slide kind-{s["kind"]}" data-id="{s["id"]}" data-title="{esc(s["title"])}" data-note="{esc(s["note"])}"><div class="eyebrow">SESIÓN {n:02d} / {s.get('phase') or phase(i)}<span>ESPECIALIDAD · H{n}</span></div><h1>{esc(s["title"])}</h1>{body(s)}{resource}</section>')
 if n >= 8:
  (path/'index.html').write_text(shell(data['title'],'\n'.join(ss),n).replace('</head>','<link rel="stylesheet" href="estilos.css"></head>',1))
 assets='<ul>'+''.join(f'<li><a href="../recursos/{esc(a)}" download>{esc(a)} ↓</a></li>' for a in data['assets'])+'</ul>'
 steps=''
 for step in data['lab']['steps']:
  h=f'<section id="paso-{step["n"]}"><h2>Paso {step["n"]} · {esc(step["titulo"]) if step.get("titulo") else ""}{" · " if step.get("titulo") else ""}{step["minutes"]} min</h2>'
  if step.get('donde'):h+=f'<p><strong>Dónde:</strong> {esc(step["donde"])}</p>'
  h+=f'<p><strong>Acción:</strong> {esc(step["action"])}</p>'
  if step.get('costo'):h+=f'<p><strong>Costo estimado:</strong> {esc(step["costo"])}</p>'
  if step.get('codigo'):h+='<pre><code>'+esc(step['codigo'])+'</code></pre>'
  if step.get('salida'):h+='<p><strong>Salida esperada:</strong></p><pre class="expected"><code>'+esc(step['salida'])+'</code></pre>'
  h+=f'<p><strong>Comprueba:</strong> {esc(step["check"])}</p>'
  if step.get('error'):h+=f'<p><strong>Error frecuente y recuperación:</strong> {esc(step["error"])}</p>'
  steps+=h+'</section>'
 codeblocks=''
 for a in data['assets']:
  if a.endswith(('.sql','.txt','.py')):
   codeblocks+=f'<details><summary>{esc(a)} · ver contenido completo</summary><pre><code>{esc((ROOT/"recursos"/a).read_text())}</code></pre></details>'
 journal_html=f'''<section id="proyecto"><h2>Transferencia al proyecto propio · {'auditoría' if n==8 else '30 minutos'}</h2><p>{esc(data['lab'].get('transferencia') or 'Repite en tu dataset propio (distinto al de otros equipos) lo que hiciste hoy con los tweets: mismo método, tus datos. Conserva grano, reglas, fuente, KPI y límites de tu dominio. El caso de tweets es el ejemplo guiado, no tu proyecto. Antes de aplicar un esquema o una consulta a tu archivo, revísalo con el docente: no asumas que sus columnas, fechas o idiomas se comportan igual.')}</p><form id="journal-form"><label>Dataset y equipo<input name="dataset" maxlength="200" required></label><label>Evidencia del hito H{n}<textarea name="evidence" rows="3" maxlength="2000" required></textarea></label><label>Qué ejecuté / qué preparó el docente / qué falta<textarea name="limits" rows="3" maxlength="1500"></textarea></label><button type="submit">Descargar registro H{n} ↓</button><span id="journal-status" role="status"></span></form><p class="micro">Solo este navegador. La ficha no asigna fuentes ni envía una entrega. No escribir credenciales. Si localStorage falla, descargar el archivo.</p><a href="entregable.md" download>Plantilla del entregable ↓</a></section>'''
 journal=journal_html if n==8 else ''
 cloudtext='<p><strong>Región y permisos:</strong> '+esc(data['lab']['region'])+'</p>'
 closing='<section><h2>Entrega, costo y cierre</h2>'+''.join(f'<p>{esc(x)}</p>' for x in data['lab']['cierre'])+'</section>'
 prereq='<h2>Antes de empezar</h2><ul>'+''.join(f'<li>{esc(x)}</li>' for x in data['lab']['prerequisitos'])+'</ul>'
 journal_js='<script src="../compartido/journal.js" defer></script>' if n==8 else ''
 htmlguide=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Guía S{n} · {esc(data['title'])}</title><link rel="stylesheet" href="../compartido/curso.css">{journal_js}</head><body data-session="{n}"><article class="guide"><a href="index.html">← Volver al deck</a><p class="eyebrow">ESPECIALIDAD / S{n} · 180 MINUTOS</p><h1>{esc(data['title'])}</h1><p class="notice">{esc(data['lab']['aviso'])}</p>{prereq}<h2>Preparación, herramientas y ruta exacta</h2><p>{esc(data['lab']['instructions'])}</p><h2>Recursos completos descargables</h2>{assets}{cloudtext}{steps}<h2>Código completo y materiales</h2>{codeblocks}{journal}{closing}<h2>Fuentes</h2><p>{links(data['sources'])}</p><p>Los casos reportan experiencias de sus publicadores; no garantizan el resultado del curso. Imprimir la guía con el navegador; el deck imprime todos los revelados desde su índice.</p><p><a href="notas.md">Notas de la sesión</a> · <a href="../">Índice de sesiones</a></p></article></body></html>'''
 (path/'laboratorio.html').write_text(htmlguide)
 if n >= 8:
  (path/'notas.md').write_text('# Notas de la sesión · '+data['title']+'\n\nEnsayar accesos y código por motor antes de clase. Solo Especialidad: sin entrenamiento de ML. Guía de 55 min + transferencia de 30 min (excepto S8 comité).\n\n'+'\n\n'.join('## '+s['id']+' · '+s['title']+'\n\n'+s['note'] for s in data['slides'])+'\n\n## Fuentes\n\n'+'\n'.join('- ['+t+']('+u+')' for t,u in data['sources'])+'\n')
 if n==8:(path/'entregable.md').write_text(f'# H{n} · {data["title"]}\n\nEquipo y dataset propio:\nPregunta / audiencia:\nFuente y versión:\nGrano / periodo:\nConsulta o acción ejecutada:\nResultado y control:\nRegla / fórmula / denominador:\nEvidencia adjunta:\nQué preparó el docente:\nQué ejecutó el equipo:\nQué queda pendiente:\nCosto/bytes/servicio observado:\nAccesos y cierre:\nUna limitación y una mejora:\n\nNo entregar credenciales ni crudos sensibles. Las cifras del modelo (tweets de marzo de 2022, uso académico) son del ejemplo guiado y no sustituyen el proyecto con dataset propio. No hay modelo predictivo obligatorio.\n')
 if n >= 8:
  (path/'README.md').write_text(f'# Especialidad · S{n}: {data["title"]}\n\n{len(data["slides"])} slides y guía de laboratorio/taller. Abrir desde servidor sobre presentaciones-v2: /especialidad-{n:02d}/.\n\nFuente única: contenido.json. Regenerar HTML/guía/notas desde la raíz con `python3 presentaciones-v2/scripts/build.py`. No editar a mano el HTML generado. S1–S7 se generan con build-editorial.py.\n\nEl laboratorio usa recursos completos de ../recursos. Las cifras del modelo vienen de tweets de marzo de 2022 (uso académico), calculadas el 2026-11-19 en BigQuery; no son una muestra representativa. Las guías cloud no se han ensayado end-to-end en una cuenta de alumno. El docente debe perfilar/adaptar cada paquete real distinto por equipo. No se exige ML técnico.\n\nVer README de la carpeta padre para navegación, límites y validación.\n')
import sys
_only=[int(x) for x in sys.argv[1:]]
for n in range(2,9):
 if _only and n not in _only:continue
 p=ROOT/f'especialidad-{n:02d}';render(json.loads((p/'contenido.json').read_text()),p)
print('Generadas guías S2–S8 y decks S8. Ejecutar build-editorial.py después para notas y README S1–S7.')
