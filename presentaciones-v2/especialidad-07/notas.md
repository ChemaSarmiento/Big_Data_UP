# Sesión 7 · La frase suena lista. La evidencia todavía no

Gran idea: Un modelo solo responde con el contexto que recibe: tú decides cuál es y compruebas cada afirmación contra los datos.

Guion para presentar en vivo. [pausa 3 s] indica silencio deliberado. Los controles se activan con clic o con las flechas; no hay avance automático.

## 01. La frase suena lista. La evidencia todavía no.

0–4 min. Abre con la pregunta, no con la herramienta: si un modelo te entrega un memo en diez segundos, ¿qué le exigirías antes de firmarlo? [pausa 3 s] Escucha dos respuestas. El número 137,598 sale de la tabla tweets_gold.tema_dia (suma del tema energía en los tres grupos de idioma, del 16 al 27 de marzo de 2022) y cuenta tweets con palabras clave, no personas ni opinión. Hoy no se entrena ningún modelo: se aprende a darle contexto y a auditar lo que escribe.

## 02. Dos memos con la misma pregunta: solo uno se puede comprobar.

4–8 min. Memos redactados a mano para esta clase, no salida de un modelo. Lee A en voz alta y pide que marquen lo que no pueden comprobar. Revela las banderas: no hay cifra, no hay fuente, la causa se afirma sin prueba. Revela B: cada frase remite a algo que puedes abrir. Las cifras de B son reales: 10,530 y 311,363 salen de la tabla tema_dia y [1] es un tweet con URL. Idea del día: un texto fluido no es un texto verdadero; lo que lo vuelve útil es poder volver a su evidencia.

## 03. El ciclo de hoy: recuperar, armar, generar, auditar.

8–12 min. Dibuja el ciclo con un clic por paso. 1: una consulta decide qué datos entran; ya sabes escribirlas. 2: se arma un texto numerado con etiquetas, para poder citar. 3: el modelo redacta usando solo ese texto. 4: cada afirmación se compara con la tabla o el tweet citado. Este patrón se llama RAG (recuperación y generación) y lo definimos con calma más adelante. Lo importante ahora: el modelo está en el paso 3 de 4; los pasos 1, 2 y 4 son tuyos.

## 04. Machine learning aprende patrones de ejemplos; una regla la escribe alguien.

15–20 min. Machine learning, en una frase: un programa que ajusta su comportamiento a partir de ejemplos en lugar de seguir reglas escritas una por una. Arriba, la regla que usó la capa Gold para asignar temas: si el tweet contiene una palabra de la lista, cuenta para el tema. Abajo, la idea de aprendizaje: se le muestran miles de tweets con su tema marcado y el modelo ajusta lo que necesita para predecir el tema de uno nuevo. Ninguno de los dos entiende lo que dice el tweet; uno sigue una lista y el otro un patrón estadístico. No hay código, métricas ni entrenamiento en este curso.

## 05. Una regla de palabras clave acierta, se equivoca y se pierde temas.

20–24 min. Tres tweets reales del 23 de marzo, en inglés. [1] contiene «gas» y trata de energía: acierto. [2] contiene «gas» pero habla de máscaras antigás: la regla lo cuenta como energía y no lo es. [3] habla de Nord Stream 2, un gasoducto, pero no contiene ninguna palabra de la lista: la regla no lo ve. Por eso las cifras de tema de Gold son un conteo de palabras, no una medición del tema; en una lectura manual de 30 tweets hubo 17 aciertos, 5 dudosos y 8 falsos positivos (muestra pequeña: cinco por tema, un día, una persona). Un modelo de aprendizaje podría equivocarse menos, pero también se equivoca: la diferencia es que se equivoca de forma menos predecible.

## 06. Un modelo de lenguaje continúa el texto con la palabra más plausible.

