"""S3 · Medallion empieza: del JSON a una tabla (Bronze). Fuente única del deck y del laboratorio de S3.
Cifras de referencia del curso (ver recursos/tweets/verdad.json). `python3 editorial/s03.py` regenera lab.steps de
contenido.json y los archivos recursos/tweets/s03_* a partir de LAB (única fuente del código)."""
import itertools, json
from html import escape as e
from pathlib import Path
from guion import slide, p, step, table, flow, code, proof, lablink, source

TITLE = 'Del JSON a una tabla: así empieza Medallion'
BIGIDEA = 'Un archivo se vuelve consultable al convertirlo en tabla; Bronze lo guarda tal como llegó y decide cuánto costará leerlo.'

# ---------------------------------------------------------------- fuentes
COSTO = source('BigQuery · control de costos', 'https://docs.cloud.google.com/bigquery/docs/best-practices-costs')
DRY = source('BigQuery · dry run', 'https://docs.cloud.google.com/bigquery/docs/dry-run-queries')
EXT = source('BigQuery · tablas externas en GCS', 'https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage')
LOADCSV = source('BigQuery · cargar CSV desde Cloud Storage', 'https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv')
CLASES = source('Cloud Storage · clases de almacenamiento', 'https://docs.cloud.google.com/storage/docs/storage-classes')
DPS = source('Dataproc Serverless', 'https://docs.cloud.google.com/dataproc-serverless/docs/overview')
PQ = source('Apache Parquet', 'https://parquet.apache.org/docs/overview/')
SPK = source('Apache Spark · guía', 'https://spark.apache.org/docs/latest/rdd-programming-guide.html')
MEDALLION = source('Medallion · documentación', 'https://docs.databricks.com/aws/en/lakehouse/medallion')
MED = 'Valores de referencia del curso · war_tweets, 16–27 de marzo de 2022, uso académico'
def src(*xs): return ' · '.join([MED, *xs])

A, C, AP, PA, LABP, CI = ('Abrir · 0–15 min', 'Comprender · 15–50 min', 'Aplicar · 50–70 min', 'Pausa · 70–80 min',
                          'Laboratorio · 80–150 min', 'Cerrar · 150–180 min')

# ---------------------------------------------------------------- ayudas de dibujo
_ids = itertools.count(1)
def svg(h, inner, label):
    i = next(_ids)
    return (f'<svg class="diag" viewBox="0 0 1440 {h}" role="img" aria-label="{e(label)}"><defs><marker id="s3a{i}" markerWidth="12" '
            f'markerHeight="10" refX="10" refY="5" orient="auto"><path d="M0 0L10 5L0 10z"/></marker></defs>' + inner.replace('ARROW', f'url(#s3a{i})') + '</svg>')
def R(x, y, w, h, cls='bx', rx=4): return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>'
def T(x, y, t, cls='', anchor=None):
    a = f' text-anchor="{anchor}"' if anchor else ''
    return f'<text class="{cls}" x="{x}" y="{y}"{a}>{t}</text>'
def L(x1, y1, x2, y2, cls='ln', arrow=True, dash=False):
    return f'<path class="{cls}{" dash" if dash else ""}" d="M{x1} {y1}L{x2} {y2}"' + (' marker-end="ARROW"' if arrow else '') + '/>'
def G(st, inner): return f'<g data-step="{st}">{inner}</g>' if st else f'<g>{inner}</g>'
def pre(t, cls=''): return f'<pre class="{cls}" tabindex="0"><code>{e(t)}</code></pre>'
def qpanel(sql, headers, rows, foot, tag='CONSULTA · GoogleSQL'):
    t = ''
    if headers:
        t = '<table class="matrix"><thead><tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr></thead><tbody>' + \
            ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table>'
    return f'<div class="qp"><div class="qh"><span>{tag}</span><span>BigQuery</span></div>{pre(sql)}{t}<div class="qf">{foot}</div></div>'

# ---------------------------------------------------------------- datos reales de esta sesión
TEXTO = "Africa's Airline Recovery Faces Setback on Ukraine War's Higher Fuel Costs https://t.co/6aejPhMfU7"
N_TXT, N_JSON = len(TEXTO), 2410   # caracteres del texto y de la línea JSON de ese primer tweet
MD5 = 'nC490+y+7Rt3nDD02VE/pg=='

