# Sesión 3 · El archivo debe sobrevivir a tus conclusiones

Gran idea: Conservar origen, versión y lectura permite revisar una decisión sin perder evidencia.

Guion para presentar en vivo. [pausa 3 s] indica silencio deliberado. Los controles se activan por el docente; no hay avance automático.

## 01. El archivo debe sobrevivir a tus conclusiones.

0–4 min. Plantear que el comité pide recalcular una comparación y alguien guardó únicamente el reporte. Preguntar qué hace falta para reconstruirlo. [pausa 3 s] Bronze conserva fuente y contexto, no la verdad validada.

## 02. Una respuesta pequeña puede exigir una lectura grande.

4–9 min. Recuperar el concepto útil del deck publicado. En BigQuery, el modelo bajo demanda depende de bytes facturables; también existen reservas/capacidad. LIMIT limita filas devueltas. No afirmar que todos los modos de BigQuery se cobran igual ni mostrar una tarifa inventada.

## 03. Bronze debe permitirte repetir la lectura.

9–15 min. Alguien ajeno al equipo debe poder reconstruir la entrada. Fuente, versión, ubicación, permisos y consulta son parte de la evidencia. Un CSV que existe sin permiso de uso o definición de filas sigue siendo un riesgo de interpretación.

## 04. Guardar un objeto y definir una tabla son acciones distintas.

15–20 min. La tabla externa describe cómo leer datos que permanecen en GCS. No duplica físicamente todo el archivo al crearse. La lectura sí tiene costos y restricciones; una tabla externa no es una optimización automática. Comparar objeto, tabla y resultado de consulta.

## 05. BigQuery reparte trabajo y reúne resultados.

20–24 min. Diagrama conceptual, no topología física del servicio ni número real de workers. El motor planifica lectura y combinación; una agregación puede requerir intercambio. Separamos cómputo de almacenamiento para elegir dónde guardar y cómo consultar. No enseñar a administrar clústeres en este track.

## 06. ETL y ELT cambian dónde ocurre la transformación.

24–28 min. Explicar que en ELT cargamos para transformar con el motor de destino; ETL puede transformar antes de cargar el destino analítico. No son religiones ni impiden conservar fuente. El curso usa una ruta ELT simplificada: original en GCS y SQL en BigQuery. Preguntar dónde pondrían una validación de datos sensibles antes de compartir.

## 07. Bronze conserva el error para poder explicarlo.

28–32 min. Los errores de esta miniatura son deliberados y ficticios. En Bronze queremos conocer qué llegó. No borrar a mano el cero o la fecha inválida del CSV para que la carga aparente estar limpia. La tabla externa usa STRING para conservarlos; la tipificación y rechazo ocurren en S4.

## 08. Un esquema explícito convierte columnas en un contrato.

32–36 min. Mostrar parte del esquema para legibilidad; la guía y SQL contienen las ocho columnas en orden. En una tabla externa CSV el orden de columnas importa. STRING aquí conserva el crudo; no es la recomendación para Gold. No aplicar este esquema al all_data.csv real cuyo perfilado sigue pendiente.

## 09. El manifiesto documenta una entrega concreta.

36–40 min. El checksum detecta diferencias de bytes, no certifica verdad ni derechos. Distinguir fecha de recepción y observación. El manifiesto del fixture contiene datos de la entrega local, no características del archivo real del Drive. Registrar responsable de preparación y permisos.

## 10. El acceso correcto también forma parte de la arquitectura.

40–45 min. Enlazar arquitectura y gobierno del módulo3. Separar permisos de datos y de ejecutar jobs. No dar roles amplios para saltar un error. La guía ofrece ruta docente; S4 profundiza privacidad, calidad y contexto GDPR/HIPAA sin asumir aplicabilidad jurídica universal.

## 11. HSBC combina fuentes para analizar riesgo.

45–50 min. El caso publicado describe GCS, Dataflow y BigQuery como parte de la solución. Este esquema omite componentes y no reproduce toda la arquitectura. Nuestra lección de trazabilidad es una interpretación pedagógica, no un resultado medido del banco. No prometemos su desempeño ni entrenamos modelos financieros.

## 12. Una tabla nativa cambia dónde queda la copia de trabajo.

50–54 min. En el laboratorio crearemos externa y materializaremos copia nativa para S4. CTAS copia datos, no limpia por sí mismo. Las tablas nativas permiten opciones de organización y optimización que se estudian después. Una externa conserva conexión al objeto, no inmutabilidad automática.

## 13. LIMIT cambia la salida; observa la lectura por separado.

54–58 min. Antes de pulsar, preguntar qué parte cambiará. La miniatura ilustra por qué LIMIT no garantiza reducir bytes, no predice un job exacto. Usar estadísticas del motor para medir. El formato, columnas, organización física y caché afectan lectura.

