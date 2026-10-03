# Facilitación — Sesión 12: MLOps con Airflow

> Guion de 3 horas: talking points + lab guiado. Última sesión técnica antes del
> capstone — hoy se conectan todas las piezas de las Sesiones 5-11 en un solo
> sistema automatizado. Dale al grupo el momento de "ver el ciclo completo" que
> se ha ido construyendo sesión por sesión.

## Antes de empezar (facilitador)

Instala Airflow con anticipación en la VM temporal de 4+ GB (recomendado: `e2-standard-2`) (o localmente para la
demo) — `airflow db migrate` la primera vez puede tardar y generar salida
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

Seguir el setup completo de [recursos/airflow/README.md](../../recursos/airflow/README.md): Python 3.11, constraints oficiales, ADC, variables y secreto de recarga. El bucket se configura sin `gs://`; copiar el DAG desde `recursos/airflow/dags/`. La UI usa `localhost:8081` y el API `localhost:8080`.

Antes del trigger, verificar el cluster temporal existente, los dos archivos Python subidos, el corte temporal y la conectividad del worker con el API. Confirmar en la UI que el DAG carga sin errores.

### Paso 2 — Disparar el DAG manualmente (40 min)

Desde la UI de Airflow: activar el DAG y disparar una corrida manual (trigger).

**Talking point mientras corre:** "Vean el grafo en la UI — cada tarea se pone
verde conforme termina. Esto es exactamente la visibilidad que un script
secuencial no les da."

**Deberías ver:** `entrenamiento_y_features` corre el job de Dataproc (puede
tardar varios minutos — real, no simulado), después `evaluar_metricas` lee el
`metrics.json`, y finalmente `puerta_calidad` decide la rama.

**Si `evaluar_metricas` falla:** confirmar que el job de entrenamiento escribió `metrics.json` en la ruta exclusiva del run y que `model_uri` coincide con el candidato.

### Paso 3 — Confirmar el despliegue condicional (25 min)

Si el AUC pasa el umbral, `desplegar_modelo` debe llamar `POST /reload` al
endpoint de la Sesión 11 — confirmar en los logs de `uvicorn` que la petición
llegó.

**Ejercicio de discusión:** subir `auc_min` o `pr_auc_min` por encima de la métrica observada, volver a correr, y ver la rama `no_desplegar` activarse — buena forma
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

## Contrato operativo de esta ruta

Seguir `recursos/airflow/README.md`: entorno Python 3.11 separado, bucket sin gs:// en variables, candidato y metrics.json por run, URI/token en recarga y rechazo HTTP propagado. Trigger por drift requiere reporte revisado y pasa de nuevo por la puerta ROC/PR-AUC. El DAG requiere cluster temporal existente y no lo crea/borra; pausar DAG y apagar VM al terminar.
