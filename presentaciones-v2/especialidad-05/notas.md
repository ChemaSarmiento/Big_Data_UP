# Sesión 5 · Un conteo no es un indicador

Gran idea: Gold convierte millones de tweets en seis tablas pequeñas, cada una con su pregunta, su grano, su denominador y sus límites escritos.

Guion para presentar en vivo. [pausa 3 s] indica silencio deliberado. Los controles se activan con clic o con las flechas; no hay avance automático.

## 01. Un conteo no es un indicador.

0–3 min. Abrir con la pregunta de un comité: ¿qué temas de la guerra vale la pena vigilar en una empresa? No analizamos el contenido bélico; buscamos temas satélite de negocio. Preguntar: «¿Qué necesitarías ver para decidir?» [pausa 3 s] Anotar dos respuestas en voz alta. Hoy aprenden a contestar con una cifra defendible: con su grano, su denominador y sus límites.

## 02. Casi el mismo conteo; un 58 % más de peso en el día.

3–8 min. Mostrar solo el conteo y pedir que voten: ¿cambió algo entre el 17 y el 23? [pausa 3 s] Casi nada: 10,167 y 10,530 (+3.6 %). Clic: el mismo conteo visto como porcentaje del día. El 17 hubo 476,188 tweets en inglés; el 23, 311,363. Con menos tweets en total, la misma cantidad de energía pesa más: 2.135 % contra 3.382 %. La pregunta de esta sesión: cuál de las dos lecturas es la correcta depende de cómo escribas el indicador. Aún no afirmamos causas: el archivo no las trae.

## 03. Silver dice qué escribió cada tweet; Gold dice qué decidir.

8–15 min. Repasar las capas con un número cada una: Bronze 22.04 GiB de JSON crudo; Silver 2.28 GiB (tweets 6,798,932 filas; autores 1,872,074; hashtags 3,339,839); Gold unos 0.5 MB en total (la suma de las siete tablas es 508,964 bytes). La diferencia de tamaño es la idea: Gold no guarda tweets, guarda respuestas. Una fila de Gold puede resumir decenas de miles de tweets. Error típico: pensar que Gold es «Silver con menos columnas». No: cambia el grano.

## 04. Gold responde una pregunta por tabla.

15–19 min. Recorrer la tabla renglón por renglón en voz alta: cada tabla nace de una pregunta de negocio, no de las columnas que existen. Las filas son reales: 216 = 12 días × 6 temas × 3 idiomas; 5 segmentos de seguidores; 36 = 12 días × 3 tipos. Aparte existe temas_palabras (42 filas): la definición de los temas, no un resultado. Pregunta: «¿cuál de estas preguntas le importaría más a un director de comunicación?» Escuchar dos respuestas.

## 05. El grano dice qué representa una fila.

19–24 min. El grano es lo que representa UNA fila. Aquí: un día, un tema y un grupo de idioma. Clic: la celda marcada es energía, inglés, 23 de marzo: 10,530 tweets de 311,363 ese día. Pedir que alguien lea la fila en voz alta con las unidades. Si el grano fuera «por mes», habría 6 filas y no verías el salto del 23. Error típico: sumar filas de granos distintos. Regla del curso: escribe el grano antes de escribir la consulta.

## 06. Un indicador necesita denominador.

24–28 min. Definir denominador con una analogía: «¿cuántos de cada cien?» El conteo crudo no se puede comparar entre días porque cada día tuvo un volumen distinto: 778,608 tweets el 17 de marzo y 505,568 el 26. Tampoco entre idiomas: el inglés tiene 4,013,172 tweets y el español 1,056,425. Por eso la fila trae tweets_tema y tweets_dia: el denominador viaja con la cifra. Error típico: dividir por el total del archivo en lugar del total del día.

## 07. Un tweet puede contar en varios temas.

28–33 min. Mostrar el tweet real: habla de carga aérea, así que aviación (airspace) y cadena de suministro (logistics) lo atrapan. En Gold cuenta una vez en cada tema, pero es un solo tweet. Clic: 314,527 tweets distintos tienen algún tema (4.6 % del total) y generan 342,484 pares tweet–tema; la diferencia son tweets en más de un tema. Error típico: sumar los seis temas y llamarlo «tweets sobre la guerra y los negocios». Pregunta: «¿cuántos tweets distintos hay si sumo 137,598 + 80,266 + 59,685 + 49,137 + 8,975 + 6,823?» No lo sabemos solo con esa suma.

## 08. Las palabras clave son una definición.

33–37 min. La tabla temas_palabras es una definición editable: tú decides qué palabras definen un tema. El SQL prueba cada tweet contra las 42 palabras (CROSS JOIN) y deja pasar solo las coincidencias (REGEXP_CONTAINS; \b marca el límite de una palabra para que «gas» no coincida con «Gascón»). GROUP BY tweet_id cuenta una vez por tema aunque el tweet use dos palabras del mismo tema. Costo real: 1.42 GB, porque solo lee el texto. Lo que NO hace: entender el tema. Eso se mide en la siguiente slide.

