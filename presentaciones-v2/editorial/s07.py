"""S7 · IA generativa con evidencia. Fuente única del deck; generar con scripts/build-editorial.py 7.
Cifras: presentaciones-v2/recursos/tweets/verdad.json y consultas de solo lectura sobre las tablas de referencia del curso."""
import sys,re
from html import escape as E
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from guion import slide,p,step,table,flow,code,proof,lablink,source

TITLE='La frase suena lista. La evidencia todavía no'
BIGIDEA='Un modelo solo responde con el contexto que recibe: tú decides cuál es y compruebas cada afirmación contra los datos.'
REC=Path(__file__).resolve().parents[1]/'recursos'/'tweets'
RAG=source('Google Cloud · recuperación y generación','https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview')
STUDIO=source('Google Cloud · prompts en Studio','https://docs.cloud.google.com/gemini-enterprise-agent-platform/agent-studio/quickstart')
PROMPT=source('Google Cloud · diseño de prompts','https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design')
PRICE=source('Google Cloud · precios de IA generativa (consulta la tarifa vigente)','https://cloud.google.com/vertex-ai/generative-ai/pricing')
DATA='Tweets de marzo de 2022 · tablas tweets_silver y tweets_gold · 12 días, no representativo'
DOC='Ejemplo redactado a mano · no es la salida de un modelo'

# ── los cinco tweets del contexto: energía, inglés, 23 de marzo de 2022, ordenados por likes ──
TOP=[
 (46186,'https://twitter.com/richimedhurst/status/1506642880919740416','Explosive. Russia is now demanding that Europe pay for gas in rubles. Europe gets 40% of its gas from Russia. That’s 200-800 million euros per day. Putin is basically saying: you want to play sanctions? Either pay up in rubles…'),
 (21483,'https://twitter.com/KyivIndependent/status/1506756373601730565','⚡The International Atomic Energy Agency reported that it was informed by Ukraine that a forest near Chornobyl Nuclear Power Plant was on fire.'),
 (18861,'https://twitter.com/KyivIndependent/status/1506623757447749640','⚡ Putin: Russia will only accept rubles for gas deliveries to EU. Vladimir Putin said that “unfriendly countries” must pay for Russian energy in rubles & ordered the changes to be implemented within a week.'),
 (16599,'https://twitter.com/spectatorindex/status/1506612829985869825','BREAKING: Putin says Russia will demand payment in ruble for natural gas purchases from \'unfriendly countries\''),
 (15710,'https://twitter.com/mchooyah/status/1506675225823485957','If you honestly think that high gas prices are because of Putin, you should put your mask back on and lock yourself in your house again. Turn off the lights too.'),
]
def short(t,n=120):return t if len(t)<=n else t[:n].rstrip()+'…'
CTX5='\n'.join(f'[{i}] ({l} likes) {u} {t}' for i,(l,u,t) in enumerate(TOP,1))

# ── contexto con tablas Gold: salida real del paso 2 (23 de marzo; tema en inglés) ──
GOLD=[
 ('T1','tweets_gold.tema_dia · 2022-03-23 · inglés · base 311363 tweets: energia 10530 (3.382 %); sanciones 6085 (1.954 %); alimentos 3600 (1.156 %); mercados 2011 (0.646 %); cadena_suministro 573 (0.184 %); aviacion 398 (0.128 %)'),
 ('T2','tweets_gold.hashtags_dia · 2022-03-23 · cinco hashtags con más tweets: #ukraine 49393 (8.711 %); #putin 14294 (2.521 %); #russia 13333 (2.351 %); #ucrania 5384 (0.950 %); #standwithukraine 4552 (0.803 %)'),
 ('T3','tweets_gold.autores_alcance · todo el archivo · segmento de seguidores: 1 · menos de 1 mil → 67.02 % de los tweets y 8.72 % de los likes; 2 · 1 mil a 10 mil → 23.41 % de los tweets y 12.62 % de los likes; 3 · 10 mil a 100 mil → 6.59 % de los tweets y 25.07 % de los likes; 4 · 100 mil a 1 millón → 2.15 % de los tweets y 35.93 % de los likes; 5 · más de 1 millón → 0.84 % de los tweets y 17.66 % de los likes'),
 ('T4','tweets_gold.conversacion_dia · 2022-03-23 · tipo de tweet: respuesta 271613 tweets, mediana 0 likes; original 241363 tweets, mediana 0 likes; cita 54047 tweets, mediana 0 likes'),
 ('T5','tweets_gold.aplicaciones_dia · 2022-03-23 · tres aplicaciones con más tweets: Twitter Web App 190856; Twitter for Android 171340; Twitter for iPhone 119482'),
 ('T6','tweets_gold.actividad_hora · 2022-03-23 · tres horas UTC con más tweets: 18:00 → 33700; 14:00 → 32958; 15:00 → 32667'),
]
CTXG='\n'.join(f'[{k}] {v}' for k,v in GOLD)
TOK5=round(len(CTX5)/4,-1); TOKG=round(len(CTXG)/4,-1); TOKALL=297000000
def tw(n,likes,text,url,cls=''):
 return f'<div class="s7-tw {cls}"><span class="n">[{n}]</span><div><p>{E(text)}</p><small>{E(url)}</small></div><span class="lk">{likes:,} likes</span></div>'
def tws(rows,cls=None):return '<div class="s7-tws">'+''.join(tw(i,l,t,u,(cls or {}).get(i,'')) for i,(l,u,t) in enumerate(rows,1))+'</div>'
def rs(headers,rows,hi=()):
 return '<table class="s7-rs"><thead><tr>'+''.join(f'<th class="{c}">{h}</th>' for h,c in headers)+'</tr></thead><tbody>'+''.join(f'<tr class="{"hi" if i in hi else ""}">'+''.join(f'<td class="{c}">{v}</td>' for v,(h,c) in zip(r,headers))+'</tr>' for i,r in enumerate(rows))+'</tbody></table>'
