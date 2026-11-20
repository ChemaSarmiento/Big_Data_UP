# Sesión 3 · Del JSON a una tabla: así empieza Medallion

Gran idea: Un archivo se vuelve consultable al convertirlo en tabla; Bronze lo guarda tal como llegó y decide cuánto costará leerlo.

Guion para presentar en vivo. [pausa 3 s] indica silencio deliberado. Los controles se activan con clic o con las flechas; no hay avance automático.

## 01. Del JSON a una tabla

0–3 min. Abrir con una pregunta: ¿cómo se convierte un archivo de 22 GiB en algo que se pueda consultar con SQL? Hoy empieza el hilo del curso: un solo conjunto de datos, los tweets sobre la guerra en Ucrania, que cada alumno copia a su propio proyecto y transforma en tres capas (Bronze, Silver y Gold). Hoy solo se construye la primera. [pausa 3 s] Aclarar que los datos se usan tal como están, con fines académicos.

## 02. Un tweet son 98 caracteres de texto dentro de 2,410 de JSON.

3–7 min. A la izquierda, el tweet como lo ve una persona; a la derecha, como llega al sistema. Primer clic: la barra. El texto ocupa 98 caracteres de una línea de 2,410; lo demás son metadatos: fecha, métricas, la cuenta autora con sus 23 campos. Segundo clic: definir JSON. Es un formato de texto donde cada dato lleva su nombre; los corchetes y llaves permiten anidar. Pregunta al grupo: ¿qué dato de la línea te serviría para contar tweets por día? [pausa 3 s] La fecha, y está escondida dentro del texto.

## 03. Un archivo no responde preguntas: una tabla sí.

7–10 min. Comparar lo que puede hacer una persona o un programa con cada forma. El archivo es una lista de textos: cada línea trae todo junto y no tiene columnas. Una tabla organiza lo mismo en filas (un tweet por fila) y columnas (un dato por columna, con su tipo). SQL solo habla con tablas. Primer clic: la tabla con la fila real del tweet de Skift. Segundo clic: el hilo de las próximas sesiones. Aclarar que filas, columnas y tipos se practican en la sesión 2; aquí basta la idea.

## 04. El hilo del curso: ¿qué temas de la guerra vale la pena vigilar?

10–15 min. Presentar el hilo que acompaña el resto del curso: un comité quiere decidir qué temas satélite de la guerra vale la pena vigilar. El archivo trae 6,798,932 tweets de doce días y no incluye retweets, así que cada tweet es una publicación propia. Clic: la advertencia. Un conteo de tweets depende del idioma, de quién publica y de cuántos días cubre el archivo; no equivale a la opinión de un país ni al efecto en la economía. Esa advertencia vuelve al final de cada sesión. Cierre de la apertura: hoy no se contesta la pregunta; se prepara el terreno.

## 05. Medallion: tres capas, cada una con una promesa.

15–19 min. Definir Medallion con una frase por capa. Bronze guarda lo que llegó. Silver lo ordena en columnas con tipo y aplica reglas de calidad escritas. Gold calcula los indicadores que usa quien decide. Primer clic: Silver. Segundo clic: Gold. No es un servicio de Google Cloud ni exige tres tecnologías distintas: en este curso son tres grupos de tablas en BigQuery. La regla que se repite en todo el curso: una capa nunca modifica a la anterior; si cambia una regla, se vuelve a construir hacia adelante. Hoy solo se construye Bronze; Silver es la sesión 4 y Gold la 5.

## 06. Un solo tweet recorre las tres capas.

19–25 min. El mismo tweet de Skift en las tres capas. Bronze: una sola celda con el JSON completo. Primer clic, Silver: la misma información en columnas con tipo; el id es un número, la fecha una fecha, los seguidores un entero. Segundo clic, Gold: el tweet desaparece como fila y pasa a ser una cuenta: suma uno en energía (menciona «fuel») y uno en aviación (menciona «airline») dentro del 27 de marzo en inglés, donde 6,666 de 318,791 tweets mencionan energía, 2.091 %. Detalle importante: un tweet puede contar en varios temas. Cada capa responde a una pregunta distinta: qué llegó, qué podemos comparar, qué pide la decisión.

