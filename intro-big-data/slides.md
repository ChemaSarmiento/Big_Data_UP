---
theme: seriph
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
title: "Introducción a Big Data"
info: |
  Sesión compartida — base para Especialidad y Maestría.
  Qué es Big Data, tipos y persistencia de datos, uso de los datos, y cloud.
---

# Introducción a Big Data

<div class="pt-6 text-sm opacity-60">
Sesión base, compartida por Especialidad y Maestría — antes de la Sesión 1 de cualquiera de los dos tracks
</div>

---
layout: center
class: text-center
---

# ¿Qué es Big Data?

<div class="mt-8 text-xl max-w-3xl mx-auto italic">
"Grandes conjuntos de datos que tienen tres características principales: volumen, velocidad y variedad — tipos de fuentes de datos no estructurados, tales como la interacción social, video, audio, cualquier cosa que se pueda clasificar en una base de datos"
</div>

<div class="mt-6 text-blue-500 font-bold">— Gartner</div>

---

# Las 5 V's de Big Data

<div class="grid grid-cols-5 gap-3 mt-8">
<div class="text-center">
<div class="text-4xl">📊</div>
<div class="font-bold mt-2">Volumen</div>
<div class="text-xs opacity-70 mt-1">Magnitud masiva — hoy, en petabytes</div>
</div>
<div class="text-center">
<div class="text-4xl">⚡</div>
<div class="font-bold mt-2">Velocidad</div>
<div class="text-xs opacity-70 mt-1">Tiempo real, casi real, o por lotes</div>
</div>
<div class="text-center">
<div class="text-4xl">🧩</div>
<div class="font-bold mt-2">Variedad</div>
<div class="text-xs opacity-70 mt-1">Estructurado, semi, no estructurado</div>
</div>
<div class="text-center">
<div class="text-4xl">✅</div>
<div class="font-bold mt-2">Veracidad</div>
<div class="text-xs opacity-70 mt-1">¿Podemos confiar en el dato?</div>
</div>
<div class="text-center">
<div class="text-4xl">💎</div>
<div class="font-bold mt-2">Valor</div>
<div class="text-xs opacity-70 mt-1">Decisiones accionables, ROI real</div>
</div>
</div>

<div class="mt-10 text-sm opacity-70">
1 Petabyte = 1,000,000,000,000,000 bytes — 1024 Terabytes
</div>

<div class="mt-2 text-xs opacity-40">
→ Cada V, a detalle, en las siguientes slides · infográfico completo en slides/infograficos/infografico_5vs.pptx
</div>

---

# Volumen

<div class="w-24 h-24 rounded-full bg-blue-500/15 flex items-center justify-center text-5xl mx-auto mt-2">📊</div>

<div class="max-w-2xl mx-auto mt-6 text-left space-y-4">
<div>
<div class="font-bold text-blue-500">Concepto</div>
<div class="text-sm mt-1 opacity-80">La cantidad total de datos generados y almacenados — hoy se mide en terabytes y petabytes, no en gigabytes.</div>
</div>
<div>
<div class="font-bold text-blue-500">Por qué importa</div>
<div class="text-sm mt-1 opacity-80">Cuando el volumen supera lo que una sola máquina puede procesar en un tiempo razonable, las herramientas tradicionales (Excel, un único servidor SQL) dejan de alcanzar — es la razón de ser de las arquitecturas distribuidas de este curso.</div>
</div>
<div class="p-3 rounded bg-blue-500/10 text-sm">
<b>Ejemplo</b> — Walmart procesa 2.5 petabytes de datos de transacciones por hora; su Data Café analiza más de 40 petabytes de historial de clientes para responder preguntas de negocio en minutos, no semanas. <span class="opacity-60">(Forbes / Bernard Marr)</span>
</div>
</div>

---

# Velocidad

<div class="w-24 h-24 rounded-full bg-amber-500/15 flex items-center justify-center text-5xl mx-auto mt-2">⚡</div>