# ---------------------------------------------------------------- LABORATORIO (única fuente del código de guía y de slides)
SPARK_SCRIPT = '''# json_a_parquet.py · lee el JSON Lines como texto y lo guarda como Parquet (una columna `value`).
from pyspark.sql import SparkSession

BUCKET = "gs://TU_BUCKET"
spark = SparkSession.builder.appName("json_a_parquet").getOrCreate()

crudo = spark.read.text(BUCKET + "/war_tweets.txt")           # transformación: cada línea queda en la columna `value`; aún no lee nada
crudo.write.mode("overwrite").parquet(BUCKET + "/tweets_parquet/")   # acción: aquí empieza el trabajo

resultado = spark.read.parquet(BUCKET + "/tweets_parquet/")
print("FILAS", resultado.count())                             # acción: cuenta las filas escritas
'''
SUBMIT = '''gcloud services enable dataproc.googleapis.com
gcloud dataproc batches submit pyspark json_a_parquet.py \\
  --region=us-central1 \\
  --batch=json-a-parquet-001 \\
  --deps-bucket=TU_BUCKET \\
  --properties=spark.dynamicAllocation.maxExecutors=4
'''
SUBMIT_SLIDE = '''gcloud dataproc batches submit pyspark \\
  json_a_parquet.py \\
  --region=us-central1 \\
  --batch=json-a-parquet-001 \\
  --deps-bucket=TU_BUCKET
'''
COLAB = 'https://colab.research.google.com/drive/1T3Q3HYP2j5n40EEj3QNX3iyDanKc99RZ'
LAB = [
    dict(n=1, minutes=12, titulo='Copiar el archivo de Drive a tu bucket',
         donde='Cloud Shell (ícono >_ arriba a la derecha de la consola de Google Cloud) para crear el bucket; después Google Colab, en otra pestaña, con el cuaderno del curso: '+COLAB+'.',
         action='Crea un bucket en la ubicación US (su nombre debe ser único en todo el mundo, por ejemplo tweets-TU_PROYECTO). Abre el cuaderno de Colab del curso (enlace arriba). Ejecuta sus dos primeras celdas: montar Drive y autenticarte con tu cuenta. En la celda que fija project_id y bucket_id escribe TU proyecto y TU bucket: el cuaderno trae valores de ensayo y, si los dejas, la copia falla por permisos. Agrega una celda con el comando de copia de war_tweets.txt (es el mismo patrón que usan las celdas de copia del cuaderno) y ejecútala: son 22 GiB y puede tardar un buen rato. Antes, el archivo debe aparecer en Mi unidad de tu Drive (si está en una carpeta compartida, agrégalo con clic derecho → Organizar → Añadir acceso directo). Cuando la celda termine, pasa al paso 2.',
         costo='Crear el bucket no cuesta. Guardar 22 GiB se cobra por GiB y por mes mientras el objeto exista; revisa los precios de tu clase de almacenamiento.',
         codigo='# Cloud Shell: crea tu bucket\ngcloud config get-value project\ngcloud storage buckets create gs://TU_BUCKET --location=US --uniform-bucket-level-access\n\n# Colab (otra pestaña): celdas del cuaderno del curso\n# 1) from google.colab import drive; drive.mount(\'/content/drive\')\n# 2) from google.colab import auth; auth.authenticate_user()\n# 3) project_id = \'TU_PROYECTO\'; bucket_id = \'TU_BUCKET\'\n#    !gcloud config set project {project_id}\n# 4) celda nueva: !gcloud storage cp /content/drive/MyDrive/war_tweets.txt gs://{bucket_id}\n',
         salida='tu-proyecto\nCreating gs://TU_BUCKET/...',
         check='El cuaderno de Colab termina sin errores y, en el paso 2, el objeto aparece con 23663541134 bytes.',
         error='Si el nombre del bucket ya existe, elige otro. Si Colab se desconecta a medias, vuelve a ejecutar la celda de copia: reescribe el mismo objeto.'),
    dict(n=2, minutes=8, titulo='Comprobar el objeto y anotar su manifiesto',
         donde='Cloud Shell.',
         action='Pide el tamaño y la huella del objeto. Si copiaste el archivo completo, el tamaño y la huella md5 coinciden con los valores de referencia: es la prueba de que tu copia es igual al original. Anota nombre, tamaño, huella y generación: es el manifiesto de tu Bronze.',
         costo='Pedir metadatos no tiene costo de consulta.',
         codigo='gcloud storage ls -l gs://TU_BUCKET/war_tweets.txt\ngcloud storage objects describe gs://TU_BUCKET/war_tweets.txt \\\n  --format="yaml(name,size,storage_class,generation,md5_hash)"\n',
         salida=f'23663541134  FECHA_DE_CREACION  gs://TU_BUCKET/war_tweets.txt\nTOTAL: 1 objects, 23663541134 bytes (22.04GiB)\n---\nmd5_hash: {MD5}\nname: war_tweets.txt\nsize: 23663541134\nstorage_class: STANDARD   # puede variar según tu bucket\n',
         check=f'size es 23663541134 (22.04 GiB) y md5_hash es {MD5}. La generación y la clase de almacenamiento pueden ser distintas.',
         error='Si el tamaño es menor, la copia se interrumpió: repite el cuaderno de Colab. Si ls dice "One or more URLs matched no objects", revisa el nombre del bucket y del archivo.'),
    dict(n=3, minutes=12, titulo='Crear tu Bronze en BigQuery',
         donde='Cloud Shell.',
         action='Crea el dataset tweets_bronze en la ubicación US y carga el archivo completo en una sola columna llamada value. El truco: el archivo es JSON Lines (un JSON por línea); si indicas un separador de columnas que nunca aparece en el texto (þ) y desactivas las comillas (--quote=\'\'), cada línea completa cae en value sin alterarse. --replace permite repetir el comando sin duplicar filas.',
         costo='La carga desde Cloud Storage no se factura como consulta. La tabla ocupará unos 22 GiB lógicos de almacenamiento en tu proyecto.',
         codigo='gcloud services enable bigquery.googleapis.com\nbq --location=US mk --dataset tweets_bronze\nbq --location=US load --replace --source_format=CSV \\\n  --field_delimiter=\'þ\' --quote=\'\' --max_bad_records=0 \\\n  tweets_bronze.entrada "gs://TU_BUCKET/war_tweets.txt" value:STRING\n',
         salida='Dataset \'TU_PROYECTO:tweets_bronze\' successfully created.\nWaiting on bqjob_... (0s) Current status: RUNNING\n...\nWaiting on bqjob_... (Ns) Current status: DONE',
         check='bq show tweets_bronze.entrada muestra una sola columna (value, STRING) y 6,798,932 filas. El método se ensayó con 2,500 líneas reales: 2,500 filas y 2,500 ids distintos. La carga completa desde tu bucket no se midió.',
         error='"Not found: URI" indica un nombre de bucket o de archivo mal escrito. Si hay errores de registros malos, comprueba que escribiste --quote=\'\' (dos comillas simples) y el delimitador þ tal cual (cópialo y pégalo).'),
    dict(n=4, minutes=10, titulo='Contar filas y mirar un tweet crudo',
         donde='BigQuery Studio → nueva consulta (con tu proyecto seleccionado) para contar; Cloud Shell para ver una línea sin costo.',
         action='Cuenta las filas (el estimador del editor debe decir 0 bytes). Después mira un tweet crudo de dos formas y compara su costo: leyendo los primeros bytes del archivo en el bucket, que no cuesta, o con SELECT value ... LIMIT 1 en la tabla, que lee toda la columna.',
         costo='COUNT(*): 0 bytes. Leer value en la tabla: 23.67 GB (≈22.05 GiB); entra en el primer TiB mensual gratuito, pero evita repetirlo sin necesidad.',
         codigo='-- BigQuery Studio\nSELECT COUNT(*) AS tweets FROM tweets_bronze.entrada;\n\n# Cloud Shell (sin costo de consulta)\ngcloud storage cat -r 0-5000 gs://TU_BUCKET/war_tweets.txt | head -n 1\n',
         salida='tweets\n6798932\n\n{"_type": "snscrape.modules.twitter.Tweet", "url": "https://twitter.com/skift/status/1508232397162258434", "date": "2022-03-27T23:59:59+00:00", "content": "Africa\'s Airline Recovery Faces Setback on Ukraine War\'s Higher Fuel Costs https://t.co/6aejPhMfU7", ... }',
         check='El conteo es 6798932 y la línea empieza con {"_type": "snscrape.modules.twitter.Tweet". En la tabla, el orden de las filas no está garantizado: SELECT ... LIMIT 1 puede devolver otro tweet.',
         error='Si COUNT(*) no da 6798932, la carga se interrumpió o se duplicó: repite el comando del paso 3 con --replace.'),
    dict(n=5, minutes=12, titulo='Estimar costos antes de ejecutar',
         donde='Cloud Shell.',
         action='Para cada consulta, predice cuántos bytes leerá y compruébalo con --dry_run (no ejecuta nada ni cuesta). Después ejecuta la cuarta con un tope de 200 MB: verás que BigQuery se niega y te dice cuánto necesitaba. La estimación de la cuarta promete 66.9 MB; la ejecución real exige 23.67 GB.',
         costo='Las estimaciones en seco no cuestan. La ejecución con tope se detiene antes de cobrar.',
         codigo='for SQL in \\\n "SELECT COUNT(*) FROM tweets_bronze.entrada" \\\n "SELECT value FROM tweets_bronze.entrada LIMIT 1" \\\n "SELECT JSON_VALUE(value, \'\\$.id\') FROM tweets_bronze.entrada" \\\n "SELECT value FROM tweets_bronze.entrada TABLESAMPLE SYSTEM (0.1 PERCENT)"; do\n  echo "$SQL"; bq query --nouse_legacy_sql --dry_run "$SQL"\ndone\n\nbq query --nouse_legacy_sql --maximum_bytes_billed=200000000 \\\n "SELECT value FROM tweets_bronze.entrada TABLESAMPLE SYSTEM (0.1 PERCENT)"\n',
         salida='... will process 0 bytes of data.\n... will process 23670340066 bytes of data.\n... will process 23670340066 bytes of data.\n... will process 66865367 bytes of data.\n\nBigQuery error in query operation: ... Query exceeded limit for bytes billed: 200000000. 23670554624 or higher required.',
         check='Tres consultas piden 23,670,340,066 bytes (22.05 GiB) y COUNT(*) pide 0. La cuarta se estima en 66,865,367 pero la ejecución con tope falla exigiendo 23,670,554,624: la estimación no siempre se cumple.',
         error='Si el comando falla por las comillas del JSON_VALUE, escríbelo en una línea o en un archivo .sql y pásalo por stdin. Un SQL que empieza con -- pasado como argumento hace fallar a bq: usa stdin.'),
    dict(n=6, minutes=16, titulo='De JSON a Parquet con Spark',
         donde='Cloud Shell (editor de texto o cat > archivo) y consola de Dataproc para ver el lote.',
         action='Guarda el script json_a_parquet.py (lee el archivo como texto y lo guarda como Parquet), activa Dataproc y envía el trabajo como lote sin servidor. --deps-bucket es obligatorio; elige una región de Estados Unidos y usa la misma en todos tus lotes. El script cuenta las filas del Parquet que escribió: deben coincidir con tu Bronze.',
         costo='Dataproc Serverless cobra por los recursos que usa mientras corre. Un lote de Silver con hasta 4 ejecutores tardó unos 8 minutos en el ensayo; este script no se midió. Revisa el costo en Facturación y no dejes lotes repetidos.',
         codigo=SUBMIT,
         salida='...\nFILAS 6798932\nBatch [json-a-parquet-001] finished.',
         check='La salida imprime FILAS 6798932, igual que COUNT(*) de tu Bronze, y gcloud storage ls gs://TU_BUCKET/tweets_parquet/ lista archivos .parquet.',
         error='Sin --deps-bucket, gcloud falla con "--deps-bucket was not specified" (se observó en el ensayo). Si el lote no arranca por red, la documentación de Dataproc Serverless exige Private Google Access en la subred (no se observó en el ensayo).'),
]
ASSET_FILES = {  # nombre → contenido (se derivan de LAB; un solo origen)
    's03_01_bucket.sh': LAB[0]['codigo'] + '# Después: abre el cuaderno de Colab del curso (Drive → Storage), apunta el destino a gs://TU_BUCKET y ejecútalo.\n',
    's03_02_manifiesto.sh': LAB[1]['codigo'],
    's03_03_cargar_bronze.sh': LAB[2]['codigo'],
    's03_04_contar_y_mirar.sql': LAB[3]['codigo'],
    's03_05_estimar_costos.sh': LAB[4]['codigo'],
    's03_06_json_a_parquet.py': SPARK_SCRIPT,
    's03_06_enviar_batch.sh': SUBMIT,
}

