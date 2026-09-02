# Big Data para Data Scientists — Dos tracks

El programa se divide en dos tracks paralelos que comparten el mismo entorno (GCP free tier)
y el mismo mapa temático general, pero con profundidad y objetivos distintos.

| | **Especialidad** | **Maestría en Ciencia de Datos** |
|---|---|---|
| Perfil | Diverso (negocio, riesgo, producto, etc.) | Ciencia de datos |
| Interés | Ejecutivo/estratégico | Técnico profundo |
| Código | Guiado y acotado (notebooks para completar) | Escrito desde cero, con tuning y optimización |
| Llega hasta | Propuesta de arquitectura + caso de negocio | Modelo entrenado, servido y monitoreado en producción |
| Duración | 9 sesiones · 3h/semana (27h) | 9 sesiones · 3h/semana (27h) |
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
│   ├── spark/                    # 4 scripts: RDD -> DataFrames -> Spark SQL -> Pipeline ML
│   ├── hive/                     # Queries: fundamentos + caso real (datos abiertos CDMX)
│   ├── sql-practica/             # SQL de nivelación sobre la base "test_db" de empleados
│   ├── datasets/                 # Datasets reales (BigQuery, Kaggle, CDMX, FRED) + generador sintético
│   ├── etl-tipo-cambio/          # Ejercicio de ETL: API pública -> Python -> MariaDB (+ versión Colab)
│   └── etl-cripto/               # Segundo ETL: enriquecimiento en 2 rondas E-T, carga en 4 tablas
├── slides/                       # Las 7 presentaciones del curso, mapeadas a sesiones
├── especialidad/
│   ├── PROGRAMA.md
│   └── sesion-00 ... sesion-09/  # Cada una con README (índice + ejemplo + recursos + slides)
└── maestria/
    ├── PROGRAMA.md
    └── sesion-00 ... sesion-09/  # Cada una con README (índice + ejemplo + recursos + slides)
```

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
