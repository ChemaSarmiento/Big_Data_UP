# Big Data para Data Scientists — Dos tracks

El programa se divide en dos tracks paralelos que comparten el mismo entorno (GCP: crédito de prueba US$300 / 90 días)
y el mismo mapa temático general, pero con profundidad y objetivos distintos.

| | **Especialidad** | **Maestría en Ciencia de Datos** |
|---|---|---|
| Perfil | Diverso (negocio, riesgo, producto, etc.) | Ciencia de datos |
| Interés | Ejecutivo/estratégico | Técnico profundo |
| Código | Guiado y acotado (notebooks para completar) | Escrito desde cero, con tuning y optimización |
| Llega hasta | Mismo proyecto final institucional (ETL + datos reales ≥15GB + visualización + documento), con código guiado/low-code | Mismo proyecto final institucional, con un prototipo reproducible: modelo entrenado, servido y monitoreado |
| Duración | 9 sesiones · 3h/semana (27h) | 13 sesiones · 3h/semana (39h) — 4 temas que no cabían en 3h se dividieron en 2 sesiones completas cada uno |
| Programa | [`especialidad/PROGRAMA.md`](especialidad/PROGRAMA.md) | [`maestria/PROGRAMA.md`](maestria/PROGRAMA.md) |

## Estructura del repo

```
big-data-course/
├── environment/
│   ├── gcp-setup.md              # Setup general de GCP, compartido por ambos tracks
│   └── mariadb-vscode-setup.md   # Conexión remota a MariaDB desde VSCode (túnel IAP)
├── recursos/                     # Material técnico reutilizable en ambos tracks
│   ├── mariadb/                  # Instancia + regla de VPC/firewall en un solo script
│   ├── managed-spark-cluster/    # Creación de cluster (antes "Dataproc") + init-actions
│   ├── spark/                    # 5 scripts: RDD -> DataFrames -> Spark SQL -> Pipeline ML -> data cleansing
│   ├── lakehouse-iceberg/        # Maestría S6: tabla Iceberg real (MERGE INTO, time travel, evolución de esquema)
│   ├── streaming/                # Maestría S7: Pub/Sub estándar → GCS → Structured Streaming + scoring
│   ├── airflow/                  # Maestría S8: DAG de MLOps (ingesta -> features -> entrenamiento -> despliegue)
│   ├── serving/                  # Maestría S8: endpoint de modelo (FastAPI) + monitoreo de drift (PSI)
│   ├── hive/                     # Queries: fundamentos + caso real (datos abiertos CDMX)
│   ├── sql-practica/             # SQL de nivelación sobre la base "test_db" de empleados
│   ├── datasets/                 # Datasets reales (BigQuery, Kaggle, CDMX, FRED) + generador sintético
│   ├── etl-tipo-cambio/          # Ejercicio de ETL: API pública -> Python -> MariaDB (+ versión Colab)
│   ├── etl-cripto/               # Segundo ETL: enriquecimiento en 2 rondas E-T, carga en 4 tablas
│   └── proyecto-ejemplo/         # Proyecto final imaginado de punta a punta (ambos tracks), datos reales de PROFECO
├── slides/                       # Las 7 presentaciones originales (.pptx), mapeadas a sesiones
├── slides_maestria/              # Decks nuevos de Maestría (Slidev) — uno por sesión, código+diagramas en vivo
├── especialidad/
│   ├── PROGRAMA.md
│   ├── TEMARIO.md                # Temas y subtemas por sesión
│   └── sesion-00 ... sesion-09/  # Cada una con README (índice + ejemplo + recursos + teoria.md + slides.md)
└── maestria/
    ├── PROGRAMA.md
    ├── TEMARIO.md                # Temas y subtemas por sesión
    └── sesion-00 ... sesion-13/  # Cada una con README (índice + ejemplo + recursos + teoria.md) — 13 sesiones, no 9 (ver Sección "Teoría y presentaciones")
```

## Presentaciones web para clase

Los dos tracks y la introducción comparten ahora un [sitio de presentaciones](presentaciones/README.md), con navegación por clic y teclado, entradas escalonadas, índice de diapositivas y pantalla completa. Mantiene una identidad visual consistente, añade rutas de aprendizaje y checkpoints, y complementa los temas detectados como incompletos.

