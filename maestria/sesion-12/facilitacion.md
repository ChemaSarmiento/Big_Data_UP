# Facilitación — Sesión 12: MLOps con Airflow

> Guion de 3 horas: talking points + lab guiado. Última sesión técnica antes del
> capstone — hoy se conectan todas las piezas de las Sesiones 5-11 en un solo
> sistema automatizado. Dale al grupo el momento de "ver el ciclo completo" que
> se ha ido construyendo sesión por sesión.

## Antes de empezar (facilitador)

Instala Airflow con anticipación en la VM `e2-micro` (o localmente para la
demo) — `airflow db init` la primera vez puede tardar y generar salida
confusa si se hace en vivo por primera vez frente al grupo.

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "Cuenta cuántas piezas separadas han construido desde la Sesión 5: un
> pipeline de features, un modelo entrenado, una tabla Iceberg versionada, un
> stream con scoring, un endpoint, un script de drift. Hoy, por primera vez,
> todo eso corre como un solo sistema, sin que ustedes tengan que ejecutar cada
> pieza a mano."

**Pregunta de apertura:**

> "Si tuvieran que automatizar 'reentrenar el modelo cada semana' con lo que ya
> saben, ¿qué usarían — un cron job simple, o algo más? ¿Qué le falta a un cron
> job simple?"

(Gancho hacia por qué Airflow: reintentos, dependencias, decisiones
condicionales — un cron job no da nada de eso.)

**Ejemplo de actualidad:**

> "Airflow nació en Airbnb para resolver exactamente este problema —
> orquestar pipelines de datos con dependencias complejas. Hoy es el estándar
> de facto en la industria; casi cualquier equipo de datos que hayan visto
> mencionar 'pipeline de ML en producción' está usando Airflow o algo muy
> similar por debajo."

---

## Bloque 2 — Teoría (0:15–1:00, 45 min)

### El DAG completo (20 min)

Dibuja el diagrama en el pizarrón mientras narras cada tarea:
`entrenamiento_y_features → evaluar_metricas → puerta_calidad → desplegar/no_desplegar`.
Pregunta en cada flecha: **"¿qué pasa si esta tarea falla? ¿Se reintenta, se
detiene todo, o sigue con la siguiente?"**

### Por qué esto no es solo el script de siempre (15 min)

Contrasta explícito con `run_etl.py` (que ya conocen desde las primeras
sesiones): secuencial, sin reintentos automáticos, sin decisión condicional
real. Airflow da las tres cosas que a ese script le faltan.

### Reentrenamiento por trigger de drift (10 min)

Conecta con la Sesión 11: el PSI > 0.25 es la señal que justificaría correr el
DAG fuera de su horario `@weekly`. Pregunta: **"¿por qué no simplemente correr
el DAG cada hora, para no depender de nadie que revise el PSI manualmente?"**
(costo — cada corrida completa consume tiempo de cluster real).

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Lab guiado (1:10–2:40, 90 min)

### Paso 1 — Setup de Airflow (25 min)

```bash
pip install apache-airflow apache-airflow-providers-google
airflow db init
airflow variables set gcp_project_id <PROJECT_ID>
airflow variables set gcp_bucket gs://<TU-BUCKET>
airflow variables set serving_host <host-del-endpoint>:8080
cp dags/mlops_pipeline_dag.py $AIRFLOW_HOME/dags/
airflow standalone
```

**Deberías ver:** Airflow standalone arranca y muestra una URL local (típicamente
`localhost:8080` — si choca con el puerto del endpoint de la Sesión 11, cambia
uno de los dos puertos antes de seguir).

**Si el DAG no aparece en la UI:** confirmar que `mlops_pipeline_dag.py` se
copió al directorio correcto (`$AIRFLOW_HOME/dags/`) y que no tiene errores de
sintaxis (`python dags/mlops_pipeline_dag.py` debe correr sin error como
chequeo rápido).

### Paso 2 — Disparar el DAG manualmente (40 min)

Desde la UI de Airflow: activar el DAG y disparar una corrida manual (trigger).

**Talking point mientras corre:** "Vean el grafo en la UI — cada tarea se pone
verde conforme termina. Esto es exactamente la visibilidad que un script
secuencial no les da."

**Deberías ver:** `entrenamiento_y_features` corre el job de Dataproc (puede
tardar varios minutos — real, no simulado), después `evaluar_metricas` lee el
`metrics.json`, y finalmente `puerta_calidad` decide la rama.

**Si `evaluar_metricas` falla:** confirmar que el notebook de la Sesión 6
efectivamente escribió `metrics.json` en la ruta esperada — es la causa #1 de
falla en esta tarea.

### Paso 3 — Confirmar el despliegue condicional (25 min)

Si el AUC pasa el umbral, `desplegar_modelo` debe llamar `POST /reload` al
endpoint de la Sesión 11 — confirmar en los logs de `uvicorn` que la petición
llegó.

**Ejercicio de discusión:** bajar `AUC_MINIMO` a un valor que sepan que va a
fallar, volver a correr, y ver la rama `no_desplegar` activarse — buena forma
de confirmar que la lógica condicional realmente funciona en ambos sentidos.

---

## Bloque 5 — Cierre (2:40–3:00, 20 min)

**Entregable de hoy:** DAG de MLOps corriendo (captura del grafo con las tareas
en verde), conectado al endpoint de la Sesión 11.

**Puente a la Sesión 13:**

> "La próxima sesión es la última — presentan el capstone técnico. Todo lo que
> construyeron desde la Sesión 5 hasta hoy es, literalmente, el esqueleto de
> ese capstone. No están empezando de cero."

---

## Notas de costo GCP

- El DAG dispara un job real de Dataproc cada vez que corre — si el grupo
  experimenta con varios triggers manuales durante la clase, recuérdales que
  cada uno consume tiempo de cluster real, no es gratis "porque es un DAG".
