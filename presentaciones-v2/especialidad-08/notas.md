# Notas de la sesión · Comité de decisión: defender el proyecto propio con evidencia

Ensayar accesos y código por motor antes de clase. Solo Especialidad: sin entrenamiento de ML. Guía de 55 min + transferencia de 30 min (excepto S8 comité).

## E08-01 · Hoy el comité decide si tu propuesta está sustentada

0–1 min. Abrir con la tensión, no con la agenda. Proyectar la frase y pedir una respuesta rápida a mano alzada: «¿lo defenderían así ante un comité?». [pausa 3 s] Escuchar dos razones. Los números son reales: se calcularon el 2026-11-19 sobre 6.8 millones de tweets de marzo de 2022 (uso académico). La pregunta de fondo del curso: contar tweets no es medir opinión ni impacto. Hoy cada equipo defiende con SU dataset; el caso de tweets es solo el modelo de cómo se defiende.

## E08-02 · Un dataset distinto por equipo, el mismo estándar

1–3 min. Los tamaños salen del metadata.json del Drive (snapshot de 255 entradas, 19 archivos distintos). Ese inventario NO valida esquema, licencia ni calidad: el docente confirma la asignación y que no haya dos equipos con la misma fuente ni con dos formatos del mismo origen. Insistir: cambia la pregunta de grano, no el rigor. PROFECO ya está cargado en BigQuery (62,530,695 filas en bronze/silver) y puede ser la fuente de un equipo; war_tweets es el modelo del curso.

## E08-03 · Defiende una decisión en siete minutos

2–4 min. Explicar el reloj y los cinco tramos (1-1-3-1-1) con el caso de tweets como ejemplo en la siguiente slide. El cronómetro es manual: lo inicia el cronometrista. Tres minutos de preguntas aparte. Hasta diez equipos caben en la agenda; si hay más, ajustar el formato antes de convocar. Preparación: respaldo local abierto (capturas y CSV) por si falla el acceso a la nube.

## E08-04 · El marco de siete minutos, aplicado al caso de tweets

4–7 min. Recorrer cada tramo con la frase modelo; no la copien, adáptenla a su dominio. Tramo 3 (3 min) es el que decide la nota: una cifra, su denominador y la consulta que la reconstruye. Decisión de ejemplo: vigilar primero energía y sanciones porque son los temas con más tweets en este dato; eso no prueba importancia económica, por eso se pide confirmar con otra fuente antes de actuar. Error típico: gastar cuatro minutos en la arquitectura y dos en la evidencia.

## E08-05 · La misma evidencia sostiene una defensa débil o una fuerte

7–10 min. Resolver la pregunta de apertura. Revelar fila por fila: primero la frase débil, luego por qué se rompe (siempre con un número real), luego la versión sustentada. Cálculos: 137,598 de 6,798,932 = 2.0 %; 2.135 % el 17 y 3.382 % el 23; 1.67 % en inglés y 0.91 % en español; 54.4 % de tweets con 0 likes y 13,928 tweets (0.2 %) con el 60 % de los likes. Pregunta al grupo: ¿cuál de las cuatro frases débiles dijeron en la apertura?

## E08-06 · Cada cifra debe poder recorrerse de vuelta hasta su fuente

10–12 min. Leer de izquierda a derecha: la decisión pide un indicador; el indicador necesita una regla; la regla se aplica a una fuente. Después, del número hacia atrás: 3.382 % = 10,530 / 311,363; esas dos cifras salen de tweets_gold.tema_dia; esa tabla sale de tweets_silver.tweets; esa, de tweets_bronze.entrada; esa, del Parquet de 180 partes que Spark escribió desde war_tweets.txt (22.04 GiB). Si el equipo no puede recorrer su camino, la cifra no se defiende.

## E08-07 · Defender es decir hasta dónde llega la evidencia

12–13 min. Dos columnas: lo que sí sostiene el dato y lo que no. Cada punto sale de un hallazgo medido: ids sin duplicados (6,798,932 distintos), 80,266 tweets de sanciones = 1.2 %, copias idénticas del mismo texto por usuarios distintos (hasta 421 veces), solo 12 días. Pedir a cada equipo que escriba su propia lista de «no puedo afirmar» antes de la defensa; es el criterio de límites de la rúbrica.

