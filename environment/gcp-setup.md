# Configuración del entorno — GCP free tier

## 1. Cuenta y proyecto
1. Crear cuenta de Google Cloud (idealmente nueva, para el crédito de $300 USD / 90 días).
2. Crear un proyecto dedicado al curso, ej. `big-data-course-<grupo>`.
3. Activar facturación y **configurar una alerta de presupuesto** (Billing → Budgets & alerts) en, por ejemplo, 50% del crédito disponible.

## 2. Herramientas locales
- Instalar [Google Cloud SDK](https://cloud.google.com/sdk) (`gcloud`, `gsutil`, `bq`).
- Autenticarse: `gcloud auth login` y `gcloud config set project <PROYECTO>`.

## 3. Servicios Always Free usados en el curso
| Servicio | Límite Always Free | Uso en el curso |
|---|---|---|
| BigQuery | 1 TB de consultas/mes, 10 GB almacenamiento | Sesión 3 (SQL distribuido) |
| Cloud Storage | 5 GB regional (us-*) | Data lake (Sesiones 5, 6) |
| Compute Engine | 1 VM `e2-micro` en us-west1/us-central1/us-east1 | Práctica ligera de Spark standalone, Airflow (Sesión 8) |
| Pub/Sub | 10 GB/mes | Streaming (Sesión 7) |

## 4. Servicios que consumen el crédito de $300
> **Nota de nombres (2026):** Google renombró Dataproc a **"Managed Service for Apache Spark"**
> (unifica el antiguo "Dataproc on Compute Engine" y "Serverless for Apache Spark" bajo un
> solo nombre). Los comandos de `gcloud` **no cambiaron** — sigue siendo `gcloud dataproc ...`
> — solo cambió el nombre comercial/documentación. En este curso usamos el nombre nuevo en la
> prosa y el nombre de comando de siempre en el código.

- **Managed Service for Apache Spark** (antes "Dataproc"; Sesiones 2, 4, 5, 7): cobra por hora de cluster. Comando típico para crear un cluster mínimo:
  ```bash
  gcloud dataproc clusters create curso-cluster \
    --region=us-central1 \
    --num-workers=2 \
    --worker-machine-type=n1-standard-2 \
    --master-machine-type=n1-standard-2
  ```
  **Siempre apagar al terminar el lab:**
  ```bash
  gcloud dataproc clusters delete curso-cluster --region=us-central1
  ```
- **Cloud Composer** (Sesión 8, opcional): siempre encendido, es el servicio más caro del curso. Se recomienda usar Airflow standalone en la VM `e2-micro` en su lugar.

## 5. Checklist antes de la Sesión 1
- [ ] Proyecto de GCP creado y facturación activa
- [ ] Alerta de presupuesto configurada
- [ ] `gcloud` CLI instalado y autenticado
- [ ] Bucket de Cloud Storage creado (`gsutil mb gs://<nombre-unico>`)
- [ ] Query de prueba corrida en BigQuery sandbox