24–28 min. Un modelo de lenguaje (LLM) se entrena con enormes cantidades de texto para predecir qué viene después. Funciona por piezas llamadas tokens (fragmentos de palabras). Dado un texto de entrada, calcula qué tan plausible es cada continuación y escribe una, y luego otra, y así hasta terminar. La gráfica es una ilustración, no una medición de un modelo real. La idea que te llevas: plausible no es lo mismo que verdadero. Un modelo puede escribir con total seguridad una cifra que nadie midió, porque «suena» como las cifras que ha visto.

## 07. Un modelo lee tokens: cinco tweets caben; seis millones no.

28–32 min. Un token es un fragmento de texto, más o menos cuatro caracteres. La ventana de contexto es el máximo de tokens que el modelo puede leer en una sola petición, y cada token leído o escrito se cobra. Cálculo de esta clase: los cinco tweets del contexto con su URL suman unos 1,245 caracteres, alrededor de 310 tokens; las seis líneas de Gold, 1,315 caracteres, alrededor de 330; el texto de los 6,798,932 tweets suma 1,187,779,540 caracteres, cerca de 297 millones. Las cifras son estimaciones con la regla de cuatro caracteres. Conclusión: no puedes pegar todo; tienes que recuperar un corte pequeño y relevante.

## 08. Lo tuyo solo existe para el modelo si lo pones en el contexto.

32–35 min. El modelo recibe conocimiento por dos vías. Entrenamiento: lo que aprendió antes de una fecha de corte, general y sin tus datos. Contexto: lo que tú le entregas en esa petición. Tus tablas, tus tweets y las cifras de hoy no están en el entrenamiento; solo existen si las pones en el contexto. Este punto parece obvio, y justo por eso se olvida. Enseguida lo vemos con un ejemplo muy pequeño.

## 09. Con cinco tweets en el contexto, el modelo solo puede hablar de esos cinco.

35–40 min. Esta slide existe para decir lo obvio en voz alta: los cinco tweets son un contexto de juguete. Sirven para ver el mecanismo. Pregunta 1: se puede responder porque el tema está en el contexto; la respuesta debe citar [3] y [4]. Pregunta 2: pide un conteo del conjunto, y el contexto solo tiene cinco filas; un modelo bien instruido dice «No hay evidencia en el contexto»; uno mal instruido inventa un número. Nada de lo que diga sobre cinco tweets se generaliza a 6.8 millones. Eso nos obliga a subir de nivel: en vez de tweets sueltos, darle al modelo resúmenes del conjunto, que son exactamente lo que producen las tablas Gold.

## 10. Un prompt ejecutivo tiene cinco partes.

40–43 min. Un prompt es el texto que le entregas al modelo. Cinco partes ordenan el trabajo. El rol fija el punto de vista. Las reglas son lo más importante para evidencia: usar solo el contexto, citar con una etiqueta y decir «No hay evidencia» cuando no alcance. El contexto es el material. La pregunta es una sola y concreta. El formato limita la longitud y el idioma. Sin la parte 2, el modelo rellena lo que falta con lo que le suena. Este prompt se escribe en el laboratorio, paso 3.

## 11. Un modelo puede fallar de tres maneras aunque escriba bien.

43–47 min. Una alucinación es un texto fluido y seguro que no tiene respaldo en el contexto ni en los datos. Tres formas típicas, todas con ejemplos redactados a mano para esta clase, no salidas de un modelo real: cifra inventada, cita que no existe y causa afirmada sin prueba. La defensa no es confiar más ni menos en el modelo: es poder comprobar cada afirmación contra una etiqueta. Por eso exigimos etiquetas en el prompt y auditamos al final.

## 12. Un tweet cuenta una anécdota; una tabla Gold cuenta el conjunto.

47–50 min. Cada tabla Gold resume millones de tweets en pocas filas y responde una pregunta concreta. Esa es su ventaja como contexto: 216 filas de tema_dia caben en un prompt; los 6.8 millones de tweets no. Las seis tablas salen de la capa Silver, y el grano de cada una dice qué es una fila. Hoy no las construimos; las usamos como material para el modelo y como referencia para auditar lo que escriba.

