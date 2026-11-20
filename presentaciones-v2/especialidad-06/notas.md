# Sesión 6 · Un tablero decide antes de que alguien lo lea

Gran idea: Un tablero útil muestra la base de la comparación, qué cubre y lo que el dato no dice, con datos de más de una tabla Gold.

Guion para presentar en vivo. [pausa 3 s] indica silencio deliberado. Los controles se activan con clic o con las flechas; no hay avance automático.

## 01. Un tablero decide antes de que alguien lo lea.

0–3 min. Abrir con una pregunta: si te muestran un tablero con una línea que sube, ¿qué necesitas ver para creerlo? [pausa 3 s] Recoge dos respuestas (la base, el periodo, el idioma). Hoy el dato son las seis tablas Gold que construiste en la sesión anterior; el trabajo es de diseño y de criterio, no de SQL nuevo.

## 02. El mismo dato cuenta dos historias según cómo lo midas.

3–8 min. Muestra solo las dos gráficas y pide que cada persona escriba qué le pasó a alimentos entre el 17 y el 25 de marzo. [pausa 3 s] Al clic aparecen los números. En conteo, alimentos pasó de 4,687 a 4,924 tweets (+5 %): parece que no cambió. Como porcentaje del día pasó de 0.60 % a 0.89 % (+48 %): su peso en la conversación sube casi la mitad. Las dos gráficas son correctas; responden preguntas distintas. La medida decide la historia, por eso Gold guarda el porcentaje y su base.

## 03. La pregunta del comité decide el tablero, no al revés.

8–11 min. Recorre la cadena de izquierda a derecha, un clic por eslabón. La medida (porcentaje del día) viene de Gold: el tablero no puede inventar una base que Gold no calculó. El título se escribe al final, con el número que el gráfico muestra. Pregunta al grupo: ¿qué acción cambiaría si el 23 de marzo hubiera sido 2.0 % en vez de 3.1 %? Si ninguna, el tablero no responde a una decisión.

## 04. Seis tablas Gold, seis preguntas, seis gráficos.

11–15 min. Esta tabla es el mapa de la sesión: cada tabla Gold que construiste responde una pregunta distinta y, por eso, pide un gráfico distinto. Recórrela fila por fila sin explicar aún los gráficos; cada uno se explica en el bloque siguiente. Los números de la última columna salen de las tablas; los comprobarás tú con SQL en el laboratorio. Hoy construyes un tablero de tres páginas con datos de las seis.

## 05. Un tablero solo puede mostrar lo que Gold ya definió.

15–18 min. Esta es la tabla que alimenta el panorama: 216 filas = 12 días × 6 temas × 3 grupos de idioma. Dimensiones dicen por qué cortamos; medidas, qué contamos; la base permite comparar días con volúmenes distintos. Lo que el tablero no puede mostrar no se arregla en el tablero: se arregla en Gold. Las otras cinco tablas existen justamente porque responden otras preguntas.

## 06. La pregunta elige el gráfico.

18–21 min. Un clic por cuadro. Línea para tiempo continuo; barras (desde cero) para comparar categorías; tabla cuando se consultan valores exactos; tarjeta cuando una cifra importa más que su forma. Evita pastel y dona: el ojo compara mal los ángulos. Cada una de las seis tablas Gold sugiere uno de estos cuatro; lo veremos con datos reales.

## 07. Un eje cortado convierte 2× en 10×.

21–24 min. Mismos dos valores: energía el 20 de marzo (1.57 %) y el 23 (3.10 %), una razón de ×1.98. Con el eje cortado en 1.4 la segunda barra se ve ×10.3 más alta. Las barras codifican el valor con su longitud, así que deben partir de cero. En una línea sí puedes acotar el eje, pero dilo en la etiqueta.

## 08. Un color de énfasis; todo lo demás, contexto.

24–27 min. Izquierda: cada serie con su color y una leyenda que obliga a ir y venir con la vista. Derecha: las series de contexto en gris con la etiqueta pegada a la línea y un solo acento en la serie que importa. Pregunta: ¿adónde miras primero en cada lado? Es el principio de Knaflic: el color es una instrucción de atención, no decoración.

## 09. El título dice la conclusión, no el contenido del gráfico.

27–30 min. Tres títulos para la misma gráfica. El primero describe, el segundo promete sin medir, el tercero lleva hecho (de 1.6–1.9 % a 3.1 %), comparación (los siete días anteriores) y límite (el dato no explica por qué). El título es lo que el comité recuerda; si el gráfico lo contradice, el comité cree al título.

## 10. Los hashtags dicen de qué se habla; no por qué.

