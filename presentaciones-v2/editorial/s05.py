"""S5 · Capa Gold: del tweet al indicador. Fuente única de las slides.
Cifras: recursos/tweets/verdad.json y consultas de solo lectura sobre las tablas de referencia (valores de referencia del curso).
El laboratorio vive en especialidad-05/contenido.json y usa los mismos archivos SQL de recursos/tweets/."""
from html import escape as e
from pathlib import Path
from guion import slide, p, step, table, flow, code, proof, lablink, source

TITLE = 'Un conteo no es un indicador'
BIGIDEA = 'Gold convierte millones de tweets en seis tablas pequeñas, cada una con su pregunta, su grano, su denominador y sus límites escritos.'
RES = Path(__file__).resolve().parents[1] / 'recursos' / 'tweets'
SRC = 'Valores de referencia · 6,798,932 tweets del 16 al 27 de marzo de 2022 · uso académico'
VIEWS = source('BigQuery · vistas', 'https://docs.cloud.google.com/bigquery/docs/views-intro')
MV = source('BigQuery · vistas materializadas', 'https://docs.cloud.google.com/bigquery/docs/materialized-views-create')
SCHED = source('BigQuery · consultas programadas', 'https://docs.cloud.google.com/bigquery/docs/scheduling-queries')
DATAFORM = source('Google Cloud · Dataform', 'https://docs.cloud.google.com/dataform/docs/overview')

PH = {'a': 'Abrir · 0–15 min', 'c': 'Comprender · 15–50 min', 'p': 'Aplicar · 50–70 min', 'z': 'Pausa · 70–80 min',
      'l': 'Laboratorio · 80–150 min', 'k': 'Cerrar · 150–180 min'}
S = []


def add(title, body, note, layout='plain', ph='c', src=SRC):
    S.append(slide(title, body, note, layout, PH[ph], src))


def n(x):
    return f'{x:,}'


def tx(x, y, s, cls='', anchor='start'):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{e(str(s))}</text>'


def svg(w, h, inner, label, uid='x'):
    d = (f'<defs><pattern id="g5h-{uid}" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<rect width="14" height="14" fill="#f6f4ef"/><rect width="7" height="14" fill="#8a93a3"/></pattern>'
         '<marker id="g5a-' + uid + '" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0L9 4L0 8Z"/></marker></defs>')
    return f'<svg class="g5" viewBox="0 0 {w} {h}" role="img" aria-label="{e(label)}">{d}{inner}</svg>'


def vbars(vals, labels, x0, y0, w, h, ymax, fmt=n, cls=None, hatch=(), uid='x', gap=0.34, vsize='m', show=True, lsize='s'):
    k = len(vals)
    sp = w / k
    bw = sp * (1 - gap)
    o = [f'<line class="axis" x1="{x0}" y1="{y0 + h}" x2="{x0 + w}" y2="{y0 + h}"/>']
    for i, (v, lab) in enumerate(zip(vals, labels)):
        bh = h * v / ymax
        x = x0 + i * sp + (sp - bw) / 2
        y = y0 + h - bh
        c = cls[i] if cls else 'bar-blue'
        st = f' style="fill:url(#g5h-{uid});stroke:#8a93a3;stroke-width:2"' if i in hatch else ''
        o.append(f'<rect class="{c}" x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}"{st}/>')
        if show:
            o.append(tx(f'{x + bw / 2:.1f}', f'{y - 9:.1f}', fmt(v), vsize + ' v', 'middle'))
        o.append(tx(f'{x + bw / 2:.1f}', y0 + h + 30, lab, lsize, 'middle'))
    return ''.join(o)


def hbars(rows, x0, y0, w, bh, gap, vmax, lab_w=300, fmt=n, cls=None, vpad=190):
    o = []
    for i, (lab, v) in enumerate(rows):
        y = y0 + i * (bh + gap)
        bw = (w - lab_w - vpad) * v / vmax
        c = cls[i] if cls else 'bar-blue'
        o.append(tx(x0 + lab_w - 16, y + bh * 0.68, lab, 'm', 'end'))
        o.append(f'<rect class="{c}" x="{x0 + lab_w}" y="{y}" width="{bw:.1f}" height="{bh}"/>')
        o.append(tx(x0 + lab_w + bw + 14, y + bh * 0.68, fmt(v), 'm v'))
    return ''.join(o)


def result(headers, rows, meta):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="rp-out"><table class="rp-t"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table><p class="rp-meta">{meta}</p></div>'


def ctable(headers, rows, cls='matrix compact'):
    return table(headers, rows).replace('class="matrix"', f'class="{cls}"')


def ex(t, cls=''):
    return f'<p class="ex {cls}">{t}</p>'


# ---------------------------------------------------------------- datos de referencia
DIAS = ['16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27']
EN_ENERGIA = [1666, 10167, 9772, 7247, 6980, 8920, 7384, 10530, 10400, 9342, 7339, 6666]
EN_DIA = [86271, 476188, 433524, 357489, 369390, 373906, 333329, 311363, 327399, 321183, 304339, 318791]
EN_PCT = [1.931, 2.135, 2.254, 2.027, 1.89, 2.386, 2.215, 3.382, 3.177, 2.909, 2.411, 2.091]
HORAS = [240135, 211465, 189902, 168449, 145033, 144018, 173123, 222931, 231936, 245825, 265097, 292693,
         326497, 355955, 370985, 369562, 371978, 369166, 371294, 361318, 348580, 329542, 300872, 257705]

# ================================================================= ABRIR (0–15)
add('Un conteo no es un indicador.',
    '<div><p class="overline">Sesión 5 · Capa Gold</p><h1>Un conteo<br>no es un indicador.</h1>'
    '<p class="lede">Hoy construimos las tablas que un comité sí puede leer.</p></div>'
    '<div class="stack"><p class="stat signal">6,798,932</p><p class="statl">tweets en Silver</p><p class="stat signal">6</p><p class="statl">tablas Gold, una por pregunta</p>'
    '<p class="caption">Energía, alimentos, aviación, sanciones, cadena de suministro y mercados<br>16 al 27 de marzo de 2022 · uso académico</p></div>',
    '0–3 min. Abrir con la pregunta de un comité: ¿qué temas de la guerra vale la pena vigilar en una empresa? No analizamos el contenido bélico; buscamos temas satélite de negocio. Preguntar: «¿Qué necesitarías ver para decidir?» [pausa 3 s] Anotar dos respuestas en voz alta. Hoy aprenden a contestar con una cifra defendible: con su grano, su denominador y sus límites.',
    'cover dark', 'a')

