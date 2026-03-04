# Laboratorio de Big Data: Arquitecturas Hive en HDFS y Google Cloud Storage (GCS)

Este repositorio contiene la implementación de estructuras de datos masivos utilizando **Apache Hive** sobre un cluster de **Dataproc**. El objetivo es demostrar la transición de entornos locales (HDFS) hacia arquitecturas modernas en la nube (GCS), aplicando técnicas de optimización.

## Contexto del Proyecto
El proyecto procesa tres fuentes de datos principales:
1. **Carpetas de Investigación**: Datos de criminalidad (CSV en HDFS).
2. **Sentiment Data**: Logs de tráfico HTTP con análisis de sentimiento (Parquet en GCS).
3. **Email Data**: Registros de comunicaciones corporativas (CSV multilínea en GCS).

---

### Contexto técnico.
1. Plantilla Universal (Sintaxis Completa)
SQL
CREATE [EXTERNAL] TABLE [IF NOT EXISTS] nombre_tabla (
    columna1 tipo_dato [COMMENT 'comentario'],
    columna2 tipo_dato,
    ...
)
[COMMENT 'Descripción de la tabla']
[PARTITIONED BY (columna_particion tipo_dato, ...)]
[CLUSTERED BY (columna_bucket) [SORTED BY (columna_orden ASC|DESC)] INTO num_buckets BUCKETS]
[ROW FORMAT DELIMITED | SERDE 'clase_serde']
    [FIELDS TERMINATED BY 'char']
    [LINES TERMINATED BY 'char']
[STORED AS formato_archivo]
[LOCATION 'gs://bucket/ruta/' | '/user/hdfs/ruta/']
[TBLPROPERTIES ('propiedad'='valor')];

2. Desglose de Cláusulas Técnicas
EXTERNAL vs. MANAGED (Internal)
EXTERNAL: Es la mejor práctica en Big Data. Hive solo gestiona los metadatos. Si ejecutas un DROP TABLE, los datos en el bucket NO se borran.

MANAGED: Hive es dueño de los datos. Si borras la tabla, los archivos físicos desaparecen.

Organización de Datos (Rendimiento)
PARTITIONED BY: Crea subdirectorios físicos. Es vital para el Partition Pruning (evita leer toda la tabla).

Ejemplo: PARTITIONED BY (anio INT, mes INT) -> Ruta: /tabla/anio=2024/mes=03/.

CLUSTERED BY (Bucketing): Distribuye los datos en un número fijo de archivos mediante un cálculo de hash. Optimiza los Joins y el muestreo.

Formatos de Almacenamiento (STORED AS)
El formato impacta directamente en el costo de almacenamiento y la velocidad de procesamiento:

TEXTFILE: Texto plano (CSV/TSV). Compatible con todo, pero pesado y lento.

PARQUET: Formato columnar. Comprime los datos y es ideal para procesos de Spark y BigQuery.

ORC: El formato nativo más optimizado para Hive.

## 1. Gestión de Tablas Externas (Raw Layer)

### A. Almacenamiento Tradicional (HDFS)
Utilizamos `EXTERNAL TABLE` para mapear datos que residen en el sistema de archivos del cluster sin tomar posesión de los archivos físicos.

```sql
-- Tabla de criminalidad cargada desde el sistema de archivos local del cluster
CREATE EXTERNAL TABLE carpetas_investigacion 
(
    id INT, 
    ao_hechos INT, 
    mes_hechos STRING, 
    fecha_hechos TIMESTAMP, 
    delito STRING, 
    categoria_delito STRING, 
    fiscalia STRING,
    agencia STRING, 
    unidad_investigacion STRING, 
    colonia_hechos STRING, 
    alcaldia_hechos STRING, 
    fecha_inicio TIMESTAMP,
    mes_inicio STRING, 
    ao_inicio INT, 
    calle_hechos STRING, 
    calle_hechos2 STRING, 
    longitud FLOAT, 
    latitud FLOAT, 
    geopoint STRING  
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION '/user/carpetas_hdfs' 
TBLPROPERTIES ("skip.header.line.count"="1");
```