def qpanel(sql,result_html,bytes_txt,title='Consulta'):
 return f'<div class="s7-qp"><div class="bar"><span><b>{title}</b></span><span>{bytes_txt}</span></div>{code(sql)}{result_html}</div>'
def defs(i):return f'<defs><marker id="a7{i}" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0L9 4L0 8"/></marker></defs>'
def arrow(i,x1,y,x2,step_=None):
 s=f' data-step="{step_}"' if step_ is not None else ''
 return f'<g{s}><path class="l" d="M{x1} {y}H{x2}" marker-end="url(#a7{i})"/></g>'
def varrow(i,x,y1,y2,step_=None):
 s=f' data-step="{step_}"' if step_ is not None else ''
 return f'<g{s}><path class="l" d="M{x} {y1}V{y2}" marker-end="url(#a7{i})"/></g>'
def box(x,y,w,h,title,sub='',cls='',step_=None,tcls='b'):
 s=f' data-step="{step_}"' if step_ is not None else ''
 t=f'<text class="{tcls}" x="{x+18}" y="{y+38}">{title}</text>'
 u=''.join(f'<text class="s" x="{x+18}" y="{y+72+28*k}">{l}</text>' for k,l in enumerate(sub.split('|'))) if sub else ''
 return f'<g class="{cls}"{s}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>{t}{u}</g>'

S=[]
def add(title,body,note,layout='dense',phase='Comprender · 15–50 min',src=DATA):S.append(slide(title,body,note,layout,phase,src))

# ═══════════ ABRIR · 0–15 ═══════════
add('La frase suena lista. La evidencia todavía no.',
 '<div><p class="overline">IA generativa con evidencia · Sesión 07</p><h1>La frase suena lista.<br>La evidencia todavía no.</h1><p class="lede">Hoy aprendes a pedirle un texto a un modelo<br>y a comprobar cada afirmación.</p></div>'
 '<div class="stack"><p class="large signal">137,598</p><p>tweets mencionan energía en 12 días de marzo de 2022</p><p class="caption">De 6,798,932 tweets observados.<br>¿Qué escribirías en un memo con ese solo número?</p></div>',
 '0–4 min. Abre con la pregunta, no con la herramienta: si un modelo te entrega un memo en diez segundos, ¿qué le exigirías antes de firmarlo? [pausa 3 s] Escucha dos respuestas. El número 137,598 sale de la tabla tweets_gold.tema_dia (suma del tema energía en los tres grupos de idioma, del 16 al 27 de marzo de 2022) y cuenta tweets con palabras clave, no personas ni opinión. Hoy no se entrena ningún modelo: se aprende a darle contexto y a auditar lo que escribe.',
 'cover dark','Abrir · 0–15 min',DATA)
add('Dos memos con la misma pregunta: solo uno se puede comprobar.',
 '<div class="s7-memos"><div class="s7-memo weak"><h2>Memo A · sin evidencia</h2><p>La energía <mark class="hl7">dominó la conversación porque las sanciones la dispararon</mark>. Es seguro que <mark class="hl7">los consumidores europeos reaccionarán pronto</mark>.</p>'
 +step(1,'<div class="s7-flags"><span class="s7-flag">¿qué cifra?</span><span class="s7-flag">¿quién lo dijo?</span><span class="s7-flag">causa sin prueba</span></div>')+'</div>'
 '<div class="s7-memo good" data-step="2"><h2>Memo B · con evidencia</h2><p>El 23 de marzo, <mark class="ok7">3.38 % de los tweets en inglés (10,530 de 311,363) mencionó energía</mark> [T1]. <mark class="ok7">El tweet con más likes del día sobre el tema anuncia que Rusia pedirá pagos de gas en rublos</mark> [1]. <mark class="ok7">Los datos no explican la causa del aumento.</mark></p>'
 +step(3,'<div class="s7-flags"><span class="s7-flag ok">cifra → tabla</span><span class="s7-flag ok">ejemplo → URL</span><span class="s7-flag ok">límite dicho</span></div>')+'</div></div>',
 '4–8 min. Memos redactados a mano para esta clase, no salida de un modelo. Lee A en voz alta y pide que marquen lo que no pueden comprobar. Revela las banderas: no hay cifra, no hay fuente, la causa se afirma sin prueba. Revela B: cada frase remite a algo que puedes abrir. Las cifras de B son reales: 10,530 y 311,363 salen de la tabla tema_dia y [1] es un tweet con URL. Idea del día: un texto fluido no es un texto verdadero; lo que lo vuelve útil es poder volver a su evidencia.',
 'dense','Abrir · 0–15 min',DOC)
add('El ciclo de hoy: recuperar, armar, generar, auditar.',
 flow([('1 · Recuperar','Una consulta SQL'),('2 · Armar contexto','Texto numerado'),('3 · Generar','El modelo redacta'),('4 · Auditar','Cada cifra a su tabla')])
 +step(4,p('El modelo escribe. La evidencia decide.','callout')),
 '8–12 min. Dibuja el ciclo con un clic por paso. 1: una consulta decide qué datos entran; ya sabes escribirlas. 2: se arma un texto numerado con etiquetas, para poder citar. 3: el modelo redacta usando solo ese texto. 4: cada afirmación se compara con la tabla o el tweet citado. Este patrón se llama RAG (recuperación y generación) y lo definimos con calma más adelante. Lo importante ahora: el modelo está en el paso 3 de 4; los pasos 1, 2 y 4 son tuyos.',
 'path','Abrir · 0–15 min',RAG)

