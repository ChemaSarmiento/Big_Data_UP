"""S1 · Introducción a big data y a la nube, y tu ambiente de trabajo. Fuente única del deck.
Sin dataset hilo (empieza en S3). Casos de apertura hipotéticos, fuentes verificables y la cuenta de ejemplo
son ilustrativos y están rotulados. La salida real del laboratorio está en especialidad-01/laboratorio.html."""
import html
from guion import slide,p,step,table,flow,code,proof,lablink,source
E=html.escape
TITLE='Antes de elegir una herramienta, entiende el problema'
BIGIDEA='Un problema de datos es «grande» cuando una restricción te detiene; entenderlo y montar tu ambiente viene antes de elegir tecnología.'
def st(k):return f' data-step="{k}"' if k else ''
NIST=source('NIST · definición de las V','https://www.nist.gov/publications/nist-big-data-interoperability-framework-volume-1-definitions')
XLS=source('Microsoft · límites de Excel','https://support.microsoft.com/en-us/office/excel-specifications-and-limits-1672b34d-7043-467e-8e27-269d656771c3')
OLTP=source('Google Cloud · qué es OLTP','https://cloud.google.com/learn/what-is-oltp')
LAKE=source('Google Cloud · qué es un data lakehouse','https://cloud.google.com/discover/what-is-a-data-lakehouse')
PAAS=source('Google Cloud · IaaS, PaaS y SaaS','https://cloud.google.com/learn/paas-vs-iaas-vs-saas')
IAMDOC=source('Google Cloud · IAM','https://docs.cloud.google.com/iam/docs/overview')
HIER=source('Google Cloud · jerarquía de recursos','https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy')
REG=source('Google Cloud · regiones y zonas','https://docs.cloud.google.com/compute/docs/regions-zones')
STOP=source('Google Cloud · detener e iniciar una VM','https://docs.cloud.google.com/compute/docs/instances/stop-start-instance')
FREE=source('Google Cloud · prueba gratuita y cupos','https://docs.cloud.google.com/free/docs/free-cloud-features')
BUDG=source('Google Cloud · presupuestos y alertas','https://docs.cloud.google.com/billing/docs/how-to/budgets')
MAP=source('Google Cloud · panorama de datos y analítica','https://cloud.google.com/products/data-analytics')
MACH=source('Google Cloud · tipos de máquina','https://docs.cloud.google.com/compute/docs/machine-resource')
HSBC=source('HSBC / Google Cloud · Risk Advisory Tool','https://cloud.google.com/customers/hsbc-risk-advisory-tool')
MAYO=source('Mayo Clinic / Google Cloud','https://cloud.google.com/blog/products/data-analytics/genome-data-analytics-with-google-cloud')
UPS=source('UPS Capital / Google Cloud','https://cloud.google.com/blog/products/data-analytics/ups-leverages-bigquery-and-striim-for-ai-secured-package-delivery')
MELI=source('Mercado Libre / Google Cloud','https://cloud.google.com/blog/products/data-analytics/improving-retail-using-bigquery-and-looker')
PROP='Elaboración propia · Especialidad'
HIPO='Casos hipotéticos de apertura · cifras supuestas'
S=[]
def add(title,body,note,layout='plain',phase='Comprender · 15–50 min',src=PROP):S.append(slide(title,body,note,layout,phase,src))
def explain(t,sp=0):return f'<p class="s1-explain"{st(sp)}>{t}</p>'
def callout(t,sp=0):return f'<p class="callout"{st(sp)}>{t}</p>'
def bars(rows):
    o='<div class="s1-bars">'
    for label,pct,val,c in rows:o+=f'<div class="b-row"><b>{label}</b><div class="b-track"><i class="b-fill {c}" style="--w:{pct}%"></i></div><output>{val}</output></div>'
    return o+'</div>'

# ───────────────────────── ABRIR · 0–15 min ─────────────────────────
add('Antes de elegir una herramienta, entiende el problema',
 '<div><p class="overline">Sistemas de datos distribuidos · Sesión 1</p><h1>Antes de elegir<br>una herramienta,<br>entiende el problema.</h1><p class="lede">Big data, nube y tu ambiente de trabajo.</p>'
 '<div class="s1-three"><div><b>Entender</b><span>qué es big data</span></div><div><b>Decidir</b><span>cuándo hace falta</span></div><div><b>Montar</b><span>tu ambiente</span></div></div></div>'
 '<img class="signature" src="../identidad/mandelbrot-deco-noche.png" alt="Ventanas fractales del kit de identidad de Chema Sarmiento">',
 '0–2 min. Abrir con la promesa: hoy no hay código pesado. Se sale con dos cosas: un criterio para decidir cuándo un problema de datos exige una inversión seria (y cuándo es sobre-ingeniería) y un ambiente propio en la nube, listo para las demás sesiones. Pregunta de entrada: ¿alguien ha estado en una reunión donde se propuso «usar big data» para algo que se resolvía con un reporte en Excel? Escuchar una o dos respuestas, sin nombres.',
 'cover dark','Abrir · 0–15 min',PROP)