# ---------------------------------------------------------------- DECK
S = []
SLIDES = S
def add(title, body, note, layout='plain', phase=C, src_=None):
    S.append(slide(title, body, note, layout, phase, src_ or MED))

# ===== ABRIR 0–15 (slides 1–4)
add('Del JSON a una tabla',
    '<div><p class="overline">Sesión 03 · Medallion empieza</p><h1>Del JSON<br>a una tabla.</h1><p class="lede">Hoy el archivo de tweets entra a tu proyecto sin perder nada.</p></div>'
    '<div class="stack"><p class="large signal">22.04 GiB</p><p>6,798,932 tweets · un JSON por línea</p><p class="caption">war_tweets · 16–27 de marzo de 2022<br>uso académico, datos sin tocar</p></div>',
    '0–3 min. Abrir con una pregunta: ¿cómo se convierte un archivo de 22 GiB en algo que se pueda consultar con SQL? Hoy empieza el hilo del curso: un solo conjunto de datos, los tweets sobre la guerra en Ucrania, que cada alumno copia a su propio proyecto y transforma en tres capas (Bronze, Silver y Gold). Hoy solo se construye la primera. [pausa 3 s] Aclarar que los datos se usan tal como están, con fines académicos.',
    'cover dark', A, MED)

add(f'Un tweet son {N_TXT} caracteres de texto dentro de {N_JSON:,} de JSON.',
    '<div class="two" style="grid-template-columns:.85fr 1.3fr;gap:36px;align-items:stretch"><div class="tw-card"><div class="who"><b>Skift</b><span class="muted">@skift · verificado · 87,507 seguidores</span></div>'
    f'<div class="txt">{e(TEXTO)}</div><div class="meta">27 mar 2022 · 23:59:59 UTC · idioma en · 0 likes · 0 retuits</div></div>'
    '<pre class="json-view">{\n  "url": "https://twitter.com/skift/status/1508232397162258434",\n  "date": "2022-03-27T23:59:59+00:00",\n'
    f'  <span class="h">"content": "{e(TEXTO[:46])}…"</span>,\n  "lang": "en", "likeCount": 0, "retweetCount": 0, …\n  <span class="k">"user"</span>: {{ "username": "skift", "followersCount": 87507, … <span class="d">23 campos</span> }},\n  <span class="d">… hasta 29 campos de primer nivel</span>\n}}</pre></div>'
    + step(1, svg(100, R(0, 8, 1440, 46, 'bx') + R(0, 8, 99, 46, 'fr') + R(99, 8, 1341, 46, 'fl') +
                  T(0, 90, f'texto · {N_TXT} caracteres (4 %)', 'b r') + T(1440, 90, f'resto de la línea · {N_JSON - N_TXT:,} caracteres', 's', 'end'), f'Barra: el texto es el 4 % de la línea JSON de {N_JSON:,} caracteres'))
    + step(2, p('JSON es texto con pares «nombre: valor», y un valor puede contener a su vez otro conjunto de pares (aquí, el autor).', 'note-line')),
    f'3–7 min. A la izquierda, el tweet como lo ve una persona; a la derecha, como llega al sistema. Primer clic: la barra. El texto ocupa {N_TXT} caracteres de una línea de {N_JSON:,}; lo demás son metadatos: fecha, métricas, la cuenta autora con sus 23 campos. Segundo clic: definir JSON. Es un formato de texto donde cada dato lleva su nombre; los corchetes y llaves permiten anidar. Pregunta al grupo: ¿qué dato de la línea te serviría para contar tweets por día? [pausa 3 s] La fecha, y está escondida dentro del texto.',
    'split', A, src('primera línea de war_tweets.txt'))

add('Un archivo no responde preguntas: una tabla sí.',
    '<div class="two" style="grid-template-columns:1fr 1.15fr;gap:34px;align-items:start"><div><p class="caption">ARCHIVO · war_tweets.txt</p>'
    '<pre class="json-view" style="font-size:19px">{"_type": "snscrape…", "url": ".../skift/status/150823…", "date": "2022-03-27T23:59:59+00:00", "content": "Africa\'s Airline Recovery…", …}\n'
    '{"_type": "snscrape…", "url": ".../Kwondeu/status/150823…", "date": "…", …}\n{"_type": "snscrape…", "url": ".../Tralfraz/status/150823…", "date": "…", …}\n<span class="d">… 6,798,932 líneas de texto</span></pre>'
    + p('Para saber cuántos tweets hay en español hay que abrir todas las líneas.', 'note-line') + '</div>'
    + step(1, '<div><p class="caption">TABLA · una fila por tweet</p><table class="matrix tiny"><thead><tr><th>tweet_id</th><th>fecha</th><th>idioma</th><th>usuario</th></tr></thead><tbody>'
            '<tr><td>1508232397162258434</td><td>2022-03-27</td><td>en</td><td>skift</td></tr><tr><td>…</td><td>…</td><td>…</td><td>…</td></tr></tbody></table>'
            + p('En una tabla, «idioma» es una columna: contar por idioma ya es una consulta.', 'note-line') + '</div>') + '</div>'
    + step(2, p('Convertir JSON en tabla es el trabajo de las tres capas de hoy en adelante.', 'callout')),
    '7–10 min. Comparar lo que puede hacer una persona o un programa con cada forma. El archivo es una lista de textos: cada línea trae todo junto y no tiene columnas. Una tabla organiza lo mismo en filas (un tweet por fila) y columnas (un dato por columna, con su tipo). SQL solo habla con tablas. Primer clic: la tabla con la fila real del tweet de Skift. Segundo clic: el hilo de las próximas sesiones. Aclarar que filas, columnas y tipos se practican en la sesión 2; aquí basta la idea.',
    'comparison', A, src('tres primeras líneas de war_tweets.txt'))

add('El hilo del curso: ¿qué temas de la guerra vale la pena vigilar?',
    '<div class="two" style="grid-template-columns:1.05fr 1fr;gap:40px;align-items:start"><div>' +
    table(['Dato', 'Valor'], [['Tweets', '6,798,932'], ['Periodo', '16–27 de marzo de 2022 (12 días)'], ['Tamaño', '22.04 GiB como JSON'],
                                              ['Idioma principal', 'inglés 59 %, español 15.5 %'], ['Retweets', 'ninguno: la extracción los excluyó']]) + '</div><div class="stack">'
    + p('Pregunta: ¿cuánto de la conversación habla de energía, alimentos, aviación, sanciones, cadena de suministro y mercados?', 'callout')
    + step(1, p('Una advertencia desde ya: contar tweets no mide opinión pública ni impacto económico.', 'callout')) + '</div></div>',
    '10–15 min. Presentar el hilo que acompaña el resto del curso: un comité quiere decidir qué temas satélite de la guerra vale la pena vigilar. El archivo trae 6,798,932 tweets de doce días y no incluye retweets, así que cada tweet es una publicación propia. Clic: la advertencia. Un conteo de tweets depende del idioma, de quién publica y de cuántos días cubre el archivo; no equivale a la opinión de un país ni al efecto en la economía. Esa advertencia vuelve al final de cada sesión. Cierre de la apertura: hoy no se contesta la pregunta; se prepara el terreno.',
    'table', A, src('perfil del archivo completo'))

