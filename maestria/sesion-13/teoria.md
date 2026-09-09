# Teoría — Sesión 13: Gobernanza, seguridad y capstone

> El cierre técnico del programa: cómo un pipeline de ML deja de ser un proyecto de
> curso y se vuelve algo que un equipo de banca/finanzas podría operar de verdad, sin
> que legal o seguridad lo bloqueen.

## 1. IAM a nivel dataset/tabla

El Módulo 0 cubrió IAM a nivel de proyecto (quién puede crear/borrar recursos). En un
pipeline de datos regulado, el control tiene que llegar más fino: quién puede leer o
modificar **qué tabla específica**, no solo "el proyecto completo".

- **A nivel dataset (BigQuery):** roles como `roles/bigquery.dataViewer` otorgados
  sobre un dataset específico, no sobre el proyecto entero — un analista puede
  consultar la tabla de transacciones agregadas sin poder ver la tabla con datos
  personales sin enmascarar.
- **A nivel columna/fila (BigQuery, avanzado):** políticas de enmascaramiento dinámico
  y seguridad a nivel de fila permiten que dos personas consulten la *misma* tabla y
  vean resultados distintos según su rol — relevante en banca, donde un analista de
  fraude necesita ver montos pero no necesariamente el nombre completo del cliente.

El principio detrás de todo esto es **mínimo privilegio**: cada rol tiene exactamente
el acceso que necesita para su función, ni más — la alternativa ("todos con acceso de
Owner porque es más simple") es exactamente el tipo de decisión que un auditor de
cumplimiento rechaza de entrada.

## 2. Data Catalog y linaje

**Data Catalog** es un catálogo centralizado y buscable de todos los datasets de una
organización — qué tablas existen, qué columnas tienen, quién es dueño de cada una, y
con qué nivel de sensibilidad están etiquetadas (PII, financiero, público). Resuelve
un problema que crece exactamente con el éxito del programa de datos: cuando hay 5
datasets, cualquiera se acuerda de qué hay en cada uno; cuando hay 500, sin un catálogo
nadie sabe qué existe ni para qué sirve.

**Linaje de datos (data lineage)** es el registro de *de dónde vino* cada dato y *qué
transformaciones sufrió* hasta llegar a su forma actual — responde "¿por qué este
número en el dashboard es el que es?" rastreando hacia atrás hasta el dato crudo. El
pipeline de este curso (bronze → silver → gold, más el `PipelineModel` versionado)
tiene linaje *implícito* en su estructura de carpetas/tablas; un Data Catalog lo hace
*explícito* y buscable a escala de organización, no solo de un pipeline individual.

## 3. Cumplimiento en contextos regulados

Para el caso de uso transversal del curso (`bank_transactions.csv`, detección de
fraude), el contexto regulatorio relevante es el financiero. Tres exigencias típicas
que un pipeline de ML en banca tiene que satisfacer, más allá de "que el modelo
funcione":

- **Explicabilidad:** un modelo que niega o marca como sospechosa una transacción de
  un cliente real necesita poder justificar *por qué*, no solo dar un score — regresión
  logística (Sesión 6) tiene esta ventaja sobre modelos más opacos: sus coeficientes
  son directamente interpretables.
- **Trazabilidad:** cada predicción debe poder rastrearse hasta la versión exacta del
  modelo y del dato que la produjo — el mismo linaje del punto anterior, aplicado a
  nivel de una predicción individual, no solo de una tabla.
- **Retención y borrado de datos:** normativas de protección de datos personales
  suelen exigir que un dato pueda eliminarse a petición del titular — un data lake
  particionado (Sesión 7) facilita esto: borrar la partición correspondiente es
  mucho más simple que buscar y eliminar filas dispersas en archivos no particionados.

## 4. FinOps de un pipeline de ML a escala

FinOps es la disciplina de gestionar el costo de la nube como una responsabilidad
compartida entre finanzas e ingeniería, con visibilidad continua — no una revisión de
factura una vez al mes. Aplicado a un pipeline de ML como el de este curso:

- **Costo por etapa:** ¿cuánto cuesta la ingesta, cuánto el entrenamiento, cuánto el
  serving? Sin desagregar, es imposible saber dónde optimizar — `mlops_pipeline_dag.py`
  ya separa estas etapas como tareas distintas, lo que facilita instrumentar costo por
  tarea.
- **Costo de reentrenamiento vs. costo de degradación:** reentrenar tiene un costo de
  cómputo explícito (horas de cluster); *no* reentrenar cuando hay drift significativo
  tiene un costo implícito (decisiones de negocio basadas en un modelo degradado) — la
  puerta de calidad del DAG (AUC mínimo) es, en el fondo, una decisión de FinOps
  disfrazada de decisión técnica.

## 5. El capstone técnico

La presentación de hoy (máx. 15 min, ver `PROGRAMA.md` Sección 5) tiene que demostrar
el ciclo completo — no basta con "el modelo funciona", el criterio pide evidencia de
cada etapa: ingesta distribuida, feature engineering, entrenamiento con métricas
justificadas, serving o inferencia programada, streaming u orquestación, al menos una
visualización de las conclusiones, y evidencia de pruebas. Es, en esencia, demostrar
que las Sesiones 1-8 se conectan en un solo sistema — no ocho ejercicios sueltos.

---

## Referencias

- [Google Cloud — Dataplex / Data Catalog overview](https://cloud.google.com/dataplex/docs/catalog-overview)
- [Google Cloud — BigQuery column-level and row-level security](https://cloud.google.com/bigquery/docs/column-level-security-intro)
- [Google Cloud — Responsible AI practices (explicabilidad)](https://ai.google/responsibility/responsible-ai-practices/)
- [FinOps Foundation — What is FinOps?](https://www.finops.org/introduction/what-is-finops/)
