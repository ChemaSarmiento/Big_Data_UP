"""S4 · Silver: tablas con significado. Fuente única del deck de la sesión 4.
Cifras: recursos/tweets/verdad.json y consultas de verificación sobre las tablas del proyecto de referencia.
La guía de laboratorio vive en especialidad-04/contenido.json; los scripts, en recursos/tweets/.
"""
import sys, json
from html import escape as e
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from guion import slide, p, step, flow, proof, lablink, source

TITLE = 'Silver: tablas con significado'
BIGIDEA = 'Silver convierte el JSON crudo en tablas con tipo, con una fila que significa una sola cosa y con reglas de calidad escritas.'

JSONF = source('BigQuery · funciones JSON', 'https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions')
SAFE = source('BigQuery · SAFE_CAST', 'https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions')
PART = source('BigQuery · tablas particionadas', 'https://docs.cloud.google.com/bigquery/docs/partitioned-tables')
CLUST = source('BigQuery · tablas con clustering', 'https://docs.cloud.google.com/bigquery/docs/clustered-tables')
NUMF = source('BigQuery · funciones de numeración', 'https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions')
ARRF = source('BigQuery · trabajar con arreglos', 'https://docs.cloud.google.com/bigquery/docs/arrays')
WITHF = source('BigQuery · cláusula WITH', 'https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax')
IAM = source('BigQuery · control de acceso con IAM', 'https://docs.cloud.google.com/bigquery/docs/access-control')
GDPR = source('Comisión Europea · principios del GDPR', 'https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr_en')
HIPAA = source('HHS · entidades cubiertas por HIPAA', 'https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html')
DATO = 'Valores de referencia del curso · tweets del 16 al 27 de marzo de 2022 · uso académico'
DATO_SQL = 'Consulta real sobre tweets_silver.tweets · valores de referencia del curso'

ABRIR = 'Abrir · 0–15 min'
COMPR = 'Comprender · 15–50 min'
APLIC = 'Aplicar · 50–70 min'
PAUSA = 'Pausa · 70–80 min'
LABOR = 'Laboratorio · 80–150 min'
CERRAR = 'Cerrar · 150–180 min'

# Las 16 combinaciones reales de las cuatro banderas: [día parcial, idioma und, texto repetido, respuesta, tweets]
COMBOS = [[0, 0, 0, 1, 3304318], [0, 0, 0, 0, 3257636], [1, 0, 0, 1, 69027], [1, 0, 0, 0, 63930], [0, 1, 0, 0, 58484],
          [0, 1, 0, 1, 36098], [0, 0, 1, 0, 3338], [0, 0, 1, 1, 2978], [1, 1, 0, 0, 1125], [0, 1, 1, 1, 1043],
          [1, 1, 0, 1, 554], [0, 1, 1, 0, 166], [1, 0, 1, 1, 164], [1, 0, 1, 0, 51], [1, 1, 1, 1, 19], [1, 1, 1, 0, 1]]

TWEETS_POR_DIA = [('16', 134871), ('17', 778608), ('18', 735033), ('19', 590028), ('20', 614483), ('21', 632383),
                  ('22', 586523), ('23', 567023), ('24', 584497), ('25', 554519), ('26', 505568), ('27', 515396)]


# ---------- ayudantes de presentación ----------
def n(x): return f'{x:,}'


def res(head, rows, hot=(), right=(), caprow=None):
    t = '<table class="s4-res"><thead><tr>' + ''.join(f'<th class="{"n" if i in right else ""}">{c}</th>' for i, c in enumerate(head)) + '</tr></thead><tbody>'
    for ri, r in enumerate(rows):
        t += f'<tr class="{"hot" if ri in hot else ""}">' + ''.join(f'<td class="{"n" if i in right else ""}">{c}</td>' for i, c in enumerate(r)) + '</tr>'
    if caprow: t += '<tr class="cap">' + ''.join(f'<td>{c}</td>' for c in caprow) + '</tr>'
    return t + '</tbody></table>'


def panel(sql=None, head=None, rows=None, meta='', title='BigQuery · resultado real', hot=(), right=(), cls='', caprow=None):
    h = f'<div class="s4-panel {cls}"><div class="s4-bar"><span>{title}</span>' + (f'<b>{meta}</b>' if meta else '') + '</div>'
    if sql: h += '<pre class="s4-sql" tabindex="0"><code>' + e(sql) + '</code></pre>'
    if rows is not None: h += res(head, rows, hot, right, caprow)
    return h + '</div>'


def tbl(head, rows, cls='', right=()):
    t = f'<table class="s4-tbl {cls}"><thead><tr>' + ''.join(f'<th>{c}</th>' for c in head) + '</tr></thead><tbody>'
    for r in rows:
        t += '<tr>' + ''.join(f'<td class="{"n" if j in right else ""}" data-l="{head[j]}">{c}</td>' for j, c in enumerate(r)) + '</tr>'
    return t + '</tbody></table>'


def bars(items, lw=230, vw=190, cls=''):
    h = f'<div class="s4-bars {cls}" style="--lw:{lw}px;--vw:{vw}px">'
    for it in items:
        label, w, val = it[0], it[1], it[2]
        k = it[3] if len(it) > 3 else ''
        h += f'<div class="s4-barrow {k}"><span>{label}</span><div class="trk"><i style="--w:{w:.2f}%"></i></div><b>{val}</b></div>'
    return h + '</div>'


def kpi(big, label, cls=''): return f'<div class="s4-kpi {cls}"><b>{big}</b><span>{label}</span></div>'


def kv(pairs, cols=2):
    return f'<dl class="s4-kv c{cols}">' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in pairs) + '</dl>'


def layer(tag, big, body, small='', cls=''):
    return f'<div class="s4-layer {cls}"><span class="tag">{tag}</span><b>{big}</b><p>{body}</p>' + (f'<small>{small}</small>' if small else '') + '</div>'


def dias_svg():
    mx = 778608
    W, H, base, top = 1240, 380, 316, 58
    bw, gap = 78, 24
    x0 = 20
    s = f'<svg class="s4-svg" viewBox="0 0 {W} {H}" role="img" aria-label="Tweets por día del 16 al 27 de marzo de 2022; el 16 de marzo solo tiene cuatro horas y 134,871 tweets">'
    s += f'<line class="ax" x1="10" y1="{base}" x2="{W - 10}" y2="{base}"/>'
    for i, (d, v) in enumerate(TWEETS_POR_DIA):
        h = (base - top) * v / mx
        x = x0 + i * (bw + gap)
        hot = d == '16'
        s += f'<rect class="b4{" hot" if hot else ""}" x="{x}" y="{base - h:.1f}" width="{bw}" height="{h:.1f}"/>'
        s += f'<text class="val{" hotv" if hot else ""}" x="{x + bw / 2}" y="{base - h - 10:.1f}">{v / 1000:.0f} mil</text>'
        s += f'<text class="lab" x="{x + bw / 2}" y="{base + 32}">{d}</text>'
    s += f'<text class="lab" x="{W / 2}" y="{base + 62}">marzo de 2022</text>'
    s += f'<text class="annt" x="{x0 + bw / 2}" y="{base + 62}" style="text-anchor:middle">4 h</text>'
    return s + '</svg>'