## 09. Lee lo que atrapan las palabras clave.

37–42 min. Los ocho renglones salen de la consulta del paso 6 del laboratorio (5 tweets por tema el 23 de marzo, inglés y español). Mi lectura de las 30 filas: 17 aciertos, 6 dudosos y 7 falsos positivos. Otra persona clasificaría distinto, y eso es parte de la lección: la precisión se mide con varias personas leyendo una muestra más grande. Dos errores típicos: palabras con otro sentido (markets en «Wuhan fish markets»; «guerra contra la inflación» es una expresión) y temas militares que parecen de negocio (air superiority no es aviación comercial). Aviso: el mismo tweet de la Pentagon aparece como dudoso en energía y falso en alimentos.

## 10. El umbral decide qué ves.

42–46 min. Demo con cuatro umbrales (cifras reales de hashtags_dia): con ≥ 25 tweets al día quedan 2,261 hashtags y 71.8 % de las menciones; con ≥ 100, 525 hashtags y 61.1 %; con ≥ 500, 97 y 47.5 %; con ≥ 2,000, 21 y 33.4 %. La tabla Gold del curso usa 25. Mensaje: el umbral es una decisión de negocio con costo (qué dejas fuera). Silver conserva las 3,339,839 menciones; Gold, un resumen. Error típico: presentar el top de Gold como «todos los hashtags».

## 11. El hashtag más grande pesa 8.7 % de un día.

46–50 min. Hashtags del 23 de marzo, en porcentaje del día: #ukraine 8.7 %, #putin 2.5 %, #russia 2.4 %. Un hashtag es una etiqueta que el autor escribe; no mide a favor o en contra. Clic: el 27 de marzo aparecen etiquetas ajenas a la guerra (#27mar, #oscars, #annewill, #trumprally) que el 17 no llegaban al umbral: la conversación se abre a otros temas. Límite: solo 1,226,642 de 6,798,932 tweets (18 %) llevan al menos un hashtag. Pregunta: «¿qué decidirías con esta tabla y qué no?»

## 12. Pocas cuentas concentran los likes.

50–54 min. Tabla autores_alcance: 5 filas, una por segmento de seguidores del autor. Barra gris: porcentaje de tweets; barra roja: porcentaje de likes. El 67 % de los tweets lo escriben autores con menos de mil seguidores y reciben 8.7 % de los likes. Las cuentas de 100 mil a 1 millón escriben 2.15 % de los tweets y reciben 35.93 %. Seguidores es el dato del autor en su último tweet del archivo; likes no es influencia ni persuasión. Pregunta: «¿qué haría un director de comunicación con esta tabla?» Límite: es una foto de 12 días.

## 13. Quien más publica no es quien más audiencia tiene.

54–57 min. Tabla Silver autores (1,872,074 filas, una por autor) contra autores_alcance. 1,091,593 autores aparecen una sola vez; 11,917 (0.64 %) escriben más de 50 tweets y suman 1,310,632 tweets, 19.3 % del archivo. El autor con más tweets: 7,492, con 88 seguidores. No sabemos si son personas o cuentas automatizadas: el archivo no lo dice. Por eso Gold dice «cuentas» y «autores», no «personas». Error típico: leer «6.8 millones de tweets» como «6.8 millones de voces».

## 14. El ritmo del día tiene forma; el 16 de marzo solo trae cuatro horas.

57–60 min. Tabla actividad_hora (804 filas: día × hora UTC × idioma). Los días completos tienen un valle a las 5 UTC (2.2 %) y una meseta de 13 a 19 UTC (5.3 a 5.6 % por hora). El inglés tiene su pico a las 18 UTC, el español a las 14 y el resto de idiomas a las 13. Clic: el 16 de marzo solo tiene datos de 20 a 23 UTC: es un día parcial, por eso sus conteos no se comparan con los demás. UTC no es hora local: el patrón mezcla usuarios de muchos países.

## 15. Casi 9 de cada 10 tweets salen de las aplicaciones oficiales.

60–63 min. Tabla aplicaciones_dia (108 filas: día × aplicación; las ocho mayores del archivo y «otras»). Suma de las cuatro aplicaciones oficiales: 89.0 %. WordPress, TweetDeck, dlvr.it e IFTTT suman 5.3 %: son herramientas que programan o automatizan publicaciones. Límite: usar una herramienta de publicación no prueba que la cuenta sea automática, y usar la app oficial no prueba que sea una persona. Sirve para describir el origen del tráfico, no para clasificar autores.

## 16. La mitad de los tweets son respuestas; los likes están en los originales.