## E08-08 · Rúbrica común (1/2): valor, arquitectura y evidencia

13–14 min. La rúbrica es de 100 puntos y la misma para todos los sectores. Mostrar para cada criterio qué se puede observar (no «se siente bien») y qué señal de alerta baja puntos. SQL, calidad y KPIs vale 25 porque es donde se cae la mayoría: cifras sin consulta y conteos que no cuadran entre capas.

## E08-09 · Rúbrica común (2/2): comunicación, IA y reproducibilidad

14–15 min. Comunicación vale 20: títulos que concluyen, ejes desde cero, filtros que no ocultan cobertura (el día parcial se marca). Evaluación crítica de IA vale 10: se pide al menos una afirmación contrastada y una contradicha o sin respaldo. Reproducibilidad vale 5: otra persona puede repetir con el SQL, los bytes y el cierre de recursos.

## E08-10 · Calibra el criterio: la misma evidencia obtiene puntajes distintos

15 min. Ejercicio de calibración: dos defensas hipotéticas sobre el mismo dato. La A dice «energía subió: 137,598 tweets»; la B dice «2.0 % de los tweets; 3.4 % el 23 de marzo en inglés; día parcial señalado; límites explícitos». Los puntajes (29 y 83) son ilustrativos para calibrar al comité, no la evaluación de ningún equipo. Pedir al comité que justifique un punto de diferencia en SQL, calidad y KPIs.

## E08-11 · Primer bloque de defensas

15–65 min. Hasta cinco equipos, siete minutos de defensa y tres de preguntas. Roles rotativos: cronometrista, moderador, registrador de la hoja del comité y relator de preguntas. Cada integrante del comité anota una pregunta y una evidencia por equipo; la rúbrica es la misma aunque cambie el sector. Si falla el acceso a la nube, se defiende desde el respaldo local y se dice en el tramo de límites.

## E08-12 · El comité registra una pregunta, una evidencia y un veredicto

15–65 min, durante los bloques. Mostrar la hoja con el ejemplo del modelo: el comité pregunta por el denominador, el equipo responde con 311,363 tweets del día en inglés, y el veredicto es «sustentada con límites». Insistir: la pregunta debe poder responderse con una consulta o con un dato, no con una opinión. El puntaje se asigna al final de cada defensa con la rúbrica.

## E08-13 · Pausa y rotación del comité

65–75 min. Pausa real de diez minutos. Rotar los roles del comité. Los equipos del segundo bloque comprueban que su respaldo o sus enlaces abren. No se instala infraestructura nueva.

## E08-14 · Segundo bloque: mismo formato, misma rúbrica

75–125 min. Hasta cinco equipos más. Misma estructura de siete minutos y tres de preguntas. El comité rotó roles; quien defendió en el primer bloque ahora registra. Al final del bloque, cada equipo anota en una fila la cifra de otro equipo que quiere auditar en la siguiente fase.

## E08-15 · La arquitectura debe distinguir lo ejecutado de lo propuesto

125–132 min. Mostrar qué se ejecutó de verdad el 2026-11-19: carga del Parquet a Bronze (6,798,932 filas), Silver en SQL (2.28 GiB) y en PySpark (mismo resultado: 6,798,932 filas y 6,798,932 ids), Gold (216 filas). Data Studio y Vertex AI son las herramientas de las sesiones 6 y 7 en el laboratorio de cada equipo: no las ensayó el docente. Pedir a cada equipo que marque en su diagrama qué ejecutó, qué preparó el docente y qué es propuesta.

## E08-16 · El KPI debe sobrevivir a una pregunta de grano y de denominador

132–140 min. La gráfica usa pct_del_dia (tweets del tema ÷ tweets del día en inglés), no el conteo. Con conteos, el 17 de marzo (10,167 tweets) parecería el pico; con porcentaje, el pico es el 23 (3.382 %) y el 24 (3.177 %). El 16 de marzo tiene solo 134,871 tweets (el día completo ronda 500–780 mil): está rayado y no debe compararse. Las tres preguntas de la derecha son las que hace el comité a cualquier KPI.

## E08-17 · Reconstruye una cifra con SQL antes de aceptarla