SLIDES = []


def add(title, body, nota, layout='plain', phase=COMPR, src=DATO):
    SLIDES.append(slide(title, body, nota, layout, phase, src))


# ====================== ABRIR 0–15 ======================
add('Silver: tablas con significado',
    '<div><p class="overline">Sesión 4 · Silver</p><h1>Silver: tablas<br>con significado.</h1><p class="lede">Del JSON crudo a tablas<br>que se pueden contar y unir.</p></div>'
    '<div class="s4-coverstats">' + kpi(n(6798932), 'tweets · una fila por tweet') + kpi(n(1872074), 'autores · una fila por autor') + kpi(n(3339839), 'hashtags · una fila por tweet y hashtag', 'hot') + '</div>',
    '0–3 min. Hoy salen tres tablas de un mismo archivo, y las tres cifras son correctas. Pregunta al grupo: ¿cómo puede el mismo archivo dar 6.8 millones de filas en una tabla, 1.9 millones en otra y 3.3 millones en una tercera? [pausa 3 s] Sin dar la respuesta: al terminar la sesión la darán ellos. La idea que recorre la clase es el grano: qué significa una fila.',
    'cover dark', ABRIR, DATO)

add('Bronze guarda todo, pero no responde ninguna pregunta',
    '<div class="s4-cols c2"><div class="stack">'
    '<div class="s4-panel json"><div class="s4-bar"><span>Bronze · una fila = un tweet completo</span><b>2,411 caracteres</b></div>'
    '<pre class="s4-sql" tabindex="0"><code>' + e('{"url": ".../skift/status/1508232397162258434",\n "date": "2022-03-27T23:59:59+00:00",\n "content": "Africa\'s Airline Recovery Faces Setback\n   on Ukraine War\'s Higher Fuel Costs ...",\n "id": 1508232397162258434, "lang": "en",\n "user": {"username": "skift", "verified": true,\n          "followersCount": 87507, ...},\n "likeCount": 0, ...}') + '</code></pre></div>'
    '<p class="s4-fine">Fragmento del primer registro de la tabla <code>tweets_bronze.entrada</code>. Son 29 campos y el autor trae otros 23 dentro.</p></div>'
    '<div class="stack">' + panel('SELECT idioma\nFROM tweets_bronze.entrada', title='Consulta · pregunta por el idioma')
    + '<div class="s4-err"><b>Error</b><span>Unrecognized name: idioma at [1:8]</span></div>'
    + step(1, '<p class="callout">El idioma sí está ahí dentro, pero para BigQuery Bronze tiene una sola columna: <code>value</code>, un texto largo.</p>') + '</div></div>',
    '3–8 min. Repaso rápido de la sesión 3: Bronze es el archivo tal como llegó, un tweet por fila dentro de una sola columna de texto llamada value. A la izquierda un fragmento real del primer registro (la línea completa mide 2,411 caracteres). A la derecha, el error real al pedir la columna idioma: no existe. Pregunta al grupo: ¿qué hay que hacer para poder filtrar por idioma? [pausa 3 s] Respuesta: abrir el texto, tomar el dato de su camino y guardarlo como columna con su tipo. Eso es Silver.',
    'hook', ABRIR, 'Primer registro de tweets_bronze.entrada · valores de referencia del curso · uso académico')

add('Silver promete cuatro cosas',
    '<div class="s4-cols c21"><div class="s4-steps">'
    + step(0, '<div><b>1 · Columnas con tipo</b><span>«likes» deja de ser texto y pasa a número. Ordenar «9», «100» y «25» como texto da 100, 25, 9.</span></div>')
    + step(1, '<div><b>2 · Una fila significa una sola cosa</b><span>En <code>tweets</code> una fila es un tweet; en <code>autores</code>, un autor; en <code>hashtags</code>, un tweet con un hashtag.</span></div>')
    + step(2, '<div><b>3 · Reglas escritas</b><span>Qué se marca, qué se excluye, a cuántas filas toca cada regla y quién decide.</span></div>')
    + step(3, '<div><b>4 · Bronze queda intacto</b><span>Silver se calcula desde Bronze. Si una regla cambia, se vuelve a calcular; nada se corrige a mano.</span></div>')
    + '</div><div class="stack">' + kpi('1 → 18', 'columnas por tweet: de un texto a campos con tipo') + kpi('22.04 → 2.28 GiB', 'de Bronze a la tabla Silver de tweets')
    + kpi('6,798,932', 'filas en Bronze y en Silver: no se pierde ningún tweet', 'hot') + '</div></div>',
    '8–15 min. Silver no es una limpieza mágica: es un contrato con cuatro promesas. Ir de una en una con clic. Para la primera, mostrar en voz alta que «100» va antes que «9» cuando son texto. En la segunda, adelantar que hoy construimos tres tablas con tres significados de fila. En la tercera, aclarar que una regla puede marcar sin borrar. La cuarta explica por qué guardamos Bronze: si cambia una regla, se recalcula. A la derecha, tres cifras medidas: 1 columna en Bronze y 18 en Silver; 22.04 GiB frente a 2.28 GiB; mismas filas.',
    'path', ABRIR, DATO)

# ====================== COMPRENDER 15–50 ======================
add('JSON_VALUE sigue el camino hasta el dato',
    '<div class="stack">' + tbl(['Camino dentro del JSON', 'Valor en este tweet', 'Columna en Silver'],
        [['<code>$.id</code>', '1508232397162258434', '<code>tweet_id</code> · INT64'],
         ['<code>$.date</code>', '2022-03-27T23:59:59+00:00', '<code>fecha_hora</code> · TIMESTAMP'],
         ['<code>$.lang</code>', 'en', '<code>idioma</code> · STRING'],
         ['<code>$.user.username</code>', 'skift', '<code>usuario</code> · STRING'],
         ['<code>$.user.followersCount</code>', '87507', '<code>seguidores</code> · INT64'],
         ['<code>$.likeCount</code>', '0', '<code>likes</code> · INT64']], cls='traps')
    + '<p class="s4-note">El <code>$</code> es el tweet completo y cada punto baja un nivel: <code>$.user.username</code> entra a <code>user</code> y toma <code>username</code>.</p>'
    + step(1, '<p class="callout">JSON_VALUE siempre devuelve texto. Por eso, cuando el campo es número o fecha, se convierte después.</p>') + '</div>',
    '15–18 min. Primera herramienta: JSON_VALUE(value, camino). Leer la tabla de izquierda a derecha con el mismo tweet de la diapositiva anterior: el camino, lo que hay en ese lugar y la columna que queda. Pregunta al grupo: ¿por qué user.username lleva un punto más? [pausa 3 s] Porque user es un objeto dentro del tweet. Error típico: escribir mal el camino; BigQuery no avisa, devuelve NULL. Por eso al final se revisan los NULL.',
    'path', COMPR, JSONF)