## 07. Bronze guarda el original, aunque tenga defectos.

25–28 min. Esto es Bronze: la tabla que contiene lo que llegó, en una sola columna llamada value. No es una tabla fea; es una tabla honesta. Tres filas del resultado, abreviadas. Insistir en lo que no tiene: tipos (la fecha es texto), limpieza (entran duplicados y textos repetidos) y filtros. Es a propósito: si decides mañana excluir las respuestas, o cambiar cómo se lee la fecha, puedes volver a calcular desde el original. Analogía: la factura original se guarda aunque ya la hayas registrado en la contabilidad.

## 08. Cargar es copiar cada línea a una celda, sin cambiarla.

28–32 min. Cómo se convierte un archivo de líneas JSON en una tabla de BigQuery sin transformar nada. Se usa la herramienta de cargar CSV con un truco: se declara un separador de columnas que nunca aparece en el texto (la letra þ) y se desactivan las comillas. Entonces cada línea completa cae en una sola columna llamada value. Primer clic: el comando. Segundo clic: las tres razones. Tercer clic: la prueba. Se probó con 2,500 líneas reales y las 2,500 filas llegaron con 2,500 ids distintos. Definir delimitador (el carácter que separa columnas) y comillas (las que encierran un texto que contiene separadores). La carga en sí no se factura como consulta.

## 09. El archivo vive en Cloud Storage; la tabla, en BigQuery.

32–35 min. El camino del archivo: Drive, Cloud Storage, BigQuery. El cuaderno de Colab del curso copia el archivo de Drive a tu bucket; la carga lo pasa a una tabla. Definir bucket (contenedor con nombre único en todo el mundo), objeto (el archivo) y URI gs:// (su dirección). Almacenar el archivo y almacenar la tabla son dos cobros distintos: Cloud Storage cobra por GiB y mes según la clase de almacenamiento; BigQuery cobra por GiB y mes de la tabla y por los bytes que cada consulta lee. Ubicación: usa US para ambos para que la carga no cruce regiones. Todo vive en tu proyecto.

## 10. ELT: primero cargas el original, después transformas dentro.

35–38 min. ETL (extraer, transformar, cargar) transforma antes de que los datos lleguen a la base: lo que no pasó por la regla se pierde. ELT (extraer, cargar, transformar) carga primero el original y transforma después, con el motor de la propia base. BigQuery está pensado para ELT: calcula sobre tablas enormes y cobra por lo que lee, así que conviene conservar el original en Bronze y construir encima. Con el tweet de Skift: en ETL llegaría ya convertido en fila; en ELT llega como texto y se convierte en la capa siguiente. Primer clic: ELT. Segundo clic: la consecuencia.

## 11. Tres formas de guardar los mismos tweets: JSON, CSV y Parquet.

38–40 min. Los tres formatos que verás en cualquier proyecto de datos. JSON Lines: un JSON por línea, flexible pero repite los nombres de campo en cada línea. CSV: plano y universal, pero un tweet con un autor anidado no cabe sin aplanarlo. Parquet: guarda por columnas y comprime; si una consulta pide solo dos columnas, no lee las demás. El mismo contenido de tweets pesa 22.04 GiB como JSON y 5.78 GiB como Parquet. Pregunta al grupo: si Parquet pesa casi cuatro veces menos, ¿también cuesta cuatro veces menos consultarlo en BigQuery? [pausa 3 s] La siguiente slide lo responde.

## 12. El tamaño en disco no es lo que te cobran por consultar.