30–33 min. Tabla hashtags_dia: solo incluye hashtags con al menos 25 tweets ese día. Izquierda, el 23 de marzo: #ukraine aparece en 8.71 % de los tweets (49,393); #putin en 2.52 %, #russia en 2.35 %. Barras horizontales ordenadas, desde cero, con el valor al final. Clic: dos hashtags, #standwithukraine y #nato, tienen su máximo el 24 de marzo (4,999 y 4,431 tweets). Clic: el dato no dice por qué. No escribas «por la cumbre» ni «por el discurso»: el archivo contiene tweets, no eventos.

## 11. Los autores grandes concentran los likes.

33–36 min. Tabla autores_alcance: cinco segmentos por seguidores del autor. Barras agrupadas con el mismo eje para poder comparar dos medidas del mismo segmento. Los autores con menos de 1 mil seguidores escriben 67.02 % de los tweets y reciben 8.72 % de los likes. Clic: el segmento de 100 mil a 1 millón escribe 2.15 % y recibe 35.93 %. Clic: los 1,375 autores de más de 1 millón escriben 0.84 % y reciben 17.66 %. Cuidado con la lectura: es concentración de likes, no influencia ni persuasión.

## 12. El idioma cambia el ritmo del día.

36–39 min. Tabla actividad_hora: tweets por hora UTC y grupo de idioma. Tres líneas del 23 de marzo con la etiqueta pegada al máximo. Clic: inglés 18,476 a las 18 UTC; español 5,679 a las 14; otros idiomas 9,769 a las 14. Esa hora es UTC, no la hora local de quien escribe: los otros idiomas suben desde las 6 UTC por la mañana europea. Clic: el 16 de marzo solo tiene las horas 20 a 23 UTC, así que un tablero por hora que lo incluya parece que el día empezó tarde.

## 13. Las respuestas son la mitad de los tweets y reúnen 15 % de los likes.

39–42 min. Tabla conversacion_dia: cada tweet es original, respuesta o cita. Dos barras apiladas al 100 %: partes de un todo. Tweets: originales 40.2 %, respuestas 50.2 %, citas 9.6 %. Clic: likes: originales 78.5 %, respuestas 15.2 %, citas 6.3 %. Clic: la mediana de likes es 0 en los tres tipos el 27 de marzo, así que decir «promedio de likes por tweet» mezcla un puñado de tweets enormes con millones de ceros.

## 14. El 16 de marzo no es el inicio del tema: es medio día.

42–44 min. Izquierda: tweets por día, con barras desde cero; el 16 de marzo tiene 134,871, un 17 % del 17. El archivo empieza esa tarde. Derecha: energía del 16 al 17 en conteo se ve multiplicada por 6.2; en porcentaje del día casi no cambia. Un tablero debe marcar el día parcial o excluirlo, y decirlo.

## 15. Mezclar idiomas diluye o infla el tema.

44–47 min. El mismo tema se ve distinto según el idioma: sanciones pesa 1.67 % en inglés, 0.91 % en español y 0.21 % en el resto. El grupo «otros» agrupa un cuarto de todos los tweets: mezclarlos diluye el tema. Un filtro de idioma no es un adorno: define de qué población habla el título.

## 16. Una palabra clave no es un tema: «mercados» lo llena la inflación.

47–50 min. Hallazgo real: el tema «mercados» en español se compone de 28,280 tweets con «inflación», 9,161 con «precios», solo 1,121 con «mercados» y 746 con «bolsa» (un tweet puede contar más de una vez). El 18 de marzo hay 11,917 tweets en español con «inflación»; muchos son «guerra contra la inflación», no Ucrania. Un tablero que muestre «mercados» como tema debe decir que es una lista de palabras, no una clasificación verificada.

## 17. Un tablero puede engañar con datos correctos.

50–53 min. Este tablero no tiene un solo número falso: todos vienen de tema_dia. Aun así tiene tres defectos. 1) El 16 de marzo es un día parcial: cualquier línea de conteo arranca baja y parece una subida. 2) Conteo sin base: las seis series siguen al volumen del día, no al peso del tema. 3) Idiomas mezclados sin aviso: el inglés pesa 59 %. Pide que encuentren un cuarto defecto: título descriptivo y seis colores.

## 18. Un filtro útil cambia el título y dice qué cubre.

53–57 min. Cambia tema e idioma y lee en voz alta el título, que cambia con el filtro: porcentaje del periodo, tweets del tema y base. Sin filtro de idioma el tablero cubre todo; con «es» la base baja a 1,056,425. Energía el 23 de marzo sube en los tres grupos. Un título fijo con un filtro variable deja de ser cierto en cuanto el lector toca el control.

