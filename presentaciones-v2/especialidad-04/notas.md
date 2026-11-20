# Sesión 4 · Silver: tablas con significado

Gran idea: Silver convierte el JSON crudo en tablas con tipo, con una fila que significa una sola cosa y con reglas de calidad escritas.

Guion para presentar en vivo. [pausa 3 s] indica silencio deliberado. Los controles se activan con clic o con las flechas; no hay avance automático.

## 01. Silver: tablas con significado

0–3 min. Hoy salen tres tablas de un mismo archivo, y las tres cifras son correctas. Pregunta al grupo: ¿cómo puede el mismo archivo dar 6.8 millones de filas en una tabla, 1.9 millones en otra y 3.3 millones en una tercera? [pausa 3 s] Sin dar la respuesta: al terminar la sesión la darán ellos. La idea que recorre la clase es el grano: qué significa una fila.

## 02. Bronze guarda todo, pero no responde ninguna pregunta

3–8 min. Repaso rápido de la sesión 3: Bronze es el archivo tal como llegó, un tweet por fila dentro de una sola columna de texto llamada value. A la izquierda un fragmento real del primer registro (la línea completa mide 2,411 caracteres). A la derecha, el error real al pedir la columna idioma: no existe. Pregunta al grupo: ¿qué hay que hacer para poder filtrar por idioma? [pausa 3 s] Respuesta: abrir el texto, tomar el dato de su camino y guardarlo como columna con su tipo. Eso es Silver.

## 03. Silver promete cuatro cosas

8–15 min. Silver no es una limpieza mágica: es un contrato con cuatro promesas. Ir de una en una con clic. Para la primera, mostrar en voz alta que «100» va antes que «9» cuando son texto. En la segunda, adelantar que hoy construimos tres tablas con tres significados de fila. En la tercera, aclarar que una regla puede marcar sin borrar. La cuarta explica por qué guardamos Bronze: si cambia una regla, se recalcula. A la derecha, tres cifras medidas: 1 columna en Bronze y 18 en Silver; 22.04 GiB frente a 2.28 GiB; mismas filas.

## 04. JSON_VALUE sigue el camino hasta el dato

15–18 min. Primera herramienta: JSON_VALUE(value, camino). Leer la tabla de izquierda a derecha con el mismo tweet de la diapositiva anterior: el camino, lo que hay en ese lugar y la columna que queda. Pregunta al grupo: ¿por qué user.username lleva un punto más? [pausa 3 s] Porque user es un objeto dentro del tweet. Error típico: escribir mal el camino; BigQuery no avisa, devuelve NULL. Por eso al final se revisan los NULL.

## 05. SAFE_CAST convierte sin romper

18–21 min. SAFE_CAST es la segunda herramienta: convierte el texto al tipo correcto y, si no puede, deja NULL en vez de romper. Mostrar los tres casos reales del panel (consulta sin costo, 0 bytes). A la derecha, por qué importa el tipo: el mismo conjunto de valores ordena distinto como texto que como número. Dato real de esta tabla: ningún NULL en tweet_id ni en fecha_hora, y eso también es información: el archivo trae esos campos completos. Error típico: usar CAST, que sí se detiene con el primer valor inválido.

## 06. El script de Silver se lee de arriba abajo

21–24 min. Leer el script completo es más sencillo de lo que parece: una consulta SELECT cuyos resultados se guardan como tabla. Mostrar una versión abreviada de cinco columnas más el arreglo de hashtags; el archivo real, 20_silver_tweets.sql, tiene 18 columnas. Primera aparición de UNNEST y de arreglo: una celda con varios valores, por ejemplo [ukraine, putin]. Aquí solo se baja a minúsculas; la tabla hashtags lo usará para crear filas. Costo: una lectura completa de Bronze, 23.67 GB de referencia; se ejecuta una vez.

## 07. De 29 campos a 18 columnas: se queda lo que usarás

24–27 min. Dos ideas. Izquierda: el tamaño. Una lectura de toda la tabla Silver factura 2.45 GB frente a 23.67 GB de Bronze, casi diez veces menos, porque no guarda campos que no usaremos y porque número y fecha ocupan menos que su versión en texto. Derecha: el mismo tweet que vimos como JSON, ahora una fila con columnas tipadas (se muestran 12 de las 18). Pregunta al grupo: ¿qué dato del JSON original se perdió? [pausa 3 s] Se perdieron los campos que decidimos no usar; siguen en Bronze.