add('Casi el mismo conteo; un 58 % más de peso en el día.',
    '<div class="g5-wrap">' + svg(1296, 365,
        tx(0, 28, 'Tweets de energía en inglés', 'b') + tx(0, 58, 'conteo', 's')
        + vbars([10167, 10530], ['17 de marzo', '23 de marzo'], 40, 70, 520, 215, 12000, uid='a1', cls=['bar-grey', 'bar-blue'])
        + '<g data-step="1">' + tx(720, 28, '% de los tweets de ese día', 'b') + tx(720, 58, 'conteo ÷ tweets del día × 100', 's')
        + vbars([2.135, 3.382], ['17 de marzo', '23 de marzo'], 740, 70, 520, 215, 4, fmt=lambda v: f'{v:.3f} %', uid='a2', cls=['bar-grey', 'bar-red'])
        + tx(300, 352, 'de 476,188 tweets', 's', 'middle') + tx(1000, 352, 'de 311,363 tweets', 's', 'middle') + '</g>',
        'Dos paneles: el conteo de energía casi no cambia entre el 17 y el 23 de marzo; el porcentaje del día sube de 2.135 a 3.382', 'a')
    + '</div>' + step(2, p('Conteo +3.6 %; tweets del día −35 %: el porcentaje sube 58 %.', 'callout')),
    '3–8 min. Mostrar solo el conteo y pedir que voten: ¿cambió algo entre el 17 y el 23? [pausa 3 s] Casi nada: 10,167 y 10,530 (+3.6 %). Clic: el mismo conteo visto como porcentaje del día. El 17 hubo 476,188 tweets en inglés; el 23, 311,363. Con menos tweets en total, la misma cantidad de energía pesa más: 2.135 % contra 3.382 %. La pregunta de esta sesión: cuál de las dos lecturas es la correcta depende de cómo escribas el indicador. Aún no afirmamos causas: el archivo no las trae.',
    'comparison', 'a')

add('Silver dice qué escribió cada tweet; Gold dice qué decidir.',
    '<div class="layers"><div class="layer"><p class="caption">BRONZE</p><p class="big3">22.04 GiB</p><p>El JSON tal como llegó.</p><p class="who">Conserva</p></div>'
    '<div class="arr">→</div>'
    '<div class="layer"><p class="caption">SILVER</p><p class="big3">2.28 GiB</p><p>Tres tablas con tipos: tweets, autores, hashtags.</p><p class="who">Ordena y tipa</p></div>'
    '<div class="arr" data-step="1">→</div>'
    '<div class="layer focus" data-step="1"><p class="caption">GOLD</p><p class="big3">≈ 0.5 MB</p><p>Seis tablas más una de temas; cada fila ya es una respuesta.</p><p class="who">Responde</p></div></div>'
    + step(2, p('Gold es pequeña porque cada fila resume miles de tweets.', 'callout')),
    '8–15 min. Repasar las capas con un número cada una: Bronze 22.04 GiB de JSON crudo; Silver 2.28 GiB (tweets 6,798,932 filas; autores 1,872,074; hashtags 3,339,839); Gold unos 0.5 MB en total (la suma de las siete tablas es 508,964 bytes). La diferencia de tamaño es la idea: Gold no guarda tweets, guarda respuestas. Una fila de Gold puede resumir decenas de miles de tweets. Error típico: pensar que Gold es «Silver con menos columnas». No: cambia el grano.',
    'path', 'a')

# ================================================================= COMPRENDER (15–50)
add('Gold responde una pregunta por tabla.',
    ctable(['Tabla Gold', 'Pregunta que responde', 'Grano: una fila es…', 'Filas'], [
        ['tema_dia', '¿Qué parte de cada día habló de cada tema?', 'día × tema × grupo de idioma', '216'],
        ['hashtags_dia', '¿Qué etiquetas dominaron cada día?', 'día × hashtag (≥ 25 tweets)', '10,636'],
        ['autores_alcance', '¿Quién concentra la interacción?', 'segmento de seguidores del autor', '5'],
        ['aplicaciones_dia', '¿Desde dónde se publica?', 'día × aplicación', '108'],
        ['actividad_hora', '¿A qué hora ocurre la conversación?', 'día × hora UTC × grupo de idioma', '804'],
        ['conversacion_dia', '¿Son originales, respuestas o citas?', 'día × tipo de tweet', '36']])
    + step(1, p('Una pregunta, un grano, una tabla. Seis tablas, 0.5 MB en total.', 'callout')),
    '15–19 min. Recorrer la tabla renglón por renglón en voz alta: cada tabla nace de una pregunta de negocio, no de las columnas que existen. Las filas son reales: 216 = 12 días × 6 temas × 3 idiomas; 5 segmentos de seguidores; 36 = 12 días × 3 tipos. Aparte existe temas_palabras (42 filas): la definición de los temas, no un resultado. Pregunta: «¿cuál de estas preguntas le importaría más a un director de comunicación?» Escuchar dos respuestas.',
    'table', 'c')

# --- cuadrícula del grano
TEMAS = ['alimentos', 'aviación', 'cadena suministro', 'energía', 'mercados', 'sanciones']
cells = []
cx0, cy0, cw, ch = 235, 50, 58, 27
for ci, d in enumerate(DIAS):
    cells.append(tx(cx0 + ci * cw + cw / 2, 42, d, 's', 'middle'))
for ti, tema in enumerate(TEMAS):
    cells.append(tx(cx0 - 14, cy0 + ti * 3 * ch + 2 * ch - 2, tema, 's', 'end'))
    for gi in range(3):
        ri = ti * 3 + gi
        for ci in range(12):
            cells.append(f'<rect class="cell{"b" if ti % 2 else ""}" x="{cx0 + ci * cw}" y="{cy0 + ri * ch}" width="{cw - 2}" height="{ch - 2}"/>')
