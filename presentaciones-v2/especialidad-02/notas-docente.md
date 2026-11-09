# Sesión 2 · Una consulta también puede contar mal

Gran idea: El SQL conserva la pregunta cuando defines grano, población y vigencia.

Guion para presentar en vivo. [pausa 3 s] indica silencio deliberado. Los controles se activan por el docente; no hay avance automático.

## 01. Una consulta también puede contar mal.

0–4 min. Abrir con una pregunta: si veo tres filas al unir salarios, ¿tengo tres empleados? [pausa 3 s] El ejemplo de portada es ilustrativo. La sesión busca que puedan leer y adaptar SQL con una definición explícita, no memorizar sintaxis.

## 02. Un historial conserva varias versiones de la misma persona.

4–9 min. Pedir contar primero filas, después personas distintas. Son registros ilustrativos, no los valores reales de employees. La fecha 9999-01-01 es el marcador del snapshot. No representa a empleados vigentes hoy. No asignar moneda al salario.

## 03. Define qué representa una fila antes de contar.

9–15 min. Definir grano con dos tablas concretas. La llave identifica una fila dentro del contrato de la tabla. El nombre puede repetirse. Al unir una persona a su historial cambia el grano del resultado. Solicitar un ejemplo de grano en el dataset propio, aunque sea provisional.

## 04. Las llaves conectan entidades; los nombres pueden repetirse.

15–19 min. El esquema simplifica columnas para enseñar la relación. Una persona puede tener varias asignaciones históricas. PK es llave primaria; FK referencia la entidad. Dibujar cómo emp_no viaja, sin decir que es necesariamente la llave de cualquier resultado unido. El departamento se describe en departments.

## 05. SELECT elige columnas; FROM identifica la tabla.

19–22 min. Leer la consulta en voz alta: mostrar código y nombre desde departments ordenados por código. No pedir copiar todavía; el script completo está en la guía. Mostrar que las palabras de SQL no cambian el origen de los datos ni el acceso disponible.

## 06. WHERE conserva solo las filas que cumplen la condición.

22–25 min. Explicar intervalo semiabierto con fechas en la frontera. Evita ambigüedades de horarios si después se usan timestamps. No filtrar por el texto del año extraído como receta universal. AND exige ambas condiciones. El ejemplo completo agrega nombre, orden estable y límite.

## 07. El filtro cambia las filas que llegan al conteo.

25–28 min. Preguntar qué filas sobrevivirán antes de usar el botón. El navegador filtra esta miniatura fija; no ejecuta MariaDB. Dos pasan el rango. Volver atrás para discutir el borde de 1995. Después transferir la misma lectura al SQL real de Q2.

## 08. Ordenar vuelve reproducible la selección limitada.

28–31 min. Dos personas pueden compartir fecha. Una segunda llave hace estable el orden en esta tabla. LIMIT sin orden no significa las primeras contrataciones ni una muestra representativa. En BigQuery tampoco es un tope de lectura; volveremos al costo en Bronze.

## 09. COUNT mide cosas distintas según lo que le pidas.

31–35 min. NULL representa ausencia, no cero. Una media excluye NULL y puede cambiar su población. COUNT(DISTINCT) sirve para personas pero no justifica cualquier join ni calcula promedios correctamente después de duplicar filas. Pedir al grupo elegir la expresión para contar empleados con salario conocido.

## 10. GROUP BY cambia el grano del resultado.

35–40 min. Una fila de salida representa un departamento. El marcador de vigencia filtra la historia antes de agregar. Pedir explicar por qué emp_no deja de ser columna de salida individual. El resultado ilustrativo no anticipa los conteos de la base real.

## 11. WHERE filtra filas; HAVING filtra grupos.

40–45 min. Esta es una lectura conceptual, no el plan físico del motor. La media se calcula por grupo y luego se filtran grupos. Q4 usa AVG sobre salario vigente y asignaciones vigentes, una coincidencia por persona según controles. La cifra60000 es un umbral de ejercicio sin moneda asumida.

## 12. Un LEFT JOIN conserva a quien no tiene coincidencia.

45–49 min. Miniatura distinta del historial: dos personas, solo una coincidencia salarial. Primero INNER oculta Luis; cambiar a LEFT y discutir NULL. El nombre es etiqueta de pantalla; la relación real usa emp_no. Preguntar qué join usar para conservar departamentos vacíos.

## 13. Una relación histórica puede multiplicar las filas.

49–53 min. Volver a portada. La base no inventó empleados: respondió a la relación solicitada. No usar MAX(salary) como sustituto de vigente; alguien pudo reducir salario. Filtrar por la vigencia que define el contrato. Estos salarios son ficticios; Q6 mostrará el historial real de la cuenta preparada.

## 14. La vigencia debe aplicarse antes de interpretar el promedio.