## 08. Una fila debe significar una sola cosa: el grano

27–30 min. El grano es la pregunta «¿qué significa una fila?». Tres tablas, tres granos, tres conteos; ninguno está mal. Volver a la pregunta de la portada: 6.8 millones son tweets, 1.9 millones son autores, 3.3 millones son pares tweet-hashtag. Con el clic, un caso concreto: el tweet de AFP #UPDATE sobre Macron tiene tres hashtags (update, macron, ukraine): una fila en tweets, una fila de AFP en autores y tres filas en hashtags. Error típico: sumar filas de tablas con grano distinto.

## 09. ROW_NUMBER numera las filas dentro de cada autor

30–33 min. Problema: un autor aparece en muchas filas y sus seguidores cambian con el tiempo (skift: 10 tweets y 8 cifras distintas de seguidores). Para una tabla de autores necesitamos una sola fila por autor. ROW_NUMBER numera filas; OVER (PARTITION BY ... ORDER BY ...) define cómo: reiniciar para cada autor, el más reciente primero. La fila con orden = 1 es la que se queda. Panel real con 10 filas de skift (se muestran 5). Pregunta al grupo: ¿qué pasaría con ORDER BY fecha_hora sin DESC? [pausa 3 s] Nos quedaríamos con el dato más antiguo.

## 10. Un CTE le pone nombre a un paso para leer el resto

33–36 min. WITH define un CTE (expresión de tabla común): un paso con nombre que luego usamos como si fuera una tabla. No agrega capacidad; agrega legibilidad. Leer el script de arriba hacia abajo. Además de ROW_NUMBER usamos COUNT(*) OVER (PARTITION BY usuario) para conservar cuántos tweets tenía el autor en el archivo. Resultado: skift queda en una sola fila con 10 tweets. La tabla completa tiene 1,872,074 autores y la suma de tweets_en_archivo vuelve a dar 6,798,932: es el cuadre que revisaremos. Costo de referencia: 280 MB.

## 11. Un CTE también sirve para resumir un resumen

36–39 min. Segundo uso del CTE: primero un GROUP BY (tweets por autor) y encima otro GROUP BY (autores por tramo). Sin el nombre del paso intermedio habría que anidar consultas dentro de consultas. Resultado real: 1,091,593 autores publicaron un solo tweet; 46,581 autores publicaron más de 20 y entre todos suman 2,368,524 tweets, el 34.8 % del archivo. Pregunta al grupo: ¿contar tweets es contar personas? [pausa 3 s] No: unos pocos autores producen mucho. Costo de referencia: 90 MB.

## 12. UNNEST convierte una lista en filas

39–42 min. UNNEST es la tercera herramienta nueva: toma una lista guardada en una celda y la despliega en una fila por elemento. Seguir el ejemplo real de AFP: una fila con tres hashtags en tweets se vuelve tres filas en hashtags. Con el segundo clic, el corazón del script 22. Con el tercero, por qué DISTINCT: un tweet puede escribir el mismo hashtag dos veces y no queremos contarlo doble (3,369,433 menciones en arreglos frente a 3,339,839 filas). Costo de referencia de crear la tabla: 174 MB.

## 13. Al unir tablas con grano distinto, las filas se multiplican

42–45 min. La consecuencia práctica del grano. Al unir tweets con hashtags cada tweet se repite tantas veces como hashtags tenga: 1,226,642 tweets dan 3,339,839 filas. Si alguien cuenta COUNT(*) sobre ese resultado y dice «tweets», está contando mal. A la derecha, un caso real: ukraine aparece 514,337 veces en los arreglos pero 507,762 tweets lo usan; las 6,575 menciones de diferencia vienen de tweets que lo repiten. Pregunta al grupo: ¿qué conteo usarían en un reporte? [pausa 3 s] Depende de la pregunta, y la tabla correcta ya tiene DISTINCT.

## 14. Partición y clustering: leer menos para pagar menos