focus_y = cy0 + (3 * 3 + 0) * ch
cells.append(f'<g data-step="1"><rect class="focus" x="{cx0 + 7 * cw - 3}" y="{focus_y - 3}" width="{cw + 4}" height="{ch + 4}"/>'
             + tx(cx0 + 7 * cw + cw / 2, focus_y - 12, '▼', 'red', 'middle') + '</g>')
cells.append(tx(cx0, 20, 'marzo de 2022 →', 's'))
cells.append(tx(cx0 + 12 * cw + 6, cy0 + 13, 'en', 's') + tx(cx0 + 12 * cw + 6, cy0 + 13 + ch, 'es', 's') + tx(cx0 + 12 * cw + 6, cy0 + 13 + 2 * ch, 'otro', 's'))
GRID = svg(1000, 560, ''.join(cells), 'Cuadrícula de 12 días por 18 filas (6 temas por 3 grupos de idioma): 216 celdas, una celda destacada', 'g')

add('El grano dice qué representa una fila.',
    '<div class="two5" style="grid-template-columns:1.45fr 1fr"><div class="g5-wrap">' + GRID + '</div><div>'
    + p('216 filas = 12 días × 6 temas × 3 grupos de idioma.', 'ex sm')
    + '<div data-step="1"><div class="rp-out"><table class="mini kv"><tbody><tr><td>fecha</td><td>2022-03-23</td></tr><tr><td>tema</td><td>energia</td></tr>'
    '<tr><td>grupo_idioma</td><td>en</td></tr><tr><td>tweets_tema</td><td>10,530</td></tr><tr><td>tweets_dia</td><td>311,363</td></tr>'
    '<tr><td>pct_del_dia</td><td>3.382</td></tr></tbody></table><p class="rp-meta">Una fila = la celda marcada.</p></div></div>'
    + step(2, p('Si cambias el grano, cambia lo que significa cada número.', 'callout')) + '</div></div>',
    '19–24 min. El grano es lo que representa UNA fila. Aquí: un día, un tema y un grupo de idioma. Clic: la celda marcada es energía, inglés, 23 de marzo: 10,530 tweets de 311,363 ese día. Pedir que alguien lea la fila en voz alta con las unidades. Si el grano fuera «por mes», habría 6 filas y no verías el salto del 23. Error típico: sumar filas de granos distintos. Regla del curso: escribe el grano antes de escribir la consulta.',
    'grain', 'c')

add('Un indicador necesita denominador.',
    '<div class="eq"><p class="formula">pct_del_dia = 100 × tweets_tema ÷ tweets_dia</p></div>'
    '<div data-step="1"><div class="mb"><i style="width:3.38%"></i></div><div style="display:flex;justify-content:space-between;margin-top:8px">'
    '<p class="m s5" style="color:var(--signal)">10,530 tweets de energía en inglés</p><p class="m s5">311,363 tweets en inglés ese día</p></div>'
    '<p class="m big3" style="margin-top:10px">10,530 ÷ 311,363 = 0.03382 → 3.382 %</p></div>'
    + step(2, p('El denominador es del mismo día y del mismo grupo de idioma: inglés no se compara con español.', 'callout')),
    '24–28 min. Definir denominador con una analogía: «¿cuántos de cada cien?» El conteo crudo no se puede comparar entre días porque cada día tuvo un volumen distinto: 778,608 tweets el 17 de marzo y 505,568 el 26. Tampoco entre idiomas: el inglés tiene 4,013,172 tweets y el español 1,056,425. Por eso la fila trae tweets_tema y tweets_dia: el denominador viaja con la cifra. Error típico: dividir por el total del archivo en lugar del total del día.',
    'case', 'c')

add('Un tweet puede contar en varios temas.',
    '<div class="g5-wrap">' + svg(1296, 230,
        '<rect class="box" x="0" y="10" width="640" height="190"/>' + tx(20, 42, 'Un tweet real de la muestra', 's')
        + tx(20, 82, '«The war in Ukraine, embargoes and', 'm') + tx(20, 114, 'airspace closures are also affecting', 'm')
        + tx(20, 146, 'global air cargo operations…', 'm') + tx(20, 178, '#logistics»', 'm')
        + '<g data-step="1"><path d="M645 80L765 55" stroke="#1c3664" stroke-width="3" marker-end="url(#g5a-t)"/>'
        '<path d="M645 130L765 160" stroke="#1c3664" stroke-width="3" marker-end="url(#g5a-t)"/>'
        '<rect class="ok" x="770" y="10" width="520" height="76"/>' + tx(790, 42, 'AVIACIÓN', 'b') + tx(790, 72, 'palabra: airspace', 's')
        + '<rect class="ok" x="770" y="124" width="520" height="76"/>' + tx(790, 156, 'CADENA DE SUMINISTRO', 'b') + tx(790, 186, 'palabra: logistics', 's') + '</g>',
        'Un tweet de la muestra conectado con dos temas: aviación por la palabra airspace y cadena de suministro por la palabra logistics', 't')
    + '</div>'
    + '<div data-step="2"><div class="lin"><div class="ln1"><p class="cap">TWEETS</p><p class="m big3">6,798,932</p></div>'
    '<div class="ln1"><p class="cap">CON ALGÚN TEMA</p><p class="m big3">314,527</p><p class="s5">4.6 %</p></div>'
    '<div class="ln1"><p class="cap">PARES TWEET–TEMA</p><p class="m big3">342,484</p></div></div></div>'
    + step(3, p('No sumes los temas: son pares, no tweets distintos.', 'callout')),
    '28–33 min. Mostrar el tweet real: habla de carga aérea, así que aviación (airspace) y cadena de suministro (logistics) lo atrapan. En Gold cuenta una vez en cada tema, pero es un solo tweet. Clic: 314,527 tweets distintos tienen algún tema (4.6 % del total) y generan 342,484 pares tweet–tema; la diferencia son tweets en más de un tema. Error típico: sumar los seis temas y llamarlo «tweets sobre la guerra y los negocios». Pregunta: «¿cuántos tweets distintos hay si sumo 137,598 + 80,266 + 59,685 + 49,137 + 8,975 + 6,823?» No lo sabemos solo con esa suma.',
    'path', 'c')

