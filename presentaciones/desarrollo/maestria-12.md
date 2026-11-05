# Caso de apertura — una decisión con consecuencias

Caso hipotético: el job de entrenamiento termina, pero `/reload` falla. El tablero del orquestador sigue verde y el equipo cree que el modelo se actualizó. ¿Qué significa realmente “pipeline exitoso”?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

Un DAG expresa dependencias y estados, no solo una lista de comandos. El éxito de entrenamiento no implica calidad del candidato ni éxito de despliegue. Separar entrenamiento, lectura de métricas, decisión y recarga permite atribuir un fallo al paso que realmente ocurrió.

---

# Elegir bien exige reconocer el límite

Reintentar no debe sobrescribir otro candidato ni ignorar una respuesta fallida. El contrato exige métricas de ese run y URI coincidente. El reporte de drift revisado puede pedir entrenamiento, pero el candidato todavía debe pasar ROC/PR-AUC. Orquestar el modelo no crea por sí solo el cluster.

---

# Laboratorio guiado — preparación y objetivo

Preparación obligatoria fuera de clase: Airflow instalado en entorno separado, DAG importable, ADC, scripts en GCS, variables y token, API saludable. Durante el lab crear/verificar cluster temporal. Sin preparación, esta integración necesita una clínica separada de tres horas.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — validar antes de gastar

Ejecuta `airflow dags list-import-errors` y revisa el DAG en la UI. Confirma bucket sin gs://, fecha de corte y URI del endpoint accesible desde el worker. Mantén pausado el schedule fuera de la práctica.

---

# Laboratorio · paso 2 — seguir un run exclusivo

Dispara una ejecución manual con dataset de muestra. Registra RUN_ID, job, metrics.json y model_uri. Comprueba conteo test y métricas finitas antes de aceptar la lectura.

---

# Laboratorio — ejecuta y comprueba

En el entorno Airflow preparado:
```bash
airflow dags list-import-errors
airflow dags list
airflow dags trigger mlops_fraude_bank_transactions
```
Abrir la UI en puerto 8081. Seguir el run hasta su rama final; no activar un schedule sin infraestructura disponible.

---

# Laboratorio · paso 3 — observar las dos decisiones

Para probar rechazo, sube el umbral por encima de la métrica observada. Verifica `no_desplegar` y que `/health` conserva versión. Para aceptación usa umbrales justificados; registra la URI después de recarga.

---

# Laboratorio · paso 4 — hacer visible una falla

En una ejecución de prueba apunta a un puerto sin API. La tarea de despliegue debe fallar, no quedar verde. Restaura la configuración y registra recuperación. Guarda evidencia y borra cluster al cerrar.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar grafo con estados interpretados, candidato/metricas correspondientes y evidencia de rechazo o fallo de recarga. Tareas skipped por branching no son errores; tareas verdes no prueban calidad si no comprueban contratos.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

Import falla: entorno/proveedor incompatible. Training falla: cluster inexistente, permiso o scripts ausentes. Métricas no coinciden: run equivocado. Reload falla: conectividad, token o URI; no suprimas el error para mostrar éxito.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 2–3 horas: nueva corrida completa, trigger de drift revisado y recuperación. Si se quiere construir DAG, red y entorno desde cero durante clase, añadir una sesión de integración; no comprimir el resto del temario.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Referencias — qué buscar en cada fuente

- [DAGs, dependencias y ejecución](https://airflow.apache.org/docs/apache-airflow/2.11.0/core-concepts/dags.html).
- [Permisos y recursos IAM](https://docs.cloud.google.com/iam/docs/overview).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