63–66 min. Tabla conversacion_dia (36 filas: día × tipo). Tweets: 3,414,201 respuestas (50.2 %), 2,729,906 originales (40.2 %) y 654,825 citas (9.6 %). Likes: 84.7 millones de 108 millones están en originales (78.5 %). Promedio de likes por tweet: originales 31.04, citas 10.45, respuestas 4.80 (la mediana diaria de los tres tipos es 0). Pregunta: «si quieres medir qué dice la gente, ¿cuentas respuestas?» No hay una respuesta única: depende de la pregunta. Límite: la extracción excluye retweets.

## 17. Seis tablas, cinco técnicas de SQL.

66–68 min. No hay que memorizar sintaxis: sí reconocer la receta. Cada tabla combina la misma estructura (FROM tabla Silver, GROUP BY el grano, SUM/COUNT) con una técnica: un JOIN para traer el denominador, HAVING para un umbral, CASE WHEN para crear categorías, SUM() OVER () para obtener el total de la tabla sin perder filas, IF para agrupar en «otras», EXTRACT para sacar la hora y APPROX_QUANTILES para una mediana aproximada. Todo el código está en los archivos 30 a 35 del laboratorio.

## 18. Un KPI es una ficha, no una fórmula suelta.

68–70 min. Un KPI (indicador clave) es una cifra con definición escrita. Recorrer los ocho campos con el ejemplo de tema_dia. El paso 6 del laboratorio entrega una plantilla para llenar la tuya. Pregunta: «¿qué campo se olvida más a menudo?» Normalmente el denominador y los límites. Error típico: publicar la cifra sin la ficha; seis meses después nadie recuerda si incluía el día parcial.

## 19. Pausa. Vuelve con la consola de consultas abierta.

70–80 min. Pausa real. Antes de continuar, comprobar que tweets_silver.tweets, tweets_silver.autores y tweets_silver.hashtags existen en tu proyecto (sesión anterior) y que la consola de BigQuery está abierta. Si falta alguna, créala con los scripts de Silver antes de empezar el laboratorio.

## 20. Laboratorio: construye las seis tablas Gold.

80–150 min. Una sola slide para toda la práctica: la guía tiene el código completo, la salida esperada, el costo y el error frecuente de cada paso. Total 70 min. Cada paso termina con una comprobación numérica que debe coincidir con las cifras de esta sesión. Si una cifra no coincide, no sigas: revisa el grano o el JOIN del paso.

## 21. Las tablas Gold cuadran entre sí… salvo donde no deben.

150–156 min. El cuadre es la prueba de que el GROUP BY no perdió ni duplicó filas. Cuatro tablas con grano por tweet deben sumar 6,798,932 (el total de Silver); el paso 5 del laboratorio lo comprueba con una sola consulta. Las otras dos no cuadran por diseño: tema_dia cuenta pares tweet–tema (342,484 contra 314,527 tweets distintos) y hashtags_dia cuenta menciones con umbral. Regla: cuando una tabla NO cuadra, escribe por qué en su ficha.

## 22. Gold es una tabla que alguien tiene que volver a construir.

156–162 min. Gold no se actualiza sola. Opciones: una tabla que reconstruyes (la del curso), una vista (se ejecuta cada vez), una vista materializada (BigQuery la mantiene, pero solo admite ciertas consultas; no prometas que la tuya califique sin revisar la documentación), una consulta programada o un flujo de Dataform. Para este curso basta la tabla: reconstruir las seis cuesta ≈ 2.2 GB de lectura. Regla: toda tabla Gold debe decir cuándo se construyó y quién la actualiza.

## 23. Qué puedes afirmar y qué no.

162–168 min. Cierre honesto de la sesión, una sola vez. A la izquierda, lo que las tablas demuestran con sus límites escritos. A la derecha, saltos que un comité podría dar sin darse cuenta. El 18 de marzo, mercados en español llegó a 10.57 % del día, pero 11,917 de esos tweets mencionan «inflación», muchos en la expresión «guerra contra la inflación». Pedir que cada persona escriba una frase de su propio indicador con el verbo «no puedo afirmar».

## 24. Practica con cinco preguntas.

168–176 min. Ejercicios individuales de práctica: cada uno usa una tabla Gold distinta y tiene respuesta de referencia. Dejar que cada persona resuelva uno antes de mostrar la respuesta. Errores típicos: dividir por el total del archivo en E1; olvidar el umbral en E2; usar likes totales en lugar de likes por tweet en E3. Si algo no coincide, comparar el grano de la tabla con el de la pregunta.

## 25. Seis tablas listas: la siguiente sesión las convierte en gráficas.

176–180 min. Cerrar con la idea central: Gold pesa unos 0.5 MB porque cada fila ya es una respuesta con su denominador y sus límites. La siguiente sesión usa estas mismas seis tablas para construir un tablero: qué gráfico elegir y cómo evitar que un filtro oculte lo que el indicador no puede afirmar. Pedir a cada persona que anote la ficha de su indicador favorito antes de salir.
