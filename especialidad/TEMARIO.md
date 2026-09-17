# Temario — Track Especialidad

> Desglose de temas y subtemas por sesión. Para el contenido desarrollado de cada
> tema ver `sesion-XX/teoria.md`; para cómo enseñarlo, `sesion-XX/facilitacion.md`.
> Resumen ejecutivo del programa (objetivos, evaluación): [`PROGRAMA.md`](PROGRAMA.md).

## Módulo 0 — Sesión 00: Nivelación
1. Linux esencial
   - Qué es una terminal (analogía: explorador de archivos)
   - Comandos básicos de navegación (`cd`, `ls`, `pwd`, `mkdir`)
2. Python esencial
   - Qué es una variable
   - Qué es un notebook (Jupyter/Colab) y cómo correr una celda
   - Por qué el orden de ejecución de celdas importa
3. SQL esencial
   - `SELECT` / `WHERE` / `GROUP BY`
   - Cómo leer una consulta en lenguaje natural
4. Acceso a la consola web de GCP
   - Cuenta, proyecto, alerta de presupuesto (sin instalar nada localmente)

## Sesión 01: Big Data para decisiones de negocio
1. Las 5 V's (Volumen, Velocidad, Variedad, Veracidad, Valor)
   - Ejemplos por industria (banca, retail, salud)
2. Cuándo sí se necesita Big Data y cuándo no
   - La pregunta correcta vs. "¿tenemos muchos datos?"
   - Sobre-ingeniería: el error más caro
3. El ecosistema, a nivel de mapa
   - Storage, cómputo distribuido, bases analíticas, streaming, orquestación

## Sesión 02: Cómo funciona por dentro (sin código pesado)
1. Almacenamiento y cómputo distribuido, con analogías
   - La biblioteca repartida en bodegas (storage)
   - El equipo de 10 personas contando documentos (cómputo distribuido)
2. Qué es un cluster
   - Nodo maestro vs. nodos trabajadores
3. Qué significa "procesar en paralelo"
   - Límites del paralelismo (coordinar cuesta)
   - Introducción al concepto de skew (sin resolverlo)

## Sesión 03: SQL para analítica a escala
1. BigQuery desde la consola web
   - El editor, el explorador de esquema, el estimador de bytes
2. Cómo leer una consulta
   - Orden lógico real: `FROM → WHERE → GROUP BY → SELECT → ORDER BY`
3. Qué es "particionar" una tabla
   - Analogía del archivero con un cajón por mes
4. Cómo se ve el costo de una consulta
   - Por qué `SELECT *` cuesta de más
   - Por qué `LIMIT` no reduce el costo

## Sesión 04: Introducción a Spark
1. Qué problema resuelve Spark que SQL no resuelve
   - Lógica de negocio compleja, ML, combinar fuentes distintas
2. Vocabulario mínimo
   - DataFrame, transformación (planea), acción (ejecuta)
3. Por qué no entramos a shuffle/optimización aquí
   - Ese contenido es de Maestría — solo reconocer el vocabulario

## Sesión 05: Cómo se ve un pipeline de datos real
1. Qué es un ETL
   - Extract, Transform, Load — qué puede fallar en cada etapa
2. De dónde vienen los datos, a dónde van
   - Quién consume el dato al final: dashboard, modelo, reporte
   - Por qué "nadie lo usa" es el fracaso silencioso de un ETL técnicamente correcto

## Sesión 06: Data Lakes y gobierno del dato
1. Qué es un data lake
   - Bodega vs. archivero organizado
2. Arquitectura medallion, en términos simples
   - Bronze (crudo) → Silver (limpio) → Gold (listo para usar)
3. Por qué importa el gobierno del dato
   - Sin control de acceso, sin validación de calidad, sin linaje

## Sesión 07: Datos en tiempo real
1. Batch vs. tiempo real
   - La pregunta que los separa: ¿alguien actúa distinto si llega en segundos?
2. Trade-offs de optar por tiempo real
   - Costo de infraestructura, complejidad de desarrollo
   - El error común: tiempo real por prestigio, no por necesidad

## Sesión 08: Costos, gobernanza y cómo evaluar un proyecto de datos
1. Cómo se cobra la nube
   - Por uso, por hora, por almacenamiento
2. Qué preguntas hacer para evitar sorpresas de costo
   - Las 5 preguntas de evaluación
3. Framework para evaluar una propuesta técnica
   - Arquitectura, Costo, Riesgo, Tiempo

## Sesión 09: Presentación del proyecto final
1. Por qué la estructura del documento no es arbitraria
   - Las 6 secciones institucionales y qué pregunta responde cada una
2. Cómo presentar sin perder al público en 15 minutos
   - Título = conclusión, visualización obligatoria, código mostrado no explicado línea por línea

---

## Mapa de progresión (para ver el hilo completo)

| Sesión | Construye sobre | Prepara para |
|---|---|---|
| 00 | — | Todo el curso |
| 01 | 00 | El criterio de "cuándo sí" se usa en 06, 07, 08 |
| 02 | 01 | El vocabulario de cluster se usa en 04 |
| 03 | 00, 02 | La disciplina de costo se usa en 08 |
| 04 | 02, 03 | — |
| 05 | 03, 04 | El patrón ETL se usa en el proyecto final (09) |
| 06 | 05 | — |
| 07 | 01, 06 | — |
| 08 | 01–07 (todo el vocabulario acumulado) | El framework se aplica al proyecto final |
| 09 | Todo el curso | — |