40–43 min. Cuatro barras para el mismo contenido. JSON en Storage: 22.04 GiB. Parquet: 5.78 GiB, casi cuatro veces menos. Pero al cargarlo, BigQuery guarda y factura por bytes lógicos, sin comprimir: la tabla Bronze ocupa 22.04 GiB lógicos, y una consulta que lee la columna value lee 23,670,340,066 bytes. Resultado: la compresión ahorra espacio y transferencia, no consulta. Lo que sí baja la factura es leer menos columnas, y para eso sirve Silver. Aviso de unidades: GiB es 1024³ bytes; el estimador habla de bytes y GB. 23.67 GB y 22.05 GiB son la misma cantidad.

## 13. Tabla externa o nativa: dónde viven los bytes.

43–45 min. Dos formas de que BigQuery vea un archivo. Externa: la tabla apunta al archivo que sigue en Cloud Storage; no ocupa almacenamiento de BigQuery, pero cada consulta lee el archivo. Nativa: cargas una copia dentro de BigQuery; permite particiones y clustering. Medido con este archivo: las consultas sobre la tabla externa de Parquet pidieron 16.8 y 21 GB; la nativa pidió 23.67 GB al leer value. Ninguna de las dos resuelve el costo si lees la misma columna entera: la mejora llega en Silver. En el laboratorio usas la nativa, que es la que se consulta muchas veces.

## 14. Spark reparte el trabajo entre varias máquinas.

45–48 min. Spark es un motor para repartir un trabajo grande entre varias máquinas. Un coordinador (driver) divide el archivo en pedazos (particiones), manda cada pedazo a un trabajador (ejecutor) y junta los resultados. Primer clic: los pedazos. Segundo clic: los ejecutores. Tercero: el resultado. Cuarto: cuándo conviene. Arrancar y coordinar cuesta tiempo, así que para un trabajo pequeño una sola consulta SQL es más rápida. Anclaje real: el Parquet de 5.78 GiB se guarda en muchos archivos precisamente para que se puedan repartir.

## 15. PySpark: un plan que no corre hasta que pides un resultado.

48–50 min. El script del laboratorio, línea por línea. PySpark es Spark controlado con Python. Spark es perezoso: leer el archivo solo apunta el plan, y nada ocurre hasta una acción como escribir o contar. Eso le permite optimizar todo el plan antes de repartirlo. Las líneas en verde son transformaciones; las rojas, acciones. Este mismo método de leer el archivo como texto y guardarlo en Parquet es como se generó el Parquet del curso con una sola columna value. Clic: la comprobación esperada. Este script no se ensayó tal cual; el patrón de envío sí se ensayó con otro lote de Spark.

## 16. BigQuery cobra por bytes leídos, no por filas devueltas.

50–56 min. Elegir una consulta y mirar dos cifras: la estimación que muestra el editor antes de ejecutar y lo que pasó al ejecutar. 1) COUNT(*): 0 bytes, usa metadatos. 2) LIMIT 1: la estimación sigue siendo 23.67 GB; LIMIT limita lo que ves, no lo que se lee. 3) JSON_VALUE de un campo: lee toda la columna value; es el costo de construir Silver. 4) TABLESAMPLE: la estimación decía 66.9 MB, pero al ejecutar con un tope de 200 MB falló pidiendo 23.67 GB. Moraleja: BigQuery cobra por bytes leídos de las columnas que nombras; usa dry-run y tope, y no te fíes de una sola estimación. El primer TiB de consultas de cada mes es gratuito.

## 17. Dataproc Serverless: Spark sin administrar un clúster.

60–63 min. Cómo se envía el trabajo de Spark sin administrar máquinas. Dataproc Serverless crea los recursos al enviar el lote y los apaga al terminar; tú pagas por lo que usa mientras corre. Primer clic: el parámetro obligatorio --deps-bucket, que se descubrió al ensayar. Segundo clic: tiempos del ensayo con otro lote (Silver, hasta 4 ejecutores): unos 8 minutos, con 0 clústeres activos al terminar. Esos 8 minutos incluyen el arranque, escribir y dos conteos; no se pueden comparar con una consulta SQL de segundos. La región debe ser de Estados Unidos y la misma en todos tus lotes.

