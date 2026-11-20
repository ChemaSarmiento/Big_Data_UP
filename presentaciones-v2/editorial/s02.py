"""S2 · SQL con MariaDB y la base employees. Fuente única de las slides.
Todas las cifras salen de consultas reales sobre la base de muestra employees (datacharmer/test_db) en MariaDB 10.6."""
import re
from html import escape as _e
from guion import slide, p, step, lablink, source

TITLE = 'SQL con MariaDB: de una pregunta de negocio a una consulta'
BIGIDEA = 'Una consulta responde lo que contó: la pregunta decide la tabla, el grano y el filtro.'

REAL = 'Base de muestra employees en MariaDB · resultados reales'
DB = source('Base employees (datacharmer/test_db)', 'https://github.com/datacharmer/test_db')
SEL = source('MariaDB · SELECT', 'https://mariadb.com/kb/en/select/')
WHR = source('MariaDB · WHERE', 'https://mariadb.com/kb/en/where/')
ORD = source('MariaDB · ORDER BY', 'https://mariadb.com/kb/en/order-by/')
GRP = source('MariaDB · GROUP BY', 'https://mariadb.com/kb/en/group-by/')
AGG = source('MariaDB · funciones de agregación', 'https://mariadb.com/kb/en/aggregate-functions/')
CAS = source('MariaDB · CASE', 'https://mariadb.com/kb/en/case-operator/')
JOI = source('MariaDB · JOIN', 'https://mariadb.com/kb/en/join-syntax/')
SUB = source('MariaDB · subconsultas', 'https://mariadb.com/kb/en/subqueries/')


def hl(t):
    t = _e(t, quote=False)
    pat = r"(--[^\n]*)|('(?:[^'\n])*')|(\b\d+(?:\.\d+)?\b)|(\b(?:GROUP BY|ORDER BY|[A-Z][A-Z_]{1,})\b)"

    def f(m):
        c, s, n, k = m.groups()
        if c: return f'<span class="c">{c}</span>'
        if s: return f'<span class="s">{s}</span>'
        if n: return f'<span class="n">{n}</span>'
        return f'<span class="k">{k}</span>'
    return re.sub(pat, f, t)


def sql(t, cls=''):
    return f'<pre class="s2-sql {cls}" tabindex="0"><code>{hl(t)}</code></pre>'


def T(cols, rows, hot=(), cls=''):
    h = ''.join(f'<th>{_e(c)}</th>' for c in cols)
    out = ''
    for i, r in enumerate(rows):
        tds = ''
        for v in r:
            v = str(v)
            if v == 'NULL': tds += '<td class="null">NULL</td>'
            elif re.fullmatch(r'-?[\d,]+(\.\d+)?', v): tds += f'<td class="num">{_e(v)}</td>'
            else: tds += f'<td>{_e(v)}</td>'
        out += f'<tr class="{"hl" if i in hot else ""}">{tds}</tr>'
    return f'<table class="s2-data {cls}"><thead><tr>{h}</tr></thead><tbody>{out}</tbody></table>'


def bars(items, vmax=None, lw=230, vw=150, cls=''):
    vmax = vmax or max(v for _, v, _ in items)
    o = f'<div class="s2-bars {cls}" style="--lw:{lw}px;--vw:{vw}px">'
    for lab, v, c in items:
        w = max(0.6, 100 * v / vmax) if v else 0
        o += f'<div class="s2-bar {c}"><span class="lab">{lab}</span><span class="track"><span class="fill" style="width:{w:.2f}%"></span></span><span class="val">{v:,}</span></div>'
    return o + '</div>'


def cap(t): return f'<p class="s2-cap">{t}</p>'
def msg(t, warn=False): return f'<p class="s2-msg{" warn" if warn else ""}">{t}</p>'
def meta(n): return f'<div class="s2-meta"><span>Filas devueltas <b>{n}</b></span></div>'
def call(t): return p(t, 'callout')


def schema():
    def box(x, y, w, name, n, rows, pk=0, hot=False):
        h = 34 + 26 * len(rows) + 10
        o = f'<rect class="t" x="{x}" y="{y}" width="{w}" height="{h}" rx="3"/><rect class="{"hot" if hot else "h"}" x="{x}" y="{y}" width="{w}" height="34"/>'
        o += f'<text class="th" x="{x + 12}" y="{y + 24}">{name}</text><text class="n" x="{x + w - 12}" y="{y + 24}">{n}</text>'
        for i, r in enumerate(rows):
            cls = ' class="pk"' if i < pk else ''
            o += f'<text{cls} x="{x + 14}" y="{y + 34 + 26 * (i + 1) - 6}">{r}</text>'
        return o
    s = '<svg class="s2-schema" viewBox="0 0 1296 440" role="img" aria-label="Seis tablas: employees al centro, unida con dept_emp, dept_manager, salaries y titles por emp_no; departments se une con dept_emp y dept_manager por dept_no">'
    s += '<g>' + box(500, 40, 300, 'employees', '300,024', ['emp_no', 'birth_date', 'first_name', 'last_name', 'gender', 'hire_date'], 1, True) + '</g>'
    s += '<g data-step="1"><path class="l k" d="M340 112H500"/><text class="lk" x="372" y="102">emp_no</text>' + box(40, 70, 300, 'dept_emp', '331,603', ['emp_no', 'dept_no', 'from_date', 'to_date'], 2)
    s += '<path class="l k" d="M190 218V300"/><text class="lk" x="204" y="266">dept_no</text>' + box(40, 300, 300, 'departments', '9', ['dept_no', 'dept_name'], 1) + '</g>'
    s += '<g data-step="2"><path class="l k" d="M800 96H956"/><text class="lk" x="840" y="86">emp_no</text>' + box(956, 20, 300, 'salaries', '2,844,047', ['emp_no', 'salary', 'from_date', 'to_date'], 1)
    s += '<path class="l k" d="M800 200H880V260H956"/><text class="lk" x="884" y="250">emp_no</text>' + box(956, 210, 300, 'titles', '443,308', ['emp_no', 'title', 'from_date', 'to_date'], 1) + '</g>'
    s += '<g data-step="3"><path class="l k" d="M650 240V290"/><text class="lk" x="664" y="272">emp_no</text>' + box(500, 290, 300, 'dept_manager', '24', ['emp_no', 'dept_no', 'from_date', 'to_date'], 2)
    s += '<path class="l" d="M500 366H340"/><text class="lk" x="372" y="356">dept_no</text></g></svg>'
    return s