45–50 min. Cómo se guarda la tabla afecta lo que pagas. Silver está particionada por fecha (un cajón por día) y agrupada por idioma (clustering: dentro de cada día, ordenada por idioma). Probar los tres botones: el estimador y el trabajo real coincidieron en las tres mediciones, 1,231.6 MB para todo el texto, 107.5 MB para un día y 33.3 MB para un día y el idioma español. Aclarar el error típico: LIMIT limita las filas que ves, no los bytes que se leen. Esto vuelve en el laboratorio, paso 6.

## 15. Seis cosas que revisar antes de contar

50–53 min. Panorama de lo que sigue: seis revisiones que salieron de medir el archivo, no de suponer. Cada una termina en una decisión: marcar, conservar o no excluir. Atención: marcar no es borrar; la fila sigue en Silver con una columna verdadero/falso. Las siguientes cinco diapositivas muestran la evidencia de cada fila de la tabla; después un simulador deja ver cuánto cambian los conteos. Pregunta al grupo: ¿cuál de las seis creen que cambia más los números? [pausa 3 s]

## 16. El 16 de marzo solo tiene cuatro horas de datos

53–56 min. Primera trampa. La gráfica es real: tweets por día, doce barras. La primera es mucho más baja y no porque haya menos conversación: el archivo empieza esa tarde y solo cubre de 20:00 a 23:59 UTC (por hora: 12,684, 45,347, 41,166 y 35,674 tweets). Pregunta al grupo: ¿qué conclusión errónea sacaría alguien que solo mira el total diario? [pausa 3 s] Que el tema creció el día 17. La regla: marcar el día parcial para poder excluirlo o compararlo con horas equivalentes.

## 17. Un mismo texto puede repetirse cientos de veces

56–59 min. Segunda trampa. Tres textos exactamente iguales: 421 copias de 416 cuentas distintas (muchas personas escribiendo la misma frase), 375 copias de una sola cuenta (un aviso automático) y 362 de 352 cuentas. El conteo de tweets no distingue entre ambos casos. Umbral que usaremos: 20 copias o más marca 182 textos y 7,760 tweets. Anécdota real con el clic: escribir el SELECT con un alias igual al nombre de la columna agrupa por el texto recortado y da 1,424; el CTE evita la ambigüedad. Lección: revisar un resultado extraño antes de publicarlo.

## 18. Idioma sin determinar y ubicación vacía: dato ausente no es cero

59–61 min. Tercera y cuarta trampas, ambas de datos ausentes. «und» significa indeterminado y es un valor de texto; ningún filtro lo atrapa a menos que lo nombres. La ubicación es texto libre que el autor escribe y 39.2 % la dejó vacía. Dos decisiones: marcar «und» (columna idioma_desconocido) y convertir la ubicación vacía en NULL para que cuente como ausente. Nunca rellenar. Pregunta al grupo: ¿qué pasa con el porcentaje de tweets en español si descartamos «und»? [pausa 3 s] Cambia el denominador.

## 19. El promedio de likes engaña

61–64 min. Quinta trampa, esta vez de valores extremos. Más de la mitad de los tweets no recibió ningún like, y 13,928 tweets (0.2 %) reúnen el 60.4 % de todos los likes. Por eso el promedio de 15.88 no describe a ningún tweet típico: la mediana es 0. Decisión: no es un error, es la forma real de la distribución; se reporta mediana y percentiles. Pregunta al grupo: ¿borrarían los tweets virales como si fueran atípicos? [pausa 3 s] No: son el fenómeno que queremos entender.

## 20. La mitad son respuestas; los originales reúnen los likes

64–67 min. Sexta revisión: qué es una fila. Tres tipos de tweet, definidos de forma excluyente: respuesta (si responde a otro tweet), cita (si cita otro y no responde) y original. La mitad del archivo son respuestas, pero los originales, 40.2 % de los tweets, reúnen el 78.5 % de los likes. Contar «tweets» mezcla cosas muy distintas. Advertencia de cobertura: en la parte del Parquet que revisamos (37,875 tweets) retweetedTweet viene vacío en todos; la extracción excluyó retuits, y no escaneamos todo Bronze para comprobarlo.

## 21. Elige reglas y mira cuántos tweets quedan