# ═══════════ COMPRENDER · 15–50 ═══════════
def ml_diagram():
 return ('<svg class="s7svg s7-wide" viewBox="0 0 1360 440" role="img" aria-label="Regla escrita a mano frente a modelo que aprende de ejemplos">'+defs('m')
  +'<text class="t" x="0" y="34">Regla escrita a mano</text>'
  +box(0,60,270,110,'Un tweet','',step_=0)+arrow('m',275,115,350,0)
  +box(355,60,440,110,'¿Contiene oil, gas, fuel…?','Palabras que alguien escribió','hot',0)+arrow('m',800,115,875,0)
  +box(880,60,300,110,'Sí → energía','No → otro tema','',0)
  +'<text class="t" x="0" y="262">Modelo que aprende de ejemplos</text>'
  +box(0,288,270,130,'Miles de tweets','con su tema ya marcado','',1)+arrow('m',275,353,350,1)
  +box(355,288,440,130,'Entrenamiento','Busca patrones|que separan los temas','ok',1)+arrow('m',800,353,875,1)
  +box(880,288,400,130,'Modelo','Predice el tema|de un tweet nuevo','ok',1)
  +'</svg>')
add('Machine learning aprende patrones de ejemplos; una regla la escribe alguien.',
 ml_diagram()+step(2,p('Gold clasificó los tweets con una regla de palabras. Hoy no entrenamos nada: solo distinguimos las dos ideas.','callout')),
 '15–20 min. Machine learning, en una frase: un programa que ajusta su comportamiento a partir de ejemplos en lugar de seguir reglas escritas una por una. Arriba, la regla que usó la capa Gold para asignar temas: si el tweet contiene una palabra de la lista, cuenta para el tema. Abajo, la idea de aprendizaje: se le muestran miles de tweets con su tema marcado y el modelo ajusta lo que necesita para predecir el tema de uno nuevo. Ninguno de los dos entiende lo que dice el tweet; uno sigue una lista y el otro un patrón estadístico. No hay código, métricas ni entrenamiento en este curso.',
 'path','Comprender · 15–50 min',DATA)
add('Una regla de palabras clave acierta, se equivoca y se pierde temas.',
 tws([(46186,'https://twitter.com/richimedhurst/status/1506642880919740416','Russia is now demanding that Europe pay for gas in rubles. Europe gets 40% of its gas from Russia…'),
      (93,'https://twitter.com/markito0171/status/1506629151649939464','#NATO allies set to agree \'additional support\' to Ukraine against nuclear, chemical threats means: Gas Masks ?!'),
      (463,'https://twitter.com/anders_aslund/status/1506699631559856131','The Ukraine war is really degrading Merkel\'s rule… she supported Nord Stream 2 &…')],
      {1:'ok',2:'bad',3:'miss'})
 +step(1,'<p><span class="s7-tag ok">ACIERTO</span><span class="s7-tag bad">FALSO POSITIVO</span><span class="s7-tag miss">SE ESCAPA</span> Palabras clave de energía: oil, gas, fuel, petrol, energy.</p>'),
 '20–24 min. Tres tweets reales del 23 de marzo, en inglés. [1] contiene «gas» y trata de energía: acierto. [2] contiene «gas» pero habla de máscaras antigás: la regla lo cuenta como energía y no lo es. [3] habla de Nord Stream 2, un gasoducto, pero no contiene ninguna palabra de la lista: la regla no lo ve. Por eso las cifras de tema de Gold son un conteo de palabras, no una medición del tema; en una lectura manual de 30 tweets hubo 17 aciertos, 5 dudosos y 8 falsos positivos (muestra pequeña: cinco por tema, un día, una persona). Un modelo de aprendizaje podría equivocarse menos, pero también se equivoca: la diferencia es que se equivoca de forma menos predecible.',
 'dense','Comprender · 15–50 min',DATA)
def lm_diagram():
 return ('<svg class="s7svg s7-wide" viewBox="0 0 1360 420" role="img" aria-label="Un modelo de lenguaje elige la siguiente palabra más plausible">'+defs('l')
  +box(0,30,640,110,'Texto de entrada','Rusia exigirá pagar el gas en…','',0)+arrow('l',645,85,740,0)
  +box(745,30,250,110,'Modelo','','ok',0)+varrow('l',870,145,200,1)
  +'<g data-step="1"><text class="t" x="745" y="236">Siguientes palabras posibles</text>'
  +'<text class="q" x="745" y="282">rublos</text><rect class="fill-brand" x="900" y="262" width="420" height="26"/>'
  +'<text class="q" x="745" y="328">euros</text><rect class="fill-muted" x="900" y="308" width="200" height="26"/>'
  +'<text class="q" x="745" y="374">dólares</text><rect class="fill-muted" x="900" y="354" width="90" height="26"/></g>'
  +'<g data-step="2"><text class="s" x="0" y="236">Ilustración sin cifras reales: el modelo asigna</text><text class="s" x="0" y="266">una probabilidad a cada continuación y elige una.</text>'
  +'<text class="t" x="0" y="330">Plausible no significa verdadero.</text></g>'
  +'</svg>')
add('Un modelo de lenguaje continúa el texto con la palabra más plausible.',
 lm_diagram(),
 '24–28 min. Un modelo de lenguaje (LLM) se entrena con enormes cantidades de texto para predecir qué viene después. Funciona por piezas llamadas tokens (fragmentos de palabras). Dado un texto de entrada, calcula qué tan plausible es cada continuación y escribe una, y luego otra, y así hasta terminar. La gráfica es una ilustración, no una medición de un modelo real. La idea que te llevas: plausible no es lo mismo que verdadero. Un modelo puede escribir con total seguridad una cifra que nadie midió, porque «suena» como las cifras que ha visto.',
 'path','Comprender · 15–50 min',PROMPT)
