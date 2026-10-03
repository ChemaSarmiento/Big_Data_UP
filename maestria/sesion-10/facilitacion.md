# Facilitación — Streaming: práctica técnica de tres horas

Antes: probar permisos Pub/Sub/GCS, cluster 2.2, scripts cargados, muestra CSV y saldo. Preparar tres terminales: puente, Spark y productor. Cada equipo define STREAM_RUN único; ver `recursos/streaming/README.md` para comandos completos.

| Tiempo | Trabajo | Evidencia |
|---|---|---|
| 0:00–0:15 | Predecir qué ocurre si se repite o retrasa un evento | Hipótesis por equipo |
| 0:15–1:00 | Tiempo de evento, watermark, ACK/checkpoint y límite de unicidad | Infográfico explicado con sus propias palabras |
| 1:00–1:10 | Descanso y verificación de entorno | Cluster listo, saldo revisado |
| 1:10–1:30 | Topic/suscripción + puente + input vacío listo | Primer JSON inmutable |
| 1:30–2:10 | S9 conteo / S10 scoring con candidato versionado | Ventanas o scores y modelo_uri |
| 2:10–2:40 | Reentrega, evento tardío y reinicio con checkpoint | Resultado contra hipótesis |
| 2:40–3:00 | Conclusión, evidencia y limpieza | Cluster borrado, procesos detenidos |

Arrancar Spark y puente antes del productor. Spark debe encontrar el prefijo de entrada: crear un JSON de prueba válido o comenzar el puente antes de iniciar el job. S9 omite modelo; S10 usa el candidato completo de S6 y un STREAM_RUN nuevo. El lab usa `append` para combinar deduplicación y agregación: la consola muestra ventanas cerradas, no cada actualización. Si no hay salida, revisar si avanzó el tiempo de evento para cerrar ventanas. No borrar checkpoints de consultas activas. Si se cambia watermark/consulta, hacer un experimento nuevo y comparar condiciones.

Preguntas de cierre: ¿qué hora agrupa?, ¿qué falla entre escritura y ACK?, ¿qué garantía acota la deduplicación?, ¿qué contribuye a la latencia?