add('SAFE_CAST convierte sin romper',
    '<div class="s4-cols c2"><div class="stack">'
    + panel("SELECT\n  SAFE_CAST('15' AS INT64) AS texto_15,\n  SAFE_CAST('abc' AS INT64) AS texto_abc,\n  SAFE_CAST('23/03/2022' AS TIMESTAMP) AS fecha_rara",
            ['texto_15', 'texto_abc', 'fecha_rara'], [['15', 'NULL', 'NULL']], meta='0 bytes', hot=(0,), right=(0,), cls='code18')
    + '<p class="s4-note">Si el valor no se puede convertir, <code>SAFE_CAST</code> devuelve NULL en lugar de detener toda la consulta.</p></div>'
    '<div class="stack"><div class="s4-cols c2" style="gap:20px">'
    + panel("SELECT valor\nFROM UNNEST(['9','100','25']) AS valor\nORDER BY valor", ['como texto'], [['100'], ['25'], ['9']], title='Ordenado como texto', hot=(0, 1, 2), cls='mini code18')
    + panel("SELECT valor\nFROM UNNEST([9,100,25]) AS valor\nORDER BY valor", ['como número'], [['9'], ['25'], ['100']], title='Ordenado como número', cls='mini code18')
    + '</div>' + step(1, '<p class="callout">En Silver, <code>tweet_id</code> y <code>fecha_hora</code> no tienen ningún NULL: 0 y 0. Aquí SAFE_CAST no encontró nada que corregir.</p>') + '</div></div>',
    '18–21 min. SAFE_CAST es la segunda herramienta: convierte el texto al tipo correcto y, si no puede, deja NULL en vez de romper. Mostrar los tres casos reales del panel (consulta sin costo, 0 bytes). A la derecha, por qué importa el tipo: el mismo conjunto de valores ordena distinto como texto que como número. Dato real de esta tabla: ningún NULL en tweet_id ni en fecha_hora, y eso también es información: el archivo trae esos campos completos. Error típico: usar CAST, que sí se detiene con el primer valor inválido.',
    'query', COMPR, SAFE)

add('El script de Silver se lee de arriba abajo',
    '<div class="s4-cols c21">'
    + panel('CREATE OR REPLACE TABLE tweets_silver.tweets\nPARTITION BY fecha\nCLUSTER BY idioma AS\nSELECT\n  SAFE_CAST(JSON_VALUE(value, \'$.id\') AS INT64)\n    AS tweet_id,\n  SAFE_CAST(JSON_VALUE(value, \'$.date\') AS TIMESTAMP)\n    AS fecha_hora,\n  JSON_VALUE(value, \'$.lang\') AS idioma,\n  JSON_VALUE(value, \'$.user.username\') AS usuario,\n  SAFE_CAST(JSON_VALUE(value, \'$.likeCount\') AS INT64)\n    AS likes,\n  ARRAY(SELECT LOWER(h) FROM UNNEST(\n    JSON_VALUE_ARRAY(value, \'$.hashtags\')) AS h)\n    AS hashtags,\n  -- ... 12 columnas más\nFROM tweets_bronze.entrada;', title='20_silver_tweets.sql · versión abreviada', cls='code18')
    + '<div class="s4-steps">'
    + step(0, '<div><b>CREATE OR REPLACE TABLE … AS SELECT</b><span>Guarda el resultado de la consulta como una tabla nueva.</span></div>')
    + step(1, '<div><b>Una línea = una columna</b><span>Cada <code>AS nombre</code> es una columna de Silver.</span></div>')
    + step(2, '<div><b>PARTITION BY · CLUSTER BY</b><span>Cómo se guarda: por día y ordenada por idioma. Lo usaremos para pagar menos.</span></div>')
    + step(3, '<div><b>ARRAY( … UNNEST … )</b><span>Los hashtags son una lista dentro de una celda: un <i>arreglo</i>.</span></div>')
    + '</div></div>',
    '21–24 min. Leer el script completo es más sencillo de lo que parece: una consulta SELECT cuyos resultados se guardan como tabla. Mostrar una versión abreviada de cinco columnas más el arreglo de hashtags; el archivo real, 20_silver_tweets.sql, tiene 18 columnas. Primera aparición de UNNEST y de arreglo: una celda con varios valores, por ejemplo [ukraine, putin]. Aquí solo se baja a minúsculas; la tabla hashtags lo usará para crear filas. Costo: una lectura completa de Bronze, 23.67 GB de referencia; se ejecuta una vez.',
    'query', COMPR, DATO)

add('De 29 campos a 18 columnas: se queda lo que usarás',
    '<div class="s4-cols c2" style="align-items:start"><div class="stack">'
    + bars([('Bronze · lectura completa', 100, '23.67 GB', 'dim'), ('Silver · todas las columnas', 10.36, '2.45 GB', 'hot')], lw=290, vw=130)
    + '<p class="s4-note">Casi 10 veces menos: Silver guarda 18 campos con tipo y no el JSON completo con 29 campos y 23 más del autor.</p>'
    + '<div class="s4-steps">'
    + '<div><b>Texto → número</b><span><code>likeCount</code> y <code>followersCount</code> pasan a INT64.</span></div>'
    + '<div><b>Texto → fecha</b><span><code>date</code> pasa a TIMESTAMP y a una columna DATE.</span></div>'
    + '<div><b>Anidado → plano</b><span><code>user.username</code> pasa a la columna <code>usuario</code>.</span></div>'
    + '<div><b>Lista → arreglo</b><span><code>hashtags</code> queda como lista en minúsculas.</span></div></div></div>'
    + '<div>' + kv([('tweet_id', '1508232397162258434'), ('fecha_hora', '2022-03-27 23:59:59'), ('idioma', 'en'), ('texto', "Africa's Airline Recovery…"),
                   ('usuario', 'skift'), ('verificado', 'true'), ('seguidores', '87507'), ('ubicación', 'New York City, NY'),
                   ('likes · retuits', '0 · 0'), ('respuestas · citas', '0 · 0'), ('es_respuesta', 'false'), ('aplicacion', 'HubSpot')], cols=1)
    + '<p class="s4-fine">Una fila de Silver: el mismo tweet de la diapositiva anterior.</p></div></div>',
    '24–27 min. Dos ideas. Izquierda: el tamaño. Una lectura de toda la tabla Silver factura 2.45 GB frente a 23.67 GB de Bronze, casi diez veces menos, porque no guarda campos que no usaremos y porque número y fecha ocupan menos que su versión en texto. Derecha: el mismo tweet que vimos como JSON, ahora una fila con columnas tipadas (se muestran 12 de las 18). Pregunta al grupo: ¿qué dato del JSON original se perdió? [pausa 3 s] Se perdieron los campos que decidimos no usar; siguen en Bronze.',
    'size', COMPR, DATO)