SLIDES = []
ABRIR = 'Abrir · 0–15 min'; COMP = 'Comprender · 15–50 min'; APL = 'Aplicar · 50–70 min'
PAU = 'Pausa · 70–80 min'; LAB = 'Laboratorio · 80–150 min'; CIE = 'Cerrar · 150–180 min'


def add(title, body, note, layout='plain', phase=COMP, src=REAL):
    SLIDES.append(slide(title, body, note, layout, phase, src))


# ---------------------------------------------------------------- ABRIR
add('Una pregunta de negocio se convierte en una consulta.',
    '<div><p class="overline">Sesión 2 · SQL con MariaDB y employees</p><h1>Una pregunta<br>de negocio<br>se convierte<br>en una consulta.</h1>'
    '<p class="lede">Una empresa de muestra con 300,024 personas en su historia. ¿Cuántas trabajan hoy? La respuesta no es 300,024, ni 331,603.</p></div>'
    '<div class="stack"><p class="large signal">240,124</p><p>personas trabajan hoy</p><p class="caption">Un número que sale de una consulta SQL.<br>Al final de la sesión sabrás escribirla.</p></div>',
    '0–3 min. Abrir con la pregunta sin SQL: «¿cuántas personas trabajan hoy en esta empresa?». Pedir un número a mano alzada. [pausa 3 s] Revelar 240,124. La base tiene 300,024 personas en toda su historia y 331,603 asignaciones a departamentos; hoy trabajan 240,124. La sesión enseña a hacer esa distinción con SQL. Los datos son de muestra, generados para practicar; ninguna cifra es de una empresa real.',
    'cover dark', ABRIR, REAL)

add('employees es una empresa de muestra con seis tablas conectadas.',
    '<p class="s2-lead">Cada caja es una tabla; el número es cuántas filas tiene. Las líneas son columnas en común: así se conectan.</p>' + schema(),
    '3–9 min. Dibujar la base con clics. Primero employees: una fila por persona (300,024). Segundo, dept_emp (en qué departamento trabajó cada persona y entre qué fechas) y departments (9 nombres). Tercero, salaries y titles: historial de sueldos y de cargos. Cuarto, dept_manager: quién dirigió cada departamento (24 filas). Subrayar que dept_emp tiene más filas que personas (331,603 contra 300,024): hay personas que cambiaron de departamento. La base es un ejemplo generado con licencia CC BY-SA 3.0: sirve para practicar, no describe una empresa real.',
    'schema', ABRIR, REAL)

add('«¿Cuántos empleados hay?» tiene cuatro respuestas distintas.',
    '<div class="s2-two wl"><div class="s2-col">' + bars([('employees · personas', 300024, ''), ('dept_emp · asignaciones', 331603, ''), ('salaries · sueldos', 2844047, 'dim')], lw=300) +
    step(1, bars([('trabajan hoy', 240124, 'hot')], vmax=2844047, lw=300)) + '</div>'
    '<div class="s2-col">' + step(2, msg('Cada número cuenta algo distinto: <b>personas</b>, <b>asignaciones</b>, <b>sueldos</b> o <b>personas vigentes</b>.') + msg('La pregunta de negocio decide qué tabla usar y qué contar. SQL no adivina qué querías decir.', True)) + '</div></div>',
    '9–15 min. Gancho de la sesión. Mostrar tres barras y pedir «¿cuál de estas es la respuesta correcta a cuántos empleados hay?». [pausa 3 s] Revelar la cuarta: 240,124 personas trabajan hoy. Ninguna de las otras tres es mentira, pero cada una responde otra pregunta. Aquí aparecen dos ideas que usaremos toda la sesión: el grano (qué representa una fila) y el filtro (qué filas cuentan). Error típico: contar filas de una tabla de historial como si fueran personas.',
    'path', ABRIR, REAL)

# ---------------------------------------------------------------- COMPRENDER
add('employees llega a tu base con tres comandos y unos cuatro minutos.',
    '<div class="s2-flow"><div class="fb">GitHub<small>repositorio test_db, ≈ 215 MB</small></div><span class="ar">→</span><div class="fb">git clone<small>copia los archivos a tu VM</small></div><span class="ar">→</span><div class="fb">mysql &lt; employees.sql<small>3 min 29 s en una e2-micro</small></div><span class="ar">→</span><div class="fb hot">tu base employees<small>6 tablas · 367 MB en disco</small></div></div>' +
    step(1, sql("git clone --depth 1 https://github.com/datacharmer/test_db.git\ncd test_db\nmysql -u big_data_user -pExample123 -t < employees.sql", 'sm')) +
    step(2, msg('Es una <b>base de muestra con datos generados</b> (licencia CC BY-SA 3.0): sirve para practicar y puede tener inconsistencias. No representa a una empresa real.')),
    '15–20 min. Explicar de dónde sale la base antes de usarla. git clone copia el repositorio a la VM; --depth 1 evita bajar todo el historial de versiones. El archivo employees.sql contiene las instrucciones que crean las tablas y llenan sus filas. Tiempos reales de nuestro ensayo en una VM e2-micro: 3 min 29 s de carga y 367 MB en disco. La carga se hace en el laboratorio, paso 1. El usuario big_data_user con contraseña compartida es una decisión didáctica para datos de práctica; nunca se usa en un sistema con datos reales.',
    'process', COMP, DB)

add('Una base relacional guarda datos en tablas con columnas de tipo fijo.',
    '<div class="s2-two wl"><dl class="s2-defs"><div><dt>tabla</dt><dd>Lista de filas que comparten las mismas columnas. Ejemplo: <code>employees</code>.</dd></div><div><dt>fila</dt><dd>Un registro. Aquí, una persona.</dd></div><div><dt>columna</dt><dd>Un dato con nombre y tipo. <code>hire_date</code> es una fecha.</dd></div><div><dt>clave primaria</dt><dd>Columna que identifica una fila sin repetirse: <code>emp_no</code> (PRI).</dd></div><div><dt>NULL</dt><dd>«No hay valor». No es 0 ni texto vacío.</dd></div></dl>'
    '<div class="s2-col">' + cap('DESCRIBE employees;') + T(['Field', 'Type', 'Null', 'Key'], [['emp_no', 'int(11)', 'NO', 'PRI'], ['birth_date', 'date', 'NO', ''], ['first_name', 'varchar(14)', 'NO', ''], ['last_name', 'varchar(16)', 'NO', ''], ['gender', "enum('M','F')", 'NO', ''], ['hire_date', 'date', 'NO', '']], hot=(0,), cls='sm') +
    cap('Tres filas de la tabla') + T(['emp_no', 'first_name', 'last_name', 'gender', 'hire_date'], [['10001', 'Georgi', 'Facello', 'M', '1986-06-26'], ['10002', 'Bezalel', 'Simmel', 'F', '1985-11-21'], ['10003', 'Parto', 'Bamford', 'M', '1986-08-28']], cls='sm') + '</div></div>',
    '20–23 min. Definir cinco palabras con la tabla real delante. Tabla: lista de filas con las mismas columnas. Fila: una persona. Columna: un dato con nombre y tipo (date, varchar, enum). Clave primaria: el emp_no identifica a cada persona y no se repite. NULL: ausencia de valor; en employees ninguna columna acepta NULL (Null = NO), pero lo veremos aparecer cuando unamos tablas. DESCRIBE es el comando para ver las columnas de una tabla.',
    'definitions', COMP, DB)