53–57 min. Fragmento de Q4, no consulta completa ejecutable sola. Filtramos ambos historiales para evitar cruzar asignaciones y salarios de distintas épocas. Si hay más de un salario marcado vigente por persona, el control debe detectarlo y la media se investiga antes de usarla.

## 15. Un filtro mal colocado puede borrar los departamentos vacíos.

57–61 min. Primer fragmento: la condición decide qué asignaciones coinciden y preserva todos los departamentos. Segundo: después del LEFT, WHERE rechaza NULL y borra departamentos sin asignación vigente. Pedir anticipar el efecto antes del clic siguiente. No hace falta aprender todos los joins para comprender este error.

## 16. Prueba la pregunta con un caso que podría romperla.

61–65 min. Dividir la sala en pares y asignar un caso de prueba. La consulta correcta debe conservar el significado en casos límite, no solamente devolver un número. Estas pruebas anticipan el reporte de calidad de Silver. Registrar qué consulta revisarían primero.

## 17. Vuelve con acceso a employees comprobado.

65–75 min. Pausa. La guía contiene ruta de conexión preparada por el docente. No dedicar el SQL Fast Track a instalar una VM. Si falla acceso, confirmar la configuración con el docente y mantener el trabajo de lectura; distinguirlo de ejecución real.

## 18. Una consulta mínima comprueba la conexión.

75–80 min. Usar el cliente y credenciales que entregue el docente, sin proyectarlas. Si no existe la base, el docente aún no cargó test_db; instalar MariaDB no basta. SELECT1 solo comprueba acceso, no calidad de datos. El archivo completo tiene únicamente SELECT y USE.

## 19. Comprueba columnas antes de escribir la respuesta.

80–88 min. Abrir employees-fast-track.sql, ejecutar bloques Q1 y Q2. No ejecutar una selección parcial que mezcle consultas. Comparar columnas con el esquema. Q2 limita20 filas, no representa todas las contrataciones del rango. Corregir proyecto/base si no existen tablas.

## 20. Cuenta personas sin perder departamentos vacíos.

88–100 min. Esta versión corta es ejecutable; Q3 descargable agrega nombre y orden. Explicar COUNT(de.emp_no) frente a COUNT(*): la fila preservada de un departamento vacío tiene emp_no NULL. Guardar consulta y resultado de la base real; no inventar conteos esperados.

## 21. El promedio exige definir a quién incluyes.

100–112 min. Ejecutar Q4 y Q5 completos desde la guía. Q4 aplica HAVING AVG>=60000. Exigir que describan la población de la media y la unidad pendiente de verificar. Q5 devuelve20 filas ordenadas, no todo el personal. Si media o conteo sorprende, revisar cardinalidad y vigencia antes de corregir a ojo.

## 22. Una persona permite inspeccionar la multiplicación.

112–122 min. No producir un join masivo para mostrar un error que cabe en una persona. Registrar filas y emp_no distinto antes/después. Los datos reales tendrán su propio historial; no esperar las tres filas ficticias de portada. Comentar el filtro de vigencia y la diferencia obtenida.

## 23. Una consulta de control también forma parte de la entrega.

122–130 min. Cero resultados no prueba toda la calidad de la base: responde solo a esta regla. Si hay filas, detener interpretación de promedios y explicar el conflicto. Guardar consultas comentadas y evidencias. No borrar ni corregir la base compartida del docente.

## 24. Tu pregunta necesita entidad, periodo y denominador.

130–140 min. No trasladar salarios ni departamentos a todos los proyectos. Mapear pregunta a columnas existentes en su paquete; si todavía no hay esquema validado, escribir pseudoconsulta y declarar pendiente. El docente adapta consulta base al dominio. No entregar conteos imaginados.

## 25. La consulta debe poder leerse como una decisión de alcance.

140–150 min. Intercambiar consulta o pseudoconsulta. El receptor explica población, periodo y grupo. Si la interpretación difiere, corregir comentario o consulta. No confundir lectura conceptual con orden físico de ejecución. El objetivo es hacer visible la definición, no tener más líneas.

## 26. El resultado necesita una prueba que pueda fallar.

150–160 min. Cada equipo registra casos límite de su fuente. Si usa un ejemplo inventado, etiquetarlo como prueba hipotética; no mezclarlo con evidencia real. Identificar un join potencial y su cardinalidad. Registrar qué falta conocer para verificarlo.

## 27. Entrega SQL que otro equipo pueda explicar.

160–170 min. H2 distingue ejercicios guiados de transferencia al dataset propio. Guardar resultados reales con consulta; si solo hubo lectura por falta de conexión, reportarlo. La calidad no depende de que el SQL sea largo. No entregar credenciales. El docente gestiona apagado de VM compartida.

## 28. Ahora pregunta qué tuvo que leer el motor.

170–180 min. Volver a Q2: LIMIT20 habla de salida, no del total examinado. Pregunta de salida: qué cuenta COUNT(*) después de unir un historial. Esto abre la tensión de S3 sin introducir el motor distribuido a fondo todavía.