# ===== COMPRENDER 15–50 y APLICAR 50–70 (slides 5–20)
add('Medallion: tres capas, cada una con una promesa.',
    svg(430,
        G(0, R(0, 70, 440, 260, 'bx u') + T(220, 130, 'Bronze', 'xl u', 'middle') + T(220, 190, 'Lo que recibimos', 'b', 'middle') + T(220, 232, 'El original, sin corregir', 's', 'middle') + T(220, 264, 'y con su origen anotado', 's', 'middle'))
        + G(1, L(448, 200, 500, 200, 'ln u') + R(500, 70, 440, 260, 'bx') + T(720, 130, 'Silver', 'xl', 'middle') + T(720, 190, 'Lo que podemos comparar', 'b', 'middle') + T(720, 232, 'Columnas con tipo y', 's', 'middle') + T(720, 264, 'reglas de calidad escritas', 's', 'middle'))
        + G(2, L(948, 200, 1000, 200, 'ln u') + R(1000, 70, 440, 260, 'bx g') + T(1220, 130, 'Gold', 'xl g', 'middle') + T(1220, 190, 'Lo que necesita la decisión', 'b', 'middle') + T(1220, 232, 'Indicadores con nombre,', 's', 'middle') + T(1220, 264, 'grano y denominador', 's', 'middle'))
        + T(0, 380, 'Medallion («de medalla») es un patrón de capas de calidad. No es un producto de Google Cloud: aquí cada capa es un conjunto de tablas en BigQuery.', 's'),
        'Tres capas: Bronze lo recibido, Silver lo comparable, Gold lo que necesita la decisión')
    + p('Cada capa se construye a partir de la anterior; la anterior no se modifica.', 'callout'),
    '15–19 min. Definir Medallion con una frase por capa. Bronze guarda lo que llegó. Silver lo ordena en columnas con tipo y aplica reglas de calidad escritas. Gold calcula los indicadores que usa quien decide. Primer clic: Silver. Segundo clic: Gold. No es un servicio de Google Cloud ni exige tres tecnologías distintas: en este curso son tres grupos de tablas en BigQuery. La regla que se repite en todo el curso: una capa nunca modifica a la anterior; si cambia una regla, se vuelve a construir hacia adelante. Hoy solo se construye Bronze; Silver es la sesión 4 y Gold la 5.',
    'path', C, src('definiciones de capas') + ' · ' + MEDALLION)

add('Un solo tweet recorre las tres capas.',
    '<div class="tri">'
    '<div class="tri-c"><span class="pill u">BRONZE</span><h2>Una celda de texto</h2><p class="mono sm">value =<br>{"url": "…/skift/status/1508232397162258434",<br>"date": "2022-03-27T23:59:59+00:00",<br>"content": "Africa\'s Airline Recovery…", …}</p><small>1 columna · 2,410 caracteres</small></div>'
    + step(1, '<div class="tri-c"><span class="pill">SILVER</span><h2>Una fila con columnas</h2><table class="matrix tiny"><tbody><tr><th>tweet_id</th><td>1508232397162258434</td></tr><tr><th>fecha_hora</th><td>2022-03-27 23:59:59</td></tr><tr><th>idioma</th><td>en</td></tr><tr><th>usuario</th><td>skift</td></tr><tr><th>seguidores</th><td>87507</td></tr><tr><th>likes</th><td>0</td></tr><tr><th>aplicacion</th><td>HubSpot</td></tr></tbody></table><small>18 columnas con su tipo</small></div>')
    + step(2, '<div class="tri-c"><span class="pill g">GOLD</span><h2>Un +1 en un indicador</h2><p class="sm">Día 27 de marzo, tweets en inglés (318,791):</p><p class="sm"><b>energía</b> menciona «fuel» → 6,666 tweets = 2.091 %</p><p class="sm"><b>aviación</b> menciona «airline» → 282 tweets = 0.088 %</p><small>este tweet cuenta en los dos temas</small></div>')
    + '</div>',
    '19–25 min. El mismo tweet de Skift en las tres capas. Bronze: una sola celda con el JSON completo. Primer clic, Silver: la misma información en columnas con tipo; el id es un número, la fecha una fecha, los seguidores un entero. Segundo clic, Gold: el tweet desaparece como fila y pasa a ser una cuenta: suma uno en energía (menciona «fuel») y uno en aviación (menciona «airline») dentro del 27 de marzo en inglés, donde 6,666 de 318,791 tweets mencionan energía, 2.091 %. Detalle importante: un tweet puede contar en varios temas. Cada capa responde a una pregunta distinta: qué llegó, qué podemos comparar, qué pide la decisión.',
    'path', C, src('fila real de Silver y Gold de ese tweet'))

add('Bronze guarda el original, aunque tenga defectos.',
    '<div class="split"><div>' + qpanel('SELECT value FROM tweets_bronze.entrada LIMIT 3',
        ['fila', 'value  (JSON crudo, abreviado)', 'caracteres'],
        [['1', '{"_type": "snscrape.modules.twitter.Tweet", "url": ".../skift/status/1508232397162258434", …', '2,410'],
         ['2', '{"_type": "snscrape.modules.twitter.Tweet", "url": ".../Kwondeu/status/1508232396625350662", …', '3,624'],
         ['3', '{"_type": "snscrape.modules.twitter.Tweet", "url": ".../Tralfraz/status/1508232396625260545", …', '2,811']],
        '<span><b>6,798,932</b> filas</span><span><b>1</b> columna: value STRING</span><span class="bad">leer value cuesta 23.67 GB</span>', 'RESULTADO · abreviado') +
    '</div><div class="stack">' + p('Sin tipos: la fecha y los likes son texto dentro del JSON.', 'callout') + p('Sin limpieza: duplicados, spam e idiomas raros entran igual.', 'callout') +
    step(1, p('Si mañana cambias una regla, vuelves a calcular desde aquí.', 'callout')) + '</div></div>',
    '25–28 min. Esto es Bronze: la tabla que contiene lo que llegó, en una sola columna llamada value. No es una tabla fea; es una tabla honesta. Tres filas del resultado, abreviadas. Insistir en lo que no tiene: tipos (la fecha es texto), limpieza (entran duplicados y textos repetidos) y filtros. Es a propósito: si decides mañana excluir las respuestas, o cambiar cómo se lee la fecha, puedes volver a calcular desde el original. Analogía: la factura original se guarda aunque ya la hayas registrado en la contabilidad.',
    'plain', C, src('tabla creada con el método del laboratorio'))