add('Las palabras clave son una definición.',
    '<div class="two5"><div>' + ctable(['Tema', 'Algunas de sus 42 palabras'], [
        ['energía', 'oil · gas · fuel · energy'],
        ['alimentos', 'wheat · grain · food · trigo'],
        ['aviación', 'airline · flights · airspace'],
        ['sanciones', 'sanctions · sanciones · sanción'],
        ['cadena', 'supply chain · shipping · puerto'],
        ['mercados', 'inflation · markets · inflación']])
    + '</div><div>' + code("""SELECT t.fecha, p.tema, t.tweet_id
FROM tweets_silver.tweets AS t
CROSS JOIN tweets_gold.temas_palabras AS p
WHERE REGEXP_CONTAINS(LOWER(t.texto),
        CONCAT(r'\\b', p.palabra, r'\\b'))
GROUP BY t.fecha, p.tema, t.tweet_id""")
    + step(1, p('Cada tweet se prueba contra 42 palabras; GROUP BY lo cuenta una vez por tema.', 'ex s5ex')) + '</div></div>',
    '33–37 min. La tabla temas_palabras es una definición editable: tú decides qué palabras definen un tema. El SQL prueba cada tweet contra las 42 palabras (CROSS JOIN) y deja pasar solo las coincidencias (REGEXP_CONTAINS; \\b marca el límite de una palabra para que «gas» no coincida con «Gascón»). GROUP BY tweet_id cuenta una vez por tema aunque el tweet use dos palabras del mismo tema. Costo real: 1.42 GB, porque solo lee el texto. Lo que NO hace: entender el tema. Eso se mide en la siguiente slide.',
    'query', 'c')

add('Lee lo que atrapan las palabras clave.',
    ctable(['Tema · palabra', 'Tweet (primeros caracteres)', 'Lectura'], [
        ['energía · gas', 'Putin says Russia will switch gas sales to rubles…', '<span class="tag ok">acierto</span>'],
        ['alimentos · trigo', 'Fedeagro calcula aumento de 70 % en precio del trigo…', '<span class="tag ok">acierto</span>'],
        ['aviación · airspace', '…airspace closures are affecting global air cargo…', '<span class="tag ok">acierto</span>'],
        ['sanciones · sanctions', '…the sanctions pressure from the United States will not have any impact…', '<span class="tag ok">acierto</span>'],
        ['energía · fuel / alimentos · food', 'Pentagon: Russian forces lack food, ammunition… ships short of fuel…', '<span class="tag dud">dudoso</span> <span class="tag fal">falso</span>'],
        ['aviación · airspace', 'Russia has not achieved air superiority over Ukraine…', '<span class="tag fal">falso</span>'],
        ['mercados · markets', '…studies support Wuhan fish markets as the likely origin of COVID…', '<span class="tag fal">falso</span>'],
        ['mercados · inflación', 'Estamos perdiendo la guerra contra la inflación…', '<span class="tag fal">falso</span>']],
           'matrix compact sample')
    + step(1, p('Lectura de 30 filas: 17 aciertos, 6 dudosos, 7 falsos. Una persona, un día: no es precisión medida.', 'callout sm')),
    '37–42 min. Los ocho renglones salen de la consulta del paso 6 del laboratorio (5 tweets por tema el 23 de marzo, inglés y español). Mi lectura de las 30 filas: 17 aciertos, 6 dudosos y 7 falsos positivos. Otra persona clasificaría distinto, y eso es parte de la lección: la precisión se mide con varias personas leyendo una muestra más grande. Dos errores típicos: palabras con otro sentido (markets en «Wuhan fish markets»; «guerra contra la inflación» es una expresión) y temas militares que parecen de negocio (air superiority no es aviación comercial). Aviso: el mismo tweet de la Pentagon aparece como dudoso en energía y falso en alimentos.',
    'sample', 'c')

add('El umbral decide qué ves.',
    '<div data-demo="s5-umbral"><div class="actions" role="group" aria-label="Umbral de tweets por día">'
    '<button data-u="25" aria-pressed="true">≥ 25 tweets al día</button><button data-u="100" aria-pressed="false">≥ 100</button>'
    '<button data-u="500" aria-pressed="false">≥ 500</button><button data-u="2000" aria-pressed="false">≥ 2,000</button></div>'
    '<div class="g5stats"><div class="g5stat"><p class="cap">HASHTAGS QUE SOBREVIVEN</p><p class="m big2" data-out="hashtags">2,261</p><p class="s5">de 223,523 en Silver</p></div>'
    '<div class="g5stat"><p class="cap">FILAS DÍA–HASHTAG</p><p class="m big2" data-out="filas">10,636</p></div>'
    '<div class="g5stat"><p class="cap">MENCIONES CUBIERTAS</p><p class="m big2" data-out="menciones">2,397,514</p><p class="s5">de 3,339,839</p></div>'
    '<div class="g5stat"><p class="cap">% DE LAS MENCIONES</p><p class="m big2" data-out="pct">71.8 %</p></div></div>'
    '<div class="mb"><i data-bar style="width:71.8%"></i></div></div>'
    + code('HAVING COUNT(*) >= 25   -- umbral de hashtags_dia')
    + step(1, p('Un umbral ahorra filas, pero esconde la cola larga: alguien debe firmarlo.', 'callout sm')),
    '42–46 min. Demo con cuatro umbrales (cifras reales de hashtags_dia): con ≥ 25 tweets al día quedan 2,261 hashtags y 71.8 % de las menciones; con ≥ 100, 525 hashtags y 61.1 %; con ≥ 500, 97 y 47.5 %; con ≥ 2,000, 21 y 33.4 %. La tabla Gold del curso usa 25. Mensaje: el umbral es una decisión de negocio con costo (qué dejas fuera). Silver conserva las 3,339,839 menciones; Gold, un resumen. Error típico: presentar el top de Gold como «todos los hashtags».',
    'chart', 'c')