add('SQL es el idioma para pedirle datos a la base; hoy solo vas a leer.',
    '<div class="s2-two wl"><div class="s2-col"><dl class="s2-defs"><div><dt>SELECT</dt><dd><b>Lee</b> datos. No cambia nada. Es lo único que usaremos hoy.</dd></div><div><dt>INSERT UPDATE DELETE</dt><dd><b>Cambian</b> filas.</dd></div><div><dt>CREATE DROP</dt><dd><b>Crean o borran</b> tablas.</dd></div></dl>' + msg('SQL es declarativo: dices <b>qué</b> quieres y la base decide <b>cómo</b> encontrarlo.') + '</div>'
    '<div class="s2-col">' + sql('SELECT first_name, last_name\nFROM employees\nLIMIT 5;', 'sm') + T(['first_name', 'last_name'], [['Georgi', 'Facello'], ['Bezalel', 'Simmel'], ['Parto', 'Bamford'], ['Chirstian', 'Koblick'], ['Kyoichi', 'Maliniak']], cls='sm') + meta(5) + '</div></div>',
    '23–26 min. SQL (Structured Query Language) es el lenguaje estándar para consultar bases relacionales. Tres familias de sentencias: leer (SELECT), cambiar filas (INSERT, UPDATE, DELETE) y definir tablas (CREATE, DROP). Hoy solo leemos: es seguro experimentar porque SELECT no modifica nada. Declarativo significa que describimos el resultado, no los pasos. Aclarar que LIMIT 5 sin ORDER BY devuelve cinco filas cualesquiera: el orden no está garantizado.',
    'query', COMP, SEL)

add('SELECT elige las columnas y FROM dice de qué tabla.',
    '<div class="s2-two"><div class="s2-col">' + sql("SELECT emp_no,\n       CONCAT(first_name, ' ', last_name) AS nombre,\n       hire_date AS contratado\nFROM employees\nLIMIT 3;", 'sm') +
    step(1, msg('<b>AS</b> le pone un nombre nuevo a una columna. <b>CONCAT</b> junta textos. Una columna puede ser un cálculo.')) + '</div>'
    '<div class="s2-col">' + T(['emp_no', 'nombre', 'contratado'], [['10001', 'Georgi Facello', '1986-06-26'], ['10002', 'Bezalel Simmel', '1985-11-21'], ['10003', 'Parto Bamford', '1986-08-28']]) + meta(3) +
    step(2, msg('Tres partes: <b>qué columnas</b> (SELECT), <b>de qué tabla</b> (FROM) y <b>cuántas filas</b> (LIMIT). Cada consulta que escribas empieza así.')) + '</div></div>',
    '26–29 min. Leer la consulta en voz alta: «dame el número, el nombre completo y la fecha de contratación, de la tabla employees, solo tres filas». CONCAT une textos; AS pone un alias, es decir, un nombre más claro para la columna del resultado. Una columna del resultado puede ser un cálculo, no solo una columna guardada. Pregunta al grupo: ¿qué cambiaría si quitamos LIMIT 3? Devuelve las 300,024 filas.',
    'query', COMP, SEL)

add('WHERE deja solo las filas que cumplen la condición.',
    '<div class="s2-two wl"><div class="s2-col">' + sql("SELECT COUNT(*)\nFROM employees\nWHERE gender = 'F'\n  AND hire_date >= '1990-01-01';", 'sm') + T(['COUNT(*)'], [['53,839']], hot=(0,), cls='sm') + '</div>'
    '<div class="s2-col">' + cap('Cuántas filas quedan después de cada condición') + bars([('todas las filas', 300024, 'dim')], lw=300) + step(1, bars([("gender = 'F'", 120051, '')], vmax=300024, lw=300)) + step(2, bars([("+ hire_date >= 1990", 53839, 'hot')], vmax=300024, lw=300)) +
    step(2, msg('COUNT(*) cuenta filas. Cada condición con AND <b>reduce</b> el resultado; ninguna agrega filas.')) + '</div></div>',
    '29–32 min. WHERE es el filtro: la fila se queda solo si cumple la condición. Con AND deben cumplirse las dos. Mostrar el embudo: 300,024 filas, 120,051 mujeres, 53,839 mujeres contratadas desde 1990. COUNT(*) devuelve cuántas filas hay. Las fechas se escriben entre comillas con el formato año-mes-día. Pregunta al grupo: ¿puede el resultado ser mayor que 120,051 si agrego otra condición con AND? No.',
    'query', COMP, WHR)

add('Sin paréntesis, AND y OR pueden darte otra respuesta.',
    '<div class="s2-two"><div class="s2-col">' + cap('Sin paréntesis') + sql("WHERE gender = 'F'\n  AND hire_date >= '1999-01-01'\n   OR first_name = 'Georgi'", 'sm') + T(['COUNT(*)'], [['869']], hot=(0,), cls='sm') + '</div>'
    '<div class="s2-col">' + cap('Con paréntesis') + sql("WHERE gender = 'F'\n  AND (hire_date >= '1999-01-01'\n    OR first_name = 'Georgi')", 'sm') + T(['COUNT(*)'], [['722']], hot=(0,), cls='sm') + '</div></div>' +
    step(1, msg('AND se calcula <b>antes</b> que OR. Sin paréntesis la consulta dice: «mujeres desde 1999» <b>o</b> «cualquier persona llamada Georgi»: 616 + 253 = 869. Con paréntesis dice «mujeres que entraron desde 1999 o se llaman Georgi»: 616 + 106 = 722.', True)),
    '32–35 min. Dos consultas casi idénticas y dos respuestas. Preguntar antes de revelar: ¿cuál creen que cuenta lo que dijo el negocio? La respuesta depende de la pregunta. AND tiene prioridad sobre OR, como la multiplicación sobre la suma. Los números: 616 mujeres contratadas desde 1999, 253 personas llamadas Georgi y 106 mujeres llamadas Georgi. Regla práctica: cuando mezcles AND y OR, usa paréntesis siempre.',
    'trap', COMP, WHR)