add('Cargar es copiar cada línea a una celda, sin cambiarla.',
    svg(380,
        R(0, 30, 600, 150, 'bx') + T(20, 70, 'una línea del archivo (JSON)', 's') + T(20, 112, '{"url": "…/skift/…",', 'm') + T(20, 150, '"date": "2022-03-27…", …}', 'm')
        + G(1, L(615, 105, 905, 105, 'ln u') + T(760, 70, 'bq load', 'm b u', 'middle') + T(760, 152, 'CSV · þ · sin comillas', 's', 'middle')
              + R(920, 30, 520, 150, 'bx u') + T(940, 70, 'value  STRING', 'b') + T(940, 112, 'la línea completa,', 'm') + T(940, 150, 'sin alterarla', 'm'))
        + G(2, T(0, 240, 'Por qué funciona:', 'b') + T(0, 282, '1 · el separador de columnas (þ) nunca aparece en un tweet, así que no se parte nada.', '')
              + T(0, 320, '2 · con --quote=\'\' las comillas del JSON no se interpretan como comillas del CSV.', '')
              + T(0, 358, '3 · el resultado es una tabla de una columna: la capa Bronze.', '')),
        'Una línea de JSON pasa completa a una celda de la columna value usando una carga CSV con separador þ y sin comillas')
    + step(3, p('Ensayado con 2,500 líneas reales: 2,500 filas y 2,500 ids distintos.', 'callout')),
    '28–32 min. Cómo se convierte un archivo de líneas JSON en una tabla de BigQuery sin transformar nada. Se usa la herramienta de cargar CSV con un truco: se declara un separador de columnas que nunca aparece en el texto (la letra þ) y se desactivan las comillas. Entonces cada línea completa cae en una sola columna llamada value. Primer clic: el comando. Segundo clic: las tres razones. Tercer clic: la prueba. Se probó con 2,500 líneas reales y las 2,500 filas llegaron con 2,500 ids distintos. Definir delimitador (el carácter que separa columnas) y comillas (las que encierran un texto que contiene separadores). La carga en sí no se factura como consulta.',
    'path', C, src('ensayo con 2,500 líneas reales') + ' · ' + LOADCSV)

add('El archivo vive en Cloud Storage; la tabla, en BigQuery.',
    svg(330,
        R(0, 70, 290, 150, 'bx') + T(145, 130, 'Google Drive', 'b', 'middle') + T(145, 176, 'donde está el archivo', 's', 'middle')
        + G(1, L(298, 145, 410, 145, 'ln u') + T(354, 118, 'Colab', 'm b u', 'middle') + R(420, 70, 360, 150, 'bx u') + T(600, 120, 'Cloud Storage', 'b', 'middle') + T(600, 160, 'gs://TU_BUCKET/', 'm', 'middle') + T(600, 196, 'war_tweets.txt', 'm', 'middle'))
        + G(2, L(788, 145, 900, 145, 'ln u') + T(844, 118, 'bq load', 'm b u', 'middle') + R(910, 70, 530, 150, 'bx g') + T(1175, 120, 'BigQuery', 'b', 'middle') + T(1175, 160, 'tweets_bronze.entrada', 'm', 'middle') + T(1175, 196, 'tu proyecto, ubicación US', 's', 'middle'))
        + T(0, 290, 'Un bucket es un contenedor de archivos con nombre único; un objeto es un archivo dentro de él; la URI gs:// es su dirección.', 's'),
        'Del archivo en Drive a un bucket de Cloud Storage y de ahí a una tabla de BigQuery en tu proyecto')
    + step(3, p('Los dos viven en tu proyecto: tú pagas y tú decides cuándo borrarlos.', 'callout')),
    '32–35 min. El camino del archivo: Drive, Cloud Storage, BigQuery. El cuaderno de Colab del curso copia el archivo de Drive a tu bucket; la carga lo pasa a una tabla. Definir bucket (contenedor con nombre único en todo el mundo), objeto (el archivo) y URI gs:// (su dirección). Almacenar el archivo y almacenar la tabla son dos cobros distintos: Cloud Storage cobra por GiB y mes según la clase de almacenamiento; BigQuery cobra por GiB y mes de la tabla y por los bytes que cada consulta lee. Ubicación: usa US para ambos para que la carga no cruce regiones. Todo vive en tu proyecto.',
    'path', C, src('ruta del laboratorio') + ' · ' + CLASES)

add('ELT: primero cargas el original, después transformas dentro.',
    svg(450,
        T(0, 36, 'ETL · transformar antes de cargar', 'b') + R(0, 56, 360, 90, 'bx') + T(180, 112, 'Extraer', '', 'middle') + L(368, 101, 460, 101) + R(470, 56, 360, 90, 'bx r') + T(650, 112, 'Transformar fuera', '', 'middle')
        + L(838, 101, 930, 101) + R(940, 56, 500, 90, 'bx') + T(1190, 100, 'Cargar: solo queda', '', 'middle') + T(1190, 132, 'el resultado limpio', '', 'middle')
        + G(1, T(0, 250, 'ELT · cargar primero, transformar después', 'b u') + R(0, 270, 360, 90, 'bx') + T(180, 326, 'Extraer', '', 'middle') + L(368, 315, 460, 315, 'ln u') + R(470, 270, 360, 90, 'bx u') + T(650, 314, 'Cargar el original', '', 'middle') + T(650, 346, 'Bronze', 's', 'middle')
              + L(838, 315, 930, 315, 'ln u') + R(940, 270, 500, 90, 'bx g') + T(1190, 314, 'Transformar en BigQuery', '', 'middle') + T(1190, 346, 'Silver y Gold', 's', 'middle'))
        + G(2, T(0, 420, 'Con ELT el original se conserva: si una regla cambia, vuelves a transformar sin ir otra vez a la fuente.', 's')),
        'ETL transforma antes de cargar; ELT carga el original primero y transforma dentro de la base'),
    '35–38 min. ETL (extraer, transformar, cargar) transforma antes de que los datos lleguen a la base: lo que no pasó por la regla se pierde. ELT (extraer, cargar, transformar) carga primero el original y transforma después, con el motor de la propia base. BigQuery está pensado para ELT: calcula sobre tablas enormes y cobra por lo que lee, así que conviene conservar el original en Bronze y construir encima. Con el tweet de Skift: en ETL llegaría ya convertido en fila; en ELT llega como texto y se convierte en la capa siguiente. Primer clic: ELT. Segundo clic: la consecuencia.',
    'comparison', C, src('definiciones ETL/ELT'))

add('Tres formas de guardar los mismos tweets: JSON, CSV y Parquet.',
    '<div class="fmt3"><div><h2>JSON Lines</h2><pre>{"url": "…", "date": "…"}\n{"url": "…", "date": "…"}</pre><p>Un JSON por línea. Cada línea trae sus propios nombres; admite campos anidados.</p><span class="eg">war_tweets.txt · 22.04 GiB</span></div>'
    '<div><h2>CSV</h2><pre>url,date,content\n"…","…","…"</pre><p>Filas y columnas planas separadas por comas. Un tweet anidado no cabe sin aplanarlo antes.</p><span class="eg">no aplica sin aplanar</span></div>'
    '<div><h2>Parquet</h2><div class="cols"><span>url<br>url<br>url</span><span>date<br>date<br>date</span><span>value<br>value<br>value</span></div><p>Guarda por columnas y comprimido. Lee solo las columnas que pides.</p><span class="eg">el mismo contenido · 5.78 GiB</span></div></div>',
    '38–40 min. Los tres formatos que verás en cualquier proyecto de datos. JSON Lines: un JSON por línea, flexible pero repite los nombres de campo en cada línea. CSV: plano y universal, pero un tweet con un autor anidado no cabe sin aplanarlo. Parquet: guarda por columnas y comprime; si una consulta pide solo dos columnas, no lee las demás. El mismo contenido de tweets pesa 22.04 GiB como JSON y 5.78 GiB como Parquet. Pregunta al grupo: si Parquet pesa casi cuatro veces menos, ¿también cuesta cuatro veces menos consultarlo en BigQuery? [pausa 3 s] La siguiente slide lo responde.',
    'compare', C, src('tamaños medidos del mismo contenido') + ' · ' + PQ)

