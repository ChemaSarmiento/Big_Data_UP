# Ejercicio de ETL: Tipo de cambio USD→MXN

Ejercicio completo de **Extracción → Transformación → Carga** usando Python y MariaDB,
pensado para correrse en una sola sesión de clase (o como tarea entre dos sesiones).

## Por qué esta API

**Frankfurter** (https://api.frankfurter.app) publica tipos de cambio históricos del
Banco Central Europeo desde 1999. Se eligió sobre otras opciones (como la API del propio
Banxico) por una razón puramente pedagógica: **no requiere registrarse ni pedir un token**
— toda la clase puede correr el ejercicio en el momento, sin fricción de credenciales.
Como extensión (ver sección 7) se sugiere migrar a Banxico para quien quiera trabajar con
la fuente "oficial" mexicana, una vez que el pipeline básico ya funciona.

> Nota: si en algún momento `api.frankfurter.app` deja de responder, el proyecto se movió
> a `api.frankfurter.dev/v1/` — revisar https://frankfurter.dev/docs si algo falla. Es un
> buen ejemplo real de por qué un pipeline de producción nunca debe hardcodear un solo
> proveedor de datos sin manejo de errores.

## Arquitectura del ejercicio

```
extract.py   → llama a la API, guarda el JSON crudo en data/raw/         (capa "bronze")
transform.py → limpia, calcula columnas derivadas, valida calidad de datos → data/processed/ (capa "silver")
load.py      → conecta a MariaDB y carga con upsert idempotente          (capa "gold" / consumo)
run_etl.py   → orquesta las tres etapas en orden, con logging
```

Esta separación en 3 archivos es intencional (no es solo un script): en clase se puede
correr cada etapa por separado con `print()`/inspección manual entre pasos, para que el
grupo vea el dato transformándose etapa por etapa, antes de automatizarlo con `run_etl.py`.

## 1. Preparar el entorno

```bash
cd recursos/etl-tipo-cambio
pip install -r requirements.txt
cp .env.example .env   # y editar con los datos de tu instancia de MariaDB
```

La instancia de MariaDB es la que se crea en `environment/mariadb-vscode-setup.md`.

## 2. Crear la tabla

```bash
mysql -h <host> -u big_data_user -p curso_bigdata < schema.sql
```

## 3. Correr el pipeline completo

```bash
python run_etl.py --base USD --symbols MXN --dias 90
```

Esto trae los últimos 90 días de tipo de cambio USD→MXN, los transforma y los carga a
MariaDB. Volver a correrlo con las mismas fechas **no duplica filas** — el `load.py` usa
`ON DUPLICATE KEY UPDATE`, así que es seguro reintentar si algo falla a la mitad.

## 4. Correr etapa por etapa (recomendado para la primera vez en clase)

```bash
python extract.py --base USD --symbols MXN --dias 90
python transform.py
python load.py
```

Cada script imprime cuántas filas produjo, para que el grupo vea el volumen de datos
moviéndose entre etapas.

## 5. Verificar la carga

Conectarse con VSCode (ver `environment/mariadb-vscode-setup.md`) y correr:

```sql
SELECT * FROM tipo_cambio ORDER BY fecha DESC LIMIT 10;
```

## 6. Versión para Google Colab

`etl_tipo_cambio_colab.ipynb` es la misma lógica de extract/transform/load, pero en un
solo notebook pensado para correr en Colab. La diferencia importante está en la carga:
Colab no tiene una IP fija (cambia cada vez que se reinicia el entorno), así que la
Opción A de conexión (restringir el firewall a tu IP) no sirve ahí — el notebook usa en
su lugar un **túnel IAP** (`gcloud compute start-iap-tunnel`), que no depende de qué IP
tenga Colab en ese momento. Requiere una regla de firewall adicional (documentada dentro
del propio notebook) que permite tráfico desde el rango fijo de IAP hacia el puerto 3306.

## 7. Extensiones sugeridas (para tarea o para Maestría)

- **Más monedas:** correr con `--symbols MXN,EUR,JPY` y comparar volatilidad.
- **Migrar a Banxico:** cambiar `extract.py` para usar la API de Banxico (requiere token
  gratuito) y comparar si el dato oficial mexicano difiere del de Frankfurter.
- **Calidad de datos:** agregar una validación que rechace la carga si `variacion_pct`
  de un día supera un umbral irreal (ej. 20%), como se vería un chequeo de calidad real
  en un pipeline bancario.
- **Orquestación:** convertir `run_etl.py` en un DAG de Airflow que corra diario (conecta
  directo con la Sesión 8 de Maestría).
- **Data Lake:** en vez de cargar directo a MariaDB, escribir la capa `processed/` como
  Parquet particionado por año-mes en Cloud Storage antes de cargar a la base (conecta
  con la Sesión 6 de arquitectura medallion).