add('IN, BETWEEN y LIKE resumen condiciones que usarás todo el tiempo.',
    T(['Operador', 'Pregunta que responde', 'Ejemplo en employees', 'Filas'], [
        ['IN', '¿Es uno de estos valores?', "first_name IN ('Georgi', 'Bezalel', 'Parto')", '709'],
        ['BETWEEN', '¿Está entre dos valores, extremos incluidos?', "hire_date BETWEEN '1990-01-01' AND '1990-12-31'", '25,610'],
        ['LIKE …%', '¿Empieza con este texto? (% = cualquier cosa)', "last_name LIKE 'Fac%'", '186'],
        ['LIKE %…', '¿Termina con este texto?', "last_name LIKE '%ez'", '577']], cls='txt') +
    step(1, msg('Todos van dentro de un <b>WHERE</b>. BETWEEN y LIKE son atajos: BETWEEN evita escribir dos comparaciones y LIKE busca patrones en texto.')),
    '35–38 min. Cuatro atajos con números reales. IN reemplaza varios OR sobre la misma columna: 709 personas se llaman Georgi, Bezalel o Parto. BETWEEN incluye ambos extremos: 25,610 personas fueron contratadas en 1990. LIKE busca patrones: el símbolo % significa cualquier cantidad de caracteres. Mostrar que Fac% encuentra Facello y 186 apellidos más. Error típico: usar BETWEEN con fechas sin pensar en que el último día queda incluido.',
    'operators', COMP, WHR)

add('ORDER BY ordena el resultado y LIMIT corta cuántas filas ves.',
    '<div class="s2-two"><div class="s2-col">' + cap('Los cinco salarios más altos de hoy') + sql("SELECT emp_no, salary\nFROM salaries\nWHERE to_date = '9999-01-01'\nORDER BY salary DESC\nLIMIT 5;", 'sm') + T(['emp_no', 'salary'], [['43624', '158,220'], ['254466', '156,286'], ['47978', '155,709'], ['253939', '155,513'], ['109334', '155,190']], cls='sm') + '</div>'
    '<div class="s2-col">' + step(1, cap('Empates: 9 personas entraron el 1985-01-01') + T(['Sin segunda llave', 'Con ORDER BY hire_date, emp_no'], [['110022', '110022'], ['110511', '110085'], ['110303', '110183'], ['110085', '110303'], ['110183', '110511']], cls='sm')) +
    step(2, msg('Si hay empates, el orden entre ellos <b>no está garantizado</b>. Agrega una segunda columna de orden para que el resultado sea siempre el mismo.', True)) + '</div></div>',
    '38–41 min. ORDER BY ordena; DESC es de mayor a menor. LIMIT corta: «los cinco primeros». to_date = 9999-01-01 es la convención de esta base para decir «sigue vigente»; la veremos más adelante. Segundo clic: nueve personas entraron el primer día de la base; sin una segunda llave de orden, el resultado puede cambiar entre ejecuciones (de hecho en nuestra prueba apareció en un orden distinto al ordenado por emp_no). Regla: todo ORDER BY con empates posibles lleva desempate.',
    'query', COMP, ORD)

add('Una función de agregación resume muchas filas en un número.',
    '<div class="s2-two wl"><div class="s2-col">' + sql("SELECT COUNT(*)        AS vigentes,\n       MIN(salary)     AS minimo,\n       MAX(salary)     AS maximo,\n       ROUND(AVG(salary)) AS promedio,\n       SUM(salary)     AS nomina\nFROM salaries\nWHERE to_date = '9999-01-01';", 'sm') + '</div>'
    '<div class="s2-col">' + T(['función', 'resultado'], [['COUNT', '240,124'], ['MIN', '38,623'], ['MAX', '158,220'], ['AVG', '72,012'], ['SUM', '17,291,866,123']], cls='sm') +
    step(1, msg('Se pasa de <b>240,124 filas a una sola</b>. La <b>mediana</b> (el valor del medio) es 69,805: junto al promedio 72,012 cuenta mejor cómo se reparten los sueldos.')) + '</div></div>',
    '41–44 min. Las funciones de agregación reciben muchas filas y devuelven una: COUNT cuenta, MIN y MAX dan los extremos, AVG el promedio y SUM el total. Aquí: 240,124 salarios vigentes, entre 38,623 y 158,220, promedio 72,012 y una nómina de 17,291,866,123. Segundo clic: la mediana es el valor que deja la mitad de las personas por debajo; aquí es 69,805. Cuando los datos tienen valores extremos, mirar ambos evita conclusiones apresuradas.',
    'query', COMP, AGG)

add('GROUP BY hace una cuenta por cada grupo.',
    '<div class="s2-two"><div class="s2-col">' + sql("SELECT gender, COUNT(*) AS empleados\nFROM employees\nGROUP BY gender;", 'sm') + T(['gender', 'empleados'], [['M', '179,973'], ['F', '120,051']], cls='sm') + meta(2) + '</div>'
    '<div class="s2-col"><div class="s2-piles"><div class="s2-pile"><div class="dots" style="--cols:6">' + '<i></i>' * 18 + '</div><b>M</b><span>179,973</span></div><div class="s2-pile b"><div class="dots" style="--cols:6">' + '<i></i>' * 12 + '</div><b>F</b><span>120,051</span></div></div>' + p('Cada punto son unas 10,000 personas.', 's2-sm') +
    step(1, msg('GROUP BY reparte las filas en montones, uno por valor, y la función de agregación <b>cuenta cada montón</b>. Sin GROUP BY, COUNT(*) daría un solo número: 300,024.')) + '</div></div>',
    '44–46 min. Imaginar que las 300,024 filas se reparten en dos montones según gender y luego se cuenta cada uno: 179,973 y 120,051. Cada punto de la figura son unas 10,000 personas. Regla: en un SELECT con GROUP BY, cada columna que no es una función de agregación debe estar en el GROUP BY. Pregunta al grupo: ¿por qué sumar 179,973 + 120,051 devuelve 300,024? Porque cada persona cae en exactamente un montón.',
    'diagram', COMP, GRP)