add('El tamaño en disco no es lo que te cobran por consultar.',
    svg(430,
        T(0, 36, 'Mismo contenido, cuatro medidas (GiB)', 'b')
        + G(0, T(0, 92, 'JSON en Storage', 'b') + R(330, 66, 1000, 38, 'fu') + T(1340, 96, '22.04', 'm b'))
        + G(1, T(0, 156, 'Parquet en Storage', 'b') + R(330, 130, 260, 38, 'fg') + T(600, 160, '5.78', 'm b'))
        + G(2, T(0, 220, 'Tabla Bronze (lógico)', 'b') + R(330, 194, 1000, 38, 'fu') + T(1340, 224, '22.04', 'm b'))
        + G(3, T(0, 284, 'Lo que lee una consulta', 'b') + R(330, 258, 1000, 38, 'fr') + T(1340, 288, '22.05', 'm b') + T(0, 350, '23,670,340,066 bytes facturados al leer la columna value.', 's')),
        'Barras: JSON 22.04 GiB, Parquet 5.78 GiB, tabla Bronze 22.04 GiB lógicos y consulta 22.05 GiB')
    + step(4, p('La compresión ahorra almacenamiento y transferencia, no consulta. Lo que baja la factura es leer menos columnas.', 'callout')),
    '40–43 min. Cuatro barras para el mismo contenido. JSON en Storage: 22.04 GiB. Parquet: 5.78 GiB, casi cuatro veces menos. Pero al cargarlo, BigQuery guarda y factura por bytes lógicos, sin comprimir: la tabla Bronze ocupa 22.04 GiB lógicos, y una consulta que lee la columna value lee 23,670,340,066 bytes. Resultado: la compresión ahorra espacio y transferencia, no consulta. Lo que sí baja la factura es leer menos columnas, y para eso sirve Silver. Aviso de unidades: GiB es 1024³ bytes; el estimador habla de bytes y GB. 23.67 GB y 22.05 GiB son la misma cantidad.',
    'bars', C, src('bytes medidos') + ' · ' + COSTO)

add('Tabla externa o nativa: dónde viven los bytes.',
    table(['', 'Tabla externa', 'Tabla nativa'],
          [['Dónde viven los datos', 'En el archivo, dentro de Cloud Storage', 'Copiados dentro de BigQuery'],
           ['Qué haces', 'Declaras la ruta del archivo', 'Cargas el archivo (la carga no se factura como consulta)'],
           ['Cuánto lee una consulta (medido)', '16.8 y 21 GB sobre el Parquet', '23.67 GB al leer la columna value'],
           ['Ventaja', 'No duplicas los datos', 'Particiones, clustering y más rapidez'],
           ['Cuándo conviene', 'Para mirar un archivo una vez', 'Para consultarlo muchas veces']])
    + p('Ninguna abarata leer la misma columna completa: la diferencia llega al reducir columnas y filas.', 'callout'),
    '43–45 min. Dos formas de que BigQuery vea un archivo. Externa: la tabla apunta al archivo que sigue en Cloud Storage; no ocupa almacenamiento de BigQuery, pero cada consulta lee el archivo. Nativa: cargas una copia dentro de BigQuery; permite particiones y clustering. Medido con este archivo: las consultas sobre la tabla externa de Parquet pidieron 16.8 y 21 GB; la nativa pidió 23.67 GB al leer value. Ninguna de las dos resuelve el costo si lees la misma columna entera: la mejora llega en Silver. En el laboratorio usas la nativa, que es la que se consulta muchas veces.',
    'compare', C, src('consultas medidas') + ' · ' + EXT)

