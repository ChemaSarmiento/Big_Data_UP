# Sesión 2 · SQL con MariaDB: de una pregunta de negocio a una consulta

Gran idea: Una consulta responde lo que contó: la pregunta decide la tabla, el grano y el filtro.

Guion para presentar en vivo. [pausa 3 s] indica silencio deliberado. Los controles se activan con clic o con las flechas; no hay avance automático.

## 01. Una pregunta de negocio se convierte en una consulta.

0–3 min. Abrir con la pregunta sin SQL: «¿cuántas personas trabajan hoy en esta empresa?». Pedir un número a mano alzada. [pausa 3 s] Revelar 240,124. La base tiene 300,024 personas en toda su historia y 331,603 asignaciones a departamentos; hoy trabajan 240,124. La sesión enseña a hacer esa distinción con SQL. Los datos son de muestra, generados para practicar; ninguna cifra es de una empresa real.

## 02. employees es una empresa de muestra con seis tablas conectadas.

3–9 min. Dibujar la base con clics. Primero employees: una fila por persona (300,024). Segundo, dept_emp (en qué departamento trabajó cada persona y entre qué fechas) y departments (9 nombres). Tercero, salaries y titles: historial de sueldos y de cargos. Cuarto, dept_manager: quién dirigió cada departamento (24 filas). Subrayar que dept_emp tiene más filas que personas (331,603 contra 300,024): hay personas que cambiaron de departamento. La base es un ejemplo generado con licencia CC BY-SA 3.0: sirve para practicar, no describe una empresa real.

## 03. «¿Cuántos empleados hay?» tiene cuatro respuestas distintas.

9–15 min. Gancho de la sesión. Mostrar tres barras y pedir «¿cuál de estas es la respuesta correcta a cuántos empleados hay?». [pausa 3 s] Revelar la cuarta: 240,124 personas trabajan hoy. Ninguna de las otras tres es mentira, pero cada una responde otra pregunta. Aquí aparecen dos ideas que usaremos toda la sesión: el grano (qué representa una fila) y el filtro (qué filas cuentan). Error típico: contar filas de una tabla de historial como si fueran personas.

## 04. employees llega a tu base con tres comandos y unos cuatro minutos.

15–20 min. Explicar de dónde sale la base antes de usarla. git clone copia el repositorio a la VM; --depth 1 evita bajar todo el historial de versiones. El archivo employees.sql contiene las instrucciones que crean las tablas y llenan sus filas. Tiempos reales de nuestro ensayo en una VM e2-micro: 3 min 29 s de carga y 367 MB en disco. La carga se hace en el laboratorio, paso 1. El usuario big_data_user con contraseña compartida es una decisión didáctica para datos de práctica; nunca se usa en un sistema con datos reales.

## 05. Una base relacional guarda datos en tablas con columnas de tipo fijo.

20–23 min. Definir cinco palabras con la tabla real delante. Tabla: lista de filas con las mismas columnas. Fila: una persona. Columna: un dato con nombre y tipo (date, varchar, enum). Clave primaria: el emp_no identifica a cada persona y no se repite. NULL: ausencia de valor; en employees ninguna columna acepta NULL (Null = NO), pero lo veremos aparecer cuando unamos tablas. DESCRIBE es el comando para ver las columnas de una tabla.

## 06. SQL es el idioma para pedirle datos a la base; hoy solo vas a leer.

23–26 min. SQL (Structured Query Language) es el lenguaje estándar para consultar bases relacionales. Tres familias de sentencias: leer (SELECT), cambiar filas (INSERT, UPDATE, DELETE) y definir tablas (CREATE, DROP). Hoy solo leemos: es seguro experimentar porque SELECT no modifica nada. Declarativo significa que describimos el resultado, no los pasos. Aclarar que LIMIT 5 sin ORDER BY devuelve cinco filas cualesquiera: el orden no está garantizado.

## 07. SELECT elige las columnas y FROM dice de qué tabla.