add('Una función de fecha te deja agrupar por año.',
    '<div class="s2-two wl"><div class="s2-col">' + sql("SELECT YEAR(hire_date) AS anio,\n       COUNT(*) AS contratados\nFROM employees\nGROUP BY YEAR(hire_date)\nORDER BY anio;", 'sm') + step(1, msg('El año 2000 solo tiene <b>13</b> contrataciones porque el archivo termina el <b>28 de enero de 2000</b>: no sabemos si la empresa dejó de contratar.', True)) + '</div>'
    '<div class="s2-col">' + bars([(str(a), n, 'hot' if a == 2000 else '') for a, n in [(1985, 35316), (1986, 36150), (1987, 33501), (1988, 31436), (1989, 28394), (1990, 25610), (1991, 22568), (1992, 20402), (1993, 17772), (1994, 14835), (1995, 12115), (1996, 9574), (1997, 6669), (1998, 4155), (1999, 1514), (2000, 13)]], lw=70, vw=100, cls='tight') + '</div></div>',
    '46–48 min. YEAR() extrae el año de una fecha; MONTH(), DAY() y DATE_FORMAT() hacen lo mismo con otras partes. Con GROUP BY YEAR(...) contamos contrataciones por año. La gráfica baja de 36,150 en 1986 a 1,514 en 1999. Segundo clic: el 2000 tiene 13 porque la última fecha de contratación del archivo es 2000-01-28; leerlo como «la empresa dejó de contratar» sería inventar. Ese es el tipo de límite que conviene decir en voz alta.',
    'chart', COMP, GRP)

add('HAVING filtra grupos; WHERE filtra filas.',
    '<div class="s2-two wl"><div class="s2-col">' + sql("SELECT dept_no, COUNT(*) AS vigentes\nFROM dept_emp\nWHERE to_date = '9999-01-01'\nGROUP BY dept_no\nHAVING COUNT(*) > 30000\nORDER BY vigentes DESC;", 'sm') + T(['dept_no', 'vigentes'], [['d005', '61,386'], ['d004', '53,304'], ['d007', '37,701']], cls='sm') + '</div>'
    '<div class="s2-col"><div class="s2-stages"><div class="s2-stage"><span class="num">1</span><b>FROM</b><span class="what">todas las asignaciones</span><span class="cnt">331,603 filas</span></div>'
    '<div class="s2-stage"><span class="num">2</span><b>WHERE</b><span class="what">solo las vigentes</span><span class="cnt">240,124 filas</span></div>'
    '<div class="s2-stage"><span class="num">3</span><b>GROUP BY</b><span class="what">un grupo por departamento</span><span class="cnt">9 grupos</span></div>'
    '<div class="s2-stage hot"><span class="num">4</span><b>HAVING</b><span class="what">grupos de más de 30,000</span><span class="cnt">3 grupos</span></div></div>' +
    step(1, msg('WHERE actúa <b>antes</b> de agrupar y mira filas. HAVING actúa <b>después</b> y mira el resultado de cada grupo.')) + '</div></div>',
    '48–50 min. La diferencia clave: WHERE descarta filas antes de formar grupos; HAVING descarta grupos después de contarlos. Seguir la tabla de etapas: 331,603 filas, 240,124 vigentes, 9 departamentos, 3 con más de 30,000 personas. No se puede poner COUNT(*) dentro de un WHERE porque el conteo aún no existe en esa etapa. Los códigos d005, d004 y d007 se leerán como nombres cuando unamos tablas.',
    'diagram', COMP, GRP)

add('CASE convierte una regla de negocio en una columna.',
    '<div class="s2-two wr"><div class="s2-col">' + sql("SELECT CASE\n  WHEN salary < 50000  THEN '1 · menos de 50 mil'\n  WHEN salary < 70000  THEN '2 · 50 a 70 mil'\n  WHEN salary < 100000 THEN '3 · 70 a 100 mil'\n  ELSE '4 · 100 mil o más'\n END AS banda,\n COUNT(*) AS empleados\nFROM salaries\nWHERE to_date = '9999-01-01'\nGROUP BY banda\nORDER BY banda;", 'xs') + '</div>'
    '<div class="s2-col">' + cap('Salarios vigentes por banda') + bars([('menos de 50 mil', 20305, ''), ('50 a 70 mil', 100902, ''), ('70 a 100 mil', 101418, 'hot'), ('100 mil o más', 17499, '')], lw=190, vw=110) + step(1, msg('CASE revisa las condiciones <b>en orden</b> y usa la primera que se cumple. Las bandas son una <b>regla del negocio</b>, no un dato: cambiarlas cambia la gráfica.')) + p('Suma: 240,124 personas. Ninguna se pierde.', 's2-sm') + '</div></div>',
    '50–52 min. CASE es el «si… entonces…» de SQL. Revisa cada WHEN en orden y se queda con el primero que se cumple, por eso las condiciones van de menor a mayor. Los cortes de 50, 70 y 100 mil los inventamos nosotros; si el negocio define otras bandas, el resultado cambia, y por eso conviene escribirlas explícitas. Comprobación útil: las cuatro bandas suman 240,124, igual que los salarios vigentes: ninguna fila se perdió ni se duplicó.',
    'query', COMP, CAS)

add('Una tabla de historial guarda varias filas por persona.',
    '<div class="s2-two"><div class="s2-col">' + cap('Salarios de la persona 10001: 17 filas') + T(['emp_no', 'salary', 'from_date', 'to_date'], [['10001', '60,117', '1986-06-26', '1987-06-26'], ['10001', '62,102', '1987-06-26', '1988-06-25'], ['…', '13 filas más', '', ''], ['10001', '85,097', '2001-06-22', '2002-06-22'], ['10001', '88,958', '2002-06-22', '9999-01-01']], hot=(4,), cls='sm') +
    step(1, msg('<b>to_date = 9999-01-01</b> es la convención para «sigue vigente»: es el sueldo de hoy. Las demás filas son historia.')) + '</div>'
    '<div class="s2-col"><div class="s2-big"><b>63,811</b><span>promedio de <b>todas</b> las filas de salaries</span></div>' + step(2, '<div class="s2-big"><b class="z">72,012</b><span>promedio de los salarios <b>vigentes</b></span></div>') +
    step(2, msg('Promediar todo el historial <b>subestima el sueldo de hoy</b>: cada persona pesa tantas veces como cambios de sueldo tuvo.', True)) + '</div></div>',
    '52–54 min. Una persona puede tener muchas filas: la 10001 tiene 17 salarios entre 1986 y 2002. La fila con to_date = 9999-01-01 es el sueldo vigente (88,958); la fecha lejana es el truco de esta base para decir «aún no termina». Segundo clic: el promedio de todas las filas es 63,811, pero el de los vigentes es 72,012. Cada persona cuenta tantas veces como filas de salario tiene. Pregunta al grupo: ¿qué pregunta de negocio responde cada promedio?',
    'history', COMP, REAL)