B. Integración con Google Cloud Storage (GCS)
Mapeo de datos directamente desde Buckets de GCP, utilizando el formato Parquet para optimizar el rendimiento y el SerDe de Hive para parsear formatos de fecha complejos.

```sql
-- Datos de sentimiento HTTP optimizados en formato Columnar (Parquet)
CREATE EXTERNAL TABLE HTTP_DATA (
    seq INT,
    id STRING,
    visited TIMESTAMP,
    logged_user STRING,
    pc STRING,
    url STRING,
    content STRING,
    sentiment DOUBLE
)
STORED AS PARQUET
LOCATION 'gs://BUCKET/http_sentiment/http_sentiment_compressed';


-- Datos de Email con formato de fecha personalizado
CREATE TABLE EMAIL_DATA
(
    id STRING, 
    sent_date TIMESTAMP,
    logged_user STRING, 
    pc STRING,
    to_mail STRING, 
    cc_mail STRING,
    bcc_mail STRING, 
    from_mail STRING, 
    size INT, 
    attachment_count INT,
    content STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  "field.delim" = ",",
  "timestamp.formats" = "MM/dd/yyyy HH:mm:ss" 
)
LOCATION 'gs://BUCKET/email/'
TBLPROPERTIES ("skip.header.line.count"="1");
```

2. Optimizaciones de Rendimiento
Particionamiento Dinámico (Partitioning)
Implementamos particionamiento para mejorar la velocidad de consulta mediante el filtrado de directorios (Partition Pruning).

```sql
-- Estructura particionada por año y mes
CREATE EXTERNAL TABLE HTTP_DATA_PARTITIONED (
    seq INT,
    id STRING,
    visited TIMESTAMP,
    logged_user STRING,
    pc STRING,
    url STRING,
    content STRING,
    sentiment DOUBLE
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET;

-- Configuración de Hive para permitir particionamiento dinámico
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

-- Inserción y distribución de datos
INSERT INTO HTTP_DATA_PARTITIONED 
SELECT seq, id, visited, logged_user, pc, url, content, sentiment, 
       year(visited) as year, month(visited) as month 
FROM HTTP_DATA;
```

Segmentación (Bucketing)
El bucketing permite distribuir los datos uniformemente basados en un hash de columna, optimizando los procesos de JOIN y SAMPLE.

```sql
-- Distribución de datos en 30 buckets basados en el ID de la PC
CREATE EXTERNAL TABLE HTTP_DATA_BUCKETS (
    seq INT,
    id STRING,
    visited TIMESTAMP,
    logged_user STRING,
    pc STRING,
    url STRING,
    content STRING,
    sentiment DOUBLE
)
CLUSTERED BY (pc) SORTED BY (visited) INTO 30 BUCKETS
STORED AS PARQUET
LOCATION 'gs://BUCKET/http_sentiment_bucketed';

-- Activación de cumplimiento de bucketing
SET hive.enforce.bucketing = true;

-- Carga de datos segmentados
INSERT INTO HTTP_DATA_BUCKETS 
SELECT seq, id, visited, logged_user, pc, url, content, sentiment 
FROM HTTP_DATA;
```

3. Glosario de Contexto Técnico Notas Técnicas y Troubleshooting
   - Dynamic Partitioning Error: Si Hive arroja errores durante la inserción en tablas particionadas, asegúrese de que el modo esté en nonstrict.
   - Bucketing Validation: El bucketing se valida verificando que en el bucket de GCS existan exactamente 30 archivos de salida dentro de la carpeta de la tabla.
   - External vs Internal: Todas las tablas en este laboratorio son EXTERNAL para garantizar que la eliminación de metadatos en Hive no afecte los datos persistentes en Google Cloud Storage.
   - EXTERNAL TABLE: Indica que Hive no es "dueño" de los datos. Si borras la tabla, los archivos en GCS/HDFS permanecen intactos.
   - PARQUET: Formato de almacenamiento columnar que reduce drásticamente el uso de espacio y mejora la velocidad de lectura.
   - SERDE: (Serializer/Deserializer) Permite a Hive leer datos en formatos específicos (como el formato de fecha de los emails).
   - NONSTRICT: Permite insertar datos en particiones sin tener que definir cada una manualmente.