add('Una fila debe significar una sola cosa: el grano',
    '<div class="s4-layers" style="grid-template-columns:1fr 1fr 1fr;gap:18px">'
    + layer('TWEETS · una fila = un tweet', n(6798932), 'Texto, fecha, idioma, autor y likes de cada tweet.', 'tweet_id es único: 6,798,932 ids distintos.')
    + layer('AUTORES · una fila = un autor', n(1872074), 'Cuántos seguidores tiene, si está verificado y dónde dice estar.', 'Un autor publica varios tweets; aquí aparece una vez.', 'focus')
    + layer('HASHTAGS · una fila = tweet + hashtag', n(3339839), 'Un tweet con tres hashtags ocupa tres filas.', 'Solo 1,226,642 tweets tienen hashtags.') + '</div>'
    + step(1, '<p class="callout">Ejemplo real: un tweet de AFP con tres hashtags es 1 fila en <code>tweets</code>, 1 fila de AFP en <code>autores</code> y 3 filas en <code>hashtags</code>.</p>'),
    '27–30 min. El grano es la pregunta «¿qué significa una fila?». Tres tablas, tres granos, tres conteos; ninguno está mal. Volver a la pregunta de la portada: 6.8 millones son tweets, 1.9 millones son autores, 3.3 millones son pares tweet-hashtag. Con el clic, un caso concreto: el tweet de AFP #UPDATE sobre Macron tiene tres hashtags (update, macron, ukraine): una fila en tweets, una fila de AFP en autores y tres filas en hashtags. Error típico: sumar filas de tablas con grano distinto.',
    'grain', COMPR, DATO)

add('ROW_NUMBER numera las filas dentro de cada autor',
    '<div class="s4-cols c21">'
    + panel("SELECT tweet_id, fecha_hora, seguidores,\n       ROW_NUMBER() OVER (\n         PARTITION BY usuario\n         ORDER BY fecha_hora DESC) AS orden\nFROM tweets_silver.tweets\nWHERE usuario = 'skift'", ['tweet_id', 'fecha_hora', 'seguidores', 'orden'],
            [['1508232397162258434', '2022-03-27 23:59:59', '87507', '1'], ['1507960605889683458', '2022-03-27 05:59:59', '87507', '2'], ['1507671384033357827', '2022-03-26 10:50:43', '87507', '3'],
             ['1507000006317907977', '2022-03-24 14:22:54', '87510', '4'], ['…', '…', '…', '…'], ['1504503847837847567', '2022-03-17 17:04:04', '87529', '10']],
            meta='10 filas · 253 MB', hot=(0,), right=(2, 3), cls='code18')
    + '<div class="s4-steps">'
    + step(0, '<div><b>PARTITION BY usuario</b><span>Reinicia la numeración para cada autor.</span></div>')
    + step(1, '<div><b>ORDER BY fecha_hora DESC</b><span>El tweet más reciente recibe el 1.</span></div>')
    + step(2, '<div><b>orden = 1</b><span>Es la fila que nos quedamos: el dato más reciente del autor. Fíjate en <code>seguidores</code>: bajó de 87,529 a 87,507 durante el periodo.</span></div>')
    + '</div></div>',
    '30–33 min. Problema: un autor aparece en muchas filas y sus seguidores cambian con el tiempo (skift: 10 tweets y 8 cifras distintas de seguidores). Para una tabla de autores necesitamos una sola fila por autor. ROW_NUMBER numera filas; OVER (PARTITION BY ... ORDER BY ...) define cómo: reiniciar para cada autor, el más reciente primero. La fila con orden = 1 es la que se queda. Panel real con 10 filas de skift (se muestran 5). Pregunta al grupo: ¿qué pasaría con ORDER BY fecha_hora sin DESC? [pausa 3 s] Nos quedaríamos con el dato más antiguo.',
    'window', COMPR, NUMF)

add('Un CTE le pone nombre a un paso para leer el resto',
    '<div class="s4-cols c12">'
    + panel('CREATE OR REPLACE TABLE tweets_silver.autores AS\nWITH ordenados AS (\n  SELECT usuario, usuario_verificado, seguidores,\n    NULLIF(TRIM(ubicacion_usuario), \'\')\n      AS ubicacion,\n    ROW_NUMBER() OVER (\n      PARTITION BY usuario\n      ORDER BY fecha_hora DESC) AS orden,\n    COUNT(*) OVER (PARTITION BY usuario)\n      AS tweets_en_archivo\n  FROM tweets_silver.tweets\n)\nSELECT usuario, usuario_verificado,\n  seguidores, ubicacion, tweets_en_archivo\nFROM ordenados\nWHERE orden = 1;', title='21_silver_autores.sql · formato ajustado', cls='code18')
    + '<div class="stack"><div class="s4-steps">'
    + step(0, '<div><b>WITH ordenados AS ( … )</b><span>Un CTE: un paso intermedio con nombre. Se lee como una receta: primero «ordenados», luego el resultado.</span></div>')
    + step(1, '<div><b>NULLIF(TRIM(…), \'\')</b><span>Quita espacios y convierte el vacío en NULL: «sin dato» deja de parecer un texto.</span></div>')
    + step(2, '<div><b>WHERE orden = 1</b><span>Solo pasa la fila más reciente de cada autor.</span></div>')
    + '</div>' + step(3, panel(None, ['usuario', 'verificado', 'seguidores', 'ubicación', 'tweets'], [['skift', 'true', '87507', 'New York City, NY', '10']], meta='1 fila', right=(2, 4), cls='mini')) + '</div></div>',
    '33–36 min. WITH define un CTE (expresión de tabla común): un paso con nombre que luego usamos como si fuera una tabla. No agrega capacidad; agrega legibilidad. Leer el script de arriba hacia abajo. Además de ROW_NUMBER usamos COUNT(*) OVER (PARTITION BY usuario) para conservar cuántos tweets tenía el autor en el archivo. Resultado: skift queda en una sola fila con 10 tweets. La tabla completa tiene 1,872,074 autores y la suma de tweets_en_archivo vuelve a dar 6,798,932: es el cuadre que revisaremos. Costo de referencia: 280 MB.',
    'cte', COMPR, WITHF)

add('Un CTE también sirve para resumir un resumen',
    '<div class="s4-cols c12"><div class="stack">'
    + panel('WITH tweets_por_autor AS (\n  SELECT usuario, COUNT(*) AS tweets\n  FROM tweets_silver.tweets\n  GROUP BY usuario\n)\nSELECT CASE WHEN tweets = 1 THEN \'1\'\n            WHEN tweets = 2 THEN \'2\'\n            WHEN tweets <= 5 THEN \'3 a 5\'\n            WHEN tweets <= 20 THEN \'6 a 20\'\n            ELSE \'más de 20\' END AS tramo,\n       COUNT(*) AS autores,\n       SUM(tweets) AS tweets_totales\nFROM tweets_por_autor\nGROUP BY tramo', title='Primero cuenta por autor; después cuenta autores por tramo', cls='code18') + '</div>'
    '<div class="stack">' + bars([('1 tweet', 58.3, '1,091,593', 'dim'), ('2 tweets', 15.4, '288,520', 'dim'), ('3 a 5', 14.2, '266,027', 'dim'), ('6 a 20', 9.6, '179,353', 'dim'), ('más de 20', 2.5, '46,581', 'hot')], lw=120, vw=140, cls='slim')
    + '<p class="s4-note">Autores por tramo: el 58 % publicó un solo tweet. Los 46,581 autores con más de 20 tweets (2.5 %) publicaron 2,368,524 tweets: el 34.8 % del archivo.</p></div></div>',
    '36–39 min. Segundo uso del CTE: primero un GROUP BY (tweets por autor) y encima otro GROUP BY (autores por tramo). Sin el nombre del paso intermedio habría que anidar consultas dentro de consultas. Resultado real: 1,091,593 autores publicaron un solo tweet; 46,581 autores publicaron más de 20 y entre todos suman 2,368,524 tweets, el 34.8 % del archivo. Pregunta al grupo: ¿contar tweets es contar personas? [pausa 3 s] No: unos pocos autores producen mucho. Costo de referencia: 90 MB.',
    'cte', COMPR, DATO_SQL)