add('JOIN une tablas por una columna en común.',
    '<div class="s2-flow"><div class="fb">employees<small>emp_no · nombre</small></div><span class="ar">⇄</span><div class="fb">dept_emp<small>emp_no · dept_no · fechas</small></div><span class="ar">⇄</span><div class="fb">departments<small>dept_no · dept_name</small></div></div>' +
    sql("SELECT e.emp_no, e.first_name, e.last_name, d.dept_name, de.from_date, de.to_date\nFROM employees AS e\nJOIN dept_emp AS de ON de.emp_no = e.emp_no\nJOIN departments AS d ON d.dept_no = de.dept_no\nWHERE e.emp_no IN (10001, 10010);", 'xs') +
    T(['emp_no', 'first_name', 'last_name', 'dept_name', 'from_date', 'to_date'], [['10001', 'Georgi', 'Facello', 'Development', '1986-06-26', '9999-01-01'], ['10010', 'Duangkaew', 'Piveteau', 'Production', '1996-11-24', '2000-06-26'], ['10010', 'Duangkaew', 'Piveteau', 'Quality Management', '2000-06-26', '9999-01-01']], hot=(2,), cls='sm') +
    step(1, msg('<b>ON</b> dice qué columnas hacen pareja. La persona 10010 aparece dos veces: cambió de departamento en 2000. <b>AS</b> da un apodo corto a cada tabla.')),
    '54–57 min. Un JOIN une filas de dos tablas cuando una columna coincide: ON de.emp_no = e.emp_no. Encadenamos dos uniones para pasar de empleado a departamento y de código a nombre. Resultado: 10001 trabaja en Development; 10010 pasó de Production a Quality Management en 2000, por eso aparece en dos filas. Los apodos e, de y d acortan la consulta. Error típico: olvidar la condición ON; lo veremos más adelante con números.',
    'join', COMP, JOI)

add('INNER descarta a quien no tiene pareja; LEFT lo conserva con NULL.',
    '<div class="s2-demo" data-demo="inner-left"><div class="s2-toggle" role="group" aria-label="Tipo de unión"><button type="button" data-mode="inner" aria-pressed="true">INNER JOIN</button><button type="button" data-mode="left" aria-pressed="false">LEFT JOIN</button></div>'
    '<div class="s2-two"><div class="s2-col"><div data-sql="inner">' + sql("SELECT e.emp_no, e.first_name, m.dept_no\nFROM employees AS e\nINNER JOIN dept_manager AS m\n  ON m.emp_no = e.emp_no;", 'sm') + '</div><div data-sql="left" hidden>' + sql("SELECT e.emp_no, e.first_name, m.dept_no\nFROM employees AS e\nLEFT JOIN dept_manager AS m\n  ON m.emp_no = e.emp_no;", 'sm') + '</div>'
    '<p class="s2-msg" data-msg role="status"></p></div>'
    '<div class="s2-col"><table class="s2-data sm" data-join-table><thead><tr><th>emp_no</th><th>first_name</th><th>dept_no</th></tr></thead><tbody>'
    '<tr data-left="1"><td class="num">10001</td><td>Georgi</td><td class="null">NULL</td></tr><tr data-left="1"><td class="num">10002</td><td>Bezalel</td><td class="null">NULL</td></tr><tr data-left="1"><td class="num">10003</td><td>Parto</td><td class="null">NULL</td></tr>'
    '<tr><td class="num">110022</td><td>Margareta</td><td>d001</td></tr><tr><td class="num">110039</td><td>Vishwani</td><td>d001</td></tr><tr><td class="num">110085</td><td>Ebru</td><td>d002</td></tr></tbody></table>'
    '<p class="s2-sm">Seis personas de employees; dept_manager solo conoce a quienes fueron gerentes.</p></div></div></div>',
    '57–60 min. Demo interactiva. Primero INNER JOIN: solo quedan las tres personas que aparecen en dept_manager; las otras tres desaparecen sin aviso. Después LEFT JOIN: se conservan todas las filas de la tabla izquierda (employees) y donde no hay pareja aparece NULL. En toda la base: INNER devuelve 24 filas; LEFT devuelve 300,024, de las cuales 300,000 llevan NULL. NULL es información: dice que esa persona nunca fue gerente. Pregunta al grupo: si nos piden «todas las personas y, si fueron gerentes, de qué departamento», ¿cuál usamos?',
    'join', COMP, JOI)

add('Un JOIN puede multiplicar filas; cuenta lo que de verdad quieres contar.',
    '<div class="s2-flow"><div class="fb">300,024<small>personas en employees</small></div><span class="ar">→</span><div class="fb">JOIN salaries<small>cada persona trae todos sus sueldos</small></div><span class="ar">→</span><div class="fb hot">2,844,047<small>filas en el resultado</small></div></div>' +
    T(['Unión', 'Filas', 'Promedio de salario'], [['employees JOIN salaries', '2,844,047', '63,811 · no es el sueldo de hoy'], ["… ON … AND to_date = '9999-01-01'", '240,124', '72,012 · sueldo vigente'], ['employees CROSS JOIN departments (sin ON)', '2,700,216', '300,024 × 9 · cruce de todo con todo']], hot=(1,), cls='txt') +
    step(1, msg('Antes de interpretar un resultado compara su número de filas con el que esperabas. Si no coincide, <b>la unión multiplicó o descartó filas</b>.', True)),
    '60–63 min. Cada persona tiene varios salarios; al unir employees con salaries, cada persona se repite una vez por salario: pasamos de 300,024 a 2,844,047 filas y el promedio cae a 63,811. Si unimos solo el salario vigente (condición to_date), queda una fila por persona con salario: 240,124. Tercer renglón: un JOIN sin condición cruza todas las filas con todas: 300,024 por 9 departamentos, 2,700,216 filas sin sentido. Hábito: comparar siempre el conteo antes y después de un JOIN.',
    'trap', COMP, JOI)