def tok_diagram():
 import math
 rows=[('Cinco tweets de contexto',TOK5,'brand'),('Seis líneas de tablas Gold',TOKG,'teal'),('Los 6.8 M de tweets',TOKALL,'signal')]
 out='<svg class="s7svg s7-wide" viewBox="0 0 1360 430" role="img" aria-label="Tamaño aproximado en tokens de tres contextos, en escala logarítmica">'+'<text class="s" x="440" y="20">Tokens aproximados</text>'
 for i,(lab,v,c) in enumerate(rows):
  y=40+i*110;w=int(math.log10(v)/9*620)
  out+=f'<g data-step="{i}"><text class="b" x="0" y="{y+30}">{lab}</text><rect class="fill-{c}" x="440" y="{y}" width="{w}" height="46"/><text class="b" x="{450+w}" y="{y+34}">≈ {v:,.0f}</text></g>'
 out+='<line class="axis" x1="440" y1="360" x2="1060" y2="360"/>'+''.join(f'<text class="s" x="{440+int(k/9*620)-8}" y="392">10<tspan font-size="16" dy="-8">{k}</tspan></text>' for k in (1,3,5,7,9))
 out+='</svg>'
 return out
add('Un modelo lee tokens: cinco tweets caben; seis millones no.',
 tok_diagram()+step(2,p('Estimación: 1 token ≈ 4 caracteres. Escala logarítmica: cada marca multiplica por cien. Por eso se recupera antes de generar.','callout')),
 f'28–32 min. Un token es un fragmento de texto, más o menos cuatro caracteres. La ventana de contexto es el máximo de tokens que el modelo puede leer en una sola petición, y cada token leído o escrito se cobra. Cálculo de esta clase: los cinco tweets del contexto con su URL suman unos {len(CTX5):,} caracteres, alrededor de {TOK5:,.0f} tokens; las seis líneas de Gold, {len(CTXG):,} caracteres, alrededor de {TOKG:,.0f}; el texto de los 6,798,932 tweets suma 1,187,779,540 caracteres, cerca de 297 millones. Las cifras son estimaciones con la regla de cuatro caracteres. Conclusión: no puedes pegar todo; tienes que recuperar un corte pequeño y relevante.',
 'dense','Comprender · 15–50 min',DATA)
def know_diagram():
 return ('<svg class="s7svg s7-wide" viewBox="0 0 1360 440" role="img" aria-label="El modelo recibe conocimiento de su entrenamiento y contexto del prompt">'+defs('k')
  +box(0,30,560,150,'Entrenamiento (antes)','Texto general hasta una fecha de corte|No incluye tus tablas ni tus archivos','',0)+arrow('k',565,105,700,0)
  +box(0,260,560,150,'Contexto (ahora)','Lo que pegas en el prompt|Es lo único tuyo que el modelo puede leer','hot',1)+arrow('k',565,335,700,1)
  +box(705,125,300,200,'Modelo','','ok',0)+arrow('k',1010,225,1110,0)
  +box(1115,160,245,130,'Respuesta','','',0)
  +'</svg>')
add('Lo tuyo solo existe para el modelo si lo pones en el contexto.',
 know_diagram()+step(2,p('Si un dato no está en ninguno de los dos, el modelo lo inventa o lo calla.','callout')),
 '32–35 min. El modelo recibe conocimiento por dos vías. Entrenamiento: lo que aprendió antes de una fecha de corte, general y sin tus datos. Contexto: lo que tú le entregas en esa petición. Tus tablas, tus tweets y las cifras de hoy no están en el entrenamiento; solo existen si las pones en el contexto. Este punto parece obvio, y justo por eso se olvida. Enseguida lo vemos con un ejemplo muy pequeño.',
 'path','Comprender · 15–50 min',DATA)
add('Con cinco tweets en el contexto, el modelo solo puede hablar de esos cinco.',
 '<div class="s7-trio"><div class="ok"><span class="s7-tag ok">SE PUEDE</span><p><b>¿Qué anunció Putin sobre el pago del gas?</b></p><p>Respuesta posible: pide pagos en rublos a los «países poco amistosos» [3][4].</p></div>'
 '<div class="bad"><span class="s7-tag bad">NO SE PUEDE</span><p><b>¿Cuántos tweets hablaron de energía ese día?</b></p><p>El contexto tiene cinco: la única respuesta válida es «No hay evidencia en el contexto».</p></div>'
 '<div><span class="s7-tag">LO OBVIO</span><p>Este ejemplo no prueba nada sobre el archivo. Muestra que el modelo <b>solo responde con lo que le das</b>.</p><p>Para hablar del conjunto, el contexto debe ser el conjunto resumido: tablas Gold.</p></div></div>'
 +step(1,'<pre class="s7-ctx">'+E(CTX5.replace('https://twitter.com/','…/')[:330])+'…</pre>'),
 '35–40 min. Esta slide existe para decir lo obvio en voz alta: los cinco tweets son un contexto de juguete. Sirven para ver el mecanismo. Pregunta 1: se puede responder porque el tema está en el contexto; la respuesta debe citar [3] y [4]. Pregunta 2: pide un conteo del conjunto, y el contexto solo tiene cinco filas; un modelo bien instruido dice «No hay evidencia en el contexto»; uno mal instruido inventa un número. Nada de lo que diga sobre cinco tweets se generaliza a 6.8 millones. Eso nos obliga a subir de nivel: en vez de tweets sueltos, darle al modelo resúmenes del conjunto, que son exactamente lo que producen las tablas Gold.',
 'dense','Comprender · 15–50 min',DATA)
add('Un prompt ejecutivo tiene cinco partes.',
 '<div class="s7-prompt"><div class="r1"><span class="k">1 · Rol</span><p>Eres analista de inteligencia de mercado. Redactas para un comité que decide qué temas vigilar.</p></div>'
 '<div class="r2"><span class="k">2 · Reglas</span><p>Usa solo el contexto. Cada afirmación termina con su etiqueta [n]. Si no alcanza: «No hay evidencia en el contexto.» No afirmes causas.</p></div>'
 '<div class="r3"><span class="k">3 · Contexto</span><pre>'+E(short(CTX5.replace("https://twitter.com/","…/"),150))+'</pre></div>'
 '<div class="r4"><span class="k">4 · Pregunta</span><p>¿Qué anunció Putin sobre el pago del gas?</p></div>'
 '<div class="r5"><span class="k">5 · Formato</span><p>Máximo 120 palabras, en español, una frase por afirmación.</p></div></div>',
 '40–43 min. Un prompt es el texto que le entregas al modelo. Cinco partes ordenan el trabajo. El rol fija el punto de vista. Las reglas son lo más importante para evidencia: usar solo el contexto, citar con una etiqueta y decir «No hay evidencia» cuando no alcance. El contexto es el material. La pregunta es una sola y concreta. El formato limita la longitud y el idioma. Sin la parte 2, el modelo rellena lo que falta con lo que le suena. Este prompt se escribe en el laboratorio, paso 3.',
 'dense','Comprender · 15–50 min',PROMPT)