<div class="max-w-2xl mx-auto mt-6 text-left space-y-4">
<div>
<div class="font-bold text-amber-500">Concepto</div>
<div class="text-sm mt-1 opacity-80">La rapidez con la que los datos se generan, se mueven y necesitan procesarse — desde lotes nocturnos hasta streaming en tiempo real.</div>
</div>
<div>
<div class="font-bold text-amber-500">Por qué importa</div>
<div class="text-sm mt-1 opacity-80">No todos los datos necesitan la misma velocidad de reacción — detectar un fraude necesita milisegundos, un reporte mensual puede esperar horas. Elegir mal el modelo (batch vs. streaming) para el problema es un error caro.</div>
</div>
<div class="p-3 rounded bg-amber-500/10 text-sm">
<b>Ejemplo</b> — cada minuto del año, según Domo (Data Never Sleeps 12, 2025): YouTube recibe 3.4 millones de vistas, Netflix transmite más de 362,000 horas de contenido, y se envían 251.1 millones de correos.
</div>
</div>

---

# Variedad

<div class="w-24 h-24 rounded-full bg-purple-500/15 flex items-center justify-center text-5xl mx-auto mt-2">🧩</div>

<div class="max-w-2xl mx-auto mt-6 text-left space-y-4">
<div>
<div class="font-bold text-purple-500">Concepto</div>
<div class="text-sm mt-1 opacity-80">Los distintos formatos y estructuras en que llegan los datos — estructurados, semi-estructurados y no estructurados, casi nunca uno solo a la vez.</div>
</div>
<div>
<div class="font-bold text-purple-500">Por qué importa</div>
<div class="text-sm mt-1 opacity-80">Un mismo problema de negocio casi siempre combina fuentes distintas — el sistema que las procesa tiene que poder ingerir las tres sin forzar todo a encajar en una tabla.</div>
</div>
<div class="p-3 rounded bg-purple-500/10 text-sm">
<b>Ejemplo</b> — detectar fraude bancario combina transacciones estructuradas (montos, fechas), logs semi-estructurados de la app (JSON de cada sesión) y no estructurados (grabaciones de reportes al call center) — las tres fuentes, un mismo modelo.
</div>
</div>

---

# Veracidad

<div class="w-24 h-24 rounded-full bg-green-500/15 flex items-center justify-center text-5xl mx-auto mt-2">✅</div>

<div class="max-w-2xl mx-auto mt-6 text-left space-y-4">
<div>
<div class="font-bold text-green-500">Concepto</div>
<div class="text-sm mt-1 opacity-80">Qué tan confiables, precisos y libres de sesgo son los datos — si el dato mismo está mal, ningún análisis lo compensa.</div>
</div>
<div>
<div class="font-bold text-green-500">Por qué importa</div>
<div class="text-sm mt-1 opacity-80">"Garbage in, garbage out" — un modelo entrenado con datos sucios produce predicciones seguras, pero incorrectas, y eso es más peligroso que no tener modelo.</div>
</div>
<div class="p-3 rounded bg-green-500/10 text-sm">
<b>Ejemplo</b> — IBM / Harvard Business Review estimó que la mala calidad de datos le cuesta a la economía de EE.UU. cerca de $3.1 billones de dólares al año (~18% del PIB en ese momento) — casi todo por decisiones tomadas sobre datos que nadie verificó. <span class="opacity-60">(Redman, HBR / IBM, 2016)</span>
</div>
</div>

---

# Valor

<div class="w-24 h-24 rounded-full bg-pink-500/15 flex items-center justify-center text-5xl mx-auto mt-2">💎</div>