add('Dos preguntas de un mismo banco piden arquitecturas distintas.',
 '<div class="s1-two"><div class="s1-case a"><h2>Reporte mensual</h2><p class="big">50 MB</p><dl><dt>Pregunta</dt><dd>¿Cuántas ventas tuvo cada sucursal?</dd><dt>Cuándo</dt><dd>Una vez al mes</dd><dt>Quién actúa</dt><dd>Una persona que lee el reporte</dd></dl></div>'
 '<div class="s1-case b"><h2>Alerta de fraude</h2><p class="big">millones</p><dl><dt>Pregunta</dt><dd>¿Esta compra es fraude?</dd><dt>Cuándo</dt><dd>Mientras se aprueba el pago</dd><dt>Quién actúa</dt><dd>Un sistema, en segundos</dd></dl></div></div>'
 +callout('Mismo banco y misma nube: lo que cambia la arquitectura es la decisión y cuánto puede esperar, no el tamaño de la empresa.',1),
 '2–6 min. Dibujar la diferencia con las dos tarjetas. Reporte: 50 MB, cabe en la memoria de cualquier laptop, nadie sufre si tarda un minuto. Fraude: millones de eventos, cada uno exige una decisión en segundos. Preguntar al grupo: ¿necesitan la misma arquitectura? Dejar que respondan antes del clic. Las cifras son supuestos del caso, no mediciones. Idea a clavar: la pregunta útil nunca es «cuántos datos tenemos», sino «qué decisión hay que tomar, con cuánta demora tolerable y qué trabajo impide cumplirla».',
 'comparison','Abrir · 0–15 min',HIPO)
add('Un dato es un hecho suelto; solo sirve cuando apoya una decisión.',
 '<div class="s1-chain"><div class="s1-step on"><b>1 · Dato</b><h2>Un hecho suelto</h2><p>Un registro sin interpretar.</p><div class="ej">Sucursal Centro · 12 ventas · $4,800</div></div>'
 '<div class="link" data-step="1">→</div><div class="s1-step on" data-step="1"><b>2 · Información</b><h2>Datos que responden</h2><p>Se agrupan y comparan para contestar una pregunta.</p><div class="ej">Ventas del mes por sucursal: Centro $4,800 · Norte $9,100</div></div>'
 '<div class="link" data-step="2">→</div><div class="s1-step on" data-step="2"><b>3 · Decisión</b><h2>Una acción posible</h2><p>Alguien puede hacer algo con lo que sabe.</p><div class="ej">Reforzar personal en Norte y revisar horarios en Centro</div></div></div>',
 '6–9 min. Definir con el ejemplo, un paso por clic. Dato: «Centro, 12 ventas, $4,800» no dice nada por sí solo. Información: al comparar sucursales aparece algo que se puede leer. Decisión: la acción que alguien puede tomar. Insistir en que toda la sesión (y el curso) se mide contra esta cadena: si no hay decisión al final, el dato guardado no vale nada. Las cifras son un ejemplo inventado para ilustrar.',
 'path','Abrir · 0–15 min','Ejemplo ilustrativo · cifras inventadas')
add('Un problema es «grande» cuando una restricción te detiene, no por su peso.',
 '<div class="s1-bal"><div class="col l"><h2>Lo que el problema exige</h2><ul><li>Mucho volumen</li><li>Respuestas rápidas</li><li>Formatos mezclados</li><li>Datos poco confiables</li></ul></div><div class="mid">&gt;<small>si exige más de lo que tienes</small></div><div class="col r"><h2>Lo que tienes</h2><ul><li>La memoria de una máquina</li><li>El plazo para responder</li><li>Personas y presupuesto</li><li>Tiempo para limpiar</li></ul></div></div>'
 +callout('Un tamaño por sí solo no decide el diseño: depende de la decisión y del plazo.',1),
 '9–13 min. Es la definición de trabajo de big data para todo el curso: no existe un número mágico de GB. Un problema se vuelve de big data cuando lo que exige (volumen, velocidad, variedad, confiabilidad) supera lo que permiten tu memoria, tu plazo, tu gente y tu dinero. Un archivo de 20 GB puede resolverse en una máquina si el plazo es amplio; una aplicación pequeña puede exigir otra arquitectura si hay que responder en segundos. Pausar [pausa 3 s] y pedir un ejemplo de su propia industria donde la restricción sea el plazo y no el tamaño.',
 'comparison','Abrir · 0–15 min',PROP)
add('Ocho sesiones: de entender el problema a defender una recomendación.',
 '<div class="s1-path"><div class="now"><b>S1</b><span>Introducción y tu ambiente</span></div><div><b>S2</b><span>SQL para hacer preguntas</span></div><div><b>S3</b><span>Ingesta: guardar lo que llega</span></div><div><b>S4</b><span>Calidad: limpiar con reglas</span></div><div><b>S5</b><span>Indicadores de negocio</span></div><div><b>S6</b><span>Dashboards</span></div><div><b>S7</b><span>IA generativa con evidencia</span></div><div><b>S8</b><span>Defensa de una recomendación</span></div></div>'
 +explain('Hoy no hay código: entendemos el problema y dejamos tu ambiente listo para la sesión 2.',1),
 '13–15 min. Una línea con las ocho sesiones, sin explicar ninguna todavía. Cada sesión dura 180 minutos y tiene teoría, un laboratorio guiado con pasos, y cierre. Hoy: concepto y ambiente. Mañana empieza SQL. Cerrar el bloque de apertura y pasar a los conceptos.',
 'path','Abrir · 0–15 min',PROP)