add('El hashtag más grande pesa 8.7 % de un día.',
    '<div class="two5"><div class="g5-wrap">' + svg(760, 400, hbars([
        ('#ukraine', 8.711), ('#putin', 2.521), ('#russia', 2.351), ('#ucrania', 0.95), ('#standwithukraine', 0.803), ('#ukrainerussianwar', 0.652)],
        0, 20, 760, 42, 14, 9.5, lab_w=330, fmt=lambda v: f'{v:.2f} %', vpad=110) + tx(0, 392, '% de los tweets del 23 de marzo', 's'),
        'Barras horizontales: porcentaje del día de los seis hashtags más usados el 23 de marzo', 'h')
    + '</div><div>' + step(1, '<p class="cap">NUEVOS EL 27 DE MARZO</p>' + result(['hashtag', 'tweets'], [
        ['#27mar', '582'], ['#oscars', '482'], ['#annewill', '284'], ['#trumprally', '224']], 'tweets_gold.hashtags_dia'))
    + step(2, p('Etiquetas ajenas a la guerra: la conversación se abre. Solo 18 % de los tweets lleva hashtag.', 'ex s5ex')) + '</div></div>',
    '46–50 min. Hashtags del 23 de marzo, en porcentaje del día: #ukraine 8.7 %, #putin 2.5 %, #russia 2.4 %. Un hashtag es una etiqueta que el autor escribe; no mide a favor o en contra. Clic: el 27 de marzo aparecen etiquetas ajenas a la guerra (#27mar, #oscars, #annewill, #trumprally) que el 17 no llegaban al umbral: la conversación se abre a otros temas. Límite: solo 1,226,642 de 6,798,932 tweets (18 %) llevan al menos un hashtag. Pregunta: «¿qué decidirías con esta tabla y qué no?»',
    'chart', 'c')

# ================================================================= APLICAR (50–70)
SEG = [('menos de 1 mil', 67.02, 8.72), ('1 mil a 10 mil', 23.41, 12.62), ('10 mil a 100 mil', 6.59, 25.07),
       ('100 mil a 1 millón', 2.15, 35.93), ('más de 1 millón', 0.84, 17.66)]
g = ['<rect class="bar-grey" x="310" y="9" width="22" height="22"/>' + tx(342, 28, '% de los tweets', 's')
     + '<rect class="bar-red" x="640" y="9" width="22" height="22"/>' + tx(672, 28, '% de los likes', 's')]
for i, (lab, a, b_) in enumerate(SEG):
    y = 48 + i * 72
    g.append(tx(290, y + 32, lab, 'm', 'end'))
    g.append(f'<rect class="bar-grey" x="310" y="{y}" width="{780 * a / 70:.1f}" height="28"/>' + tx(316 + 780 * a / 70, y + 22, f'{a:.2f} %', 's v'))
    g.append(f'<rect class="bar-red" x="310" y="{y + 32}" width="{780 * b_ / 70:.1f}" height="28"/>' + tx(316 + 780 * b_ / 70, y + 54, f'{b_:.2f} %', 'm v'))
ALCANCE = svg(1296, 420, ''.join(g), 'Barras agrupadas por segmento de seguidores: porcentaje de tweets frente a porcentaje de likes', 'al')
add('Pocas cuentas concentran los likes.',
    '<div class="g5-wrap">' + ALCANCE + '</div>' + step(1, p('Más de 1 millón de seguidores: 0.84 % de los tweets, 17.66 % de los likes.', 'callout sm')),
    '50–54 min. Tabla autores_alcance: 5 filas, una por segmento de seguidores del autor. Barra gris: porcentaje de tweets; barra roja: porcentaje de likes. El 67 % de los tweets lo escriben autores con menos de mil seguidores y reciben 8.7 % de los likes. Las cuentas de 100 mil a 1 millón escriben 2.15 % de los tweets y reciben 35.93 %. Seguidores es el dato del autor en su último tweet del archivo; likes no es influencia ni persuasión. Pregunta: «¿qué haría un director de comunicación con esta tabla?» Límite: es una foto de 12 días.',
    'chart', 'p')

add('Quien más publica no es quien más audiencia tiene.',
    '<div class="two5"><div><p class="stat signal">11,917</p><p class="statl">autores con más de 50 tweets<br>(0.64 % de los 1,872,074 autores)</p>'
    + step(1, '<p class="stat signal">1,310,632</p><p class="statl">tweets suyos: 19.3 % del total</p>') + '</div><div>'
    + ctable(['Tweets del autor', 'Autores'], [['1', '1,091,593'], ['2 a 5', '554,547'], ['6 a 50', '214,017'], ['más de 50', '11,917']])
    + step(2, p('El autor más activo escribió 7,492 tweets y tenía 88 seguidores.', 'callout sm')) + '</div></div>',
    '54–57 min. Tabla Silver autores (1,872,074 filas, una por autor) contra autores_alcance. 1,091,593 autores aparecen una sola vez; 11,917 (0.64 %) escriben más de 50 tweets y suman 1,310,632 tweets, 19.3 % del archivo. El autor con más tweets: 7,492, con 88 seguidores. No sabemos si son personas o cuentas automatizadas: el archivo no lo dice. Por eso Gold dice «cuentas» y «autores», no «personas». Error típico: leer «6.8 millones de tweets» como «6.8 millones de voces».',
    'compare', 'p')

hr = []
hr.append(tx(0, 26, 'Tweets por hora UTC, días completos (17 al 27 de marzo)', 'b'))
hr.append(vbars(HORAS, [f'{h:02d}' for h in range(24)], 20, 120, 1250, 200, 400000, uid='h', show=False,
                cls=['bar-blue' if 13 <= h <= 19 else 'bar-grey' for h in range(24)]))