add('Un modelo puede fallar de tres maneras aunque escriba bien.',
 table(['Cómo falla','Ejemplo redactado a mano','Cómo lo detectas'],[
  ['Cifra inventada','«El 62 % de los tweets habla de rublos.»','Ninguna etiqueta la respalda: buscas esa cifra en la tabla y no está.'],
  ['Cita falsa','«… según [7].»  (el contexto solo tiene [1] a [5])','La etiqueta no existe o el tweet citado no dice eso.'],
  ['Causa sin prueba','«La energía subió porque Rusia pidió rublos.»','Ninguna tabla trae causas: solo se ve que ambas cosas coinciden.']])
 +step(1,p('Esto se llama alucinación: texto plausible sin respaldo. No se arregla con otro modelo; se arregla con auditoría.','callout')),
 '43–47 min. Una alucinación es un texto fluido y seguro que no tiene respaldo en el contexto ni en los datos. Tres formas típicas, todas con ejemplos redactados a mano para esta clase, no salidas de un modelo real: cifra inventada, cita que no existe y causa afirmada sin prueba. La defensa no es confiar más ni menos en el modelo: es poder comprobar cada afirmación contra una etiqueta. Por eso exigimos etiquetas en el prompt y auditamos al final.',
 'dense','Comprender · 15–50 min',DOC)
add('Un tweet cuenta una anécdota; una tabla Gold cuenta el conjunto.',
 table(['Tabla Gold','Una fila es…','Responde','Filas'],[
  ['tema_dia','un día, un tema y un idioma','¿cuánto pesa cada tema?','216'],
  ['hashtags_dia','un día y un hashtag','¿de qué se habló?','10,636'],
  ['autores_alcance','un segmento de seguidores','¿quién concentra la interacción?','5'],
  ['aplicaciones_dia','un día y una aplicación','¿desde dónde se publica?','108'],
  ['actividad_hora','un día, una hora y un idioma','¿cuándo se publica?','804'],
  ['conversacion_dia','un día y un tipo de tweet','¿respuestas, originales o citas?','36']]),
 '47–50 min. Cada tabla Gold resume millones de tweets en pocas filas y responde una pregunta concreta. Esa es su ventaja como contexto: 216 filas de tema_dia caben en un prompt; los 6.8 millones de tweets no. Las seis tablas salen de la capa Silver, y el grano de cada una dice qué es una fila. Hoy no las construimos; las usamos como material para el modelo y como referencia para auditar lo que escriba.',
 'dense','Comprender · 15–50 min',DATA)

# ═══════════ APLICAR · 50–70 ═══════════
add('Un paquete de contexto con tablas: una línea numerada por tabla.',
 '<pre class="s7-ctx" style="font-size:18px;line-height:1.4">'+'\n'.join(f'<b>[{k}]</b> {E(v)}' for k,v in GOLD)+'</pre>',
 '50–53 min. Esta es la salida real de la consulta del paso 2: seis líneas, una por tabla Gold, cada una con su etiqueta, el nombre de la tabla, el filtro (fecha, idioma) y la base. Fíjate en lo que incluye una línea útil: de dónde viene, qué cubre y contra qué base se mide. Con este paquete el modelo puede responder preguntas sobre el conjunto y citar [T1] a [T6]. Todo el paquete mide unos 330 tokens: cabe sin problema. Las cifras salen sin separador de miles porque así las devuelve la consulta.',
 'dense','Aplicar · 50–70 min',DATA)
add('Con el paquete de tablas se responden preguntas del conjunto, o se admite que no hay respuesta.',
 table(['Pregunta','Respuesta con cita','Límite'],[
  ['¿Qué tema pesó más el 23 de marzo en inglés?','Energía: 10,530 tweets, 3.382 % de 311,363 [T1]','Cuenta palabras clave'],
  ['¿Qué hashtag dominó ese día?','#ukraine: 49,393 tweets, 8.711 % del día [T2]','Un tweet puede llevar varios'],
  ['¿Quién concentra la interacción?','Cuentas de 100 mil o más seguidores: 2.99 % de los tweets y 53.59 % de los likes [T3]','Suma de dos segmentos'],
  ['¿Cuándo se publicó más?','A las 18:00 UTC: 33,700 tweets [T6]','Hora UTC, no local'],
  ['¿Por qué subió la energía?','No hay evidencia en el contexto','Ninguna tabla trae causas']]),
 '53–56 min. Recorre las filas. Las cuatro primeras se contestan con una cita porque el paquete trae la cifra. La tercera combina dos segmentos de T3: 2.15 + 0.84 = 2.99 % de los tweets y 35.93 + 17.66 = 53.59 % de los likes; si el modelo suma, tú puedes comprobarlo. La última pregunta es la importante: el paquete no tiene causas, y la respuesta correcta es admitirlo. Un buen prompt hace que ese «no hay evidencia» sea la salida por defecto.',
 'dense','Aplicar · 50–70 min',DATA)
