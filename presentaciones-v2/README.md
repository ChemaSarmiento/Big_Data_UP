# Big Data · Especialidad · ocho sesiones completas para revisión local

**8 × 180 minutos / 203 slides.** Solo Especialidad. S1–S7 se rediseñaron con el kit de identidad y storytelling de Chema: 189 slides con narrativas, composiciones y demostraciones propias. S8 conservan la versión base; el piloto original sigue disponible.

Revisión propuesta: [intro](especialidad-01/), [SQL](especialidad-02/), [Bronze](especialidad-03/). El syllabus específico y la justificación editorial están en `docs/rediseno-especialidad/propuesta-editorial-s01-s03.md` desde la raíz del repo.

Desde la raíz del repo:

```bash
python3 -m http.server 4183 --bind 127.0.0.1 --directory presentaciones-v2
```

Abrir **http://localhost:4183/**. El catálogo enlaza cada deck y laboratorio. Servir esta carpeta completa: todas las sesiones usan `compartido/` y `recursos/`. No se publicó el sitio ni se modificó Firebase.

## Navegación

Clic en espacio libre, flecha derecha o espacio revela/avanza; izquierda retrocede. `O` abre índice, `L` guía, `F` pantalla completa. Controles, enlaces, formularios y código no navegan accidentalmente. «Mostrar todo» revela la pantalla; el índice permite imprimir todas las slides. Se respeta movimiento reducido y el móvil permite scroll vertical.

La guía se abre en otra pestaña y se imprime aparte. Los registros H2–H8 se guardan en ese navegador y se descargan como JSON: no envían una entrega ni reservan datasets. No escribir secretos. S1 tiene la [ficha del proyecto](especialidad-01/ficha-proyecto.html) y la plantilla H1. El mapa se declara propuesto, no implementado.

## Qué está incluido

| Sesión | Slides | Laboratorio/taller |
|---|---:|---|
| 1 · Una compra merece evidencia | 27 | GCP, presupuesto, bucket y pregunta propia |
| 2 · SQL esencial | 28 | Seis consultas `employees` + controles temporales |
| 3 · Bronze | 26 | CSV, manifiesto, tabla externa y consulta |
| 4 · Silver y gobierno | 27 | Tipos, rechazos, reconciliación y matriz |
| 5 · Gold | 27 | Catálogo, selección, costo/cobertura y KPIs |
| 6 · Dashboard | 28 | BigQuery/BI, agregación, filtro y comunicación |
| 7 · GenAI y evidencia | 28 | Recuperación local, prompt, memo y auditoría |
| 8 · Comité | 14 | Defensa con reloj manual, rúbrica, auditoría y cierre |

**Proyecto:** un dataset distinto por equipo. Las clases usan employees y un fixture de precios como apoyo; los KPIs de cada proyecto dependen del dominio. ML se limita a 10 minutos conceptuales en S7, sin entrenamiento ni entregable predictivo.

## Datos y código: distinguir tres niveles

1. **Fixture ilustrativo runnable:** `recursos/precios-ilustrativos.csv`, manifiesto y SQL GoogleSQL para aprender Bronze/Silver/Gold con esquema conocido. 16 filas → una copia exacta retirada + dos rechazadas + 13 válidas. Canastas A150/B160 completas; C54 es subtotal de 3/5 productos. No son filas de PROFECO ni evidencia de escala.
2. **Datos reales a escala:** all_data y los otros archivos del Drive requieren perfilado, licencias/procedencia, región, permisos y una consulta de costo controlado. No aplicarles automáticamente el esquema de ocho columnas del fixture. Este trabajo previo no se ha completado desde estas presentaciones.
3. **Proyectos diversos:** el docente prepara/valida un paquete distinto por equipo y adapta SQL base, controles y salidas antes de clase. Las plantillas de gobierno/KPI/evidencia ayudan; no sustituyen ese contrato de datos. Otro formato o filtro del mismo origen no cuenta como fuente diferente.

Los scripts escriben/reemplazan solo tablas `curso_*` en el proyecto elegido: leer y ejecutar manualmente en un proyecto de laboratorio. Región propuesta `us-central1`; comprobar política y compatibilidad antes de usarla. S2 usa SQL MariaDB sobre la base cargada por el docente; su test local reducido usa SQLite y **no equivale a un ensayo del servidor real**.

## GenAI y recuperación

`especialidad-07/practica.html` busca fichas por coincidencia de términos con IDs. Funciona localmente, sin embeddings, claves ni llamadas LLM. La generación se hace aparte en la interfaz GCP autorizada: se copian fragmentos revisados y el agregado a un prompt. Es una demostración asistida del patrón recuperación/generación, no un servicio RAG automático desplegado.

`respuesta-ejemplo.txt` es un texto **escrito a mano** con errores para auditar; no se presenta como ejecución de un modelo. No se eligió un modelo fijo ni se comprobó su disponibilidad para la cuenta del grupo. Looker Studio/Vertex AI son nombres del syllabus; la documentación consultada puede mostrar Data Studio/Agent Studio: revisar la interfaz real antes de clase.

## Editar y regenerar

S1–S7: `editorial/guion.py` contiene títulos, composiciones HTML/SVG, fuentes y guion hablado. `editorial/editorial.css` define el lienzo16:9 y la adaptación móvil; `editorial/interacciones.js` contiene las demostraciones locales. El generador escribe slides, notas y README; no modifica las guías.

S2–S8: `contenido.json` mantiene la fuente de las guías. Solo S8 usan además sus slides JSON; el campo slides de S2/S3 se conserva como referencia anterior, claramente marcado. `scripts/build.py` preserva decks/notas/README editoriales. S1 mantiene una guía HTML escrita directamente.

```bash
python3 presentaciones-v2/scripts/build.py
python3 presentaciones-v2/scripts/build-editorial.py
python3 presentaciones-v2/scripts/catalogo.py
```

Editar las fuentes, no los HTML generados. `compartido/deck.js` conserva navegación por pasos. El manifiesto cuenta automáticamente S1–S7. Las fuentes y la imagen del kit están en `identidad/`; las slides no requieren llamadas externas para presentarse.

## Verificación reproducible

Con el servidor en marcha:

```bash
python3 presentaciones-v2/scripts/verify-resources.py
node presentaciones-v2/scripts/verify-editorial.mjs
node presentaciones-v2/scripts/verify-course.mjs
```

Los recorridos usan Chromium instalado en `slides_maestria/node_modules/playwright-chromium` y pueden requerir permiso del entorno. `verify-editorial.mjs` recorre S1–S7 a 1440×900, 1280×720 y 390×844; comprueba interacción, contraste oscuro, ausencia de recortes, guías, persistencia y descargas. Capturas, PDFs16:9 y reporte en `/tmp/bigdata-editorial/`. `verify-course.mjs` verifica S8 y sus prácticas, con artefactos en `/tmp/bigdata-plan3-curso/`. Los verificadores antiguos del piloto/S1 corresponden a esas versiones históricas; para S1 vigente usar verify-editorial.

Los controles de recursos validan fixture, SQL común sobre SQLite reducido y resultados esperados. No prueban el motor MariaDB ni GCP.

**Pendiente de validación docente:** ejecución end-to-end en GCP/MariaDB real, permisos del alumnado, cuotas, costos observados, conexión/compartición BI, modelo de GenAI y paquetes de fuentes reales distintas. Los checks locales no prueban esas integraciones. Las fuentes externas están enlazadas en cada caso y guía; beneficios reportados no se convierten en ROI prometido para la clase.