add('UNNEST convierte una lista en filas',
    '<div class="s4-cols c2"><div class="stack">'
    + panel("SELECT tweet_id, usuario, hashtags\nFROM tweets_silver.tweets\nWHERE tweet_id = 1508054980313370628", ['usuario', 'hashtags'], [['AFP', '["update", "macron", "ukraine"]']], meta='1 fila', hot=(0,), cls='mini')
    + '<p class="s4-note">Una celda, tres valores: así llegan los hashtags desde el JSON.</p>'
    + step(1, panel("SELECT DISTINCT t.tweet_id, t.fecha, t.idioma,\n       h AS hashtag\nFROM tweets_silver.tweets AS t,\n     UNNEST(t.hashtags) AS h", cls='mini', title='22_silver_hashtags.sql · el corazón')) + '</div>'
    '<div class="stack">' + panel(None, ['tweet_id', 'hashtag'], [['1508054980313370628', 'macron'], ['1508054980313370628', 'ukraine'], ['1508054980313370628', 'update']], meta='3 filas', hot=(0, 1, 2), cls='mini', title='Tabla hashtags')
    + step(2, '<p class="callout">DISTINCT quita los hashtags repetidos dentro de un mismo tweet: había 3,369,433 en los arreglos y quedaron 3,339,839 filas.</p>') + '</div></div>',
    '39–42 min. UNNEST es la tercera herramienta nueva: toma una lista guardada en una celda y la despliega en una fila por elemento. Seguir el ejemplo real de AFP: una fila con tres hashtags en tweets se vuelve tres filas en hashtags. Con el segundo clic, el corazón del script 22. Con el tercero, por qué DISTINCT: un tweet puede escribir el mismo hashtag dos veces y no queremos contarlo doble (3,369,433 menciones en arreglos frente a 3,339,839 filas). Costo de referencia de crear la tabla: 174 MB.',
    'unnest', COMPR, ARRF)

add('Al unir tablas con grano distinto, las filas se multiplican',
    '<div class="s4-cols c2"><div class="stack">'
    + panel('SELECT COUNT(*) AS filas_del_join,\n       COUNT(DISTINCT t.tweet_id) AS tweets_distintos\nFROM tweets_silver.tweets AS t\nJOIN tweets_silver.hashtags AS h USING (tweet_id)', ['filas_del_join', 'tweets_distintos'], [['3339839', '1226642']], meta='81 MB', hot=(0,), right=(0, 1))
    + '<p class="s4-note">Cada tweet aparece una vez por cada hashtag: 1,226,642 tweets se vuelven 3,339,839 filas, 2.7 por tweet en promedio.</p></div>'
    '<div class="stack">' + bars([('ukraine · menciones', 100, '514,337', 'dim'), ('ukraine · tweets', 98.7, '507,762', 'hot')], lw=250, vw=130)
    + '<p class="s4-note">Contar menciones y contar tweets no da lo mismo: sobran 6,575 menciones porque algunos tweets repiten «ukraine» dentro del mismo tweet.</p>'
    + step(1, '<p class="callout">Regla práctica: después de unir, cuenta con <code>COUNT(DISTINCT tweet_id)</code>, no con <code>COUNT(*)</code>.</p>') + '</div></div>',
    '42–45 min. La consecuencia práctica del grano. Al unir tweets con hashtags cada tweet se repite tantas veces como hashtags tenga: 1,226,642 tweets dan 3,339,839 filas. Si alguien cuenta COUNT(*) sobre ese resultado y dice «tweets», está contando mal. A la derecha, un caso real: ukraine aparece 514,337 veces en los arreglos pero 507,762 tweets lo usan; las 6,575 menciones de diferencia vienen de tweets que lo repiten. Pregunta al grupo: ¿qué conteo usarían en un reporte? [pausa 3 s] Depende de la pregunta, y la tabla correcta ya tiene DISTINCT.',
    'join', COMPR, DATO_SQL)

add('Partición y clustering: leer menos para pagar menos',
    '<div class="s4-cols c2"><div class="stack"><div class="s4-days opts" data-demo="s4-particion" role="group" aria-label="Elige qué filtros usar y mira cuántos bytes lee BigQuery">'
    '<button type="button" data-mb="1231.6" aria-pressed="false"><b>Toda la tabla</b><span>SELECT texto</span></button>'
    '<button type="button" data-mb="107.5" aria-pressed="true"><b>Un día</b><span>… WHERE fecha = «día»</span></button>'
    '<button type="button" data-mb="33.3" aria-pressed="false"><b>Un día y un idioma</b><span>… AND idioma = «es»</span></button></div>'
    '<p class="s4-note"><b>Partición</b>: BigQuery guarda cada día aparte. <b>Clustering</b>: dentro de cada día ordena por idioma. Si tu filtro usa esas columnas, salta lo que no necesita.</p></div>'
    '<div class="stack"><div class="s4-readout"><span>Bytes que lee BigQuery</span><b class="signal"><i data-out="mb">107.5</i> MB</b><span>Del texto completo (1,231.6 MB)</span><b><i data-out="pct">8.7</i> %</b></div>'
    + step(1, '<p class="callout">LIMIT no abarata: <code>SELECT * … LIMIT 10</code> lee las 18 columnas completas, 2.45 GB. Lo que abarata es filtrar por fecha o idioma.</p>') + '</div></div>',
    '45–50 min. Cómo se guarda la tabla afecta lo que pagas. Silver está particionada por fecha (un cajón por día) y agrupada por idioma (clustering: dentro de cada día, ordenada por idioma). Probar los tres botones: el estimador y el trabajo real coincidieron en las tres mediciones, 1,231.6 MB para todo el texto, 107.5 MB para un día y 33.3 MB para un día y el idioma español. Aclarar el error típico: LIMIT limita las filas que ves, no los bytes que se leen. Esto vuelve en el laboratorio, paso 6.',
    'partition', COMPR, PART)