# ───────────────────────── COMPRENDER · 15–50 min ─────────────────────────
add('Cinco preguntas miden qué tan «grande» es un problema de datos.',
 '<div class="s1-v">'
 '<div class="s1-vrow"><i>V</i><b>Volumen</b><span class="q">¿Cuántos datos hay?</span><span>Millones de transacciones al día en un banco: una sola tabla puede pesar cientos de GB al mes.</span></div>'
 f'<div class="s1-vrow"{st(1)}><i>V</i><b>Velocidad</b><span class="q">¿Qué tan rápido llegan y hay que responder?</span><span>Detectar un fraude mientras ocurre, no en el reporte del día siguiente.</span></div>'
 f'<div class="s1-vrow"{st(2)}><i>V</i><b>Variedad</b><span class="q">¿En cuántos formatos llegan?</span><span>Texto de redes sociales, imágenes de radiografías y registros de sensores no caben en una misma tabla.</span></div>'
 f'<div class="s1-vrow"{st(3)}><i>V</i><b>Veracidad</b><span class="q">¿Qué tan confiable es el dato?</span><span>Sensores que fallan, formularios mal llenados y duplicados: el dato «sucio» es la norma, no la excepción.</span></div>'
 f'<div class="s1-vrow"{st(4)}><i>V</i><b>Valor</b><span class="q">¿Vale la pena el esfuerzo?</span><span>Procesar 20 TB de registros que nadie usará es big data mal aplicado.</span></div></div>',
 '15–18 min. Una V por clic; antes de revelar el ejemplo, preguntar «¿alguien tiene un ejemplo de su propia industria para esta V?». Volumen y velocidad son las que más se citan; variedad y veracidad son las que más duelen en la práctica; valor es la que más se olvida y la más cara de ignorar. Ejemplo de salud para contrastar: un hospital que analiza 500 expedientes en Excel no tiene un problema de big data; una red que cruza millones de expedientes con datos genómicos y de sensores sí. Las cinco preguntas son un marco para conversar, no un examen con puntaje.',
 'ladder','Comprender · 15–50 min',NIST)
add('Volumen: un archivo deja de abrirse entero cuando supera tu memoria.',
 bars([('Reporte mensual',0.3,'50 MB','ctx'),('Memoria de una laptop típica',16,'16 GB','ctx'),('Un archivo de registros',20,'20 GB','hl'),('Una tabla de ventas de varios años',100,'100 GB','hl')])
 +explain('Escala lineal: a esta escala, 50 MB casi no se ve. Un archivo mayor que tu memoria no se abre entero: se lee por partes o se reparte entre varias máquinas.',1)
 +f'<p class="s1-cap"{st(2)} style="margin-top:14px">Referencia real: una hoja de cálculo admite 1,048,576 filas por hoja ({XLS}).</p>',
 '18–21 min. Las barras son un orden de magnitud, no mediciones: 50 MB (reporte del caso), 16 GB (memoria de una laptop típica, supuesto), 20 GB y 100 GB (ejemplos). La idea es sentir cuándo cruzas el límite de memoria. Cruzarlo no hace imposible el trabajo: significa leer por partes, ir a disco o repartir entre máquinas, lo que veremos en tres slides. Dato verificable: una hoja de Excel tiene un máximo de filas por hoja; pasar de ahí obliga a cambiar de herramienta antes de hablar de big data.',
 'scale','Comprender · 15–50 min','Valores de ejemplo · escala lineal · '+'Microsoft Excel')
add('Velocidad: lote o flujo depende de cuándo alguien debe actuar.',
 '<div class="s1-lane slow"><h2>Revisión mensual · lote (batch)</h2><div class="trk"><div class="blk">Datos del mes<small>se acumulan</small></div><span class="arr">→</span><div class="blk">Proceso al cierre<small>una vez</small></div><span class="arr">→</span><div class="blk">Reporte</div><span class="dem">espera: días</span></div></div>'
 f'<div class="s1-lane fast"{st(1)}><h2>Alerta de fraude · flujo (streaming)</h2><div class="trk"><div class="blk">Evento<small>cada compra</small></div><span class="arr">→</span><div class="blk">Decisión<small>al llegar</small></div><span class="arr">→</span><div class="blk">Bloqueo</div><span class="dem">espera: segundos</span></div></div>'
 +callout('Procesar de forma continua exige operar de forma continua; si la decisión puede esperar, el lote es más simple y barato.',2),
 '21–24 min. Lote: se junta el trabajo y se procesa de una vez (el reporte mensual). Flujo: se procesa cada evento al llegar (la alerta de fraude). Pedir al grupo que diga cuánta demora aceptaría su organización en una decisión concreta. Aclarar un malentendido frecuente: más servicios no hacen los datos más frescos que su fuente; si el archivo llega una vez al día, un flujo continuo no mejora nada. Lote simplifica la recuperación y la repetición; el flujo reacciona antes a cambio de mantener operación continua.',
 'lanes','Comprender · 15–50 min',PROP)
add('Antes de distribuir, pregunta si una sola máquina lo resuelve.',
 '<div class="s1-dec"><div class="s1-q"><b>PREGUNTA 1</b><span>¿Cabe en la memoria de una máquina?</span><small>sí → sigue</small></div>'
 f'<div class="s1-q"{st(1)}><b>PREGUNTA 2</b><span>¿Una máquina termina a tiempo?</span><small>sí → sigue</small></div>'
 f'<div class="s1-q"{st(2)}><b>PREGUNTA 3</b><span>¿Pocas personas o procesos la usan a la vez?</span><small>sí → sigue</small></div>'
 f'<div class="s1-out"{st(3)}><h2>Tres «sí»</h2><p>Una máquina con SQL basta.</p><p><b>Algún «no»:</b> evalúa repartir el trabajo.</p></div></div>'
 f'<div class="s1-ex"{st(3)}><div>Ventas por sucursal del mes: sí, sí, sí → una consulta SQL en una máquina.</div><div class="f">Fraude entre millones de eventos mientras ocurren: no en la pregunta 2 → flujo y trabajo repartido.</div></div>'
 +callout('El error caro no es usar poca tecnología: es montar un clúster para un problema que una consulta resuelve en segundos.',3),
 '24–27 min. Tres preguntas, un clic cada una. Es la herramienta de decisión central de la sesión: no distribuir por prestigio sino por restricción. Si se responde «sí» a las tres, una base de datos normal o incluso una hoja bien usada basta. La sobre-ingeniería no solo cuesta dinero de infraestructura: cuesta el tiempo de un equipo técnico construyendo algo que nadie necesitaba. Pedir al grupo que clasifique un caso de su trabajo antes del último clic.',
 'decision','Comprender · 15–50 min',PROP)