<div class="max-w-2xl mx-auto mt-6 text-left space-y-4">
<div>
<div class="font-bold text-pink-500">Concepto</div>
<div class="text-sm mt-1 opacity-80">La utilidad real que se extrae del dato — si no se traduce en una mejor decisión, el dato, por grande que sea, no vale nada.</div>
</div>
<div>
<div class="font-bold text-pink-500">Por qué importa</div>
<div class="text-sm mt-1 opacity-80">Es la V que justifica invertir en todas las demás — volumen, velocidad, variedad y veracidad no importan si el resultado final no cambia una decisión de negocio.</div>
</div>
<div class="p-3 rounded bg-pink-500/10 text-sm">
<b>Ejemplo</b> — el motor de recomendaciones de Netflix le ahorra a la empresa más de mil millones de dólares al año, al reducir cuántos suscriptores cancelan su cuenta cada mes. <span class="opacity-60">(The Motley Fool, 2016)</span>
</div>
</div>

---

# ¿Cuántos datos hay en el mundo?

<div class="grid grid-cols-4 gap-4 mt-10 text-center">
<div><div class="text-3xl font-bold text-blue-500">3.0B</div><div class="text-sm opacity-70">2014</div></div>
<div><div class="text-3xl font-bold text-blue-500">4.3B</div><div class="text-sm opacity-70">2018</div></div>
<div><div class="text-3xl font-bold text-blue-500">4.5B</div><div class="text-sm opacity-70">2020</div></div>
<div><div class="text-3xl font-bold text-blue-500">5.5B</div><div class="text-sm opacity-70">2024</div></div>
</div>
<div class="text-xs opacity-50 mt-2">Población mundial conectada a internet (miles de millones) — Domo, Data Never Sleeps 12</div>

<div class="mt-10 text-xl">
181 ZB en 2025 → proyección de <b>221-240 ZB para 2026</b>
</div>
<div class="text-sm opacity-60 mt-2">Fuente: Statista / IDC</div>

---

# Tipos de datos

<div class="grid grid-cols-3 gap-4 mt-8">
<div class="p-4 border rounded">
<div class="font-bold text-blue-500">Estructurados</div>
<div class="text-sm mt-2 opacity-80">Tablas, columnas bien definidas — xls, SQL</div>
</div>
<div class="p-4 border rounded">
<div class="font-bold text-blue-500">Semi-estructurados</div>
<div class="text-sm mt-2 opacity-80">JSON, XML — estructura flexible</div>
</div>
<div class="p-4 border rounded">
<div class="font-bold text-blue-500">No estructurados</div>
<div class="text-sm mt-2 opacity-80">Texto, imágenes, video, audio</div>
</div>
</div>

<div class="mt-10 grid grid-cols-2 gap-6 text-left">
<div class="p-4 bg-gray-500/10 rounded">
<b>Schema-on-write</b><br/>
<span class="text-sm opacity-70">Se define un esquema ANTES de escribir los datos</span>
</div>
<div class="p-4 bg-blue-500/10 rounded">
<b>Schema-on-read</b><br/>
<span class="text-sm opacity-70">Se ingieren en su formato original; el esquema se aplica al consultar</span>
</div>
</div>

<div class="mt-6 text-xs opacity-40">
→ Cada tipo, a detalle y con ejemplo, en las siguientes slides
</div>

---

# Estructurados

<div class="w-24 h-24 rounded-full bg-blue-500/15 flex items-center justify-center text-5xl mx-auto mt-2">🗂️</div>

<div class="max-w-2xl mx-auto mt-6 text-left space-y-4">
<div>
<div class="font-bold text-blue-500">Concepto</div>
<div class="text-sm mt-1 opacity-80">Datos organizados en un modelo tabular fijo — filas y columnas, con un tipo de dato definido para cada campo.</div>
</div>
<div>
<div class="font-bold text-blue-500">Por qué importa</div>
<div class="text-sm mt-1 opacity-80">El esquema fijo hace que las consultas SQL sean rápidas y predecibles — el costo es que agregar un campo nuevo requiere modificar la estructura completa antes de poder usarlo.</div>
</div>
<div class="p-3 rounded bg-blue-500/10 text-sm">
<b>Ejemplo</b> — <code>bank_transactions.csv</code>, el dataset que usas en Maestría: cada fila es una transacción con columnas fijas (id, monto, fecha, moneda) — el mismo formato que llena cualquier base de datos relacional o un Excel.
</div>
</div>