# ====================== APLICAR 50–70 ======================
add('Seis cosas que revisar antes de contar',
    tbl(['Qué revisamos', 'Lo que mostró el archivo', 'Decisión'],
        [['Día parcial', '16 de marzo: 134,871 tweets, solo de 20:00 a 23:59 UTC', 'Marcar'],
         ['Texto repetido', 'Un mismo texto 421 veces, de 416 cuentas', 'Marcar'],
         ['Idioma sin determinar', '97,490 tweets con idioma «und» (1.4 %)', 'Marcar'],
         ['Ubicación vacía', '2,664,367 tweets cuyo autor no puso ubicación (39.2 %)', 'Conservar el vacío'],
         ['Likes de cola larga', 'Mediana 0; 0.2 % de los tweets reúne el 60.4 % de los likes', 'No excluir'],
         ['Qué es una fila', '50.2 % son respuestas; 40.2 %, originales', 'Marcar el tipo']], cls='traps wide')
    + step(1, '<p class="callout">Cada decisión se escribe como regla: qué hace, a cuántas filas toca, quién la decide y qué cambia en los números.</p>'),
    '50–53 min. Panorama de lo que sigue: seis revisiones que salieron de medir el archivo, no de suponer. Cada una termina en una decisión: marcar, conservar o no excluir. Atención: marcar no es borrar; la fila sigue en Silver con una columna verdadero/falso. Las siguientes cinco diapositivas muestran la evidencia de cada fila de la tabla; después un simulador deja ver cuánto cambian los conteos. Pregunta al grupo: ¿cuál de las seis creen que cambia más los números? [pausa 3 s]',
    'matrix', APLIC, DATO_SQL)

add('El 16 de marzo solo tiene cuatro horas de datos',
    '<div class="stack">' + dias_svg()
    + '<p class="s4-note">Tweets por día. El 16 empieza a las 20:00 UTC y tiene 134,871 tweets; un día completo como el 17 tiene 778,608. Comparar sus totales dice «el tema cayó», cuando en realidad el 16 es un día incompleto.</p>'
    + step(1, '<p class="callout">Regla: columna <code>dia_parcial</code> verdadera para 2022-03-16. No se borra; se decide en cada análisis.</p>') + '</div>',
    '53–56 min. Primera trampa. La gráfica es real: tweets por día, doce barras. La primera es mucho más baja y no porque haya menos conversación: el archivo empieza esa tarde y solo cubre de 20:00 a 23:59 UTC (por hora: 12,684, 45,347, 41,166 y 35,674 tweets). Pregunta al grupo: ¿qué conclusión errónea sacaría alguien que solo mira el total diario? [pausa 3 s] Que el tema creció el día 17. La regla: marcar el día parcial para poder excluirlo o compararlo con horas equivalentes.',
    'chart', APLIC, DATO_SQL)

add('Un mismo texto puede repetirse cientos de veces',
    '<div class="stack">' + panel('WITH por_texto AS (\n  SELECT texto, COUNT(*) AS copias, COUNT(DISTINCT usuario) AS cuentas\n  FROM tweets_silver.tweets GROUP BY texto)\nSELECT SUBSTR(texto, 1, 40) AS inicio, copias, cuentas\nFROM por_texto ORDER BY copias DESC LIMIT 3',
        ['inicio', 'copias', 'cuentas'], [['@nathaliejacoby1 Putin', '421', '416'], ["@wiki_war's account is temporarily unavailable…", '375', '1'], ['@joncoopertweets Putin', '362', '352']],
        meta='1.3 GB', hot=(1,), right=(1, 2), cls='code18')
    + '<div class="s4-cols c2" style="gap:30px">' + kpi('416 cuentas', 'escribieron lo mismo: una campaña de respuestas, no una opinión') + kpi('1 cuenta', 'publicó el mismo aviso 375 veces', 'hot') + '</div>'
    + step(1, '<p class="callout">Aviso real: si el nombre del paso se llama igual que la columna (<code>… AS texto … GROUP BY texto</code>), BigQuery agrupa por el valor recortado y dice 1,424 copias. Con el CTE, 421.</p>') + '</div>',
    '56–59 min. Segunda trampa. Tres textos exactamente iguales: 421 copias de 416 cuentas distintas (muchas personas escribiendo la misma frase), 375 copias de una sola cuenta (un aviso automático) y 362 de 352 cuentas. El conteo de tweets no distingue entre ambos casos. Umbral que usaremos: 20 copias o más marca 182 textos y 7,760 tweets. Anécdota real con el clic: escribir el SELECT con un alias igual al nombre de la columna agrupa por el texto recortado y da 1,424; el CTE evita la ambigüedad. Lección: revisar un resultado extraño antes de publicarlo.',
    'dup', APLIC, DATO_SQL)

add('Idioma sin determinar y ubicación vacía: dato ausente no es cero',
    '<div class="s4-cols c2"><div class="stack">' + kpi('97,490', 'tweets con idioma «und»: Twitter no pudo determinarlo (1.4 %)', 'hot')
    + '<p class="s4-note">«und» es un valor, no un NULL. Si filtras por <code>idioma IN (\'en\', \'es\')</code> estos tweets desaparecen sin aviso.</p></div>'
    '<div class="stack">' + kpi('2,664,367', 'tweets de autores sin ubicación (39.2 %): cadena vacía o solo espacios')
    + '<p class="s4-note">En autores, <code>NULLIF(TRIM(…), \'\')</code> convierte ese vacío en NULL. Así «no sabemos» se ve como NULL y no como un texto.</p></div></div>'
    + step(1, '<p class="callout">Regla: conservar el vacío y marcarlo. Inventar un idioma o una ubicación sería peor que no tenerlos.</p>'),
    '59–61 min. Tercera y cuarta trampas, ambas de datos ausentes. «und» significa indeterminado y es un valor de texto; ningún filtro lo atrapa a menos que lo nombres. La ubicación es texto libre que el autor escribe y 39.2 % la dejó vacía. Dos decisiones: marcar «und» (columna idioma_desconocido) y convertir la ubicación vacía en NULL para que cuente como ausente. Nunca rellenar. Pregunta al grupo: ¿qué pasa con el porcentaje de tweets en español si descartamos «und»? [pausa 3 s] Cambia el denominador.',
    'null', APLIC, DATO_SQL)

add('El promedio de likes engaña',
    '<div class="s4-cols c2"><div class="stack">'
    + bars([('Tweets con 0 likes', 54.4, '54.4 %', 'dim'), ('Tweets con 1,000+ likes', 0.2, '13,928 · 0.2 %', 'hot'), ('Likes que reúnen esos tweets', 60.4, '60.4 %', 'hot')], lw=300, vw=190)
    + '<p class="s4-note">De 107,966,871 likes, 65,176,277 son de solo 13,928 tweets.</p></div>'
    '<div class="stack">' + panel(None, ['medida', 'valor'], [['promedio', '15.88'], ['mediana', '0'], ['máximo', '195,299']], meta='tweets_silver.tweets', hot=(1,), right=(1,), cls='mini', title='Tres formas de resumir los likes')
    + step(1, '<p class="callout">No se excluyen los virales. Se usa la mediana y los percentiles, y se dice cuántos tweets concentran el interés.</p>') + '</div></div>',
    '61–64 min. Quinta trampa, esta vez de valores extremos. Más de la mitad de los tweets no recibió ningún like, y 13,928 tweets (0.2 %) reúnen el 60.4 % de todos los likes. Por eso el promedio de 15.88 no describe a ningún tweet típico: la mediana es 0. Decisión: no es un error, es la forma real de la distribución; se reporta mediana y percentiles. Pregunta al grupo: ¿borrarían los tweets virales como si fueran atípicos? [pausa 3 s] No: son el fenómeno que queremos entender.',
    'dist', APLIC, DATO_SQL)