add('Distribuir es repartir el trabajo y luego combinar los resultados.',
 '<div class="s1-par" data-demo="reparto"><p class="s1-explain" style="font-size:26px">Cuenta los votos de 12 cajas. Cada caja tarda 1 minuto (supuesto del ejemplo).</p>'
 '<div class="s1-cajas">'+''.join(f'<i>{i+1}</i>' for i in range(12))+'</div>'
 '<div class="s1-parctl"><span>Personas:</span>'+''.join(f'<button data-w="{w}" aria-pressed="false">{w}</button>' for w in (1,2,3,4,6))+'<output data-par-out></output></div>'
 '<div class="s1-comb"><span>Al terminar</span><span class="res">sumar los conteos parciales</span></div></div>'
 +callout('Más personas acortan el conteo, pero añaden coordinación: repartir las cajas, combinar los totales y esperar a la más lenta.',1),
 '27–30 min. Pulsar 1, 2, 3, 4 y 6 personas y leer el resultado. Con una persona son 12 minutos; con tres, 4 minutos más el tiempo de sumar los tres conteos; con seis, 2 minutos más combinar. Es el mismo principio de los sistemas distribuidos: dividir el trabajo en partes independientes, procesarlas en paralelo y combinar. Dos matices que importan después: combinar y repartir también cuestan, y si una persona recibe más cajas que las demás, el trabajo termina cuando termina la más lenta. Nada de esto se mide aquí: es un modelo con supuestos.',
 'parallel','Comprender · 15–50 min','Modelo didáctico · tiempos supuestos')
add('Registrar una compra y analizar el año son dos trabajos distintos.',
 '<div class="s1-oltp"><div><p class="s1-cap">Transaccional · OLTP</p><p class="s1-big">1</p><p><b>Registrar una compra.</b> Una operación pequeña, miles por segundo, que debe quedar completa o no existir.</p><div class="dots"><span></span></div><p class="term">ejemplo: guardar la compra n.º 8841</p></div>'
 f'<div{st(1)}><p class="s1-cap">Analítico · OLAP</p><p class="s1-big">millones</p><p><b>Comparar las ventas del año por sucursal.</b> Pocas consultas que leen muchísimas filas y devuelven resultados resumidos.</p><div class="dots">'+'<span></span>'*18+'</div><p class="term">ejemplo: ventas por sucursal y mes</p></div></div>'
 +callout('Transacción: un conjunto de cambios que se guarda completo o no se guarda. Cada trabajo se optimiza distinto.',2),
 '30–33 min. Primero el lado de registrar: una compra es una escritura pequeña y frecuente; lo importante es que no quede a medias (si se cobra, debe quedar guardada). Luego el lado analítico: leer años de historia y resumirla. Por eso la base que registra las compras rara vez es la mejor para analizar todo el historial. Siglas: OLTP (procesamiento transaccional en línea) y OLAP (procesamiento analítico en línea). Más adelante, en SQL, usarás una base relacional con datos de empleados; ahí verás el lado analítico con consultas reales.',
 'oltp','Comprender · 15–50 min',OLTP)
add('Warehouse, lake y lakehouse: tres formas de guardar datos para analizarlos.',
 table(['Forma','Qué guarda','Una imagen cotidiana','Conviene cuando'],[
  ['Data warehouse','Datos ya organizados en tablas, listos para consultar','Una biblioteca catalogada','Las preguntas son conocidas y quieres respuestas rápidas con SQL'],
  ['Data lake','Archivos en su formato original: CSV, JSON, imágenes','Un almacén donde llegan cajas sin abrir','Aún no sabes qué usarás o hay formatos mezclados'],
  ['Data lakehouse','Archivos más reglas de gestión de tablas encima','Un almacén con inventario','Quieres flexibilidad de archivos con orden de tablas']])
 +callout('Pueden convivir en una misma organización; ninguna es una evolución obligatoria de la anterior.',1),
 '33–36 min. Son definiciones, no un camino obligatorio. Warehouse: tablas ordenadas, ideal para SQL. Lake: lo que llega, tal cual, barato de guardar pero con menos orden. Lakehouse: busca juntar lo mejor de los dos con garantías de gestión de tablas sobre archivos. No decir que cualquier carpeta de archivos más una base ya equivale a un lakehouse. En las siguientes sesiones se verá una forma concreta de ordenar los datos por etapas; hoy solo importa conocer los tres nombres y su idea.',
 'matrix','Comprender · 15–50 min',LAKE)
add('La nube es alquilar capacidad por uso en lugar de comprarla.',
 '<p class="s1-explain" style="margin-bottom:18px"><b>Nube (cloud computing):</b> cómputo, almacenamiento y red ofrecidos como servicio por internet, bajo demanda y con pago por uso.</p>'
 '<div class="s1-rent"><div class="c"><h2>Comprar un servidor</h2><p>Compras la máquina y esperas semanas.</p><p>Pagas aunque esté apagado.</p><p>Tú lo instalas, lo respaldas y lo reparas.</p></div>'
 f'<div class="c new"{st(1)}><h2>Alquilar en la nube</h2><p>Pides capacidad y la tienes en minutos.</p><p>Pagas por el tiempo y el espacio que usas.</p><p>El proveedor mantiene el hardware.</p></div></div>'
 +callout('Servidor administrado no significa gratis ni sin responsabilidad: tú sigues decidiendo accesos, región y cuánto dejas encendido.',2),
 '36–38 min. Definición de trabajo primero, luego el contraste. Alquilar permite empezar pequeño y crecer o apagar sin comprar nada; el precio es que el gasto continúa mientras haya recursos encendidos y que algunas decisiones siguen siendo tuyas. Una máquina virtual pequeña también es «nube»: no hace falta un clúster para usarla. En el laboratorio de hoy crearás justamente una máquina pequeña.',
 'rent','Comprender · 15–50 min',PAAS)