hr.append(tx(20 + 1250 * 16.5 / 24, 104, '13 a 19 UTC: 5.3 a 5.6 % por hora', 's', 'middle'))
hr.append(tx(20 + 1250 * 5.5 / 24, 220, '5 UTC: 2.2 %', 's red', 'middle'))
hr.append('<g data-step="1"><rect x="20" y="48" width="570" height="124" fill="#f6f4ef" stroke="#8a93a3" stroke-width="2"/>'
          + tx(36, 82, '16 de marzo: día parcial', 'b')
          + tx(36, 112, 'solo horas 20 a 23 UTC', 's')
          + tx(36, 148, '12,684 · 45,347 · 41,166 · 35,674', 'm') + '</g>')
add('El ritmo del día tiene forma; el 16 de marzo solo trae cuatro horas.',
    '<div class="g5-wrap">' + svg(1296, 360, ''.join(hr), 'Barras de 24 horas UTC con el mínimo a las 5 y la meseta de 13 a 19 horas; un recuadro muestra las cuatro horas del 16 de marzo', 'h')
    + '</div>' + step(2, p('Horas en UTC, no hora local: el patrón mezcla zonas horarias.', 'callout sm')),
    '57–60 min. Tabla actividad_hora (804 filas: día × hora UTC × idioma). Los días completos tienen un valle a las 5 UTC (2.2 %) y una meseta de 13 a 19 UTC (5.3 a 5.6 % por hora). El inglés tiene su pico a las 18 UTC, el español a las 14 y el resto de idiomas a las 13. Clic: el 16 de marzo solo tiene datos de 20 a 23 UTC: es un día parcial, por eso sus conteos no se comparan con los demás. UTC no es hora local: el patrón mezcla usuarios de muchos países.',
    'chart', 'p')

add('Casi 9 de cada 10 tweets salen de las aplicaciones oficiales.',
    '<div class="two5"><div class="g5-wrap">' + svg(800, 480, hbars([
        ('Twitter Web App', 32.5), ('Twitter for Android', 30.7), ('Twitter for iPhone', 22.7), ('otras', 5.6), ('Twitter for iPad', 3.1),
        ('WordPress.com', 2.0), ('TweetDeck', 1.5), ('dlvr.it', 1.1), ('IFTTT', 0.7)], 0, 8, 800, 40, 12, 35, lab_w=280, fmt=lambda v: f'{v:.1f} %', vpad=110,
        cls=['bar-blue'] * 3 + ['bar-grey'] + ['bar-blue'] + ['bar-red'] * 4),
        'Barras horizontales con el porcentaje de tweets por aplicación de publicación', 'ap') + '</div><div>'
    + '<p class="stat signal">89.0 %</p><p class="statl">en las aplicaciones oficiales<br>(web, Android, iPhone, iPad)</p>'
    + step(1, '<p class="stat signal">5.3 %</p><p class="statl">en herramientas de publicación<br>(WordPress, TweetDeck, dlvr.it, IFTTT)</p>')
    + step(2, p('La aplicación no dice si hay una persona detrás.', 'ex s5ex')) + '</div></div>',
    '60–63 min. Tabla aplicaciones_dia (108 filas: día × aplicación; las ocho mayores del archivo y «otras»). Suma de las cuatro aplicaciones oficiales: 89.0 %. WordPress, TweetDeck, dlvr.it e IFTTT suman 5.3 %: son herramientas que programan o automatizan publicaciones. Límite: usar una herramienta de publicación no prueba que la cuenta sea automática, y usar la app oficial no prueba que sea una persona. Sirve para describir el origen del tráfico, no para clasificar autores.',
    'chart', 'p')

W = 1120
def seg(y, parts):
    out, x = [], 140
    for (v, cls, lab, mode) in parts:
        w = W * v / 100
        out.append(f'<rect class="{cls}" x="{x:.1f}" y="{y}" width="{w:.1f}" height="54"/>')
        if mode == 'in':
            out.append(tx(f'{x + w / 2:.1f}', y + 34, lab, 's w', 'middle'))
        elif mode == 'above':
            out.append(tx(f'{x + w / 2:.1f}', y - 10, lab, 's', 'middle'))
        else:
            out.append(tx(f'{x + w / 2:.1f}', y + 82, lab, 's', 'middle'))
        x += w
    return ''.join(out)
CONV = svg(1296, 300,
           tx(120, 78, 'tweets', 'b', 'end') + seg(50, [(50.2, 'bar-grey', 'respuestas 50.2 %', 'in'), (40.2, 'bar-blue', 'originales 40.2 %', 'in'), (9.6, 'bar-red', 'citas 9.6 %', 'above')])
           + '<g data-step="1">' + tx(120, 188, 'likes', 'b', 'end') + seg(160, [(78.5, 'bar-blue', 'originales 78.5 %', 'in'), (15.2, 'bar-grey', 'respuestas 15.2 %', 'above'), (6.3, 'bar-red', 'citas 6.3 %', 'below')])
           + tx(140, 285, 'Likes por tweet: originales 31.0 · citas 10.4 · respuestas 4.8', 'm') + '</g>',
           'Dos barras apiladas: la mitad de los tweets son respuestas, pero casi cuatro quintos de los likes están en los tweets originales', 'cv')
add('La mitad de los tweets son respuestas; los likes están en los originales.',
    '<div class="g5-wrap">' + CONV + '</div>' + step(2, p('Un original recibe en promedio 31 likes; una respuesta, 4.8. La mediana de los tres es 0.', 'callout sm')),
    '63–66 min. Tabla conversacion_dia (36 filas: día × tipo). Tweets: 3,414,201 respuestas (50.2 %), 2,729,906 originales (40.2 %) y 654,825 citas (9.6 %). Likes: 84.7 millones de 108 millones están en originales (78.5 %). Promedio de likes por tweet: originales 31.04, citas 10.45, respuestas 4.80 (la mediana diaria de los tres tipos es 0). Pregunta: «si quieres medir qué dice la gente, ¿cuentas respuestas?» No hay una respuesta única: depende de la pregunta. Límite: la extracción excluye retweets.',
    'compare', 'p')