add('La mitad son respuestas; los originales reúnen los likes',
    '<div class="s4-cols c2"><div class="stack"><p class="s4-fine">Porcentaje de los tweets de cada tipo</p>'
    + bars([('Respuestas', 50.2, '3,414,201 · 50.2 %', 'dim'), ('Originales', 40.2, '2,729,906 · 40.2 %', 'hot'), ('Citas', 9.6, '654,825 · 9.6 %', 'dim')], lw=150, vw=270)
    + '</div><div class="stack"><p class="s4-fine">Porcentaje de los likes de cada tipo</p>'
    + bars([('Respuestas', 15.2, '15.2 %', 'dim'), ('Originales', 78.5, '78.5 %', 'hot'), ('Citas', 6.3, '6.3 %', 'dim')], lw=170, vw=110) + '</div></div>'
    + '<p class="s4-note">Un tweet que responde cuenta como respuesta aunque también cite. En la parte del archivo revisada (37,875 tweets) ningún tweet es un retuit: la extracción no los trajo.</p>'
    + step(1, '<p class="callout">Las columnas <code>es_respuesta</code> y <code>es_cita</code> permiten separar conversación de contenido propio antes de comparar tweets.</p>'),
    '64–67 min. Sexta revisión: qué es una fila. Tres tipos de tweet, definidos de forma excluyente: respuesta (si responde a otro tweet), cita (si cita otro y no responde) y original. La mitad del archivo son respuestas, pero los originales, 40.2 % de los tweets, reúnen el 78.5 % de los likes. Contar «tweets» mezcla cosas muy distintas. Advertencia de cobertura: en la parte del Parquet que revisamos (37,875 tweets) retweetedTweet viene vacío en todos; la extracción excluyó retuits, y no escaneamos todo Bronze para comprobarlo.',
    'mix', APLIC, DATO_SQL)

add('Elige reglas y mira cuántos tweets quedan',
    '<div class="s4-excl" data-demo="s4-exclusion" data-combos=\'' + json.dumps(COMBOS) + '\'>'
    '<div class="s4-togs"><button type="button" aria-pressed="false" data-rule="0">Sacar el día parcial<small>marcados: 134,871</small></button>'
    '<button type="button" aria-pressed="false" data-rule="1">Sacar idioma indeterminado<small>marcados: 97,490</small></button>'
    '<button type="button" aria-pressed="false" data-rule="2">Sacar texto repetido (20 o más)<small>marcados: 7,760</small></button>'
    '<button type="button" aria-pressed="false" data-rule="3">Sacar respuestas<small>marcados: 3,414,201</small></button></div>'
    '<div class="s4-out"><span>Quedan</span><b data-out="resto">6,798,932</b><div class="trk"><i data-out="barra" style="--w:100%"></i></div>'
    '<span><i data-out="pct">100.0</i> % de 6,798,932 · se van <i data-out="fuera">0</i></span></div></div>'
    + step(1, '<p class="callout">Tres reglas de calidad: quedan 6,561,954 (96.5 %). Sin respuestas además: 3,257,636 (47.9 %). Esa decisión es de negocio.</p>')
    + '<p class="s4-fine">Cada regla se escribe con cuatro preguntas: qué hace · a cuántas filas toca · quién decide · qué cambia.</p>',
    '67–70 min. Cierre de Aplicar. Activar las reglas de una en una y combinarlas. Las cifras salen de las 16 combinaciones reales de las cuatro banderas sobre Silver (consulta de 1.3 GB). Un tweet puede caer en varias reglas, por eso los marcados no se suman. Observación: las tres reglas de calidad sacan 3.5 % de los tweets, pero quitar respuestas saca la mitad. La primera es una decisión técnica; la segunda es de quien usa el análisis. Pregunta al grupo: ¿quién debe decidir si las respuestas cuentan? [pausa 3 s] Lo escribiremos en la regla.',
    'demo', APLIC, DATO_SQL)

add('Vuelve con tu Bronze cargado y el estimador a la vista',
    '<p class="time">10 min</p><p>Necesitas <code>tweets_bronze.entrada</code> de la sesión 3 y BigQuery Studio abierto.</p>',
    '70–80 min. Pausa real. Al volver cada persona debe tener su tabla tweets_bronze.entrada con 6,798,932 filas. Recordar el estimador de bytes: arriba a la derecha del editor aparece antes de ejecutar. Hoy hay una sola consulta cara, la del paso 1 (23.67 GB de referencia); las demás cuestan menos de 1.4 GB.',
    'statement dark', PAUSA)

# ====================== LABORATORIO 80–150 ======================
add('Laboratorio: construye tus tres tablas Silver',
    '<p class="lab-ribbon">LABORATORIO · 70 MIN</p>'
    + tbl(['Paso', 'Qué haces', 'Qué obtienes'],
          [['1 · 12 min', 'Creas <code>tweets_silver.tweets</code>', 'La tabla de tweets, desde tu Bronze (23.67 GB de lectura)'],
           ['2 · 10 min', 'Compruebas que cuadra con Bronze', '6,798,932 = 6,798,932 y 0 vacíos en id y fecha'],
           ['3 · 12 min', 'Creas <code>autores</code> con CTE y ROW_NUMBER', '1,872,074 autores; la suma de tweets cuadra'],
           ['4 · 12 min', 'Creas <code>hashtags</code> con UNNEST', '3,339,839 filas y el grano comprobado'],
           ['5 · 12 min', 'Marcas la calidad sin borrar', '7,760 textos repetidos, 134,871 del día parcial y más'],
           ['6 · 12 min', 'Mides costos y cuadras las tres tablas', '1.23 GB, 107.5 MB y 33.3 MB para leer lo mismo'], ], cls='traps')
    + lablink(1),
    '80–150 min. La guía paso a paso (laboratorio.html) trae el código completo, el costo estimado de cada consulta, la salida esperada y el error más frecuente. Los pasos son secuenciales: cada tabla se usa en el siguiente. Si el paso 1 falla, revisa primero que tweets_bronze.entrada exista y que el dataset esté en la ubicación US. Consejo: mira siempre el estimador antes de pulsar Ejecutar.',
    'lab-taller', LABOR, DATO)

# ====================== CERRAR 150–180 ======================
add('Antes de confiar, haz que las tablas cuadren',
    tbl(['Comprobación', 'Resultado', 'Qué demuestra'],
        [['Bronze = tweets', '6,798,932 = 6,798,932', 'No se perdió ningún tweet al abrir el JSON'],
         ['Ids distintos = filas', '6,798,932 = 6,798,932', 'Ningún tweet está repetido'],
         ['Suma de tweets por autor', '6,798,932', 'Cada tweet pertenece a un autor, una sola vez'],
         ['Autores', '1,872,074', 'Una fila por autor'],
         ['Tweets con hashtag', '1,226,642 (18.0 %)', 'El resto no usa hashtags y no aparece en la tabla'],
         ['Filas de hashtags', '3,339,839', 'Un tweet por hashtag: no se compara con tweets']], cls='traps')
    + step(1, '<p class="callout">Que cuadre no prueba que sea correcto: prueba que no se perdió ni se duplicó nada al transformar.</p>'),
    '150–155 min. Reconciliar es comparar totales entre una capa y la siguiente. Con estas seis comprobaciones se puede decir que el paso de JSON a tablas no perdió ni duplicó filas. Pregunta al grupo: ¿qué NO demuestra un cuadre? [pausa 3 s] Que los valores estén bien: una fecha mal convertida también cuadra en conteo; por eso hay revisiones de NULL, de rangos y de reglas. Estos números son los que verán en el paso 6 del laboratorio.',
    'check', CERRAR, DATO_SQL)