add('IaaS, PaaS y SaaS: cuánto administras tú.',
 '<div class="s1-cloud"><div class="s1-model"><h2>IaaS</h2><small>infraestructura como servicio</small><div class="lay you">Aplicación</div><div class="lay you">Datos</div><div class="lay you">Entorno de ejecución</div><div class="lay you">Sistema operativo</div><div class="lay g">Hardware y red</div></div>'
 f'<div class="s1-model"{st(1)}><h2>PaaS</h2><small>plataforma como servicio</small><div class="lay you">Aplicación</div><div class="lay you">Datos</div><div class="lay g">Entorno de ejecución</div><div class="lay g">Sistema operativo</div><div class="lay g">Hardware y red</div></div>'
 f'<div class="s1-model"{st(2)}><h2>SaaS</h2><small>software como servicio</small><div class="lay g">Aplicación</div><div class="lay you">Datos y accesos</div><div class="lay g">Entorno de ejecución</div><div class="lay g">Sistema operativo</div><div class="lay g">Hardware y red</div></div></div>'
 '<div class="s1-legend"><span class="sw you"></span>lo administras tú<span class="sw g"></span>lo administra el proveedor</div>'
 f'<p class="s1-explain" style="margin-top:12px;font-size:25px"{st(2)}><b>Ejemplos:</b> IaaS, una máquina virtual (la que crearás hoy) · PaaS, una base de datos administrada · SaaS, una hoja de cálculo o un correo en línea.</p>',
 '38–40 min. Un clic por modelo. Cuanto más a la derecha, menos administras y menos control tienes. IaaS: te dan la máquina; instalas el sistema, el software y los datos. PaaS: te dan la plataforma; subes tu aplicación y tus datos. SaaS: usas la aplicación y administras tus datos y accesos. Hoy usarás IaaS (una máquina virtual con una base de datos instalada), porque queremos ver qué hay dentro; más adelante usarás servicios que administran por ti más capas.',
 'cloud','Comprender · 15–50 min',PAAS)
add('Cuenta de facturación, proyecto y permisos: quién paga y quién puede hacer qué.',
 '<div class="s1-hier"><div class="col"><div class="box pay"><h2>Cuenta de facturación</h2><p>Quién paga: tarjeta o crédito.</p></div></div><div class="link">→</div>'
 '<div class="col"><div class="box proj"><h2>Proyecto</h2><p>Contenedor de recursos con un ID único (el ID no es el nombre).</p><div class="res"><span>máquina virtual</span><span>disco</span><span>almacenamiento</span></div></div></div></div>'
 '<div class="s1-iam"><div><b>Quién</b>Una cuenta o un grupo.</div><div'+st(1)+'><b>Qué puede hacer</b>Un rol: lector, editor, propietario.</div><div'+st(2)+'><b>Sobre qué</b>Un recurso o el proyecto entero.</div></div>'
 +callout('Da el rol mínimo necesario: «Propietario» no es una solución rutinaria.',2),
 '40–42 min. Dos ideas separadas: quién paga (la cuenta de facturación) y dónde viven los recursos (el proyecto). Un proyecto agrupa máquinas, discos y almacenamiento, y se identifica por un ID único que suele diferir del nombre que le pones; en los comandos se usa el ID. Después, permisos: un permiso es la combinación de quién, qué rol y sobre qué recurso. Principio de privilegio mínimo: nadie recibe «Propietario» para que algo funcione más rápido. Más adelante, cuando algo falle con «permiso denegado», este es el esquema para buscar la causa.',
 'hierarchy','Comprender · 15–50 min',IAMDOC+' · '+HIER)
add('Región y zona: dónde corre tu máquina cambia costo, distancia y reglas legales.',
 '<div class="s1-reg"><div><div class="s1-regmap"><h2>Región: us-central1</h2><small>Council Bluffs, Iowa · Estados Unidos</small><div class="s1-zones"><span class="me">zona a</span><span>zona b</span><span>zona c</span><span>…</span></div></div>'
 '<p class="s1-name"><span class="r">us-central1</span>-<span class="z">a</span></p><p class="s1-cap" style="margin:0">región + zona = nombre completo. La máquina de hoy vivirá en <b>us-central1-a</b>.</p></div>'
 '<ul class="s1-why"><li><b>Costo:</b> el precio cambia según la región.</li><li><b>Distancia:</b> cuanto más lejos del usuario o de tus datos, más demora.</li><li><b>Reglas:</b> algunos datos deben permanecer en un país o región.</li><li><b>Cerca:</b> cómputo y datos en la misma región evitan cobros por moverlos.</li></ul></div>',
 '42–44 min. Una región es una ubicación geográfica; una zona es un área de despliegue dentro de la región. El nombre completo junta ambas: us-central1-a. Cuatro razones para elegir con cuidado: precio, distancia, regulación y cercanía entre cómputo y datos. En este curso la máquina del laboratorio vive en us-central1-a; el curso no fija una región para todo: se elige según la política de la cuenta. Aclarar que la zona resaltada es la del laboratorio y que las demás existen sin necesidad de detallarlas hoy.',
 'region','Comprender · 15–50 min',REG)
