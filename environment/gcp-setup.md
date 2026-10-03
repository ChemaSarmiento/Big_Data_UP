# Entorno del curso — prueba de GCP con US$300 / 90 días

La ruta principal usa **crédito de prueba**, no promete que todos los servicios sean Always Free. Cada estudiante/equipo debe verificar elegibilidad, fecha de vencimiento, saldo y cuotas antes de crear recursos. No presupuestar cuentas nuevas sucesivas. Las 13 semanas de Maestría dejan poco margen dentro de 90 días: activar la prueba cuando empiecen los labs, no durante la nivelación.

## 1. Cuenta, acceso y presupuesto

1. Crear un proyecto exclusivo, confirmar crédito y fecha de vencimiento en Billing.
2. Configurar alertas de consumo de US$75, 150, 225 y 270. Las alertas informan; **no cortan automáticamente el gasto**. No activar facturación de pago sin entender el cambio.
3. Usar una región (`us-central1`) y guardar datos, modelos y resultados en un bucket privado de esa región.
4. Definir presupuesto por equipo/cuenta de facturación. Las cuotas gratuitas se comparten donde corresponda; no se multiplican por abrir proyectos.
5. Registrar después de cada lab: saldo, horas de cómputo, bytes almacenados y recursos restantes. Si se llega a US$225, revisar el plan antes del siguiente lab.

### Reserva de planificación, no cotización

| Partida | Tope objetivo de planificación |
|---|---:|
| Spark distribuido (labs y proyecto) | US$130 |
| VM temporal de Airflow/API | US$35 |
| BigQuery y almacenamiento | US$45 |
| Pub/Sub y operaciones de ingesta | US$15 |
| Reserva para repeticiones, red y diferencias de tarifas | US$75 |
| **Total máximo de la prueba** | **US$300** |

Estos importes son una **asignación docente**, no precios calculados ni garantía de suficiencia. Antes de crear el cluster, usar la [calculadora oficial](https://cloud.google.com/products/calculator) con región, tipo/número de VMs, discos y tiempo. Compartir cluster por equipo cuando corresponda, limitar duración, trabajar primero con muestras y medir antes de escalar. El saldo puede consumirse por almacenamiento/red aunque el job termine.

## 2. Herramientas y bucket

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project <PROJECT_ID>
gcloud services enable dataproc.googleapis.com compute.googleapis.com storage.googleapis.com pubsub.googleapis.com bigquery.googleapis.com
gcloud storage buckets create gs://<BUCKET_UNICO> --location=us-central1 --uniform-bucket-level-access
```

Para Pub/Sub/API/monitor local se usa Application Default Credentials. Los jobs de Spark usan la cuenta de servicio del cluster con permisos específicos sobre su bucket. Mantener recursos privados; acceso por IAP y gateway. Instalar dependencias según `environment/requirements-lab.txt`; Airflow tiene su propio entorno (ver `recursos/airflow/README.md`).

## 3. Qué cubre el nivel gratuito y qué consume crédito

| Servicio | Límite gratuito publicado | Uso de la ruta del curso |
|---|---|---|
| BigQuery | 1 TiB de consultas y 10 GiB de almacenamiento/mes | Consultas con dry run y máximo de bytes; exceso consume crédito |
| Cloud Storage | 5 GB-mes regional en regiones admitidas de EE.UU. | Datasets grandes, snapshots y modelos consumen crédito |
| Compute Engine | Horas equivalentes a una `e2-micro` y 30 GB-mes de disco estándar en regiones admitidas | No se dimensiona Airflow/Spark para una micro; VM de 4+ GB temporal consume crédito |
| Pub/Sub estándar | 10 GiB de mensajes/mes | Eventos acotados; verificar volumen publicado y entregado |
| Managed Service for Apache Spark | Sin franquicia equivalente al cluster docente | VMs + discos + tarifa de servicio consumen crédito |
| Cloud Composer / Vertex AI | No forman parte del lab obligatorio | Panorama; no crear endpoints/entornos persistentes por defecto |

## 4. Cluster temporal y ejecución

Usar [la receta de cluster](../recursos/managed-spark-cluster/README.md): imagen `2.2-debian12` (Spark 3.5), dos workers, gateway e IPs internas. El perfil con Iceberg se usa solo en S7–8. No crear varios clusters por estudiante para comparar estrategias: ejecutar secuencialmente sobre el mismo tamaño y registrar condiciones.

`--max-idle=20m --max-age=3h` limita la vida del cluster; no hace gratis su uso. Tres horas incluyen el setup: si el lab necesita más, estimar el costo antes de extenderlo. Guardar modelos y checkpoints en GCS antes de borrar el cluster. No mantener una VM de Airflow encendida entre semanas.

### Streaming actualizado

Pub/Sub Lite cerró el 18 de marzo de 2026. La ruta del curso es **Pub/Sub estándar → puente Python → JSON inmutable en GCS → Spark Structured Streaming**. Es streaming por microlotes; medir su latencia, no prometer respuesta en milisegundos. Ver [lab S9–10](../recursos/streaming/README.md).

## 5. Salida de cada práctica

- Borrar el cluster al terminar (la eliminación automática es un respaldo).
- Detener Airflow/API y la VM temporal; un disco conservado sigue generando almacenamiento.
- Borrar topics/suscripciones solo tras guardar la evidencia y finalizar productores/consumidores.
- Revisar snapshots/versiones de modelos, objetos temporales y transferencias de red. Conservar solo artefactos necesarios para la siguiente sesión.
- BigQuery: usar dry run, filtrar particiones y fijar `maximum_bytes_billed` en consultas de práctica.
- Descargar evidencia y documentar limpieza antes de vencer los 90 días; no asumir continuidad del servicio al vencer la prueba.

## Fuentes verificadas (revisión: 2026-10-02)

- [Free Trial y Free Tier](https://docs.cloud.google.com/free/docs/free-cloud-features)
- [Precios de Managed Service for Apache Spark](https://cloud.google.com/products/managed-service-for-apache-spark/pricing)
- [Alertas de presupuesto](https://docs.cloud.google.com/billing/docs/how-to/budgets)
- [Imágenes de cluster soportadas](https://docs.cloud.google.com/managed-spark/docs/concepts/versioning/image-version-lists)
- [Retiro de Pub/Sub Lite](https://docs.cloud.google.com/pubsub/lite/docs/release-notes)