67–70 min. Cierre de Aplicar. Activar las reglas de una en una y combinarlas. Las cifras salen de las 16 combinaciones reales de las cuatro banderas sobre Silver (consulta de 1.3 GB). Un tweet puede caer en varias reglas, por eso los marcados no se suman. Observación: las tres reglas de calidad sacan 3.5 % de los tweets, pero quitar respuestas saca la mitad. La primera es una decisión técnica; la segunda es de quien usa el análisis. Pregunta al grupo: ¿quién debe decidir si las respuestas cuentan? [pausa 3 s] Lo escribiremos en la regla.

## 22. Vuelve con tu Bronze cargado y el estimador a la vista

70–80 min. Pausa real. Al volver cada persona debe tener su tabla tweets_bronze.entrada con 6,798,932 filas. Recordar el estimador de bytes: arriba a la derecha del editor aparece antes de ejecutar. Hoy hay una sola consulta cara, la del paso 1 (23.67 GB de referencia); las demás cuestan menos de 1.4 GB.

## 23. Laboratorio: construye tus tres tablas Silver

80–150 min. La guía paso a paso (laboratorio.html) trae el código completo, el costo estimado de cada consulta, la salida esperada y el error más frecuente. Los pasos son secuenciales: cada tabla se usa en el siguiente. Si el paso 1 falla, revisa primero que tweets_bronze.entrada exista y que el dataset esté en la ubicación US. Consejo: mira siempre el estimador antes de pulsar Ejecutar.

## 24. Antes de confiar, haz que las tablas cuadren

150–155 min. Reconciliar es comparar totales entre una capa y la siguiente. Con estas seis comprobaciones se puede decir que el paso de JSON a tablas no perdió ni duplicó filas. Pregunta al grupo: ¿qué NO demuestra un cuadre? [pausa 3 s] Que los valores estén bien: una fecha mal convertida también cuadra en conteo; por eso hay revisiones de NULL, de rangos y de reglas. Estos números son los que verán en el paso 6 del laboratorio.

## 25. Quién puede leer qué en cada capa

155–160 min. Gobierno en una sola diapositiva. Cada capa tiene contenido distinto y por eso un público distinto: Bronze guarda más de lo que se usa; Silver expone lo que analizamos; Gold publica lo que se decide. En BigQuery el permiso de lectura se concede por dataset (control de acceso con IAM). Los datos de autores de este archivo se dejan como están por ser públicos y de uso académico; no se anonimizan aquí. Mencionar sin profundizar que GDPR y HIPAA son normas sobre datos personales y de salud. Pregunta al grupo: ¿qué columna de Silver no daríamos a un área de marketing? [pausa 3 s]

## 26. SQL y Spark producen el mismo Silver con dos motores

160–165 min. Spark ya apareció en la sesión 3. Aquí solo se muestra que la misma transformación se puede escribir con otro motor y obtener el mismo Silver: mismas filas, mismos ids, los mismos 12 días. Un detalle revelador: el script de Spark no pasa los hashtags a minúsculas, y el de SQL sí; son decisiones que hay que escribir en las reglas. Los tiempos no se comparan: el trabajo de Spark incluyó arrancar, leer, escribir Parquet y contar. No es parte del laboratorio de hoy.

## 27. Practica por tu cuenta: cuatro ejercicios

165–172 min. Cuatro ejercicios individuales para consolidar. Los tres primeros se resuelven con lo visto y tienen resultado esperado para comprobar; el cuarto es escritura, no código. Si sobra tiempo, pedir que cada persona lea su regla en voz alta y que otra identifique qué pregunta falta. No hay entrega: sirven para comprobar que se entendió el grano, el CTE y UNNEST.

## 28. Qué puedes afirmar con Silver, y qué no

172–180 min. Cierre honesto. Izquierda, lo que las comprobaciones sí demuestran. Derecha, saltos que alguien podría dar sin darse cuenta: confundir tweets con personas, comparar un día parcial con uno completo y creer que limpiar elimina el criterio. Silver no es la verdad: es una decisión documentada. Con el clic, el puente a la sesión 5: Gold toma estas tablas y calcula indicadores con una definición escrita. Pregunta de salida: ¿qué regla cambiarían y cuántos tweets moverían? [pausa 3 s]