add('La nube cobra por lo que usas: tiempo de cómputo, GB guardados y datos que salen.',
 '<div class="s1-cards"><div class="s1-card"><h2>Cómputo</h2><p class="unit">por tiempo encendido</p><p>Una máquina virtual cobra mientras está encendida.</p></div>'
 f'<div class="s1-card"{st(1)}><h2>Almacenamiento</h2><p class="unit">por GB al mes</p><p>Discos y archivos cobran mientras existan, se usen o no.</p></div>'
 f'<div class="s1-card"{st(2)}><h2>Red</h2><p class="unit">por GB que salen</p><p>Mover datos entre regiones o hacia internet puede tener costo.</p></div></div>'
 f'<div class="s1-states"{st(3)}><div class="s1-state on"><b>Encendida</b>Cobra cómputo y disco.</div><div class="s1-state off"><b>Detenida</b>No cobra cómputo; el disco sigue cobrando.</div><div class="s1-state del"><b>Borrada</b>Deja de cobrar; los datos se pierden.</div></div>',
 '44–46 min. Tres medidores. Cómputo: se mide por tiempo de uso; una máquina apagada no consume cómputo. Almacenamiento: se paga por GB mientras exista el recurso. Red: la salida de datos tiene tarifa. Luego los tres estados de una máquina: encendida (cobra cómputo y disco), detenida (el cómputo se detiene, el disco sigue existiendo y cobrando según tu cuota) y borrada (todo se va, incluidos los datos). Detener no es borrar. Los precios cambian: se consultan en la calculadora de precios y no se memorizan.',
 'cards','Comprender · 15–50 min',STOP)
add('Un presupuesto avisa; solo detener o borrar recursos frena el gasto.',
 '<div class="s1-brakes"><div class="s1-brake"><span class="t a">avisa</span><h2>Presupuesto y alertas</h2><p>Envía un correo al cruzar umbrales como 50 %, 90 % y 100 %. No apaga nada.</p></div>'
 f'<div class="s1-brake"{st(1)}><span class="t a">se acaba</span><h2>Crédito de prueba</h2><p>Los clientes nuevos pueden recibir US$300 de crédito por 90 días y cupos gratis (por ejemplo, una VM e2-micro al mes en tres regiones de EE. UU.). Verifica las condiciones en tu cuenta.</p></div>'
 f'<div class="s1-brake"{st(2)}><span class="t b">frena</span><h2>Detener o borrar</h2><p>Lo único que detiene el gasto: apagar o eliminar lo que no usas y revisar la facturación.</p></div></div>',
 '46–48 min. Tres controles distintos. El presupuesto y sus alertas avisan, no frenan. El crédito de prueba es un medio de financiar práctica, no una mensualidad; según la documentación oficial incluye US$300 para clientes nuevos durante 90 días y un cupo de uso gratuito por producto (una e2-micro por mes en tres regiones de EE. UU., con 30 GB de disco estándar); condiciones, vigencia y elegibilidad deben verificarse en la cuenta de cada persona. Lo que realmente frena es detener o borrar recursos. Hoy configurarás un presupuesto en el laboratorio.',
 'brakes','Comprender · 15–50 min',FREE+' · '+BUDG)
add('Cuatro organizaciones, cuatro preguntas de datos distintas.',
 table(['Sector','Organización','Qué reportó públicamente'],[
  ['Banca','HSBC','Una herramienta de análisis de riesgo (Risk Advisory Tool) con datos en la nube.'],
  ['Salud','Mayo Clinic','Análisis de datos genómicos en una plataforma de analítica en la nube.'],
  ['Logística','UPS Capital','Análisis de riesgo en entregas de paquetes con BigQuery y Striim.'],
  ['Retail','Mercado Libre','Analítica de retail con BigQuery y Looker.']])
 
 +callout('Son casos reportados por las propias organizaciones: no son auditorías independientes ni garantizan el mismo resultado en tu caso.',1),
 '48–49 min. Cuatro sectores del temario (banca, salud, logística, retail). No prometen ahorros ni garantizan resultados: son publicaciones de cada organización y se leen como ejemplos de qué preguntas se hicieron. Pedir al grupo que ubique cuál de las cinco V pesa más en cada uno (riesgo: volumen y plazo; genómica: volumen y variedad; entregas: velocidad; retail: volumen y valor). Las herramientas que aparecen se irán explicando después; hoy solo importa la pregunta.',
 'cases','Comprender · 15–50 min',HSBC+' · '+MAYO+' · '+UPS+' · '+MELI)
add('Un mapa del ecosistema: cinco categorías para reconocer nombres.',
 table(['Categoría','Qué resuelve','Nombres que escucharás'],[
  ['Almacenamiento','Dónde viven los datos crudos','Cloud Storage, HDFS'],
  ['Cómputo distribuido','Procesar datos repartidos entre varias máquinas','Spark'],
  ['Bases analíticas','Responder preguntas SQL sobre grandes volúmenes','BigQuery'],
  ['Streaming','Procesar datos que llegan continuamente','Pub/Sub, Kafka'],
  ['Orquestación','Coordinar que cada paso corra en orden','Airflow']])
 +callout('Es un mapa para orientarte, no un manual de manejo: basta reconocer el nombre y su categoría.',1),
 '49–50 min. Mapa de ciudad, no manual de manejo. No hace falta saber operar ninguna pieza hoy; sí reconocer el nombre cuando se mencione en una reunión. Las bases relacionales (MySQL, MariaDB, PostgreSQL) son la categoría con la que empezarás a trabajar en la sesión 2. Cerrar el bloque de conceptos y pasar a aplicarlos.',
 'matrix map','Comprender · 15–50 min',MAP)