---

# Semi-estructurados

<div class="w-24 h-24 rounded-full bg-purple-500/15 flex items-center justify-center text-5xl mx-auto mt-2">🧬</div>

<div class="max-w-2xl mx-auto mt-6 text-left space-y-4">
<div>
<div class="font-bold text-purple-500">Concepto</div>
<div class="text-sm mt-1 opacity-80">Tienen cierta organización (etiquetas, jerarquía, pares clave-valor) pero sin filas y columnas fijas — cada registro puede tener campos distintos. JSON y XML son los formatos más comunes.</div>
</div>
<div>
<div class="font-bold text-purple-500">Por qué importa</div>
<div class="text-sm mt-1 opacity-80">Es el formato nativo de casi cualquier API o sistema de logs moderno — flexible para evolucionar sin romper nada, a costa de ser más lento de consultar sin procesarlo primero.</div>
</div>
<div class="p-3 rounded bg-purple-500/10 text-sm">
<b>Ejemplo</b> — la respuesta de cualquier API (Spotify, redes sociales) llega en JSON; los logs de eventos de una app también — el formato que vas a ingerir crudo antes de aplanarlo con Spark.
</div>
</div>

---

# No estructurados

<div class="w-24 h-24 rounded-full bg-amber-500/15 flex items-center justify-center text-5xl mx-auto mt-2">🎨</div>

<div class="max-w-2xl mx-auto mt-6 text-left space-y-4">
<div>
<div class="font-bold text-amber-500">Concepto</div>
<div class="text-sm mt-1 opacity-80">Datos sin ningún modelo predefinido — texto libre, imágenes, audio, video. No caben en filas y columnas sin antes extraerles features.</div>
</div>
<div>
<div class="font-bold text-amber-500">Por qué importa</div>
<div class="text-sm mt-1 opacity-80">Son la mayoría de los datos que se generan hoy, y requieren procesamiento especializado (NLP, visión computacional) antes de poder analizarse junto con el resto.</div>
</div>
<div class="p-3 rounded bg-amber-500/10 text-sm">
<b>Ejemplo</b> — reseñas de producto, grabaciones de un call center, imágenes médicas, publicaciones en redes sociales: el mismo tipo de dato detrás de un análisis de sentimiento o un modelo de reconocimiento de imágenes.
</div>
</div>

---

# Schema-on-write

<div class="w-24 h-24 rounded-full bg-green-500/15 flex items-center justify-center text-5xl mx-auto mt-2">📐</div>

<div class="max-w-2xl mx-auto mt-6 text-left space-y-4">
<div>
<div class="font-bold text-green-500">Concepto</div>
<div class="text-sm mt-1 opacity-80">El esquema (columnas, tipos de dato, restricciones) se define ANTES de escribir un solo registro — la base de datos rechaza cualquier dato que no calce.</div>
</div>
<div>
<div class="font-bold text-green-500">Por qué importa</div>
<div class="text-sm mt-1 opacity-80">Garantiza calidad y consistencia desde el día uno, pero es rígido — cambiar el esquema después de tener datos cargados es una operación costosa y arriesgada.</div>
</div>
<div class="p-3 rounded bg-green-500/10 text-sm">
<b>Ejemplo</b> — <code>CREATE TABLE transacciones (id INT, monto DECIMAL, fecha DATE)</code> en PostgreSQL: cualquier fila que no cumpla ese contrato se rechaza al insertar, no después.
</div>
</div>

---

# Schema-on-read

<div class="w-24 h-24 rounded-full bg-pink-500/15 flex items-center justify-center text-5xl mx-auto mt-2">🔍</div>

