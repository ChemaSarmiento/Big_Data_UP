# Caso de apertura — una decisión con consecuencias

Caso hipotético: el monto promedio aumenta tras una campaña. El monitor marca cambio, pero no hay labels recientes. ¿Ya sabemos que el modelo dejó de servir o solo que los datos cambiaron?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

Serving transforma una entrada en una predicción con una versión concreta. Drift de datos es cambio de distribución; concept drift afecta la relación entre entrada y objetivo. PSI observa el primero y no demuestra por sí solo pérdida de calidad predictiva.

---

# Elegir bien exige reconocer el límite

Un API Spark local mantiene consistencia del pipeline, pero tiene inicialización y overhead por petición. Es un prototipo para medir, no una promesa de milisegundos. Un umbral PSI es una señal de investigación; la acción depende de calidad, estacionalidad y métricas con labels.

---

# Laboratorio guiado — preparación y objetivo

Preparar Python 3.11/Java 17, dependencias, ADC, pipeline y muestras de referencia/reciente acotadas. Configurar MODELO, MODELO_ROOT y RELOAD_TOKEN según `recursos/serving/README.md`. El bloque de 90 minutos mide API y drift; no instala desde cero.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — verificar la versión

Arranca el API en loopback y consulta `/health`. Conserva model_uri. Envía una transacción válida y otra con campo obligatorio ausente; registra éxito y rechazo.

---

# Laboratorio · paso 2 — medir frío y caliente

Mide la primera petición y al menos diez posteriores; registra tiempos y entorno. No elimines fallos de la muestra. Explica por qué esta evidencia no basta para un SLA bajo carga.

---

# Laboratorio · paso 3 — comparar distribuciones

Ejecuta `monitor_drift.py` sobre dos muestras con el mismo significado y unidades. Guarda drift.json y gráficos con bins comparables. Comprueba tamaño, nulos y cobertura antes de interpretar PSI.

---

# Laboratorio · paso 4 — investigar antes de actuar

Formula tres causas posibles del cambio. Propón qué labels y métricas permitirían comprobar deterioro. Prueba `/reload` con token/URI autorizados y verifica la nueva versión; un rechazo debe conservar la anterior.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar latencias, versión, reporte y una decisión justificada: seguir observando, corregir dato o pedir candidato nuevo. No convertir un PSI alto automáticamente en “modelo malo”.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

API no arranca: falta variable obligatoria o el modelo no descarga con ADC. Recarga 403: token incorrecto. PSI vacío: muestra sin valores válidos. Latencia constante alta: revisa cómputo y concurrencia, no asumas que todas las peticiones son frías.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 90 minutos: medir carga acotada y diseñar rollback. Comparar métricas etiquetadas por periodo cuando haya labels. No desplegar el prototipo públicamente para el ejercicio.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Laboratorio — iniciar y consultar el API

Python/Java, ADC y dependencias preparados. Configurar `RELOAD_TOKEN` como secreto del entorno antes de arrancar.

```bash
export MODELO=gs://$BUCKET_NAME/modelos/runs/$MODEL_RUN/pipeline
export MODELO_ROOT=gs://$BUCKET_NAME/modelos/runs
uvicorn serve_fraude:app --app-dir recursos/serving --host 127.0.0.1 --port 8080
```

En otra terminal:

```bash
curl -s localhost:8080/health
curl -s -X POST localhost:8080/score -H 'Content-Type: application/json'   -d '{"transaction_id":"t1","timestamp":"2026-03-01T14:00:00Z","amount":12000,"currency":"MXN"}'
```

No incluir tokens en la entrega; registrar respuesta, latencia y model_uri.

---

# Laboratorio — medir cambio y probar recarga

Preparar muestras acotadas según `recursos/serving/README.md`:

```bash
python recursos/serving/monitor_drift.py  \
  --referencia gs://$BUCKET_NAME/modelos/runs/$MODEL_RUN/referencia.parquet  \
  --lote-reciente gs://$BUCKET_NAME/monitoreo/reciente.parquet --salida drift.json
```

La recarga requiere URI del candidato y token; no existe una recarga válida con POST vacío:

```bash
curl -s -X POST localhost:8080/reload -H 'Content-Type: application/json'   -H "X-Reload-Token: $RELOAD_TOKEN" -d "{\"model_uri\":\"$MODELO\"}"
```

Revisar `/health` después; comparar versión ante aceptación y rechazo.

---

# Referencias — qué buscar en cada fuente

- [Selección de modelos y tuning](https://spark.apache.org/docs/3.5.5/ml-tuning.html).
- [El contexto da significado a los datos](https://www.storytellingwithdata.com/blog/2021/1/14/data-doesnt-speak-for-itself).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