def alcance_svg():
 segs=[('menos de 1 mil',67.02,8.72),('1 a 10 mil',23.41,12.62),('10 a 100 mil',6.59,25.07),('100 mil a 1 M',2.15,35.93),('más de 1 M',0.84,17.66)]
 out='<svg class="s7svg s7-wide" viewBox="0 0 1360 470" role="img" aria-label="Porcentaje de tweets y de likes por segmento de seguidores del autor">'
 out+='<text class="s" x="330" y="26">Barra azul: % de los tweets · Barra roja: % de los likes</text>'
 for i,(lab,a,b) in enumerate(segs):
  y=50+i*84;st=i if i<3 else 3
  out+=f'<g data-step="{0 if i<3 else 1}"><text class="b" x="0" y="{y+30}">{lab}</text><rect class="fill-brand" x="330" y="{y}" width="{a*13:.0f}" height="30"/><text class="s" x="{340+a*13:.0f}" y="{y+24}">{a:.2f} %</text><rect class="fill-signal" x="330" y="{y+36}" width="{b*13:.0f}" height="30"/><text class="s" x="{340+b*13:.0f}" y="{y+60}">{b:.2f} %</text></g>'
 out+='<line class="axis" x1="330" y1="40" x2="330" y2="460"/></svg>'
 return out
add('Gold esconde historias: 3 % de los tweets reúne 54 % de los likes.',
 alcance_svg()+step(1,p('Autores con 100 mil o más seguidores: 2.99 % de los tweets, 53.59 % de los likes. Y el 78.5 % de los likes cae en tweets originales, que son el 40.2 % de los tweets.','callout')),
 '56–59 min. Una de las seis tablas Gold, vista como gráfica: autores_alcance. Dos tercios de los tweets vienen de cuentas con menos de mil seguidores y reciben menos de 9 % de los likes; las cuentas de más de cien mil seguidores publican menos de 3 % de los tweets y reciben más de la mitad de los likes. Otra tabla, conversacion_dia, dice que 50.2 % de los tweets son respuestas, 40.2 % originales y 9.6 % citas, y que los originales concentran 78.5 % de los likes. Son cifras para poner en el contexto y hacerle al modelo preguntas sobre el conjunto; no explican por qué ocurre.',
 'path','Aplicar · 50–70 min',DATA)
def rag_diagram():
 return ('<svg class="s7svg s7-wide" viewBox="0 0 1360 430" role="img" aria-label="RAG en cuatro pasos con bucle de auditoría">'+defs('r')
  +box(0,110,290,170,'Pregunta','¿Qué tema pesó más?','',0)+arrow('r',295,195,370,1)
  +box(375,110,290,170,'1 · Recuperar','SQL sobre tablas Gold|o sobre tweets','hot',1)+arrow('r',670,195,745,2)
  +box(750,110,290,170,'2 · Armar contexto','Texto con etiquetas|[T1] … [T6]','',2)+arrow('r',1045,195,1120,3)
  +box(1125,110,235,170,'3 · Generar','Prompt con reglas','ok',3)
  +'<g data-step="4"><path class="l" d="M1240 285V380H520V285" marker-end="url(#ar)" style="stroke-dasharray:10 8"/><text class="b" x="560" y="415">4 · Auditar cada afirmación contra la tabla o el tweet citado</text></g>'
  +'</svg>')
add('RAG: recuperar primero, generar después, auditar siempre.',
 rag_diagram()+step(5,p('Pegar un CSV completo en el prompt no es RAG: no hay recuperación, ni etiquetas, ni auditoría.','callout')),
 '59–62 min. RAG significa generación aumentada con recuperación. Paso 1: una consulta recupera solo lo que responde la pregunta. Paso 2: se arma el contexto con etiquetas. Paso 3: el modelo redacta bajo reglas. Paso 4, que cierra el bucle: cada afirmación se compara con su fuente. Pegar un archivo entero y pedir un resumen no es RAG: no filtra, no cita y no se puede auditar. Mismo ciclo que vimos al inicio, ahora con nombre. Las fuentes oficiales describen el mecanismo; los costos y límites dependen de tu cuenta.',
 'path','Aplicar · 50–70 min',RAG)
add('La regla de oro: solo con el contexto, cita la etiqueta, di «no hay evidencia».',
 '<div class="s7-memo good" style="max-width:none"><h2>Respuesta anotada · '+DOC+'</h2><p><mark class="ok7">La energía fue el tema con más presencia en inglés el 23 de marzo: 10,530 tweets, 3.382 % [T1].</mark> <mark class="ok7">El hashtag más usado fue #ukraine, 8.711 % del día [T2].</mark> <mark class="hl7">La energía subió porque Rusia pidió pagos en rublos.</mark> <mark class="ok7">El contexto no incluye causas: no hay evidencia para explicar el aumento.</mark></p></div>'
 +step(1,'<div class="s7-flags"><span class="s7-flag ok">verde: cifra con etiqueta, se comprueba</span><span class="s7-flag">rojo: causa sin etiqueta, se descarta</span></div>'),
 '62–64 min. Respuesta redactada a mano, no producida por un modelo, para practicar la lectura. Verde: afirmaciones con etiqueta y cifra, que se pueden abrir en la tabla. Rojo: «subió porque…» es una causa; ninguna etiqueta la respalda y en el contexto no hay causas. Un buen texto generado deja esa frase fuera, o la convierte en «los datos no explican la causa». Esta lectura —buscar etiqueta, abrir tabla, comprobar cifra— es el método de auditoría del resto de la sesión.',
 'dense','Aplicar · 50–70 min',DOC)
