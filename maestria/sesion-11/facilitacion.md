# Facilitación — Sesión 11: Model serving y monitoreo

> Guion de 3 horas: talking points + lab guiado. Sin cluster de Dataproc hoy — el
> endpoint corre en Spark local, y el monitoreo de drift es un script de Python
> normal. Aprovecha el respiro de infraestructura para profundizar en la parte
> conceptual.

## Antes de empezar (facilitador)

Confirma que tienes acceso al `PipelineModel` guardado en la Sesión 6 y al
Parquet de scores generado en la Sesión 10 (`monitor_drift.py` los necesita a
ambos).

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "Un modelo entrenado que nadie puede consultar es un experimento, no un
> producto. Hoy lo convertimos en algo que un sistema externo puede llamar — y
> le agregamos una forma de saber cuándo dejó de ser confiable."

**Pregunta de apertura:**

> "¿Por qué creen que cargar el modelo en una SparkSession *local*, dentro del
> mismo proceso de la API, en vez de en el cluster de Dataproc, es mejor idea
> para responder una sola petición HTTP?"

(Gancho hacia la discusión de latencia vs. paralelismo.)

**Ejemplo de actualidad:**

> "Los sistemas de scoring de crédito en tiempo real (aprobar o rechazar una
> tarjeta en el checkout) tienen que responder en menos de 200ms — ningún
> cluster completo, por rápido que sea, cumple ese SLA por el overhead de
> coordinación. Por eso el patrón de 'modelo cargado localmente' que van a
> construir hoy es el real."

---

## Bloque 2 — Teoría (0:15–1:00, 45 min)

### Tres patrones de serving (15 min)

Tabla en el pizarrón: batch, online, streaming. Conecta explícito con lo ya
visto: streaming ya lo hicieron (Sesión 10); hoy es online.

### Por qué Spark local para el endpoint (10 min)

Punto de diseño central — dale espacio para que lo discutan antes de
confirmarlo: un cluster completo de Dataproc tiene overhead de coordinación
(JVMs distribuidas, scheduler) que no compensa para una sola petición.

### Drift de datos vs. drift de modelo (10 min)

Distingue con un ejemplo concreto: "el monto promedio sube por inflación" (drift
de datos) vs. "el patrón de fraude cambió y el modelo ya no lo detecta" (drift
de modelo/concept drift) — el PSI de hoy mide el primero, no el segundo.

### PSI: cómo se interpreta (10 min)

Escribe los umbrales en el pizarrón (< 0.1, 0.1-0.25, > 0.25) y pregunta:
**"¿por qué creen que 0.25 y no un número redondo como 0.5?"** (es un estándar
de industria empírico, no una fórmula matemática exacta — vale la pena que
sepan que es una convención, no una ley).

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Lab guiado (1:10–2:40, 90 min)

### Paso 1 — Desplegar el endpoint (35 min)

```bash
pip install fastapi uvicorn pyspark
MODELO=gs://<TU-BUCKET>/modelos/fraude_bank_transactions_pipeline \
  uvicorn serve_fraude:app --host 0.0.0.0 --port 8080
```

```bash
curl -X POST localhost:8080/score -H "Content-Type: application/json" -d '{
  "transaction_id": "t1", "timestamp": "2026-03-01T14:00:00", "amount": 12000, "currency": "MXN"
}'
```

**Deberías ver:** una respuesta JSON con `es_sospechosa_pred` y
`prob_sospechosa`. La primera petición puede tardar varios segundos (Spark
local inicializando) — las siguientes deben ser rápidas.

**Si tarda mucho en cada petición, no solo la primera:** revisar que
`SparkSession.builder.master("local[2]")` no esté compitiendo por recursos con
otro proceso pesado corriendo en la misma máquina.

### Paso 2 — Probar `/reload` y `/health` (15 min)

```bash
curl -X POST localhost:8080/reload
curl localhost:8080/health
```

**Talking point:** "`/reload` es la pieza que la Sesión 12 va a llamar
automáticamente desde el DAG de Airflow — hoy lo prueban a mano para entender
qué hace antes de automatizarlo."

### Paso 3 — Correr `monitor_drift.py` (40 min)

```bash
python monitor_drift.py \
    --referencia gs://<TU-BUCKET>/raw/bank_transactions/bank_transactions.csv \
    --lote_reciente gs://<TU-BUCKET>/streaming/scores \
    --columna amount
```

**Deberías ver:** un PSI impreso con su interpretación ("sin drift relevante",
"vigilar", o "considerar reentrenar").

**Si el PSI sale muy alto sin razón aparente:** revisar que `--lote_reciente`
apunte al Parquet correcto de la Sesión 10, no a una carpeta vacía o parcial —
un lote de muestra muy pequeño puede dar un PSI inestable/engañoso.

**Ejercicio adicional si sobra tiempo:** correr `monitor_drift.py` sobre una
columna distinta (`hora_del_dia`) y comparar el PSI — ¿alguna feature muestra
más drift que otra? Buena discusión de cierre.

---

## Bloque 5 — Cierre (2:40–3:00, 20 min)

**Entregable de hoy:** endpoint respondiendo a `/score` + corrida de
`monitor_drift.py` con su PSI interpretado.

**Puente a la Sesión 12:**

> "Hoy todo lo hicieron a mano — llamar al endpoint, correr el script de drift.
> La próxima sesión automatizamos todo esto en un DAG que decide solo cuándo
> reentrenar y cuándo desplegar."

---

## Notas de costo GCP

- Esta sesión es barata en cómputo de GCP (sin cluster de Dataproc) — buen
  momento para que el grupo revise cuánto crédito lleva consumido del total de
  $300, ya que faltan pocas sesiones para el capstone.
