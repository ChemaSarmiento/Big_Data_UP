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

<div class="mt-4 text-sm opacity-70 text-center">
Cuanto más a la derecha, menos infraestructura gestionas tú — y menos control tienes sobre ella
</div>

---

# ¿Y qué hay en la nube?

<div class="grid grid-cols-3 gap-4 mt-8">
<div class="p-4 rounded bg-gray-500/10">
<div class="font-bold text-center mb-3">📦 Almacenamiento</div>
<div class="text-xs space-y-1">
<div><b class="text-orange-500">AWS</b> — Amazon S3</div>
<div><b class="text-blue-500">Azure</b> — Data Lake Storage</div>
<div><b class="text-blue-400">Google</b> — Cloud Storage</div>
</div>
</div>
<div class="p-4 rounded bg-gray-500/10">
<div class="font-bold text-center mb-3">⚙️ Procesamiento</div>
<div class="text-xs space-y-1">
<div><b class="text-orange-500">AWS</b> — Amazon EMR</div>
<div><b class="text-blue-500">Azure</b> — HDInsight</div>
<div><b class="text-blue-400">Google</b> — Managed Service for Apache Spark</div>
</div>
</div>
<div class="p-4 rounded bg-gray-500/10">
<div class="font-bold text-center mb-3">🔀 Orquestación</div>
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