add('Seis tablas, cinco técnicas de SQL.',
    ctable(['Tabla', 'Técnica nueva', 'En palabras simples'], [
        ['tema_dia', 'JOIN … USING + denominador', 'cada fila lleva su total del día; de ahí sale el porcentaje'],
        ['hashtags_dia', 'GROUP BY … HAVING', 'agrupa y descarta lo que no llega al umbral'],
        ['autores_alcance', 'CASE WHEN + SUM(…) OVER ()', 'crea segmentos y calcula el % del total sin colapsar filas'],
        ['aplicaciones_dia', 'subconsulta con IN + IF', 'deja las ocho mayores y agrupa el resto en «otras»'],
        ['actividad_hora', 'EXTRACT(HOUR FROM …)', 'saca la hora de una fecha con hora'],
        ['conversacion_dia', 'CASE + APPROX_QUANTILES', 'clasifica el tipo y calcula una mediana aproximada']])
    + step(1, p('Todas siguen la misma receta: pregunta, grano, agregación y denominador.', 'callout sm')),
    '66–68 min. No hay que memorizar sintaxis: sí reconocer la receta. Cada tabla combina la misma estructura (FROM tabla Silver, GROUP BY el grano, SUM/COUNT) con una técnica: un JOIN para traer el denominador, HAVING para un umbral, CASE WHEN para crear categorías, SUM() OVER () para obtener el total de la tabla sin perder filas, IF para agrupar en «otras», EXTRACT para sacar la hora y APPROX_QUANTILES para una mediana aproximada. Todo el código está en los archivos 30 a 35 del laboratorio.',
    'table', 'p')

add('Un KPI es una ficha, no una fórmula suelta.',
    ctable(['Campo', 'Ejemplo con tema_dia'], [
        ['Nombre', 'Porcentaje diario de tweets en inglés que mencionan energía'],
        ['Pregunta', '¿Qué parte de la conversación en inglés habló de energía cada día?'],
        ['Fórmula', '100 × tweets_tema ÷ tweets_dia'],
        ['Grano', 'día × tema × grupo de idioma'],
        ['Población', 'Tweets de la extracción, sin retweets, 16 al 27 de marzo de 2022'],
        ['Denominador', 'Todos los tweets de ese día y de ese grupo de idioma'],
        ['Límites', 'El 16 es parcial; palabras clave sin precisión medida; un solo periodo'],
        ['No afirma', 'Que la gente se preocupó más ni la causa de un cambio']], 'matrix compact kpi')
    + step(1, p('Sin ficha, dos personas calculan «energía» y obtienen cifras distintas.', 'callout sm')),
    '68–70 min. Un KPI (indicador clave) es una cifra con definición escrita. Recorrer los ocho campos con el ejemplo de tema_dia. El paso 6 del laboratorio entrega una plantilla para llenar la tuya. Pregunta: «¿qué campo se olvida más a menudo?» Normalmente el denominador y los límites. Error típico: publicar la cifra sin la ficha; seis meses después nadie recuerda si incluía el día parcial.',
    'kpi', 'p')

# ================================================================= PAUSA
add('Pausa. Vuelve con la consola de consultas abierta.',
    '<p class="huge">10 min</p><p>Silver listo en tu proyecto: tweets, autores y hashtags.</p>',
    '70–80 min. Pausa real. Antes de continuar, comprobar que tweets_silver.tweets, tweets_silver.autores y tweets_silver.hashtags existen en tu proyecto (sesión anterior) y que la consola de BigQuery está abierta. Si falta alguna, créala con los scripts de Silver antes de empezar el laboratorio.',
    'statement dark', 'z')

# ================================================================= LABORATORIO (una sola slide)
add('Laboratorio: construye las seis tablas Gold.',
    '<p class="lab-ribbon">80–150 MIN · 6 PASOS · BIGQUERY STUDIO</p>' + ctable(['Paso', 'Min', 'Construyes', 'Verificas'], [
        ['1', '15', 'temas_palabras y tema_dia', '342,484 pares · base 6,798,932'],
        ['2', '10', 'hashtags_dia', '71.8 % de las menciones'],
        ['3', '10', 'autores_alcance', '5 segmentos que suman 6,798,932'],
        ['4', '12', 'aplicaciones_dia y actividad_hora', 'ritmo por hora; 16 de marzo parcial'],
        ['5', '10', 'conversacion_dia y el cuadre', 'cuatro totales iguales a Silver'],
        ['6', '13', 'precisión de palabras clave y tu ficha de KPI', '30 filas leídas por ti']])
    + '<div class="lab-proof"><strong>Costo</strong><span>Todo Gold cuesta ≈ 2.2 GB leídos desde Silver; las tablas ocupan ≈ 0.5 MB.</span></div>'
    + lablink(1),
    '80–150 min. Una sola slide para toda la práctica: la guía tiene el código completo, la salida esperada, el costo y el error frecuente de cada paso. Total 70 min. Cada paso termina con una comprobación numérica que debe coincidir con las cifras de esta sesión. Si una cifra no coincide, no sigas: revisa el grano o el JOIN del paso.',
    'lab-taller', 'l')

# ================================================================= CERRAR (150–180)
add('Las tablas Gold cuadran entre sí… salvo donde no deben.',
    ctable(['Tabla', 'Suma', '¿Igual a Silver?', 'Por qué'], [
        ['conversacion_dia', '6,798,932', '<span class="tag ok">sí</span>', 'cada tweet es original, respuesta o cita'],
        ['actividad_hora', '6,798,932', '<span class="tag ok">sí</span>', 'cada tweet tiene una hora'],
        ['aplicaciones_dia', '6,798,932', '<span class="tag ok">sí</span>', 'cada tweet tiene una aplicación (ocho mayores y «otras»)'],
        ['autores_alcance', '6,798,932', '<span class="tag ok">sí</span>', 'cada tweet tiene un autor con segmento'],
        ['tema_dia', '342,484 pares', '<span class="tag fal">no</span>', 'un tweet puede estar en varios temas o en ninguno'],
        ['hashtags_dia', '2,397,514 menciones', '<span class="tag fal">no</span>', 'solo hashtags con umbral; 18 % de los tweets tiene hashtag']])
    + step(1, p('Cuadrar no es opcional: si una suma no coincide, alguien perdió o repitió filas.', 'callout sm')),
    '150–156 min. El cuadre es la prueba de que el GROUP BY no perdió ni duplicó filas. Cuatro tablas con grano por tweet deben sumar 6,798,932 (el total de Silver); el paso 5 del laboratorio lo comprueba con una sola consulta. Las otras dos no cuadran por diseño: tema_dia cuenta pares tweet–tema (342,484 contra 314,527 tweets distintos) y hashtags_dia cuenta menciones con umbral. Regla: cuando una tabla NO cuadra, escribe por qué en su ficha.',
    'table', 'k')