<div class="max-w-2xl mx-auto mt-6 text-left space-y-4">
<div>
<div class="font-bold text-pink-500">Concepto</div>
<div class="text-sm mt-1 opacity-80">Los datos se guardan en su formato original, crudo — el esquema se aplica hasta el momento de leerlos o consultarlos, no antes.</div>
</div>
<div>
<div class="font-bold text-pink-500">Por qué importa</div>
<div class="text-sm mt-1 opacity-80">Permite ingerir datos sin saber de antemano cómo se van a usar. El precio: la responsabilidad de interpretar el dato correctamente se mueve del momento de escritura al momento del análisis.</div>
</div>
<div class="p-3 rounded bg-pink-500/10 text-sm">
<b>Ejemplo</b> — subir <code>bank_transactions.csv</code> sin procesar a Cloud Storage, y que Spark infiera el esquema (<code>inferSchema=True</code>) hasta el momento en que lo lees — el patrón exacto de Maestría Sesión 1.
</div>
</div>

---

# Persistencia de datos: cuatro patrones

| | Data Mart | Data Warehouse | Data Lake | Lakehouse |
|---|---|---|---|---|
| **Foco** | Tópico atómico | Visión consolidada | Repositorio crudo | Estructura + flexibilidad |
| **Esquema** | Schema-on-write | Schema-on-write | Schema-on-read | Schema-on-read + calidad |
| **Calidad** | Alta, curada | Alta, agregada | Baja/media | Alta |
| **Uso principal** | Reportes de un área | Análisis OLAP, BI | ML, exploración | Todo, con eficiencia |

<div class="mt-6 text-sm opacity-70 text-center">
Data Mart ⊂ Data Warehouse (una vista de un solo departamento vs. la consolidación completa)
</div>

---

# Persistencia de datos, en la práctica

<div class="grid grid-cols-2 gap-4 mt-8 text-sm text-left">
<div class="p-4 rounded bg-gray-500/10">
<b>📁 Data Mart</b><br/>
<span class="opacity-70">Un dashboard en Power BI que solo el equipo de Marketing usa, con las métricas de sus propias campañas.</span>
</div>
<div class="p-4 rounded bg-blue-500/10">
<b>🏢 Data Warehouse</b><br/>
<span class="opacity-70">El BigQuery central de la empresa, donde Finanzas, Marketing y Operaciones consultan el mismo número de ventas.</span>
</div>
<div class="p-4 rounded bg-amber-500/10">
<b>🌊 Data Lake</b><br/>
<span class="opacity-70">Un bucket de Cloud Storage donde caen logs, video y CSVs crudos sin procesar, esperando ser consumidos.</span>
</div>
<div class="p-4 rounded bg-green-500/10">
<b>🏠 Lakehouse</b><br/>
<span class="opacity-70">Apache Iceberg sobre Cloud Storage (Maestría Sesión 6) — archivos Parquet crudos, con las garantías ACID de un warehouse.</span>
</div>
</div>

---

# El riesgo de no gobernar: Data Swamp

<div class="grid grid-cols-2 gap-6 mt-8">
<div class="p-5 rounded bg-red-500/10">
<div class="font-bold text-lg">🏚️ Data Swamp</div>
<ul class="text-sm mt-3 space-y-1 opacity-80">
<li>❌ Sin metadata</li>
<li>❌ Sin gobierno de datos</li>
<li>❌ Metadata rota</li>
<li>❌ Proceso de ingesta roto</li>
</ul>
</div>
<div class="p-5 rounded bg-green-500/10">
<div class="font-bold text-lg">✅ Data Lake bien gobernado</div>
<ul class="text-sm mt-3 space-y-1 opacity-80">
<li>✔️ Metadata completa</li>
<li>✔️ Contexto del dato claro</li>
<li>✔️ Fácil de ordenar y procesar</li>
<li>✔️ Directorios y catálogo claros</li>
</ul>
</div>
</div>

<div class="mt-8 text-center text-blue-500 font-bold">
Un data lake sin gobierno no es un lake — es un pantano
</div>

---

# OLTP vs. OLAP