add('Quién puede leer qué en cada capa',
    tbl(['Capa', 'Qué contiene de las personas', 'Quién debería leerla'],
        [['Bronze', 'Todo el perfil del autor tal como llegó (descripción, ubicación, seguidores…)', 'Quien ingiere y audita; muy pocas personas'],
         ['Silver', 'Usuario, ubicación y seguidores de cada autor, en columnas', 'Quien analiza; acceso de lectura por dataset'],
         ['Gold', 'Solo agregados: sin usuario ni ubicación', 'Quien decide y quien ve tableros']], cls='traps wide')
    + '<p class="s4-note">En este curso los datos se dejan tal como llegaron porque son públicos y de uso académico. En una empresa, quién ve usuario y ubicación se decide antes de dar acceso, y regulaciones como el GDPR (Europa) o HIPAA (salud, EE. UU.) lo exigen cuando hay datos personales.</p>'
    + '<p class="s4-fine">' + IAM + ' · ' + GDPR + ' · ' + HIPAA + '</p>',
    '155–160 min. Gobierno en una sola diapositiva. Cada capa tiene contenido distinto y por eso un público distinto: Bronze guarda más de lo que se usa; Silver expone lo que analizamos; Gold publica lo que se decide. En BigQuery el permiso de lectura se concede por dataset (control de acceso con IAM). Los datos de autores de este archivo se dejan como están por ser públicos y de uso académico; no se anonimizan aquí. Mencionar sin profundizar que GDPR y HIPAA son normas sobre datos personales y de salud. Pregunta al grupo: ¿qué columna de Silver no daríamos a un área de marketing? [pausa 3 s]',
    'gov', CERRAR, DATO)

add('SQL y Spark producen el mismo Silver con dos motores',
    tbl(['Resultado', 'SQL en BigQuery', 'PySpark en Dataproc'],
        [['Filas', '6,798,932', '6,798,932'], ['Ids distintos', '6,798,932', '6,798,932'], ['Días', '12 (16 al 27 de marzo de 2022)', '12 (los mismos)'],
         ['Hashtags en minúsculas', 'Sí: <code>LOWER(h)</code>', 'No, salvo que lo escribas'],
         ['Cómo se escribe un campo', "<code>JSON_VALUE(value, '$.id')</code>", "<code>get_json_object('value', '$.id')</code>"]], cls='traps')
    + '<p class="s4-note">El mismo resultado se obtiene con otro motor. En el ensayo, el trabajo de Spark tardó unos 8 minutos de punta a punta (incluye arranque y escritura); la tabla de SQL, segundos. No es una comparación justa: miden cosas distintas.</p>'
    + step(1, '<p class="callout">Una diferencia pequeña, como las minúsculas, cambia un conteo de hashtags. Por eso se compara el resultado, no solo el conteo de filas.</p>'),
    '160–165 min. Spark ya apareció en la sesión 3. Aquí solo se muestra que la misma transformación se puede escribir con otro motor y obtener el mismo Silver: mismas filas, mismos ids, los mismos 12 días. Un detalle revelador: el script de Spark no pasa los hashtags a minúsculas, y el de SQL sí; son decisiones que hay que escribir en las reglas. Los tiempos no se comparan: el trabajo de Spark incluyó arrancar, leer, escribir Parquet y contar. No es parte del laboratorio de hoy.',
    'compare', CERRAR, DATO)

add('Practica por tu cuenta: cuatro ejercicios',
    '<div class="s4-ex">'
    '<div><b>1 · ¿Cuántos autores publicaron más de 20 tweets?</b><small>Pista: el CTE de la diapositiva 11. Esperado: 46,581.</small></div>'
    '<div><b>2 · ¿Cuántos hashtags distintos hay?</b><small>Pista: <code>COUNT(DISTINCT hashtag)</code> sobre <code>tweets_silver.hashtags</code>. Esperado: 223,523.</small></div>'
    '<div><b>3 · ¿Qué porcentaje de los tweets son de cuentas verificadas?</b><small>Pista: <code>COUNTIF(usuario_verificado)</code>. Esperado: 310,252 tweets, 4.6 %.</small></div>'
    '<div><b>4 · Escribe la regla de «ubicación vacía» con las cuatro preguntas</b><small>Qué hace · a cuántas filas toca (2,664,367) · quién decide · qué cambia en los números.</small></div></div>',
    '165–172 min. Cuatro ejercicios individuales para consolidar. Los tres primeros se resuelven con lo visto y tienen resultado esperado para comprobar; el cuarto es escritura, no código. Si sobra tiempo, pedir que cada persona lea su regla en voz alta y que otra identifique qué pregunta falta. No hay entrega: sirven para comprobar que se entendió el grano, el CTE y UNNEST.',
    'practice', CERRAR, DATO_SQL)

add('Qué puedes afirmar con Silver, y qué no',
    '<div class="s4-cols c2"><div class="s4-acts"><div class="ok"><b>Sí puedes afirmar</b><span>Hay 6,798,932 tweets distintos, de 1,872,074 autores, entre el 16 y el 27 de marzo de 2022.</span></div>'
    '<div class="ok"><span>El 0.2 % de los tweets reúne el 60.4 % de los likes.</span></div>'
    '<div class="ok"><span>Las tres tablas cuadran con Bronze y entre sí.</span></div></div>'
    '<div class="s4-acts"><div class="out"><b>No puedes afirmar</b><span>Que 6.8 millones de tweets son 6.8 millones de personas o de opiniones.</span></div>'
    '<div class="out"><span>Que el 16 de marzo tuvo menos conversación que el 17: solo tiene cuatro horas.</span></div>'
    '<div class="out"><span>Que Silver es «el dato correcto»: es el dato con reglas escritas. Otra regla da otro número.</span></div></div></div>'
    + step(1, '<p class="callout">Siguiente sesión: con tres tablas Silver claras, Gold las convierte en indicadores con definición.</p>'),
    '172–180 min. Cierre honesto. Izquierda, lo que las comprobaciones sí demuestran. Derecha, saltos que alguien podría dar sin darse cuenta: confundir tweets con personas, comparar un día parcial con uno completo y creer que limpiar elimina el criterio. Silver no es la verdad: es una decisión documentada. Con el clic, el puente a la sesión 5: Gold toma estas tablas y calcula indicadores con una definición escrita. Pregunta de salida: ¿qué regla cambiarían y cuántos tweets moverían? [pausa 3 s]',
    'close', CERRAR, DATO_SQL)