add('Gold es una tabla que alguien tiene que volver a construir.',
    ctable(['Opción', 'Qué es', 'Límite'], [
        ['Tabla (CREATE OR REPLACE TABLE)', 'una foto que reconstruyes; las seis Gold cuestan ≈ 2.2 GB desde Silver', 'se queda vieja si nadie la vuelve a ejecutar'],
        ['Vista', 'una consulta guardada; se ejecuta en cada lectura', 'cada lectura paga la consulta completa'],
        ['Vista materializada', 'resultado que BigQuery mantiene al día', 'solo admite ciertas consultas: revisa la documentación'],
        ['Consulta programada', 'una consulta que corre a una hora fija', 'otro proceso que vigilar'],
        ['Dataform', 'SQL versionado con dependencias entre tablas', 'más piezas que aprender']])
    + step(1, '<p class="ex s5ex">' + VIEWS + ' · ' + MV + ' · ' + SCHED + ' · ' + DATAFORM + '</p>'),
    '156–162 min. Gold no se actualiza sola. Opciones: una tabla que reconstruyes (la del curso), una vista (se ejecuta cada vez), una vista materializada (BigQuery la mantiene, pero solo admite ciertas consultas; no prometas que la tuya califique sin revisar la documentación), una consulta programada o un flujo de Dataform. Para este curso basta la tabla: reconstruir las seis cuesta ≈ 2.2 GB de lectura. Regla: toda tabla Gold debe decir cuándo se construyó y quién la actualiza.',
    'table', 'k')

add('Qué puedes afirmar y qué no.',
    '<div class="two5 yn"><div class="yes"><p class="caption">SÍ PUEDES AFIRMAR</p>'
    + ex('Energía fue el tema con más tweets: 137,598 (suma de los tres grupos de idioma).', 'sm')
    + ex('En inglés, 3.38 % de los tweets del 23 de marzo mencionaba energía por palabras clave.', 'sm')
    + ex('0.84 % de los tweets son de autores con más de 1 millón de seguidores y reciben 17.66 % de los likes.', 'sm')
    + ex('50.2 % de los tweets son respuestas.', 'sm') + '</div>'
    + '<div class="no"><p class="caption">NO PUEDES AFIRMAR</p>'
    + ex('Que la gente se preocupó más de energía ese día: el archivo no trae causas.', 'sm')
    + ex('Que «mercados» en español habla de Ucrania: el 18 de marzo lo dominó «inflación» (10.57 %).', 'sm')
    + ex('Que los tweets son personas distintas ni opinión pública: 12 días, sin retweets, solo lo que la extracción encontró.', 'sm')
    + ex('Que las palabras clave miden el tema: su precisión no está medida.', 'sm') + '</div></div>',
    '162–168 min. Cierre honesto de la sesión, una sola vez. A la izquierda, lo que las tablas demuestran con sus límites escritos. A la derecha, saltos que un comité podría dar sin darse cuenta. El 18 de marzo, mercados en español llegó a 10.57 % del día, pero 11,917 de esos tweets mencionan «inflación», muchos en la expresión «guerra contra la inflación». Pedir que cada persona escriba una frase de su propio indicador con el verbo «no puedo afirmar».',
    'compare', 'k')

add('Practica con cinco preguntas.',
    ctable(['#', 'Pregunta', 'Pista', 'Respuesta de referencia'], [
        ['E1', '¿Qué % de los tweets en español habla de sanciones en todo el periodo?', 'SUM(tweets_tema) ÷ SUM(tweets_dia) en tema_dia', '0.91 %'],
        ['E2', '¿Qué hashtags del 27 de marzo no llegaron al umbral el 17?', 'NOT IN con subconsulta', '#27mar 582 · #oscars 482 · #annewill 284'],
        ['E3', '¿Qué segmento de autores recibe más likes por tweet?', 'likes ÷ tweets en autores_alcance', 'más de 1 millón: 334 likes por tweet'],
        ['E4', '¿A qué hora UTC publica más cada grupo de idioma?', 'GROUP BY grupo_idioma, hora_utc', 'en 18 · es 14 · otro 13'],
        ['E5', '¿Qué día tuvo el mayor % de respuestas?', "SUM(IF(tipo='respuesta', tweets, 0)) ÷ SUM(tweets)", '27 de marzo: 55.1 %']])
    + step(1, p('Los cinco ejercicios están dentro del laboratorio, con su consulta de apoyo.', 'callout sm')),
    '168–176 min. Ejercicios individuales de práctica: cada uno usa una tabla Gold distinta y tiene respuesta de referencia. Dejar que cada persona resuelva uno antes de mostrar la respuesta. Errores típicos: dividir por el total del archivo en E1; olvidar el umbral en E2; usar likes totales en lugar de likes por tweet en E3. Si algo no coincide, comparar el grano de la tabla con el de la pregunta.',
    'table', 'k')

add('Seis tablas listas: la siguiente sesión las convierte en gráficas.',
    '<p class="huge">0.5 MB</p><p>Todo Gold cabe en un archivo pequeño: su valor está en qué cuenta cada fila.</p>'
    '<p class="caption">Siguiente: elegir el gráfico correcto y construir un tablero honesto.</p>',
    '176–180 min. Cerrar con la idea central: Gold pesa unos 0.5 MB porque cada fila ya es una respuesta con su denominador y sus límites. La siguiente sesión usa estas mismas seis tablas para construir un tablero: qué gráfico elegir y cómo evitar que un filtro oculte lo que el indicador no puede afirmar. Pedir a cada persona que anote la ficha de su indicador favorito antes de salir.',
    'statement dark', 'k')

SLIDES = S