26–29 min. Leer la consulta en voz alta: «dame el número, el nombre completo y la fecha de contratación, de la tabla employees, solo tres filas». CONCAT une textos; AS pone un alias, es decir, un nombre más claro para la columna del resultado. Una columna del resultado puede ser un cálculo, no solo una columna guardada. Pregunta al grupo: ¿qué cambiaría si quitamos LIMIT 3? Devuelve las 300,024 filas.

## 08. WHERE deja solo las filas que cumplen la condición.

29–32 min. WHERE es el filtro: la fila se queda solo si cumple la condición. Con AND deben cumplirse las dos. Mostrar el embudo: 300,024 filas, 120,051 mujeres, 53,839 mujeres contratadas desde 1990. COUNT(*) devuelve cuántas filas hay. Las fechas se escriben entre comillas con el formato año-mes-día. Pregunta al grupo: ¿puede el resultado ser mayor que 120,051 si agrego otra condición con AND? No.

## 09. Sin paréntesis, AND y OR pueden darte otra respuesta.

32–35 min. Dos consultas casi idénticas y dos respuestas. Preguntar antes de revelar: ¿cuál creen que cuenta lo que dijo el negocio? La respuesta depende de la pregunta. AND tiene prioridad sobre OR, como la multiplicación sobre la suma. Los números: 616 mujeres contratadas desde 1999, 253 personas llamadas Georgi y 106 mujeres llamadas Georgi. Regla práctica: cuando mezcles AND y OR, usa paréntesis siempre.

## 10. IN, BETWEEN y LIKE resumen condiciones que usarás todo el tiempo.

35–38 min. Cuatro atajos con números reales. IN reemplaza varios OR sobre la misma columna: 709 personas se llaman Georgi, Bezalel o Parto. BETWEEN incluye ambos extremos: 25,610 personas fueron contratadas en 1990. LIKE busca patrones: el símbolo % significa cualquier cantidad de caracteres. Mostrar que Fac% encuentra Facello y 186 apellidos más. Error típico: usar BETWEEN con fechas sin pensar en que el último día queda incluido.

## 11. ORDER BY ordena el resultado y LIMIT corta cuántas filas ves.

38–41 min. ORDER BY ordena; DESC es de mayor a menor. LIMIT corta: «los cinco primeros». to_date = 9999-01-01 es la convención de esta base para decir «sigue vigente»; la veremos más adelante. Segundo clic: nueve personas entraron el primer día de la base; sin una segunda llave de orden, el resultado puede cambiar entre ejecuciones (de hecho en nuestra prueba apareció en un orden distinto al ordenado por emp_no). Regla: todo ORDER BY con empates posibles lleva desempate.

## 12. Una función de agregación resume muchas filas en un número.

41–44 min. Las funciones de agregación reciben muchas filas y devuelven una: COUNT cuenta, MIN y MAX dan los extremos, AVG el promedio y SUM el total. Aquí: 240,124 salarios vigentes, entre 38,623 y 158,220, promedio 72,012 y una nómina de 17,291,866,123. Segundo clic: la mediana es el valor que deja la mitad de las personas por debajo; aquí es 69,805. Cuando los datos tienen valores extremos, mirar ambos evita conclusiones apresuradas.

## 13. GROUP BY hace una cuenta por cada grupo.

44–46 min. Imaginar que las 300,024 filas se reparten en dos montones según gender y luego se cuenta cada uno: 179,973 y 120,051. Cada punto de la figura son unas 10,000 personas. Regla: en un SELECT con GROUP BY, cada columna que no es una función de agregación debe estar en el GROUP BY. Pregunta al grupo: ¿por qué sumar 179,973 + 120,051 devuelve 300,024? Porque cada persona cae en exactamente un montón.

## 14. Una función de fecha te deja agrupar por año.

46–48 min. YEAR() extrae el año de una fecha; MONTH(), DAY() y DATE_FORMAT() hacen lo mismo con otras partes. Con GROUP BY YEAR(...) contamos contrataciones por año. La gráfica baja de 36,150 en 1986 a 1,514 en 1999. Segundo clic: el 2000 tiene 13 porque la última fecha de contratación del archivo es 2000-01-28; leerlo como «la empresa dejó de contratar» sería inventar. Ese es el tipo de límite que conviene decir en voz alta.