## 13. Un paquete de contexto con tablas: una línea numerada por tabla.

50–53 min. Esta es la salida real de la consulta del paso 2: seis líneas, una por tabla Gold, cada una con su etiqueta, el nombre de la tabla, el filtro (fecha, idioma) y la base. Fíjate en lo que incluye una línea útil: de dónde viene, qué cubre y contra qué base se mide. Con este paquete el modelo puede responder preguntas sobre el conjunto y citar [T1] a [T6]. Todo el paquete mide unos 330 tokens: cabe sin problema. Las cifras salen sin separador de miles porque así las devuelve la consulta.

## 14. Con el paquete de tablas se responden preguntas del conjunto, o se admite que no hay respuesta.

53–56 min. Recorre las filas. Las cuatro primeras se contestan con una cita porque el paquete trae la cifra. La tercera combina dos segmentos de T3: 2.15 + 0.84 = 2.99 % de los tweets y 35.93 + 17.66 = 53.59 % de los likes; si el modelo suma, tú puedes comprobarlo. La última pregunta es la importante: el paquete no tiene causas, y la respuesta correcta es admitirlo. Un buen prompt hace que ese «no hay evidencia» sea la salida por defecto.

## 15. Gold esconde historias: 3 % de los tweets reúne 54 % de los likes.

56–59 min. Una de las seis tablas Gold, vista como gráfica: autores_alcance. Dos tercios de los tweets vienen de cuentas con menos de mil seguidores y reciben menos de 9 % de los likes; las cuentas de más de cien mil seguidores publican menos de 3 % de los tweets y reciben más de la mitad de los likes. Otra tabla, conversacion_dia, dice que 50.2 % de los tweets son respuestas, 40.2 % originales y 9.6 % citas, y que los originales concentran 78.5 % de los likes. Son cifras para poner en el contexto y hacerle al modelo preguntas sobre el conjunto; no explican por qué ocurre.

## 16. RAG: recuperar primero, generar después, auditar siempre.

59–62 min. RAG significa generación aumentada con recuperación. Paso 1: una consulta recupera solo lo que responde la pregunta. Paso 2: se arma el contexto con etiquetas. Paso 3: el modelo redacta bajo reglas. Paso 4, que cierra el bucle: cada afirmación se compara con su fuente. Pegar un archivo entero y pedir un resumen no es RAG: no filtra, no cita y no se puede auditar. Mismo ciclo que vimos al inicio, ahora con nombre. Las fuentes oficiales describen el mecanismo; los costos y límites dependen de tu cuenta.

## 17. La regla de oro: solo con el contexto, cita la etiqueta, di «no hay evidencia».

62–64 min. Respuesta redactada a mano, no producida por un modelo, para practicar la lectura. Verde: afirmaciones con etiqueta y cifra, que se pueden abrir en la tabla. Rojo: «subió porque…» es una causa; ninguna etiqueta la respalda y en el contexto no hay causas. Un buen texto generado deja esa frase fuera, o la convierte en «los datos no explican la causa». Esta lectura —buscar etiqueta, abrir tabla, comprobar cifra— es el método de auditoría del resto de la sesión.

## 18. Audita: sustentada, contradicha o sin respaldo.

64–66 min. Pulsa cada afirmación antes de revelar el veredicto y pide que el grupo lo adivine. A1 y A4 se sostienen con una tabla. A2 y A3 suenan razonables y los datos las contradicen: 1.67 % frente a 0.91 %, y 17.66 % frente a 35.93 %. A5 y A6 son del tipo más peligroso: ni se confirman ni se niegan, porque el dato no puede decidirlo. Reglas del método: busca la etiqueta, abre la tabla, repite la cifra, y si no hay dato, escribe «sin respaldo». Las seis consultas están en el paso 5.