add('Una subconsulta es una consulta dentro de otra.',
    '<div class="s2-two"><div class="s2-col">' + cap('Subconsulta con un valor') + sql("SELECT COUNT(*) AS arriba_del_promedio\nFROM salaries\nWHERE to_date = '9999-01-01'\n  AND salary > (SELECT AVG(salary)\n                FROM salaries\n                WHERE to_date = '9999-01-01');", 'xs') + T(['arriba_del_promedio'], [['107,706']], hot=(0,), cls='xs') + step(1, msg('La consulta de adentro corre primero: promedio 72,012. Luego se comparan los 240,124 salarios: <b>107,706</b> lo superan.')) + '</div>'
    '<div class="s2-col">' + cap('Subconsulta con una lista (IN)') + sql("SELECT first_name, last_name\nFROM employees\nWHERE emp_no IN (SELECT emp_no\n                 FROM dept_manager)\nORDER BY last_name\nLIMIT 5;", 'xs') + T(['first_name', 'last_name'], [['Ebru', 'Alpin'], ['Tonny', 'Butterworth'], ['Rosine', 'Cools'], ['Leon', 'DasSarma'], ['Oscar', 'Ghazalie']], cls='xs') + step(2, msg('La de adentro devuelve los 24 números de gerentes; la de afuera busca esas personas.')) + '</div></div>',
    '63–66 min. Una subconsulta va entre paréntesis y se ejecuta primero; su resultado se usa en la consulta de afuera. Caso 1: devuelve un número (el promedio vigente, 72,012) para compararlo con cada salario; 107,706 de 240,124 lo superan. Caso 2: devuelve una lista (los emp_no de gerentes) para usarla con IN. Es otra forma de responder lo que a veces se resuelve con JOIN; elegir la más legible. Advertir que subconsultas muy anidadas se vuelven difíciles de leer.',
    'query', COMP, SUB)

add('La base lee tu consulta en un orden distinto del que la escribes.',
    '<div class="s2-two wl"><div class="s2-col">' + sql("SELECT d.dept_name, COUNT(*) AS vigentes\nFROM dept_emp AS de\nJOIN departments AS d\n  ON d.dept_no = de.dept_no\nWHERE de.to_date = '9999-01-01'\nGROUP BY d.dept_name\nHAVING COUNT(*) > 30000\nORDER BY vigentes DESC\nLIMIT 2;", 'xs') + '</div>'
    '<div class="s2-col"><div class="s2-stages">' +
    step(1, '<div class="s2-stage"><span class="num">1</span><b>FROM + JOIN</b><span class="what">une las tablas</span><span class="cnt">331,603</span></div>') +
    step(2, '<div class="s2-stage"><span class="num">2</span><b>WHERE</b><span class="what">filtra filas</span><span class="cnt">240,124</span></div>') +
    step(3, '<div class="s2-stage"><span class="num">3</span><b>GROUP BY</b><span class="what">forma grupos</span><span class="cnt">9</span></div>') +
    step(4, '<div class="s2-stage"><span class="num">4</span><b>HAVING</b><span class="what">filtra grupos</span><span class="cnt">3</span></div>') +
    step(5, '<div class="s2-stage"><span class="num">5</span><b>SELECT</b><span class="what">calcula columnas</span><span class="cnt">3</span></div>') +
    step(6, '<div class="s2-stage"><span class="num">6</span><b>ORDER BY</b><span class="what">ordena</span><span class="cnt">3</span></div>') +
    step(7, '<div class="s2-stage hot"><span class="num">7</span><b>LIMIT</b><span class="what">corta: Development 61,386 · Production 53,304</span><span class="cnt">2</span></div>') + '</div></div></div>',
    '66–70 min. Resumen de la parte de conceptos. La consulta se escribe con SELECT arriba, pero la base la procesa así: une tablas (331,603 filas), filtra filas con WHERE (240,124), agrupa (9 grupos), filtra grupos con HAVING (3), calcula las columnas del SELECT, ordena y corta. Esto explica por qué un alias definido en SELECT no se puede usar en WHERE, y por qué WHERE y HAVING no son intercambiables. Cada clic agrega una etapa con el número real de filas o grupos que quedan. Comprender: cada etapa solo ve lo que dejó la anterior.',
    'diagram', COMP, SEL)

# ---------------------------------------------------------------- APLICAR
add('Escribe primero la pregunta de negocio; la consulta viene después.',
    '<div class="s2-two"><div class="s2-xlate"><div class="s2-xl"><p class="xq">A · ¿Cuántas personas trabajan hoy en la empresa?</p>' +
    step(1, '<p class="xp">Piezas: contar personas distintas · tabla dept_emp · solo vigentes (to_date)</p>') + step(2, sql("SELECT COUNT(DISTINCT emp_no)\nFROM dept_emp\nWHERE to_date = '9999-01-01';", 'xs')) + step(3, '<p class="xa">240,124</p>') + '</div></div>'
    '<div class="s2-xlate"><div class="s2-xl"><p class="xq">B · ¿Cuál es el salario vigente promedio de cada departamento?</p>' +
    step(1, '<p class="xp">Piezas: promedio de salary · dept_emp + departments + salaries · solo vigentes · un grupo por departamento</p>') +
    step(2, sql("SELECT d.dept_name, ROUND(AVG(s.salary)) AS promedio\nFROM dept_emp AS de\nJOIN departments AS d ON d.dept_no = de.dept_no\nJOIN salaries AS s ON s.emp_no = de.emp_no\n AND s.to_date = '9999-01-01'\nWHERE de.to_date = '9999-01-01'\nGROUP BY d.dept_name\nORDER BY promedio DESC;", 'xs')) +
    step(3, '<p class="xa">Sales 88,853 · Marketing 80,059 · … · Human Resources 63,922</p>') + '</div></div></div>',
    '50–62 min. Ejercicio de traducción pregunta → consulta, en cuatro pasos por pregunta. 1) Leer la pregunta. 2) Escribir las piezas en español: qué se cuenta, de qué tabla, qué filas valen, cómo se agrupa. 3) Escribir la consulta. 4) Comprobar el resultado. Pedir que el grupo escriba las piezas en papel antes de cada clic. Pregunta A: 240,124 personas trabajan hoy (no 300,024). Pregunta B: Sales paga más (88,853) y Human Resources menos (63,922); nueve filas en total. En el laboratorio, paso 6, resuelven la pregunta C por su cuenta. Error típico: escribir la consulta sin decidir qué cuenta como «hoy».',
    'translate', APL, REAL)

add('Cuatro errores clásicos y cómo se ven en los números.',
    T(['Error', 'Cómo se ve en esta base', 'Cómo se evita'], [
        ['Contar filas en vez de personas', 'COUNT(*) en dept_emp da 331,603; las personas distintas son 300,024', 'COUNT(DISTINCT emp_no) y decidir qué es «vigente»'],
        ['Promediar todo el historial', '63,811 en lugar de 72,012', "Filtrar to_date = '9999-01-01'"],
        ['JOIN sin condición', '2,700,216 filas (300,024 × 9)', 'Todo JOIN lleva ON con las llaves'],
        ['AND y OR sin paréntesis', '869 en lugar de 722', 'Paréntesis cada vez que mezclas AND y OR']], hot=(), cls='txt') +
    step(1, msg('Los cuatro errores <b>devuelven un resultado sin avisar</b>. La base no sabe qué querías preguntar: solo ejecuta lo que escribiste.', True)),
    '62–70 min. Cierre de la parte práctica con cuatro trampas reales ya vistas. Para cada una, mostrar el síntoma con números: 331,603 contra 300,024; 63,811 contra 72,012; 2,700,216 filas; 869 contra 722. Insistir en que ninguna produce un error de sintaxis: la consulta corre y entrega un número equivocado. Hábito para el laboratorio: antes de confiar en un resultado, contar filas y compararlas con lo que se esperaba.',
    'trap', APL, REAL)