## 15. HAVING filtra grupos; WHERE filtra filas.

48–50 min. La diferencia clave: WHERE descarta filas antes de formar grupos; HAVING descarta grupos después de contarlos. Seguir la tabla de etapas: 331,603 filas, 240,124 vigentes, 9 departamentos, 3 con más de 30,000 personas. No se puede poner COUNT(*) dentro de un WHERE porque el conteo aún no existe en esa etapa. Los códigos d005, d004 y d007 se leerán como nombres cuando unamos tablas.

## 16. CASE convierte una regla de negocio en una columna.

50–52 min. CASE es el «si… entonces…» de SQL. Revisa cada WHEN en orden y se queda con el primero que se cumple, por eso las condiciones van de menor a mayor. Los cortes de 50, 70 y 100 mil los inventamos nosotros; si el negocio define otras bandas, el resultado cambia, y por eso conviene escribirlas explícitas. Comprobación útil: las cuatro bandas suman 240,124, igual que los salarios vigentes: ninguna fila se perdió ni se duplicó.

## 17. Una tabla de historial guarda varias filas por persona.

52–54 min. Una persona puede tener muchas filas: la 10001 tiene 17 salarios entre 1986 y 2002. La fila con to_date = 9999-01-01 es el sueldo vigente (88,958); la fecha lejana es el truco de esta base para decir «aún no termina». Segundo clic: el promedio de todas las filas es 63,811, pero el de los vigentes es 72,012. Cada persona cuenta tantas veces como filas de salario tiene. Pregunta al grupo: ¿qué pregunta de negocio responde cada promedio?

## 18. JOIN une tablas por una columna en común.

54–57 min. Un JOIN une filas de dos tablas cuando una columna coincide: ON de.emp_no = e.emp_no. Encadenamos dos uniones para pasar de empleado a departamento y de código a nombre. Resultado: 10001 trabaja en Development; 10010 pasó de Production a Quality Management en 2000, por eso aparece en dos filas. Los apodos e, de y d acortan la consulta. Error típico: olvidar la condición ON; lo veremos más adelante con números.

## 19. INNER descarta a quien no tiene pareja; LEFT lo conserva con NULL.

57–60 min. Demo interactiva. Primero INNER JOIN: solo quedan las tres personas que aparecen en dept_manager; las otras tres desaparecen sin aviso. Después LEFT JOIN: se conservan todas las filas de la tabla izquierda (employees) y donde no hay pareja aparece NULL. En toda la base: INNER devuelve 24 filas; LEFT devuelve 300,024, de las cuales 300,000 llevan NULL. NULL es información: dice que esa persona nunca fue gerente. Pregunta al grupo: si nos piden «todas las personas y, si fueron gerentes, de qué departamento», ¿cuál usamos?

## 20. Un JOIN puede multiplicar filas; cuenta lo que de verdad quieres contar.

60–63 min. Cada persona tiene varios salarios; al unir employees con salaries, cada persona se repite una vez por salario: pasamos de 300,024 a 2,844,047 filas y el promedio cae a 63,811. Si unimos solo el salario vigente (condición to_date), queda una fila por persona con salario: 240,124. Tercer renglón: un JOIN sin condición cruza todas las filas con todas: 300,024 por 9 departamentos, 2,700,216 filas sin sentido. Hábito: comparar siempre el conteo antes y después de un JOIN.

## 21. Una subconsulta es una consulta dentro de otra.

63–66 min. Una subconsulta va entre paréntesis y se ejecuta primero; su resultado se usa en la consulta de afuera. Caso 1: devuelve un número (el promedio vigente, 72,012) para compararlo con cada salario; 107,706 de 240,124 lo superan. Caso 2: devuelve una lista (los emp_no de gerentes) para usarla con IN. Es otra forma de responder lo que a veces se resuelve con JOIN; elegir la más legible. Advertir que subconsultas muy anidadas se vuelven difíciles de leer.

## 22. La base lee tu consulta en un orden distinto del que la escribes.