## 14. Un filtro ayuda cuando el almacenamiento puede aprovecharlo.

58–62 min. Recuperar la analogía del archivero del curso publicado, con el matiz del formato. No prometer pruning de CSV como si fuera Parquet o tabla nativa particionada. Tampoco afirmar que SELECT columnas siempre reduce escaneo en cualquier fuente externa. S4/S5 medirán sobre tablas preparadas.

## 15. El costo empieza a controlarse antes de ejecutar.

62–65 min. En fuentes externas la estimación puede ser incompleta; un cero estimado no garantiza gratis. Bajo demanda, maximum bytes billed acota jobs compatibles. Si la cuenta usa otro modelo, seguir controles docentes. Sin estimación fiable o autorización de costo, no lanzar fuente grande; practicar con fixture y declarar límite.

## 16. Vuelve con bucket, proyecto y ubicación a la vista.

65–75 min. Pausa. Preparar URI del bucket y guía completa. El fixture de16 filas sirve para comprobar el mecanismo; no será evidencia de procesamiento masivo. El docente debe tener fuente grande perfilada y autorizada para la comparación posterior.

## 17. Conserva el CSV y registra dónde quedó.

75–80 min. Usar el bucket de S1 y prefijo bronze. No cambiar caracteres ni eliminar filas del CSV. El nombre tu-bucket es placeholder, usar URI exacta de consola. El manifiesto local incluye checksum y conteos conocidos para comparar. Es material ficticio, no una muestra del Drive.

## 18. Dataset y fuente necesitan ubicaciones compatibles.

80–88 min. Crear dataset en proyecto seleccionado. us-central1 es la región propuesta de los scripts, ajustar conscientemente si el bucket/docente usan otra compatible. IF NOT EXISTS no cambia ubicación de un dataset existente. No crear Silver y Gold vacías para aparentar progreso; se usarán después.

## 19. La URI exacta conecta BigQuery con el objeto.

88–100 min. Este fragmento es la variable que se sustituye dentro del archivo completo, no crea por sí solo la externa. El SQL incluye ASSERT, esquema y DDL de ocho columnas. Revisar permiso para GCS y crear jobs. Si error de parseo, verificar CSV, separador, cabecera y orden; no ignorar filas para que pase.

## 20. El conteo de entrada comprueba la carga conocida.

100–112 min. El archivo contiene16 filas de datos más cabecera. Este conteo no valida calidad: conserva filas inválidas y duplicada. Ejecutar también 03_explorar.sql tras la materialización del script02. El CTAS nativo prepara S4; no representa limpieza ni evita gobernar dos copias.

## 21. Muestra y fuente completa deben dejar evidencias distintas.

112–122 min. No ejecutar all_data de19GB sin esquema, permisos y costo validados. Si el docente ofrece fuente grande preparada, ejecutar consulta acotada y guardar estadísticas. Si aún no está preparada, registrar pendiente o usar evidencia docente rotulada. No inventar velocidad ni extrapolar16 filas.

## 22. Un compañero debe poder encontrar la misma entrada.

122–130 min. Intercambiar manifiestos. El compañero debe localizar la fuente y entender si el resultado corresponde a muestra o universo. Acceso autorizado no significa publicar el bucket. Registrar cierre/retención: conservar capas para siguiente sesión y revisar recursos temporales.

## 23. Tu Bronze conserva la fuente de tu propia pregunta.

130–145 min. Un dataset distinto por equipo. Nunca aplicar las ocho columnas del fixture a otra fuente. El docente debe preparar paquete y SQL de lectura compatibles con el dominio. Registrar perfilado pendiente si falta. El ejecutivo interpreta y verifica; no se le transfiere toda la ingeniería de ingestión.

## 24. Declara qué todavía no promete tu capa Bronze.

145–160 min. Completar con una regla real del dominio: fecha, unidad, duplicado, permiso o cobertura. Intercambiar registro y anotar una mejora. El acceso a datos no autoriza una conclusión. El próximo paso Silver convierte esa incertidumbre en una comprobación explícita.

## 25. Entrega una fuente consultable y un registro de su lectura.

160–170 min. Exigir trazabilidad, no una carpeta con capturas sueltas. Si hubo recuperación01_fixture_bronze.sql, declarar que creó tabla nativa y no demuestra una externa. Revisar vida de objetos/retención del proyecto. No borrar datos que requiere Silver sin respaldo acordado.

## 26. La próxima regla decidirá qué puede compararse.

170–180 min. Cerrar volviendo al archivo original y la posibilidad de corregir una regla. El fixture tiene una copia y dos inválidas bajo las reglas previstas; no anticipar que cualquier archivo real tendrá esa distribución. Pregunta de salida: por qué consultar una fuente no prueba que su contenido sea comparable.