## 19. Un tablero de tres páginas: panorama, dentro del tema, quién y cuándo.

57–60 min. Esquema del tablero del laboratorio. Página 1: la pregunta de negocio, la serie del tema, tres tarjetas con su base, filtro de idioma y la nota del día parcial. Página 2: de qué se habla (hashtags) y desde dónde (aplicaciones), con el filtro de fecha puesto dentro de cada gráfica (son dos fuentes distintas). Página 3: quién (alcance del autor), cuándo (hora UTC) y cómo (originales, respuestas y citas). Cada página responde una pregunta y cada elemento sale de una tabla Gold distinta. Recuerda la lectura en Z: título arriba, cifras, serie, límites abajo.

## 20. El tablero no guarda los datos: cada gráfica es una consulta a BigQuery.

60–63 min. Un tablero de Data Studio no contiene los datos: cada gráfica o tarjeta pide los suyos a BigQuery a través del conector (proyecto, dataset y tabla, o una consulta personalizada). Seis tablas Gold son seis fuentes de datos. Para que el tablero funcione necesitas leer el dataset y poder lanzar consultas en el proyecto que factura. Las credenciales de la fuente deciden quién ve los datos: del propietario (predeterminado), del lector o de una cuenta de servicio.

## 21. Conecta el tablero a Gold: cada gráfica lee kilobytes, no gigabytes.

63–66 min. Números de referencia del curso: leer Bronze completo cuesta 23.67 GB facturables; SELECT * de Silver, 2.45 GB; el texto de un solo día en Silver, 0.11 GB por la partición por fecha; y una consulta sobre cualquiera de las tablas Gold, el mínimo de 10 MiB. Cada gráfica del tablero es una consulta, y abrir una página puede lanzar varias. Con un tablero que apunte a Silver, abrirlo cuesta cientos de MiB cada vez.

## 22. Audita tres afirmaciones contra las tablas.

66–70 min. Auditoría breve con las tablas a la vista. Decide antes de pulsar: sustentada, sin respaldo o contradicha. 1) Segmento de más de 1 millón: 0.84 % de los tweets y 17.66 % de los likes: sustentada, sin hablar de influencia. 2) #nato por la cumbre: la tabla muestra el pico del 24 de marzo, no la causa: sin respaldo. 3) «Casi no se habló de energía el 16»: es medio día; en porcentaje pesa lo mismo: contradicha.

## 23. Vuelve con Data Studio y BigQuery abiertos.

70–80 min. Pausa real. Al volver comprueba que tienes tus seis tablas Gold en tu proyecto, los permisos de lectura y de consulta sobre ellas, y el presupuesto con alerta que configuraste en la primera sesión. Si falta una tabla, vuelve al laboratorio de la sesión anterior antes de seguir.

## 24. Laboratorio: un tablero de tres páginas.

80–150 min. Los seis pasos están en la guía, con el código completo, la salida esperada y el error frecuente de cada uno. Primero verificas tus tablas y las conectas; luego construyes una página por paso (panorama; dentro del tema; quién, cuándo y cómo); después revisas el tablero con la lista de siete preguntas, y al final lo compartes y compruebas cuánto cuesta. La interfaz de Data Studio no se ensayó desde la preparación de esta guía: los nombres de menús pueden variar; las comprobaciones numéricas con SQL son las que mandan.

## 25. Tres ejercicios para practicar solo.

150–165 min. Práctica individual. Resuelve cada ejercicio en papel antes de pulsar la pista (un clic por pista). El ejercicio 1 practica título con hecho y límite; el 2, la elección del gráfico para partes de un todo; el 3, la trampa del día parcial. Si te sobra tiempo, repite el ejercicio 1 con otro segmento de autores_alcance y escribe qué cambia en el título.

## 26. Qué puedes afirmar con este tablero y qué no.

165–175 min. Cierre con lo que sostiene el tablero y lo que no. Cada afirmación de la izquierda tiene evidencia en una tabla Gold; cada una de la derecha, una razón por la que el dato no alcanza: causa, representatividad, hora local, día parcial, un solo periodo. Pide que cada persona escriba una afirmación más de cada lado con sus propias palabras.

## 27. Siguiente: ¿puede un modelo leer estas tablas sin inventar?

175–180 min. Puente a la sesión 7. Los títulos y cifras del tablero serán la evidencia contra la que se audite un texto generado. Cierra pidiendo una pregunta que el tablero no puede responder y que un modelo tampoco debería responder sin evidencia.