# ───────────────────────── APLICAR · 50–70 min ─────────────────────────
add('Decide tú: tres situaciones, una recomendación cada una.',
 '<p class="s1-explain" style="font-size:25px;margin-bottom:12px">Antes de cada clic, escribe tu recomendación y una razón. Usa las tres preguntas de «antes de distribuir».</p><div class="s1-sit">'
 '<div class="s1-sr"><div><h2>A · Reporte mensual</h2><p>Un reporte de ventas de 60 MB que lee un gerente.</p></div><div class="ans" data-step="1"><b>Una máquina con SQL</b>Cabe en memoria y el plazo es amplio. Distribuir sería sobre-ingeniería.</div></div>'
 '<div class="s1-sr"><div><h2>B · Pagos sospechosos</h2><p>Bloquear pagos mientras se aprueban, entre millones de eventos al día.</p></div><div class="ans" data-step="2"><b>Flujo continuo</b>La decisión es en segundos: un lote diario llega tarde.</div></div>'
 '<div class="s1-sr"><div><h2>C · Registros web</h2><p>Revisar cada semana un archivo de 20 GB de registros web.</p></div><div class="ans" data-step="3"><b>Mide primero</b>Si una máquina lo procesa por partes a tiempo, basta; si no, reparte por lotes. El flujo sobra: es semanal.</div></div></div>',
 '50–56 min. Ejercicio individual. Dar un minuto por situación para escribir recomendación y razón; luego revelar. No hay una sola respuesta correcta: lo que se evalúa es el razonamiento con las tres preguntas (memoria, plazo, simultaneidad) y con la demora tolerable. A: sobre-ingeniería evitada. B: flujo porque la acción es inmediata. C: es el caso ambiguo y por eso el más valioso: se decide midiendo, no por tamaño. Preguntar a dos personas qué pondrían distinto y por qué.',
 'practice','Aplicar · 50–70 min',HIPO)
add('Dimensiona un problema con una multiplicación.',
 '<div class="s1-calc"><div><pre class="s1-eq"><code>2 000 000 transacciones por día\n× 1 KB cada una            <span class="u">(supuesto)</span>\n= 2 GB por día\n× 30 días   → <span class="r">60 GB al mes</span>\n× 365 días  → <span class="r">730 GB al año</span></code></pre>'
 f'<p class="s1-explain" style="margin-top:14px;font-size:25px"{st(1)}>¿Cabe en 16 GB de memoria? <b>No.</b> ¿Cabe en un disco? <b>Sí.</b> ¿Hay que repartir? <b>Depende del plazo</b> para responder.</p></div>'
 '<div class="s1-turn"><h2>Tu turno</h2><p>500 000 lecturas de sensor por hora, de 200 bytes cada una. ¿Cuánto es por día y por año?</p>'
 f'<pre class="s1-eq" style="font-size:23px"{st(2)}><code>500 000 × 200 B = 100 MB por hora\n× 24 h   → 2.4 GB por día\n× 365 d  → <span class="r">≈ 876 GB al año</span></code></pre></div></div>',
 '56–63 min. Primero seguir el ejemplo en voz alta: filas por día × tamaño por fila = datos por día; luego por mes y por año. Es una estimación de orden de magnitud, no una medición: el tamaño por fila es un supuesto que se mide con una muestra. Tras el ejemplo, dar cinco minutos para que cada persona haga el cálculo del sensor antes del clic final. Resultado: 100 MB por hora, 2.4 GB por día, ≈ 876 GB al año. Conclusión para la discusión: la cifra anual cabe en un disco, así que la pregunta sobre repartir se decide por plazo y simultaneidad, no por tamaño.',
 'calc','Aplicar · 50–70 min','Cifras supuestas · cálculo ilustrativo')
add('Antes de crear una máquina, responde cinco preguntas.',
 table(['Pregunta','Para la máquina del curso'],[
  ['¿Dónde correrá?','Región us-central1, zona us-central1-a.'],
  ['¿De qué tamaño?','Tipo e2-micro: ≈ 1 GB de memoria y disco de 30 GB.'],
  ['¿Quién entra?','El usuario del curso (big_data_user) por el puerto 3306, abierto a internet por decisión didáctica.'],
  ['¿Cuánto cuesta?','Cómputo por hora encendida y disco por GB mientras exista; hay cupo gratis para una e2-micro (verifícalo).'],
  ['¿Cuándo se apaga?','Al terminar cada sesión; se borra al terminar el curso.']])
 +callout('El puerto abierto y la contraseña compartida son decisiones didácticas para datos públicos de práctica: nunca los uses con datos reales.',1),
 '63–70 min. Es el puente al laboratorio: cada respuesta ya se tomó, y conviene que cada persona entienda por qué. Región y zona por cercanía y cupo gratuito; tamaño pequeño porque basta para practicar SQL; acceso con usuario del curso porque es un entorno desechable con datos públicos (la regla de firewall abierta a internet y la contraseña compartida son prácticas que nunca deben replicarse con datos reales); costo claro; y una disciplina: apagar al terminar. Preguntar qué cambiarían si los datos fueran de clientes reales (acceso restringido por IP, credenciales individuales).',
 'matrix','Aplicar · 50–70 min',MACH+' · '+FREE)

# ───────────────────────── PAUSA ─────────────────────────
add('Pausa. Vuelve con la consola de Google Cloud abierta.',
 '<p class="time">10 min</p><p>Al volver: tu cuenta de Google lista y la guía de laboratorio abierta en otra pestaña.</p>',
 '70–80 min. Pausa real, sin avance automático. Antes del laboratorio conviene tener abierta la consola de Google Cloud con la cuenta propia y una pestaña con la guía de laboratorio. Si una cuenta no puede crear un proyecto o activar la facturación, anotar el motivo exacto y seguir la guía como lectura; no activar pagos a ciegas.',
 'statement dark','Pausa · 70–80 min',PROP)