| | OLTP | OLAP |
|---|---|---|
| **Propósito** | Gestión de transacciones | Análisis histórico/agregado |
| **Modelo de datos** | Normalizado | Desnormalizado (estrella/copo de nieve) |
| **Volumen** | GB a TB | TB a PB |
| **Latencia** | Milisegundos | Prioriza rendimiento analítico |
| **Usuarios** | Clientes, cajeros, IoT | Analistas, Data Scientists |
| **Ejemplos** | POS, banca en línea | BigQuery, Redshift, Delta Lake |

<div class="grid grid-cols-2 gap-4 mt-3 text-xs text-left">
<div class="p-2 rounded bg-gray-500/10">
<b>OLTP</b> — pagar en la caja de un Walmart: se registra en milisegundos
</div>
<div class="p-2 rounded bg-blue-500/10">
<b>OLAP</b> — Finanzas analiza qué categorías crecieron el trimestre: query OLAP
</div>
</div>

---

# El pipeline: de dato crudo a decisión

```mermaid {scale: 0.6}
flowchart LR
    A[Datos crudos] --> B[Feature engineering]
    B --> C[Modelo]
    C --> D[Validación y despliegue]
```

<v-clicks>

- **Feature engineering** — transformar datos crudos en variables relevantes
- **Modelo** — aplicar un algoritmo sobre los datos persistentes: *"una representación o abstracción de un fenómeno observado"*
- **Validación y despliegue** — probar con métricas de negocio y llevar a producción

</v-clicks>

---

# El mismo pipeline, en Spotify Discover Weekly

```mermaid {scale: 0.55}
flowchart LR
    A["Qué escuchaste,<br/>qué te saltaste"] --> B["Tempo, energía,<br/>hora del día"]
    B --> C["Filtrado<br/>colaborativo"]
    C --> D["A/B test antes<br/>de lanzar el lunes"]
```

<v-clicks>

- **Datos crudos** — cada canción que escuchaste completa, cada una que te saltaste a los 10 segundos
- **Feature engineering** — características de audio (tempo, energía, tonalidad) + patrones de cuándo escuchas qué género
- **Modelo** — filtrado colaborativo: encuentra usuarios con gustos parecidos al tuyo, aprende de lo que ellos escuchan
- **Validación y despliegue** — la playlist se prueba con un grupo pequeño antes de lanzarse a todos los usuarios cada lunes

</v-clicks>

---

# Anatomía de un producto de datos

<div class="grid grid-cols-4 gap-3 mt-8 text-center text-sm">
<div class="p-3 border rounded"><div class="text-2xl">🗄️</div><b>Datos crudos</b><br/><span class="opacity-70">Transacciones, clics, sensores</span></div>
<div class="p-3 border rounded"><div class="text-2xl">🧠</div><b>Modelo</b><br/><span class="opacity-70">Aprende patrones históricos</span></div>
<div class="p-3 border rounded bg-blue-500/10"><div class="text-2xl">📦</div><b>Producto de datos</b><br/><span class="opacity-70">Predicción, score, recomendación</span></div>
<div class="p-3 border rounded"><div class="text-2xl">👉</div><b>Decisión</b><br/><span class="opacity-70">El usuario actúa</span></div>
</div>

<div class="grid grid-cols-5 gap-2 mt-10 text-center text-xs">
<div>🎬 Netflix<br/><span class="opacity-60">recomienda qué ver</span></div>
<div>🎵 Spotify<br/><span class="opacity-60">arma tu playlist</span></div>
<div>🗺️ Maps<br/><span class="opacity-60">elige la ruta rápida</span></div>
<div>💳 FICO<br/><span class="opacity-60">califica tu riesgo</span></div>
<div>📈 Trading<br/><span class="opacity-60">señales de compra/venta</span></div>
</div>

