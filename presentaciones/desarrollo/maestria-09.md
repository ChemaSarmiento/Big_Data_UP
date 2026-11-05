# Caso de apertura — una decisión con consecuencias

Caso hipotético: una transacción llega dos veces y otra llega tarde. El tablero cuenta actividad por minuto. Un resultado inmediato puede cambiar después; ¿cuándo lo consideramos final?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

Tiempo de evento indica cuándo ocurrió la transacción; tiempo de procesamiento, cuándo se observa. Watermark expresa tolerancia respecto al mayor tiempo de evento visto. Una ventana en append se publica al finalizar: esperar sin eventos de tiempo posterior puede no cerrarla.

---

# Elegir bien exige reconocer el límite

El puente confirma después de persistir. Una falla intermedia permite reentrega; por eso se prueba recuperación y duplicación. La deduplicación tiene horizonte limitado. Cada checkpoint pertenece a una consulta y su configuración: compartirlo entre conteo y scoring mezcla estados incompatibles.

---

# Predice el resultado antes de comprobarlo

No llegan eventos nuevos. ¿Avanza por sí solo el watermark de evento?

<div class="knowledge-check">
<button type="button" data-correct="false">Sí, cada segundo</button>
<button type="button" data-correct="true">No necesariamente</button>
<button type="button" data-correct="false">Solo si aumenta el número de workers</button>
<p class="check-feedback" role="status" hidden data-explanation="El watermark de este ejercicio depende del máximo tiempo de evento observado. El reloj de pared no reemplaza ese avance."></p>
</div>

---

# Laboratorio guiado — preparación y objetivo

Seguir `recursos/streaming/README.md`: topic/suscripción estándar, scripts subidos y tres terminales. Verificar un primer JSON antes de iniciar Spark. Objetivo: contar por ventana sin modelo.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — seguir un evento

Registra ID y timestamp de una fila. Recorre productor → Pub/Sub → puente → objeto JSON → Spark. Comprueba que el label no viaja; no está disponible al predecir.

---

# Laboratorio · paso 2 — ejecutar el consumidor

Usa el comando S9 conteo del README con RUN_ID exclusivo. Guarda entrada y checkpoint asociados. Limita replay a 1200 eventos y 180 segundos por proceso.

---

# Laboratorio · paso 3 — probar repetición y tardanza

Envía un ID repetido y luego eventos con tiempos posteriores para avanzar el watermark. Introduce un evento fuera del horizonte. Contrasta los resultados con la hipótesis y el estado observado; no exijas emisión de ventanas que aún no terminaron.

---

# Laboratorio · paso 4 — probar continuidad

Detén el consumidor ordenadamente y reinicia con el mismo checkpoint y consulta. Verifica continuidad del conteo.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar evidencia de flujo, duplicado, tardanza y reinicio, con latencia observada. Un conteo correcto de una ventana finalizada vale más que una consola que solo muestra mensajes.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

GCS no tiene entrada: verifica persistencia antes del job. No sale una ventana: revisa avance de tiempo de evento. El modelo no transforma: revisa pipeline completo y tipos. Duplicados reaparecen: investiga horizonte y reinicio; no declares unicidad histórica.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 60–90 minutos: falla controlada antes del ACK y compacción de archivos pequeños. S9 y S10 se mantienen en sesiones distintas; no juntar ingesta, estado, scoring y recuperación en un solo laboratorio.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Laboratorio — preparar la entrada durable

Variables `PROJECT_ID`, `BUCKET_NAME` y `STREAM_RUN` ya verificadas. Topic y suscripción preparados; tres terminales independientes.

```bash
python recursos/streaming/pubsub_to_gcs.py --project "$PROJECT_ID"  \
  --bucket "$BUCKET_NAME" --prefix "streaming/$STREAM_RUN/entrada" --seconds 180
```

En otra terminal, iniciar el replay acotado:

```bash
python recursos/streaming/producer_transacciones_stream.py --project "$PROJECT_ID"  \
  --csv bank_transactions.csv --tasa 20 --max-events 1200
```

Verificar el primer objeto JSON antes de lanzar el consumidor. No esperar a que el replay termine para iniciar Spark.

---

# Laboratorio — lanzar el consumidor y guardar evidencia

```bash
gcloud dataproc jobs submit pyspark gs://$BUCKET_NAME/scripts/07a_streaming_conteo.py  \
  --cluster=curso-cluster --region=us-central1  \
  --py-files=gs://$BUCKET_NAME/scripts/stream_common.py --  \
  --input gs://$BUCKET_NAME/streaming/$STREAM_RUN/entrada  \
  --checkpoint gs://$BUCKET_NAME/streaming/$STREAM_RUN/checkpoints/conteo --seconds 180
```

Las ventanas append necesitan avance del tiempo de evento para finalizar. Conservar salida y evidencia de una ventana cerrada.

---

# Referencias — qué buscar en cada fuente

- [Tiempo de evento, estado y recuperación](https://archive.apache.org/dist/spark/docs/3.5.3/structured-streaming-programming-guide.html).
- [Reentrega y confirmación Pub/Sub](https://docs.cloud.google.com/pubsub/docs/subscribe-best-practices).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