# ───────────────────────── LABORATORIO ─────────────────────────
add('Seis pasos para montar tu ambiente.',
 '<div class="s1-labsteps">'
 '<div class="s1-lstep"><i>1</i><span>Crea tu proyecto y comprueba la facturación</span><b>8 min</b></div>'
 '<div class="s1-lstep"><i>2</i><span>Abre Cloud Shell y confirma tu identidad</span><b>7 min</b></div>'
 '<div class="s1-lstep"><i>3</i><span>Crea un presupuesto con alertas</span><b>10 min</b></div>'
 '<div class="s1-lstep"><i>4</i><span>Activa Compute Engine</span><b>5 min</b></div>'
 '<div class="s1-lstep long"><i>5</i><span>Crea la máquina con MariaDB (la instalación tarda ≈ 14 min)</span><b>25 min</b></div>'
 '<div class="s1-lstep"><i>6</i><span>Verifica, conéctate y detén la máquina</span><b>15 min</b></div></div>'
 '<p class="s1-labend"><b>Al terminar:</b> un proyecto con presupuesto y una máquina con MariaDB lista para la sesión 2.</p>'
 +lablink(1),
 '80–150 min. Seis pasos, 70 minutos; la guía completa trae dónde hacer clic, cada comando y la salida esperada. El paso 5 es el más largo porque MariaDB se instala sola dentro de la máquina y eso tarda unos 14 minutos en el ensayo; mientras tanto se explora la consola. Avanzar paso a paso y comprobar la salida antes de pasar al siguiente. Los pasos 1 a 4 se hacen en la consola y en Cloud Shell y no se ensayaron desde una cuenta nueva; los pasos 5 y 6 se ensayaron con una máquina real. Al final, detener la máquina para no gastar.',
 'lab-taller','Laboratorio · 80–150 min','Guía completa en laboratorio.html')

# ───────────────────────── CERRAR · 150–180 min ─────────────────────────
add('Tres ejercicios para practicar por tu cuenta.',
 '<div class="s1-ejs"><div class="s1-ej"><b>1</b><h2>Clasifica</h2><p>Piensa en tres procesos de datos de tu industria. Para cada uno responde las tres preguntas de «antes de distribuir».</p><small>Resultado: una tabla de tres filas con sí o no.</small></div>'
 '<div class="s1-ej"><b>2</b><h2>Dimensiona</h2><p>Estima cuántos GB generan al año tus datos: filas por día × tamaño por fila × 365. Compáralos con 16 GB de memoria.</p><small>Resultado: una cifra y una conclusión de una línea.</small></div>'
 '<div class="s1-ej"><b>3</b><h2>Ubica</h2><p>En la consola, encuentra dónde ver el gasto del mes, dónde está tu máquina y cómo se detiene.</p><small>Resultado: tres capturas, una por cada punto.</small></div></div>',
 '150–165 min. Tres ejercicios individuales para repetir lo visto sin depender de nadie. Cada uno produce un resultado pequeño y comprobable. Sugerir que se hagan después de la sesión y que guarden las respuestas: sirven como base de comparación cuando más adelante trabajen con datos reales.',
 'practice','Cerrar · 150–180 min',PROP)
add('Qué puedes afirmar después de hoy, y qué todavía no.',
 table(['Sí puedes afirmar','Todavía no puedes afirmar'],[
  ['Un problema es de big data cuando una restricción (memoria, plazo, personas, dinero) te impide resolverlo de forma simple.','Que un archivo grande necesita automáticamente un clúster.'],
  ['La nube cobra por uso y un presupuesto solo avisa.','Que la nube sale más barata por defecto.'],
  ['Detener una máquina frena el cómputo pero no borra su disco.','Que dejarla detenida no cuesta nada.'],
  ['Los casos publicados muestran qué preguntas se hicieron.','Que tu organización obtendrá los mismos resultados.']]),
 '165–172 min. Cierre honesto: cada columna separa lo que la sesión sí respalda de saltos que conviene evitar. Primera fila: el criterio es la restricción, no el tamaño. Segunda: la nube no es barata ni cara en sí; depende del uso y de lo que dejes encendido. Tercera: detener frena el cómputo, pero el disco sigue existiendo y puede cobrar. Cuarta: los casos son publicaciones de las propias organizaciones. Pedir una frase propia que empiece con «todavía no puedo afirmar que…».',
 'claims','Cerrar · 150–180 min',PROP)
add('Glosario mínimo para las próximas sesiones.',
 '<div class="s1-gloss">'
 '<div><b>Big data</b> · problema donde volumen, velocidad, variedad o veracidad superan lo que tu plazo y tus recursos permiten resolver de forma simple.</div>'
 '<div><b>Lote (batch)</b> · procesar de una vez un conjunto acumulado de datos.</div>'
 '<div><b>Flujo (streaming)</b> · procesar cada dato al llegar.</div>'
 '<div><b>Transacción</b> · cambios que se guardan completos o no se guardan.</div>'
 '<div><b>OLTP</b> · base optimizada para registrar operaciones.</div>'
 '<div><b>OLAP</b> · base optimizada para analizar muchos datos.</div>'
 '<div><b>Data warehouse</b> · tablas organizadas listas para consultar.</div>'
 '<div><b>Data lake</b> · archivos en su formato original.</div>'
 '<div><b>Lakehouse</b> · archivos más gestión de tablas encima.</div>'
 '<div><b>IaaS, PaaS, SaaS</b> · infraestructura, plataforma o aplicación como servicio.</div>'
 '<div><b>Región y zona</b> · ubicación geográfica y área de despliegue de un recurso.</div>'
 '<div><b>Proyecto</b> · contenedor de recursos con un ID único.</div>'
 '<div><b>Rol (IAM)</b> · conjunto de permisos que se asigna a una cuenta.</div>'
 '<div><b>Presupuesto</b> · aviso de gasto; no apaga recursos.</div></div>',
 '172–180 min. Catorce términos que se usarán sin volver a definirse. No hace falta memorizarlos: conviene volver a esta lámina cuando una palabra no se entienda. Cierre: la sesión 2 empieza con SQL sobre la máquina que dejaste lista hoy; antes de irte, comprueba que está detenida o encendida según lo que vayas a hacer, y que tu presupuesto existe.',
 'glossary','Cerrar · 150–180 min',PROP)
SLIDES=S