## 19. Auditar es repetir la cifra con una consulta pequeña.

66–68 min. Una afirmación, una consulta, un veredicto. La consulta sobre autores_alcance procesa 195 bytes: auditar sobre Gold es casi gratis, porque la tabla ya está resumida. Compara el costo con lanzar la misma pregunta contra los 6.8 millones de tweets. Y mira cómo una cifra ligeramente distinta cambia la conclusión: la mayor parte de los likes no está en el segmento más grande.

## 20. Qué puede salir mal con este material.

68–70 min. Cinco riesgos que el modelo no ve y tú sí. La muestra son 12 días y no incluye retweets. El 16 de marzo es día parcial: comparar su conteo con otros días engaña. Hay textos repetidos copiados por cuentas distintas. Las palabras clave aciertan menos de lo que parece; la lectura manual fue de 30 tweets, una muestra pequeña. Y el idioma no te dice el país. Si el modelo escribe algo que ignore estos límites, es una afirmación sin respaldo, por fluida que suene.

## 21. Pausa. Al volver, arma tu contexto y pruébalo.

70–80 min. Pausa real, sin avance automático. Mientras vuelven, comprueba que cada quien tiene abiertas las dos herramientas y que tiene a la mano las tablas Silver y Gold que construyó en las sesiones anteriores. Si falta alguna tabla, el paso 1 y el 2 muestran la consulta que la usa; sin las tablas el laboratorio no se puede ejecutar completo.

## 22. Laboratorio: de la consulta al texto auditado en seis pasos.

80–150 min. Esta es la única slide de laboratorio: el código, las salidas esperadas y los errores frecuentes están en la guía, paso por paso. Trabajas sobre tus propias tablas. Los pasos 1, 2 y 5 son SQL y se pueden ensayar con el estimador de bytes; el paso 4 usa la interfaz de Vertex AI Studio, cuyo texto de salida cambia en cada ejecución: tu comprobación no es que el texto coincida, sino que cada afirmación tenga su etiqueta y su veredicto.

## 23. La cuenta de un modelo se mide en tokens leídos y escritos.

150–155 min. Cierre sobre costo. Un modelo cobra por token leído (el contexto, incluidas las reglas) y por token escrito. Con contextos tan pequeños como los de hoy, cada prueba cuesta muy poco; el riesgo de costo aparece al pegar archivos grandes o al repetir miles de peticiones. Las tarifas dependen del modelo y de tu cuenta y cambian; no hay cifra aquí a propósito. Antes de lanzar muchas pruebas, revisa la página oficial y fija un presupuesto.

## 24. Tres ejercicios para practicar lo que viste hoy.

155–165 min. Práctica individual con lo aprendido, sin entrega. El ejercicio 3 es el más revelador: sin T1 en el contexto, la pregunta sobre qué tema pesó más ya no tiene respuesta, y un buen prompt lo admite. Si el modelo responde igual con cifras, esas cifras no vienen del contexto: las inventó.

## 25. Qué puedes afirmar con estos datos, y qué no.

165–175 min. Cierre honesto, una sola vez. Cada fila de la izquierda tiene una etiqueta y se comprueba con una consulta. Cada fila de la derecha es un salto que un memo puede dar sin darse cuenta: de palabras clave a «la gente», de conteo a importancia, de coincidencia a influencia. Antes de firmar un texto generado, vuelve a este cuadro.

## 26. El modelo escribe. La evidencia decide.

175–180 min. Cierra con la idea del día: un modelo es muy bueno escribiendo y no sabe nada de tus datos. Lo que lo vuelve útil es el método: recuperar un corte pequeño, armar un contexto con etiquetas, pedirle que se limite a ese contexto y auditar cada afirmación. Pregunta de salida: ¿qué frase de un texto generado te haría pedir la fuente antes de firmar?