# ---------------------------------------------------------------- PAUSA
add('Pausa. Vuelve con tu terminal abierta.',
    '<p class="huge">10 min</p><p>Al volver: abre Cloud Shell, entra a tu VM y confirma que <code>mysql</code> responde.</p>',
    '70–80 min. Pausa real. Al volver, cada persona abre Cloud Shell y entra a su VM con gcloud compute ssh. Si la VM está apagada, enciéndela con gcloud compute instances start. Si algo falla, anotar el mensaje de error completo: servirá para el paso 1 del laboratorio.',
    'statement dark', PAU, REAL)

# ---------------------------------------------------------------- LABORATORIO
add('Hoy escribes seis bloques de consultas.',
    '<div class="s2-lab">'
    '<div class="st"><span class="n">1</span><div><b>Conéctate y carga employees</b><span>git clone, cargar la base y contar sus seis tablas</span></div><span class="m">12 min</span></div>'
    '<div class="st"><span class="n">2</span><div><b>Mira la base</b><span>SHOW TABLES, DESCRIBE y tus primeras consultas con SELECT</span></div><span class="m">10 min</span></div>'
    '<div class="st"><span class="n">3</span><div><b>Filtra y ordena</b><span>WHERE, paréntesis, IN, BETWEEN, LIKE, ORDER BY y LIMIT</span></div><span class="m">12 min</span></div>'
    '<div class="st"><span class="n">4</span><div><b>Resume y agrupa</b><span>funciones de agregación, GROUP BY, HAVING y CASE</span></div><span class="m">12 min</span></div>'
    '<div class="st"><span class="n">5</span><div><b>Une tablas</b><span>JOIN, INNER contra LEFT y filas que se multiplican</span></div><span class="m">12 min</span></div>'
    '<div class="st"><span class="n">6</span><div><b>De la pregunta a la consulta</b><span>subconsultas y tres preguntas de negocio resueltas por ti</span></div><span class="m">12 min</span></div></div>' +
    lablink(1),
    '80–150 min. Una sola slide para el laboratorio: la guía completa (código, salida esperada, comprobación y error frecuente) está en laboratorio.html. Paso 1: 12 min; 2: 10; 3: 12; 4: 12; 5: 12; 6: 12. Cada paso termina con tres ejercicios cuya respuesta numérica está en el archivo SQL para que cada persona verifique sola. Recomendar abrir la guía en una pestaña y la terminal en otra. Si un paso no sale, leer el «error frecuente» de la guía antes de pedir ayuda.',
    'lab-taller', LAB, REAL)

# ---------------------------------------------------------------- CERRAR
add('Una consulta responde lo que contó, no lo que significa.',
    '<table class="s2-data can"><thead><tr><th class="ok">Sí podemos afirmar</th><th class="bad">No podemos afirmar</th></tr></thead><tbody>'
    '<tr><td>240,124 personas tienen un departamento vigente.</td><td>Que 300,024 personas trabajan hoy.</td></tr>'
    '<tr><td>El salario vigente promedio es 72,012 y la mediana, 69,805.</td><td>Que ese es «el sueldo normal»: no sabemos puestos ni costo de vida.</td></tr>'
    '<tr><td>Hombres promedian 72,045 y mujeres 71,964 (vigentes).</td><td>Que no hay desigualdad: no se controló puesto, antigüedad ni historia.</td></tr>'
    '<tr><td>La última contratación es de enero de 2000.</td><td>Que la empresa dejó de contratar: el archivo termina ahí.</td></tr>'
    '<tr><td>Ventas tiene el promedio más alto (88,853).</td><td>Que Ventas «paga mejor»: no sabemos qué puestos agrupa.</td></tr></tbody></table>' +
    step(1, msg('Los datos son una <b>muestra generada para practicar</b>: ninguna de estas frases describe una empresa real.', True)),
    '150–168 min. Cierre honesto. A la izquierda, lo que las consultas realmente demuestran con estas tablas; a la derecha, saltos que alguien podría dar sin darse cuenta. Recorrer fila por fila con las cifras reales: 240,124 contra 300,024; 72,012 y 69,805; 72,045 contra 71,964 (una diferencia de 81, 0.1 %) que no demuestra igualdad porque no se controló nada más; el 2000 se debe al corte del archivo; Ventas 88,853. Último clic: la base es de muestra generada, así que estas lecturas son ejercicios de criterio, no hallazgos.',
    'claims', CIE, REAL)

add('Practica por tu cuenta con tres preguntas más.',
    '<div class="s2-xlate"><div class="s2-xl"><p class="xq">1 · ¿Cuántas personas se llaman «Parto» y cuántas de ellas son mujeres?</p><p class="xa">Comprueba: 228 y 87</p></div>'
    '<div class="s2-xl"><p class="xq">2 · ¿En cuántos departamentos distintos ha trabajado la persona 10010?</p><p class="xa">Comprueba: 2</p></div>'
    '<div class="s2-xl"><p class="xq">3 · ¿Cuántos cargos distintos existen hoy y cuántas personas tiene el más pequeño?</p><p class="xa">Comprueba: 7 cargos; el más pequeño tiene 9 personas</p></div></div>' +
    step(1, msg('Para cada una: escribe la pregunta, las piezas y recién después la consulta. Verifica el número de filas antes de confiar en el resultado. <b>Pista:</b> usa employees, dept_emp y titles.')) +
    step(2, p('Antes de salir: apaga tu VM para no gastar. En Cloud Shell: gcloud compute instances stop mariadb-curso --zone=us-central1-a', 'callout')),
    '168–180 min. Tres preguntas extra para hacer sin ayuda; las respuestas numéricas están en la slide para que cada persona verifique. La 1 usa WHERE y COUNT con SUM(gender = \'F\'); la 2 usa COUNT(DISTINCT) sobre dept_emp; la 3 usa GROUP BY sobre titles y luego un resumen. Último clic: apagar la VM al terminar evita el cargo de cómputo; los datos se conservan en su disco. Cierre: los cinco hábitos de la sesión: escribir la pregunta, decidir qué es una fila, filtrar lo vigente, verificar el conteo, decir qué no demuestra.',
    'exercise', CIE, REAL)