CLAIMS=[
 ('A1','La energía fue el tema con más presencia el 23 de marzo en inglés.','ok','Sustentada','tema_dia · inglés · 23 de marzo','Energía: 10,530 tweets = 3.382 % de 311,363. El siguiente tema, sanciones, tiene 1.954 %.','Con límite: «presencia» significa palabras clave, no importancia.'),
 ('A2','Las sanciones pesaron más en español que en inglés.','bad','Contradicha','tema_dia · sanciones, todo el archivo','Inglés: 67,086 de 4,013,172 = 1.67 %. Español: 9,600 de 1,056,425 = 0.91 %.','El porcentaje en inglés es casi el doble.'),
 ('A3','La mayoría de los likes viene de cuentas con más de un millón de seguidores.','bad','Contradicha','autores_alcance','Más de 1 millón: 17.66 % de los likes. El segmento de 100 mil a 1 millón concentra 35.93 %.','La afirmación nombra solo el segmento de más de 1 millón, y ese no reúne la mayoría.'),
 ('A4','La mitad de los tweets son respuestas.','ok','Sustentada','conversacion_dia · todo el archivo','Respuestas: 3,414,201 de 6,798,932 = 50.2 %.','Es cierto para este archivo; no para Twitter en general.'),
 ('A5','Las sanciones causaron el pico de energía del 23 de marzo.','nd','Sin respaldo','ninguna tabla','Ninguna tabla Gold trae causas. Solo se observa que ambos temas aparecen el mismo día.','Una coincidencia en fechas no es causalidad.'),
 ('A6','A la gente en Europa le preocupó más la energía.','nd','Sin respaldo','autores (ubicación)','No hay país en los datos. El idioma no es el país y 40.5 % de los autores no declara ubicación.','Para decirlo habría que medir país, y no se puede con este archivo.')]
def audit_demo():
 SHORT=['La energía tuvo más presencia','Las sanciones pesaron más en español','La mayoría de los likes: cuentas de más de 1 M','La mitad de los tweets son respuestas','Las sanciones causaron el pico de energía','En Europa preocupó más la energía']
 btn=''.join(f'<button data-claim="{i}" aria-pressed="{"true" if i==0 else "false"}">{c[0]} · {SHORT[i]}</button>' for i,c in enumerate(CLAIMS))
 pan=''.join(f'<div class="s7-verd" data-claim-panel="{i}" data-v="{c[2]}"{"" if i==0 else " hidden"}><p class="caption"><b>Afirmación:</b> «{E(c[1])}»</p><span class="v">{c[3]}</span><p><b>Evidencia:</b> {E(c[5])}</p><p class="caption">Tabla: {E(c[4])}. {E(c[6])}</p></div>' for i,c in enumerate(CLAIMS))
 return f'<div data-demo="audit" class="s7-claims"><div class="s7-claimlist">{btn}</div><div>{pan}</div></div>'
add('Audita: sustentada, contradicha o sin respaldo.',
 audit_demo(),
 '64–66 min. Pulsa cada afirmación antes de revelar el veredicto y pide que el grupo lo adivine. A1 y A4 se sostienen con una tabla. A2 y A3 suenan razonables y los datos las contradicen: 1.67 % frente a 0.91 %, y 17.66 % frente a 35.93 %. A5 y A6 son del tipo más peligroso: ni se confirman ni se niegan, porque el dato no puede decidirlo. Reglas del método: busca la etiqueta, abre la tabla, repite la cifra, y si no hay dato, escribe «sin respaldo». Las seis consultas están en el paso 5.',
 'dense','Aplicar · 50–70 min',DATA)
add('Auditar es repetir la cifra con una consulta pequeña.',
 qpanel('SELECT segmento, pct_tweets, pct_likes\nFROM tweets_gold.autores_alcance\nORDER BY segmento;',
  rs([('segmento',''),('pct_tweets','num'),('pct_likes','num')],[('1 · menos de 1 mil','67.02','8.72'),('2 · 1 mil a 10 mil','23.41','12.62'),('3 · 10 mil a 100 mil','6.59','25.07'),('4 · 100 mil a 1 millón','2.15','35.93'),('5 · más de 1 millón','0.84','17.66')],hi=(3,4)),
  '195 bytes procesados · 5 filas','Afirmación A3')
 +step(1,p('Veredicto: contradicha. Más de 1 millón reúne 17.66 % de los likes; 100 mil a 1 millón, 35.93 %.','callout')),
 '66–68 min. Una afirmación, una consulta, un veredicto. La consulta sobre autores_alcance procesa 195 bytes: auditar sobre Gold es casi gratis, porque la tabla ya está resumida. Compara el costo con lanzar la misma pregunta contra los 6.8 millones de tweets. Y mira cómo una cifra ligeramente distinta cambia la conclusión: la mayor parte de los likes no está en el segmento más grande.',
 'dense','Aplicar · 50–70 min',DATA)
add('Qué puede salir mal con este material.',
 table(['Riesgo','Evidencia en este archivo','Qué haces'],[
  ['Muestra pequeña y sesgada','12 días de marzo de 2022, sin retweets, no representativos','Di el periodo; no hables de «la gente»'],
  ['Día parcial','El 16 de marzo solo tiene horas 20 a 23 UTC: 134,871 tweets','Compara porcentajes, no conteos'],
  ['Texto repetido','30,375 textos repetidos; uno aparece 421 veces, de 416 cuentas','Un tweet no es una voz independiente'],
  ['Palabras clave imprecisas','Lectura manual de 30 tweets: 17 aciertos, 5 dudosos, 8 falsos positivos','Trata los temas como aproximación'],
  ['Idioma no es país','40.5 % de los autores no declara ubicación','No afirmes nada por región']]),
 '68–70 min. Cinco riesgos que el modelo no ve y tú sí. La muestra son 12 días y no incluye retweets. El 16 de marzo es día parcial: comparar su conteo con otros días engaña. Hay textos repetidos copiados por cuentas distintas. Las palabras clave aciertan menos de lo que parece; la lectura manual fue de 30 tweets, una muestra pequeña. Y el idioma no te dice el país. Si el modelo escribe algo que ignore estos límites, es una afirmación sin respaldo, por fluida que suene.',
 'dense','Aplicar · 50–70 min',DATA)