## 18. Estima antes de ejecutar y pon un tope: BigQuery te dice cuánto necesitaba.

56–60 min. Dos protecciones, una gratuita y otra de seguridad. Dry run calcula los bytes que leería la consulta sin ejecutarla. El tope (maximum_bytes_billed) hace que la consulta falle antes de cobrar si necesitara más. Aquí, la consulta con TABLESAMPLE estimaba 66.9 MB pero necesitaba 23,670,554,624 bytes: sin el tope, habría leído toda la columna. Es un error útil: te dice cuánto necesitaba. En el laboratorio lo reproduces. Una buena costumbre: en consultas exploratorias, siempre con tope.

## 19. Repetir una carga no debe duplicar Bronze.

63–67 min. Idempotencia es que repetir una operación deje el mismo resultado. Cargar con --replace reescribe la tabla completa: si repites el comando, la tabla sigue con 6,798,932 filas. Cargar sin --replace añade: dos cargas del mismo archivo dejan 13,597,864 filas, y nada avisa, porque cada fila sigue siendo válida. La cifra de la tercera barra es una suma, no una medición. Moraleja: decide siempre si una carga reemplaza o añade, y comprueba el conteo después, como en el laboratorio.

## 20. Antes de cargar, anota el manifiesto del archivo.

67–70 min. El manifiesto es la ficha de identidad de lo que cargas: nombre, formato, tamaño, huella, filas y periodo. La huella md5 es un resumen del contenido: si dos archivos tienen la misma, son idénticos. Por eso tu copia debe dar el mismo tamaño y la misma huella que el archivo de referencia; la generación y la clase de almacenamiento sí cambian. Un Bronze sin manifiesto no se puede repetir ni auditar. Se anotan los datos en el laboratorio, paso 2.

## 21. Pausa.

70–80 min. Pausa real. Quien tenga el Colab de copia corriendo puede dejarlo en otra pestaña mientras descansa; la copia de 22 GiB tarda. Al volver, comprobar que el proyecto correcto aparece seleccionado.

## 22. Laboratorio: construye tu Bronze en 6 pasos.

80–150 min. Seis pasos, 70 minutos, cada uno con dónde hacerlo, el código completo, la salida esperada, la comprobación y el error más frecuente en la guía. Todo ocurre en tu propio proyecto. Los pasos 1 y 6 son los más largos y los que no se ensayaron de principio a fin: la copia de Drive depende del cuaderno de Colab y de tu cuenta, y el lote de Spark puede tardar varios minutos. Si algo falla, anota el mensaje exacto: es parte del aprendizaje. No avances al paso siguiente sin cumplir la comprobación del anterior.

## 23. Para repetir por tu cuenta.

150–165 min. Cuatro ejercicios individuales para consolidar, sin entrega. El primero entrena la intuición del costo. El segundo comprueba la idempotencia. El tercero usa el mismo método de carga con un archivo diminuto; es más barato para experimentar y se borra al terminar. El cuarto es una pregunta de diseño: si el archivo se actualiza, ¿reemplazas o añades, y cómo evitas duplicar? No hay respuesta única; lo importante es poder defenderla con el conteo.

## 24. Con un Bronze afirmas lo que llegó, no lo que significa.

165–180 min. Cierre honesto con dos columnas. A la izquierda, lo que Bronze demuestra: las filas que llegaron, el tamaño, que tu copia es igual al original y que cada línea trae 29 campos. A la derecha, lo que todavía no se puede decir: conteos por idioma o por tema necesitan columnas con tipo, que llegan en Silver; la representatividad y la independencia de las voces dependen de cómo se extrajo el archivo. Lo que sigue: en la sesión 4 se convierte este JSON en tablas con columnas con tipo y reglas de calidad. Cierre: Bronze no responde preguntas de negocio; las hace posibles.