140–147 min. Consulta de control real: filtra por la partición fecha y por idioma, así que lee solo ~63 MB de texto del día (no los 2.45 GB de la tabla). Resultado real del 2026-11-19: 311,363 · 10,530 · 3.382, idéntico a Gold. Esto prueba que la tabla Gold se reproduce desde Silver con la misma regla; NO prueba que la regla de palabras clave mida el tema. Archivo completo con tres bloques (cifra de Gold, reconstrucción, conciliación): s08_control_cifra.sql.

## E08-18 · La IA no sustituye tu responsabilidad: audita cada frase

147–152 min. Borrador de ejemplo escrito por el docente (no atribuido a un modelo real). Tres frases, tres veredictos: la primera se contradice con el dato (2.135 % a 3.382 % es 1.58 veces, no el doble, y además mide palabras, no preocupación); la segunda se reproduce con la consulta anterior; la tercera no tiene respaldo porque el dato no contiene causas. Pedir que cada equipo haga lo mismo con las frases de su memo y que lleve el veredicto a la hoja de auditoría.

## E08-19 · Rastrea una cifra de otro equipo hasta su fuente

152–160 min (con la auditoría cruzada, 30 min en total). Cada equipo audita una cifra de otro: pide la tabla y el SQL, no una captura; reconstruye desde la capa anterior; concilia conteos entre capas (en el modelo: 6,798,932 en Silver y 6,798,932 como base de Gold); y pregunta denominador, grano y límites. Un veredicto de «reproducida» exige haber ejecutado la consulta; «no reproducida» o «sin evidencia» son resultados válidos y no bajan la nota de quien audita.

## E08-20 · Registra la auditoría en una sola fila

160–165 min (dentro de la auditoría cruzada). Una fila por cifra auditada en s08_auditoria.csv. El ejemplo es la auditoría del modelo: veredicto «reproducida» porque se ejecutó el SQL de control y salió 311,363 / 10,530 / 3.382. El campo «pendiente» es obligatorio y no puede estar vacío: aunque la cifra se reproduzca, siempre queda un límite (aquí, la precisión de las palabras clave sin medir).

## E08-21 · Siete sesiones, siete herramientas, una cadena de evidencia

155–162 min. Recorrer el resumen como la cadena de evidencia que cada equipo ya tiene en su paquete: de la sesión 1 (ambiente) a la 7 (IA con evidencia). Una herramienta por sesión, tal como se practicó en cada laboratorio. Dataform se menciona como idea para versionar y programar el SQL de Gold; no se practicó. Pedir que cada equipo marque cuál de las siete piezas es la más débil de su paquete.

## E08-22 · Entrega el paquete que otra persona pueda auditar

162–170 min. La entrega es un paquete, no una presentación: ocho piezas. Cada una responde una pregunta que el comité hizo hoy. Se entregan agregados y enlaces autorizados, no credenciales ni datos crudos sensibles; en el caso de tweets el dato se deja como está (uso académico) y eso se declara en los límites. Plantilla: entregable.md.

## E08-23 · Cierra lo que puede seguir costando

170–175 min. Cerrar la página no detiene recursos en la nube. Revisar en la consola qué dejó cada equipo en SU proyecto. Una alerta de presupuesto avisa pero no frena el gasto. No borrar el proyecto ni los datasets tweets_* del docente. Los precios cambian: verificar en la consola o en la página de precios vigente, no en esta slide. El estado de batches de Dataproc se puede listar con gcloud dataproc batches list --region=us-east1.

## E08-24 · ¿Qué evidencia adicional cambiaría tu decisión?

175–180 min. Cierre con la pregunta del curso: qué dato nuevo haría cambiar la recomendación. Para el modelo de tweets: más meses, medir la precisión de las palabras clave con una muestra etiquetada a mano, datos de mercado (precios de combustible, vuelos) y separar las copias idénticas. Cada equipo dice una evidencia que cambiaría SU decisión. Retroalimentación de 10 min: una cosa que repetirías y una que cambiarías.

## Fuentes

- [Cole Nussbaumer Knaflic · el mensaje](https://www.storytellingwithdata.com/blog/2017/3/22/so-what)
- [Duarte · Resonate](https://www.duarte.com/resources/books/resonate/)
- [BigQuery · estimar y controlar costos](https://docs.cloud.google.com/bigquery/docs/best-practices-costs)