# ═══════════ PAUSA y LABORATORIO ═══════════
add('Pausa. Al volver, arma tu contexto y pruébalo.',
 '<p class="huge">10 min</p><p>Al volver: BigQuery Studio y Vertex AI Studio abiertos en dos pestañas.</p>',
 '70–80 min. Pausa real, sin avance automático. Mientras vuelven, comprueba que cada quien tiene abiertas las dos herramientas y que tiene a la mano las tablas Silver y Gold que construyó en las sesiones anteriores. Si falta alguna tabla, el paso 1 y el 2 muestran la consulta que la usa; sin las tablas el laboratorio no se puede ejecutar completo.',
 'statement dark','Pausa · 70–80 min','Descanso')
add('Laboratorio: de la consulta al texto auditado en seis pasos.',
 table(['Paso','Min','Qué haces','Qué obtienes'],[
  ['1','10','Recuperar 5 tweets con SQL','Cinco filas y un contexto numerado'],
  ['2','12','Armar el contexto con tablas Gold','Seis líneas [T1] a [T6]'],
  ['3','10','Escribir el prompt con reglas','Un prompt de cinco partes'],
  ['4','18','Probar en Vertex AI Studio','Dos pruebas: cinco tweets y tablas'],
  ['5','15','Auditar seis afirmaciones con SQL','Un veredicto por afirmación'],
  ['6','5','Cerrar: qué puedes afirmar','Tu tabla sí / no']])
 +lablink(1),
 '80–150 min. Esta es la única slide de laboratorio: el código, las salidas esperadas y los errores frecuentes están en la guía, paso por paso. Trabajas sobre tus propias tablas. Los pasos 1, 2 y 5 son SQL y se pueden ensayar con el estimador de bytes; el paso 4 usa la interfaz de Vertex AI Studio, cuyo texto de salida cambia en cada ejecución: tu comprobación no es que el texto coincida, sino que cada afirmación tenga su etiqueta y su veredicto.',
 'lab-s7','Laboratorio · 80–150 min',DATA)

# ═══════════ CERRAR · 150–180 ═══════════
add('La cuenta de un modelo se mide en tokens leídos y escritos.',
 table(['Qué entra','Tokens aproximados','Observación'],[
  ['Cinco tweets con su URL',f'≈ {TOK5:,.0f}','Caben de sobra'],
  ['Seis líneas de tablas Gold',f'≈ {TOKG:,.0f}','Resumen de millones de tweets'],
  ['Los 6.8 millones de tweets, solo texto','≈ 297 millones','No cabe; hay que recuperar']])
 +p('Cada petición cobra tokens de entrada y de salida. La tarifa depende del modelo y cambia: consúltala en la página de precios antes de ejecutar muchas pruebas.','callout'),
 '150–155 min. Cierre sobre costo. Un modelo cobra por token leído (el contexto, incluidas las reglas) y por token escrito. Con contextos tan pequeños como los de hoy, cada prueba cuesta muy poco; el riesgo de costo aparece al pegar archivos grandes o al repetir miles de peticiones. Las tarifas dependen del modelo y de tu cuenta y cambian; no hay cifra aquí a propósito. Antes de lanzar muchas pruebas, revisa la página oficial y fija un presupuesto.',
 'dense','Cerrar · 150–180 min',PRICE)
add('Tres ejercicios para practicar lo que viste hoy.',
 table(['Ejercicio','Qué haces','Cómo sabes que quedó bien'],[
  ['1 · Otro corte','Arma el contexto con hashtags_dia del 17 de marzo y pregunta por los tres hashtags principales','Cada cifra del texto aparece en la tabla con su etiqueta'],
  ['2 · Tus afirmaciones','Escribe tres afirmaciones nuevas sobre conversacion_dia: una sustentada, una contradicha, una sin respaldo','Cada una tiene su consulta y su veredicto'],
  ['3 · Cambia el contexto','Repite la pregunta del paso 4 quitando T1 del contexto','El texto debe decir «No hay evidencia en el contexto»']]),
 '155–165 min. Práctica individual con lo aprendido, sin entrega. El ejercicio 3 es el más revelador: sin T1 en el contexto, la pregunta sobre qué tema pesó más ya no tiene respuesta, y un buen prompt lo admite. Si el modelo responde igual con cifras, esas cifras no vienen del contexto: las inventó.',
 'dense','Cerrar · 150–180 min',DATA)
add('Qué puedes afirmar con estos datos, y qué no.',
 table(['Sí puedes afirmar','No puedes afirmar'],[
  ['El 23 de marzo, 3.382 % de los tweets en inglés mencionaba energía, por palabras clave [T1].','Que a «la gente» le preocupó más la energía ese día.'],
  ['El 50.2 % de los tweets de este archivo son respuestas [T4].','Que las respuestas sean más importantes que los originales.'],
  ['Las cuentas de 100 mil o más seguidores reúnen 53.59 % de los likes [T3].','Que esas cuentas «mueven» la opinión.'],
  ['El hashtag #ukraine fue el más usado el 23 de marzo [T2].','Que el hashtag represente a un país o a una postura.']]),
 '165–175 min. Cierre honesto, una sola vez. Cada fila de la izquierda tiene una etiqueta y se comprueba con una consulta. Cada fila de la derecha es un salto que un memo puede dar sin darse cuenta: de palabras clave a «la gente», de conteo a importancia, de coincidencia a influencia. Antes de firmar un texto generado, vuelve a este cuadro.',
 'dense','Cerrar · 150–180 min',DATA)
add('El modelo escribe. La evidencia decide.',
 '<p class="huge">Etiqueta<br>y comprueba.</p><p>Contexto pequeño, reglas claras, cada cifra a su tabla.</p>',
 '175–180 min. Cierra con la idea del día: un modelo es muy bueno escribiendo y no sabe nada de tus datos. Lo que lo vuelve útil es el método: recuperar un corte pequeño, armar un contexto con etiquetas, pedirle que se limite a ese contexto y auditar cada afirmación. Pregunta de salida: ¿qué frase de un texto generado te haría pedir la fuente antes de firmar?',
 'statement dark','Cerrar · 150–180 min','Cierre')

SLIDES=S