66–70 min. Resumen de la parte de conceptos. La consulta se escribe con SELECT arriba, pero la base la procesa así: une tablas (331,603 filas), filtra filas con WHERE (240,124), agrupa (9 grupos), filtra grupos con HAVING (3), calcula las columnas del SELECT, ordena y corta. Esto explica por qué un alias definido en SELECT no se puede usar en WHERE, y por qué WHERE y HAVING no son intercambiables. Cada clic agrega una etapa con el número real de filas o grupos que quedan. Comprender: cada etapa solo ve lo que dejó la anterior.

## 23. Escribe primero la pregunta de negocio; la consulta viene después.

50–62 min. Ejercicio de traducción pregunta → consulta, en cuatro pasos por pregunta. 1) Leer la pregunta. 2) Escribir las piezas en español: qué se cuenta, de qué tabla, qué filas valen, cómo se agrupa. 3) Escribir la consulta. 4) Comprobar el resultado. Pedir que el grupo escriba las piezas en papel antes de cada clic. Pregunta A: 240,124 personas trabajan hoy (no 300,024). Pregunta B: Sales paga más (88,853) y Human Resources menos (63,922); nueve filas en total. En el laboratorio, paso 6, resuelven la pregunta C por su cuenta. Error típico: escribir la consulta sin decidir qué cuenta como «hoy».

## 24. Cuatro errores clásicos y cómo se ven en los números.

62–70 min. Cierre de la parte práctica con cuatro trampas reales ya vistas. Para cada una, mostrar el síntoma con números: 331,603 contra 300,024; 63,811 contra 72,012; 2,700,216 filas; 869 contra 722. Insistir en que ninguna produce un error de sintaxis: la consulta corre y entrega un número equivocado. Hábito para el laboratorio: antes de confiar en un resultado, contar filas y compararlas con lo que se esperaba.

## 25. Pausa. Vuelve con tu terminal abierta.

70–80 min. Pausa real. Al volver, cada persona abre Cloud Shell y entra a su VM con gcloud compute ssh. Si la VM está apagada, enciéndela con gcloud compute instances start. Si algo falla, anotar el mensaje de error completo: servirá para el paso 1 del laboratorio.

## 26. Hoy escribes seis bloques de consultas.

80–150 min. Una sola slide para el laboratorio: la guía completa (código, salida esperada, comprobación y error frecuente) está en laboratorio.html. Paso 1: 12 min; 2: 10; 3: 12; 4: 12; 5: 12; 6: 12. Cada paso termina con tres ejercicios cuya respuesta numérica está en el archivo SQL para que cada persona verifique sola. Recomendar abrir la guía en una pestaña y la terminal en otra. Si un paso no sale, leer el «error frecuente» de la guía antes de pedir ayuda.

## 27. Una consulta responde lo que contó, no lo que significa.

150–168 min. Cierre honesto. A la izquierda, lo que las consultas realmente demuestran con estas tablas; a la derecha, saltos que alguien podría dar sin darse cuenta. Recorrer fila por fila con las cifras reales: 240,124 contra 300,024; 72,012 y 69,805; 72,045 contra 71,964 (una diferencia de 81, 0.1 %) que no demuestra igualdad porque no se controló nada más; el 2000 se debe al corte del archivo; Ventas 88,853. Último clic: la base es de muestra generada, así que estas lecturas son ejercicios de criterio, no hallazgos.

## 28. Practica por tu cuenta con tres preguntas más.

168–180 min. Tres preguntas extra para hacer sin ayuda; las respuestas numéricas están en la slide para que cada persona verifique. La 1 usa WHERE y COUNT con SUM(gender = 'F'); la 2 usa COUNT(DISTINCT) sobre dept_emp; la 3 usa GROUP BY sobre titles y luego un resumen. Último clic: apagar la VM al terminar evita el cargo de cómputo; los datos se conservan en su disco. Cierre: los cinco hábitos de la sesión: escribir la pregunta, decidir qué es una fila, filtrar lo vigente, verificar el conteo, decir qué no demuestra.
