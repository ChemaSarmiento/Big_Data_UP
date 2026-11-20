"""Ayudantes compartidos del editor de slides (S1–S7). El contenido vive en editorial/sNN.py.
Generar con python3 presentaciones-v2/scripts/build-editorial.py [N]."""
from html import escape as e

def step(n,html):return f'<div data-step="{n}">{html}</div>'
def p(t,cls=''):return f'<p class="{cls}">{t}</p>'
def code(t):return '<pre tabindex="0"><code>'+e(t)+'</code></pre>'
def table(headers,rows,caption=''):
 return '<table class="matrix">'+(f'<caption>{caption}</caption>' if caption else '')+'<thead><tr>'+''.join('<th scope="col">'+x+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in r)+'</tr>' for r in rows)+'</tbody></table>'
def flow(items):
 return '<div class="flow">'+''.join((f'<span class="arrow" data-step="{i}" aria-hidden="true">→</span>' if i else '')+f'<div class="node" data-step="{i}">{a}<small>{b}</small></div>' for i,(a,b) in enumerate(items))+'</div>'
def lablink(n):return f'<a class="lab-link" href="laboratorio.html#paso-{n}" target="_blank" rel="noopener">Abrir instrucciones y recuperación ↗</a>'
def proof(t):return '<div class="lab-proof"><strong>Comprueba</strong><span>'+t+'</span></div>'
def slide(title,body,note,layout='plain',phase='Comprender',source='Elaboración docente · Especialidad'):
 return dict(title=title,body=body,note=note,layout=layout,phase=phase,source=source)
def source(label,url):return f'<a href="{url}" target="_blank" rel="noopener">{label} ↗</a>'
MELI=source('Mercado Libre / Google Cloud · 2022','https://cloud.google.com/blog/products/data-analytics/improving-retail-using-bigquery-and-looker')
HSBC=source('HSBC / Google Cloud · Risk Advisory Tool','https://cloud.google.com/customers/hsbc-risk-advisory-tool')
MAYO=source('Mayo Clinic / Google Cloud · 2020','https://cloud.google.com/blog/products/data-analytics/genome-data-analytics-with-google-cloud')
UPS=source('UPS Capital / Google Cloud · 2024','https://cloud.google.com/blog/products/data-analytics/ups-leverages-bigquery-and-striim-for-ai-secured-package-delivery')