<div class="mt-8 text-xs opacity-60 text-center">
"Producto de datos" se formalizó con Data Mesh (Dehghani, O'Reilly, 2022)
</div>

<div class="mt-1 text-xs opacity-40 text-center">
infográfico completo en slides/infograficos/infografico_producto_de_datos.pptx
</div>

---
layout: center
class: text-center
---

# ¿Dónde vive todo esto?

## Cloud vs. On-Premise

---

# On-Premise vs. Cloud Computing

<div class="grid grid-cols-2 gap-6 mt-6">
<div class="p-5 rounded bg-gray-500/10">
<div class="font-bold text-lg text-center">🏢 On-Premise</div>
<ul class="text-sm mt-4 space-y-3 opacity-80 list-none pl-0">
<li><b>Costo inicial</b> — Alto: hardware, espacio, licencias</li>
<li><b>Elasticidad</b> — Limitada al hardware adquirido</li>
<li><b>Control</b> — Total, físico y lógico</li>
<li><b>Mantenimiento</b> — Tu equipo responde a fallas</li>
<li><b>Tecnología</b> — Sujeta al ciclo de vida del hardware</li>
</ul>
</div>
<div class="p-5 rounded bg-blue-500/10">
<div class="font-bold text-lg text-center">☁️ Cloud Computing</div>
<ul class="text-sm mt-4 space-y-3 opacity-80 list-none pl-0">
<li><b>Costo inicial</b> — Se paga por consumo</li>
<li><b>Elasticidad</b> — Prácticamente ilimitada, en minutos</li>
<li><b>Control</b> — Compartido con el proveedor</li>
<li><b>Mantenimiento</b> — El proveedor gestiona la plataforma</li>
<li><b>Tecnología</b> — Acceso inmediato a lo nuevo</li>
</ul>
</div>
</div>

<div class="mt-6 text-blue-500 font-bold text-center">
En Big Data, la elasticidad de la nube es lo que permite responder a picos de Volumen y Velocidad
</div>

<div class="mt-1 text-xs opacity-40 text-center">
infográfico completo en slides/infograficos/infografico_onprem_vs_cloud.pptx
</div>

---

# IaaS, PaaS, SaaS: ¿quién gestiona qué?

| Capa | On-Premises | IaaS | PaaS | SaaS |
|---|---|---|---|---|
| Aplicaciones | Tú | Tú | Tú | **Proveedor** |
| Datos | Tú | Tú | Tú | **Proveedor** |
| Runtime | Tú | Tú | **Proveedor** | **Proveedor** |
| Middleware | Tú | Tú | **Proveedor** | **Proveedor** |
| SO | Tú | Tú | **Proveedor** | **Proveedor** |
| Virtualización | Tú | **Proveedor** | **Proveedor** | **Proveedor** |
| Servidores | Tú | **Proveedor** | **Proveedor** | **Proveedor** |

<div class="grid grid-cols-4 gap-2 mt-1 text-xs text-center">
<div class="py-0.5 px-1 rounded bg-gray-500/10">Servidor propio</div>
<div class="py-0.5 px-1 rounded bg-gray-500/10">VM: EC2, Compute Engine</div>
<div class="py-0.5 px-1 rounded bg-gray-500/10">Spark gestionado, App Engine</div>
<div class="py-0.5 px-1 rounded bg-gray-500/10">Workspace, M365</div>
</div>

<div class="mt-1 text-xs opacity-60 text-center">
Cuanto más a la derecha, menos infraestructura gestionas tú, menos control tienes
</div>

---

# ¿Y qué hay en la nube?

<div class="grid grid-cols-3 gap-4 mt-8">
<div class="p-4 rounded bg-gray-500/10">
<div class="font-bold text-center mb-1">📦 Almacenamiento</div>
<div class="text-xs text-center opacity-60 mb-3">Guardar datos de forma duradera y barata</div>
<div class="text-xs space-y-1">
<div><b class="text-orange-500">AWS</b> — Amazon S3</div>
<div><b class="text-blue-500">Azure</b> — Data Lake Storage</div>
<div><b class="text-blue-400">Google</b> — Cloud Storage</div>
</div>
</div>
<div class="p-4 rounded bg-gray-500/10">
<div class="font-bold text-center mb-1">⚙️ Procesamiento</div>
<div class="text-xs text-center opacity-60 mb-3">Transformar y agregar datos a escala</div>
<div class="text-xs space-y-1">
<div><b class="text-orange-500">AWS</b> — Amazon EMR</div>
<div><b class="text-blue-500">Azure</b> — HDInsight</div>
<div><b class="text-blue-400">Google</b> — Managed Service for Apache Spark</div>
</div>
</div>
<div class="p-4 rounded bg-gray-500/10">
<div class="font-bold text-center mb-1">🔀 Orquestación</div>
<div class="text-xs text-center opacity-60 mb-3">Encadenar y programar pipelines completos</div>
<div class="text-xs space-y-1">
<div><b class="text-orange-500">AWS</b> — MWAA (Airflow)</div>
<div><b class="text-blue-500">Azure</b> — Data Factory</div>
<div><b class="text-blue-400">Google</b> — Cloud Composer</div>
</div>
</div>
</div>

<div class="mt-6 text-xs opacity-60 text-center">
+ Terraform — infraestructura como código, multicloud · nombres de servicio vigentes en 2026
</div>

<div class="mt-2 text-xs opacity-40">
→ Para qué sirve cada rubro, a detalle, en las siguientes slides · infográfico completo en slides/infograficos/infografico_que_hay_en_la_nube.pptx
</div>

---

# Almacenamiento: ¿para qué sirve?

<div class="w-24 h-24 rounded-full bg-blue-500/15 flex items-center justify-center text-5xl mx-auto mt-2">📦</div>

<div class="max-w-2xl mx-auto mt-6 text-left space-y-4">
<div class="text-sm opacity-80">
Guardar datos —crudos o ya procesados— de forma duradera, barata y accesible desde cualquier otro servicio, sin acoplarte a una sola máquina ni preocuparte por quedarte sin espacio.
</div>
<div class="p-3 rounded bg-blue-500/10 text-sm">
<b>En este curso</b> — el bucket de Cloud Storage donde subes <code>bank_transactions.csv</code> es el punto de entrada de todo el pipeline: procesamiento y orquestación leen de ahí.
</div>
</div>

---

# Procesamiento: ¿para qué sirve?

<div class="w-24 h-24 rounded-full bg-purple-500/15 flex items-center justify-center text-5xl mx-auto mt-2">⚙️</div>

<div class="max-w-2xl mx-auto mt-6 text-left space-y-4">
<div class="text-sm opacity-80">
Transformar, limpiar y agregar datos a escala — ejecutar el cómputo distribuido que una sola máquina no podría hacer en un tiempo razonable.
</div>
<div class="p-3 rounded bg-purple-500/10 text-sm">
<b>En este curso</b> — Managed Service for Apache Spark leyendo los 7.5 GB de <code>bank_transactions.csv</code> y calculando agregados: Maestría Sesión 1 en adelante.
</div>
</div>

---

# Orquestación: ¿para qué sirve?

<div class="w-24 h-24 rounded-full bg-amber-500/15 flex items-center justify-center text-5xl mx-auto mt-2">🔀</div>

<div class="max-w-2xl mx-auto mt-6 text-left space-y-4">
<div class="text-sm opacity-80">
Encadenar y programar los pasos de un pipeline completo (extraer → transformar → cargar → entrenar → servir) para que corran solos, en orden, y de forma confiable.
</div>
<div class="p-3 rounded bg-amber-500/10 text-sm">
<b>En este curso</b> — el DAG de Airflow (<code>mlops_pipeline_dag.py</code>) que ejecuta el pipeline de fraude completo cada noche: Maestría Sesión 12.
</div>
</div>

---
layout: center
class: text-center
---

# Con esto ya tienes el mapa completo

<div class="mt-8 text-lg max-w-2xl mx-auto opacity-80">
Qué es Big Data, qué tipos de dato existen, dónde persisten, cómo se usan, y dónde corre todo esto.
</div>

<div class="mt-10 text-sm opacity-60">
→ Especialidad Sesión 1: Big Data para decisiones de negocio
<br/>
→ Maestría Sesión 1: Arquitecturas distribuidas
</div>