```bash
cd slides_maestria
npm ci
npm run build:web
npm run serve:web
```

Abre http://localhost:4173. El sitio se genera desde los decks Markdown y los temarios; los PPTX originales se conservan como referencia.

## Teoría y presentaciones por sesión

Cada `sesion-XX/` tiene, además del README:

- **`teoria.md`** — explicación en prosa de cada punto del índice, con analogías
  (Especialidad) o profundidad técnica (Maestría), tablas comparativas, código
  donde aplica, y una sección de Referencias con fuentes reales.
- **Slides** — Especialidad usa [Marp](https://marp.app/) (`sesion-XX/slides.md`,
  un archivo autocontenido, sin instalación — `npx @marp-team/marp-cli`);
  Maestría usa [Slidev](https://sli.dev) (`slides_maestria/sesion-XX.md`, con
  diagramas Mermaid y bloques de código resaltado en vivo — ver
  [`slides_maestria/README.md`](slides_maestria/README.md) para setup y
  exportación a PDF/PPTX). Ambos siguen los principios de Cole Nussbaumer
  Knaflic (*Storytelling with Data*): título = conclusión, un solo acento de
  color, evitar pie charts cuando dificulten la comparación, etiqueta directa en vez de leyenda.

## Cómo usar este repo

1. Decide el track (o revisa ambos programas para confirmar cuál aplica a tu grupo).
2. Sigue `environment/gcp-setup.md` para configurar el proyecto de GCP.
3. Corre `recursos/mariadb/crear_firewall_y_instancia.sh` si el curso usa MariaDB además
   de BigQuery/Spark — deja la instancia y la regla de firewall listas en un solo paso.
4. Completa el Módulo 0 de tu track antes de la Sesión 1 (nivelación en Especialidad,
   prerequisito evaluado en Maestría).
5. Cada carpeta `sesion-XX/` dentro de tu track tiene su propio README con **índice**,
   **lab/actividad**, **entregable**, un **ejemplo concreto** apuntando a `recursos/`, y
   las **slides** correspondientes.
6. `recursos/` tiene el material técnico que ambos tracks referencian — en Especialidad
   se usa como notebook guiado; en Maestría, como punto de partida para escribir y
   extender el código.

## Sobre esta versión del repo

Este repo parte de un proyecto de curso preexistente (`Big_Data_UP`). Los cambios
principales sobre esa versión:

- **MariaDB + VPC**: crear la instancia ahora también crea la regla de firewall (antes
  era un paso manual aparte), sin exponer el puerto 3306 a `0.0.0.0/0` y sin contraseñas
  hardcodeadas en el repo — ver `recursos/mariadb/README.md` para el detalle antes/después.
- **Dataproc → Managed Service for Apache Spark**: Google renombró el producto en 2026;
  se actualizó la prosa del curso (los comandos `gcloud dataproc ...` no cambiaron).
- **Contenido real rescatado**: el lab de Hive sobre datos de criminalidad de CDMX y las
  queries de la base de empleados (`test_db`) se recuperaron y corrigieron — ver
  `recursos/hive/README.md` y `recursos/sql-practica/README.md`.
- **Se descartó** todo lo ya marcado como obsoleto en el repo original (Sqoop, scraper de
  Twitter) y las variantes de instalación de MariaDB redundantes entre sí.
- Los notebooks originales de `spark_notebooks/` (`PySpark_Intro`, `PySpark_Models`,
  `PySpark_Recommenders`) referencian buckets propios de un semestre anterior
  (`gs://big-data-lunes-20260223/...`) y no se migraron — si quieres reusarlos, hay que
  actualizar esas rutas a un bucket propio primero.

## Requisitos

- Cuenta de Google Cloud (idealmente nueva, para aprovechar el crédito de $300 USD / 90 días).
- Especialidad: sin requisitos técnicos previos formales.
- Maestría: dominio funcional de Python, SQL y ML "single-node" (pandas, scikit-learn).

## Revisión curricular y validación

Ver [REVISION_CURRICULAR.md](REVISION_CURRICULAR.md) para las correcciones, perfiles inferidos, fuentes y límites de las pruebas.