add('Spark reparte el trabajo entre varias máquinas.',
    svg(480,
        R(560, 6, 320, 64, 'bx u') + T(720, 48, 'Driver · coordina', 'b', 'middle')
        + R(0, 130, 300, 80, 'bx') + T(150, 180, 'Archivo grande', 'b', 'middle')
        + G(1, ''.join(R(340 + k * 105, 130, 85, 80, 'fl') for k in range(6)) + T(985, 178, '← se divide en pedazos', 's') + T(985, 208, '(particiones)', 's'))
        + G(2, ''.join(R(335 + k * 215, 300, 200, 70, 'bx g') + T(435 + k * 215, 345, f'Ejecutor {k + 1}', 'b', 'middle') for k in range(3))
              + ''.join(L(382 + k * 105, 214, 435 + (k // 2) * 215, 298, 'ln g', arrow=False) for k in range(6)))
        + G(3, R(0, 410, 1440, 60, 'bx u') + T(720, 450, 'Cada ejecutor trabaja sus pedazos; el driver junta los resultados', 'b', 'middle')),
        'Un archivo se divide en particiones, varios ejecutores procesan cada una y el driver junta el resultado')
    + step(4, p('Spark gana cuando el trabajo cabe repartido; pierde cuando el trabajo es pequeño.', 'callout')),
    '45–48 min. Spark es un motor para repartir un trabajo grande entre varias máquinas. Un coordinador (driver) divide el archivo en pedazos (particiones), manda cada pedazo a un trabajador (ejecutor) y junta los resultados. Primer clic: los pedazos. Segundo clic: los ejecutores. Tercero: el resultado. Cuarto: cuándo conviene. Arrancar y coordinar cuesta tiempo, así que para un trabajo pequeño una sola consulta SQL es más rápida. Anclaje real: el Parquet de 5.78 GiB se guarda en muchos archivos precisamente para que se puedan repartir.',
    'path', C, src('definición de Spark') + ' · ' + SPK)

add('PySpark: un plan que no corre hasta que pides un resultado.',
    '<div class="lazy"><pre tabindex="0"><code><span class="ln-code">spark = SparkSession.builder.appName("json_a_parquet").getOrCreate()</span>\n'
    '<span class="ln-code plan">crudo = spark.read.text("gs://TU_BUCKET/war_tweets.txt")        # plan: aún no lee nada</span>\n'
    '<span class="ln-code act">crudo.write.mode("overwrite").parquet(".../tweets_parquet/")        # acción: aquí empieza el trabajo</span>\n'
    '<span class="ln-code act">print("FILAS", spark.read.parquet(".../tweets_parquet/").count())   # acción: cuenta las filas</span></code></pre>'
    '<p class="caption">verde: transformaciones (se anotan en un plan) · rojo: acciones (ejecutan el plan sobre todos los pedazos)</p></div>'
    + step(1, p('Resultado esperado: FILAS 6798932, igual que el conteo de tu Bronze.', 'callout')),
    '48–50 min. El script del laboratorio, línea por línea. PySpark es Spark controlado con Python. Spark es perezoso: leer el archivo solo apunta el plan, y nada ocurre hasta una acción como escribir o contar. Eso le permite optimizar todo el plan antes de repartirlo. Las líneas en verde son transformaciones; las rojas, acciones. Este mismo método de leer el archivo como texto y guardarlo en Parquet es como se generó el Parquet del curso con una sola columna value. Clic: la comprobación esperada. Este script no se ensayó tal cual; el patrón de envío sí se ensayó con otro lote de Spark.',
    'code', C, src('script de s03_06_json_a_parquet.py') + ' · ' + SPK)

add('BigQuery cobra por bytes leídos, no por filas devueltas.',
    '<div class="cost-demo" data-demo="costos" data-items=\'' + e(json.dumps([
        dict(sql='SELECT COUNT(*) FROM tweets_bronze.entrada', est='0 B', real='0 B (ejecutada)', verdict='COUNT(*) usa metadatos de la tabla: no lee ninguna columna.'),
        dict(sql='SELECT value FROM tweets_bronze.entrada LIMIT 1', est='23.67 GB', real='no ejecutada: la estimación basta', verdict='LIMIT corta la salida, no la lectura: lee toda la columna igual.'),
        dict(sql="SELECT JSON_VALUE(value, '$.id') FROM tweets_bronze.entrada", est='23.67 GB', real='23.67 GB (ejecutada al construir Silver)', verdict='Sacar un solo campo obliga a leer el JSON completo de cada fila.'),
        dict(sql='SELECT value FROM tweets_bronze.entrada TABLESAMPLE SYSTEM (0.1 PERCENT)', est='66.9 MB', real='exigió 23.67 GB al ejecutar con tope', verdict='La estimación prometía 66.9 MB. Verifica con un tope antes de confiar.')],
        ensure_ascii=False), quote=True) + '\'><div class="actions"><button data-q aria-pressed="true">COUNT(*)</button><button data-q>LIMIT 1</button><button data-q>JSON_VALUE</button><button data-q>TABLESAMPLE</button></div>'
    '<pre data-qsql></pre><div class="cmp"><div><small>ESTIMACIÓN ANTES DE EJECUTAR</small><b data-est></b></div><div><small>AL EJECUTAR</small><b data-real></b></div></div><p class="callout" data-verdict></p></div>',
    '50–56 min. Elegir una consulta y mirar dos cifras: la estimación que muestra el editor antes de ejecutar y lo que pasó al ejecutar. 1) COUNT(*): 0 bytes, usa metadatos. 2) LIMIT 1: la estimación sigue siendo 23.67 GB; LIMIT limita lo que ves, no lo que se lee. 3) JSON_VALUE de un campo: lee toda la columna value; es el costo de construir Silver. 4) TABLESAMPLE: la estimación decía 66.9 MB, pero al ejecutar con un tope de 200 MB falló pidiendo 23.67 GB. Moraleja: BigQuery cobra por bytes leídos de las columnas que nombras; usa dry-run y tope, y no te fíes de una sola estimación. El primer TiB de consultas de cada mes es gratuito.',
    'interactive', AP, src('estimaciones y ejecuciones medidas') + ' · ' + DRY)

add('Dataproc Serverless: Spark sin administrar un clúster.',
    '<div class="two" style="grid-template-columns:1.25fr 1fr;gap:36px;align-items:start"><div>' + pre(SUBMIT_SLIDE, 'sm-code') + '</div><div class="stack">'
    + p('Tú envías el script; Google crea y apaga los recursos.', 'callout')
    + step(1, p('--deps-bucket es obligatorio: sin él, gcloud falla (se observó en el ensayo).', 'callout'))
    + step(2, p('Un lote de Silver con hasta 4 ejecutores tardó unos 8 minutos y dejó 0 clústeres activos al terminar.', 'callout')) + '</div></div>',
    '60–63 min. Cómo se envía el trabajo de Spark sin administrar máquinas. Dataproc Serverless crea los recursos al enviar el lote y los apaga al terminar; tú pagas por lo que usa mientras corre. Primer clic: el parámetro obligatorio --deps-bucket, que se descubrió al ensayar. Segundo clic: tiempos del ensayo con otro lote (Silver, hasta 4 ejecutores): unos 8 minutos, con 0 clústeres activos al terminar. Esos 8 minutos incluyen el arranque, escribir y dos conteos; no se pueden comparar con una consulta SQL de segundos. La región debe ser de Estados Unidos y la misma en todos tus lotes.',
    'code', AP, src('lote de referencia') + ' · ' + DPS)

add('Estima antes de ejecutar y pon un tope: BigQuery te dice cuánto necesitaba.',
    qpanel('bq query --nouse_legacy_sql --maximum_bytes_billed=200000000 \\\n  "SELECT value FROM tweets_bronze.entrada TABLESAMPLE SYSTEM (0.1 PERCENT)"',
           None, [], '<span class="bad">BigQuery error in query operation: Query exceeded limit for bytes billed: 200000000. 23670554624 or higher required.</span>', 'RESULTADO REAL · cmd en Cloud Shell')
    + table(['Estimación en seco (no cuesta)', 'Bytes'], [['SELECT COUNT(*)', '0'], ['SELECT value … LIMIT 1', '23,670,340,066'], ['… TABLESAMPLE SYSTEM (0.1 PERCENT)', '66,865,367']])
,
    '56–60 min. Dos protecciones, una gratuita y otra de seguridad. Dry run calcula los bytes que leería la consulta sin ejecutarla. El tope (maximum_bytes_billed) hace que la consulta falle antes de cobrar si necesitara más. Aquí, la consulta con TABLESAMPLE estimaba 66.9 MB pero necesitaba 23,670,554,624 bytes: sin el tope, habría leído toda la columna. Es un error útil: te dice cuánto necesitaba. En el laboratorio lo reproduces. Una buena costumbre: en consultas exploratorias, siempre con tope.',
    'query', AP, src('error real') + ' · ' + DRY)

add('Repetir una carga no debe duplicar Bronze.',
    svg(430,
        T(0, 40, 'Filas en tweets_bronze.entrada', 'b')
        + G(0, R(120, 180, 300, 120, 'fu') + T(270, 160, '6,798,932', 'm b', 'middle') + T(270, 340, 'carga 1', 's', 'middle') + T(270, 372, '--replace', 'm', 'middle'))
        + G(1, R(570, 180, 300, 120, 'fg') + T(720, 160, '6,798,932', 'm b', 'middle') + T(720, 340, 'repetir con reemplazo', 's', 'middle') + T(720, 372, '--replace', 'm', 'middle'))
        + G(2, R(1020, 60, 300, 240, 'fr') + T(1170, 40, '13,597,864', 'm b', 'middle') + T(1170, 340, 'repetir añadiendo', 's', 'middle') + T(1170, 372, 'sin --replace (cálculo)', 'm', 'middle')),
        'Cargar de nuevo con reemplazo deja 6,798,932 filas; añadir sin reemplazo las duplicaría a 13,597,864')
    + step(3, p('Los ids distintos seguirían siendo 6,798,932: el doble de filas y ninguna alarma.', 'callout')),
    '63–67 min. Idempotencia es que repetir una operación deje el mismo resultado. Cargar con --replace reescribe la tabla completa: si repites el comando, la tabla sigue con 6,798,932 filas. Cargar sin --replace añade: dos cargas del mismo archivo dejan 13,597,864 filas, y nada avisa, porque cada fila sigue siendo válida. La cifra de la tercera barra es una suma, no una medición. Moraleja: decide siempre si una carga reemplaza o añade, y comprueba el conteo después, como en el laboratorio.',
    'bars', AP, src('la tercera barra es un cálculo (2 × 6,798,932)'))

add('Antes de cargar, anota el manifiesto del archivo.',
    '<dl class="manif"><dt>NOMBRE</dt><dd>war_tweets.txt</dd><dt>FORMATO</dt><dd>JSON Lines, un tweet por línea</dd><dt>TAMAÑO</dt><dd>23,663,541,134 bytes (22.04 GiB)</dd>'
    f'<dt>HUELLA MD5</dt><dd>{MD5}</dd><dt>GENERACIÓN</dt><dd>1772091678412778 (cambia en cada copia)</dd><dt>FILAS TRAS CARGAR</dt><dd>6,798,932</dd><dt>PERIODO</dt><dd>16–27 de marzo de 2022</dd></dl>'
    + step(1, p('Si la huella de tu copia coincide, tienes exactamente el mismo archivo.', 'callout')),
    '67–70 min. El manifiesto es la ficha de identidad de lo que cargas: nombre, formato, tamaño, huella, filas y periodo. La huella md5 es un resumen del contenido: si dos archivos tienen la misma, son idénticos. Por eso tu copia debe dar el mismo tamaño y la misma huella que el archivo de referencia; la generación y la clase de almacenamiento sí cambian. Un Bronze sin manifiesto no se puede repetir ni auditar. Se anotan los datos en el laboratorio, paso 2.',
    'sources', AP, 'Valores de referencia del curso · metadatos del archivo · ' + source('Storage · clases', 'https://docs.cloud.google.com/storage/docs/storage-classes'))

# ===== PAUSA 70–80 (slide 21)
add('Pausa.',
    '<p class="huge">10 min</p><p>Al volver: Cloud Shell y BigQuery Studio abiertos en tu proyecto.</p>',
    '70–80 min. Pausa real. Quien tenga el Colab de copia corriendo puede dejarlo en otra pestaña mientras descansa; la copia de 22 GiB tarda. Al volver, comprobar que el proyecto correcto aparece seleccionado.',
    'statement dark', PA, MED)

# ===== LABORATORIO 80–150 (slide 22)
add('Laboratorio: construye tu Bronze en 6 pasos.',
    '<p class="lab-ribbon">LABORATORIO · 70 MIN</p>' + table(['Paso', 'Qué haces', 'Qué obtienes'], [
        ['1 · 12 min', 'Copiar el archivo de Drive a tu bucket', 'war_tweets.txt en tu bucket'],
        ['2 · 8 min', 'Comprobar el objeto y anotar el manifiesto', 'tamaño y huella iguales'],
        ['3 · 12 min', 'Cargar el JSON a tweets_bronze.entrada', 'una tabla de una columna'],
        ['4 · 10 min', 'Contar filas y mirar un tweet crudo', '6,798,932 filas'],
        ['5 · 12 min', 'Estimar costos y probar un tope', '0 B frente a 23.67 GB'],
        ['6 · 16 min', 'De JSON a Parquet con Spark', 'FILAS 6798932']]) + lablink(1),
    '80–150 min. Seis pasos, 70 minutos, cada uno con dónde hacerlo, el código completo, la salida esperada, la comprobación y el error más frecuente en la guía. Todo ocurre en tu propio proyecto. Los pasos 1 y 6 son los más largos y los que no se ensayaron de principio a fin: la copia de Drive depende del cuaderno de Colab y de tu cuenta, y el lote de Spark puede tardar varios minutos. Si algo falla, anota el mensaje exacto: es parte del aprendizaje. No avances al paso siguiente sin cumplir la comprobación del anterior.',
    'lab-taller', LABP, MED)

# ===== CERRAR 150–180 (slides 23–24)
add('Para repetir por tu cuenta.',
    table(['Ejercicio', 'Qué haces', 'Qué comprobar'], [
        ['1 · Predice', 'Escribe tres consultas nuevas sobre Bronze y adivina sus bytes', 'compara con --dry_run'],
        ['2 · Repite', 'Vuelve a cargar con --replace', 'sigue 6,798,932'],
        ['3 · Mide una muestra', 'Carga solo las primeras 2,500 líneas (head del archivo) en otra tabla', 'cuenta y borra la tabla'],
        ['4 · Piensa', '¿Qué cambiaría si el archivo llegara cada semana?', 'reemplazar o añadir']]),
    '150–165 min. Cuatro ejercicios individuales para consolidar, sin entrega. El primero entrena la intuición del costo. El segundo comprueba la idempotencia. El tercero usa el mismo método de carga con un archivo diminuto; es más barato para experimentar y se borra al terminar. El cuarto es una pregunta de diseño: si el archivo se actualiza, ¿reemplazas o añades, y cómo evitas duplicar? No hay respuesta única; lo importante es poder defenderla con el conteo.',
    'table', CI, MED)

add('Con un Bronze afirmas lo que llegó, no lo que significa.',
    table(['Sí puedes afirmar', 'No puedes afirmar'],
          [['Llegaron 6,798,932 líneas y pesan 22.04 GiB.', 'Cuántos tweets hay por idioma o por tema: aún no hay columnas con tipo.'],
           ['Tu copia es idéntica al original (tamaño y huella).', 'Que estos tweets representen a todos los que hablaron de la guerra.'],
           ['Cada línea es un JSON de 29 campos, con un autor anidado.', 'Que dos tweets sean voces distintas: puede haber textos copiados.'],
           ['Leer value completo cuesta 23.67 GB.', 'Que el archivo cubra todo marzo: trae 12 días, y el primero es parcial.']]),
    '165–180 min. Cierre honesto con dos columnas. A la izquierda, lo que Bronze demuestra: las filas que llegaron, el tamaño, que tu copia es igual al original y que cada línea trae 29 campos. A la derecha, lo que todavía no se puede decir: conteos por idioma o por tema necesitan columnas con tipo, que llegan en Silver; la representatividad y la independencia de las voces dependen de cómo se extrajo el archivo. Lo que sigue: en la sesión 4 se convierte este JSON en tablas con columnas con tipo y reglas de calidad. Cierre: Bronze no responde preguntas de negocio; las hace posibles.',
    'can-say', CI, MED)

# ---------------------------------------------------------------- sincronía: lab de contenido.json y archivos de recursos
def sync():
    root = Path(__file__).resolve().parents[1]
    d = json.loads((root / 'especialidad-03/contenido.json').read_text())
    d['title'] = TITLE
    d['status'] = ('Guía con valores de referencia reales. Sin ensayar de principio a fin: la copia de war_tweets.txt con el cuaderno de Colab (sus celdas de copia de otros archivos sí se revisaron), la creación del bucket, '
                   'la carga completa del archivo desde tu bucket y el script de Spark de este laboratorio.')
    d['assets'] = [f'tweets/{n}' for n in ASSET_FILES] + ['tweets/10_bronze_tweets.sql']
    d['sources'] = [['BigQuery · cargar CSV desde Cloud Storage', 'https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv'],
                    ['BigQuery · estimar y controlar costos', 'https://docs.cloud.google.com/bigquery/docs/best-practices-costs'],
                    ['BigQuery · dry run', 'https://docs.cloud.google.com/bigquery/docs/dry-run-queries'],
                    ['Cloud Storage · clases de almacenamiento', 'https://docs.cloud.google.com/storage/docs/storage-classes'],
                    ['Dataproc Serverless', 'https://docs.cloud.google.com/dataproc-serverless/docs/overview'],
                    ['Apache Spark · guía', 'https://spark.apache.org/docs/latest/rdd-programming-guide.html']]
    d['lab'] = dict(
        aviso=('Las cifras de esta guía (tamaños, bytes, tiempos) son valores de referencia de ejecuciones reales del curso y pueden variar ligeramente en tu cuenta. '
               'Se ensayaron: la carga del método con 2,500 líneas reales, las estimaciones en seco y el patrón de envío de un lote Spark. '
               'No se ensayaron de principio a fin: la copia de war_tweets.txt con el cuaderno de Colab, la creación del bucket, la carga completa del archivo desde tu bucket y el script de Spark de este laboratorio.'),
        prerequisitos=['Un proyecto de Google Cloud con facturación activa (de la sesión 1) y Cloud Shell abierto.',
                       'Cuenta de Google con acceso al archivo war_tweets.txt en Drive y al cuaderno de Colab del curso, que copia de Drive a Storage: '+COLAB+'.',
                       'Unos 22 GiB de almacenamiento disponibles en tu proyecto para el archivo y otros 22 GiB para la tabla Bronze.'],
        instructions=('Ruta: Cloud Shell → crear el bucket → Colab para copiar el archivo → Cloud Shell para comprobarlo y cargarlo en BigQuery → BigQuery Studio '
                      'para contar → Cloud Shell para estimar costos y enviar el lote de Spark. Sustituye TU_PROYECTO y TU_BUCKET por tus valores. '
                      'El nombre del bucket debe ser único en todo el mundo.'),
        region=('Usa la ubicación US para el bucket y para los datasets de BigQuery: la carga funciona cuando el bucket está en la misma ubicación '
                'o dentro de la multirregión del dataset. Para Dataproc Serverless usa una región de Estados Unidos (por ejemplo us-central1) y la misma en todos tus lotes.'),
        steps=[{k: v for k, v in s.items()} for s in LAB],
        cierre=['Qué conservar: la tabla tweets_bronze.entrada y el objeto war_tweets.txt; la sesión 4 parte de ellas. Anota tu manifiesto (nombre, tamaño, huella y filas).',
                'Costo: el almacenamiento (22 GiB del archivo, 22 GiB de la tabla y unos 5.8 GiB del Parquet) se cobra por GiB y por mes; las consultas estimadas en seco no cuestan. '
                'Revisa Facturación después del lote de Spark.',
                'Cierre de recursos: puedes borrar el Parquet que escribió Spark con gcloud storage rm -r gs://TU_BUCKET/tweets_parquet/ si no lo vas a usar. '
                'No borres tweets_bronze ni el archivo original.',
                'Si falta un paso anterior, repítelo antes de seguir: cada comprobación depende de la anterior.'])
    (root / 'especialidad-03/contenido.json').write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
    rec = root / 'recursos/tweets'
    for old in rec.glob('s03_*'):
        if old.name not in ASSET_FILES: old.unlink()
    for name, content in ASSET_FILES.items(): (rec / name).write_text(content)
    print('contenido.json y recursos/tweets/s03_* actualizados')


if __name__ == '__main__':
    sync()
