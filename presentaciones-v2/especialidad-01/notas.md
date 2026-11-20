# Sesión 1 · Antes de elegir una herramienta, entiende el problema

Gran idea: Un problema de datos es «grande» cuando una restricción te detiene; entenderlo y montar tu ambiente viene antes de elegir tecnología.

Guion para presentar en vivo. [pausa 3 s] indica silencio deliberado. Los controles se activan con clic o con las flechas; no hay avance automático.

## 01. Antes de elegir una herramienta, entiende el problema

0–2 min. Abrir con la promesa: hoy no hay código pesado. Se sale con dos cosas: un criterio para decidir cuándo un problema de datos exige una inversión seria (y cuándo es sobre-ingeniería) y un ambiente propio en la nube, listo para las demás sesiones. Pregunta de entrada: ¿alguien ha estado en una reunión donde se propuso «usar big data» para algo que se resolvía con un reporte en Excel? Escuchar una o dos respuestas, sin nombres.

## 02. Dos preguntas de un mismo banco piden arquitecturas distintas.

2–6 min. Dibujar la diferencia con las dos tarjetas. Reporte: 50 MB, cabe en la memoria de cualquier laptop, nadie sufre si tarda un minuto. Fraude: millones de eventos, cada uno exige una decisión en segundos. Preguntar al grupo: ¿necesitan la misma arquitectura? Dejar que respondan antes del clic. Las cifras son supuestos del caso, no mediciones. Idea a clavar: la pregunta útil nunca es «cuántos datos tenemos», sino «qué decisión hay que tomar, con cuánta demora tolerable y qué trabajo impide cumplirla».

## 03. Un dato es un hecho suelto; solo sirve cuando apoya una decisión.

6–9 min. Definir con el ejemplo, un paso por clic. Dato: «Centro, 12 ventas, $4,800» no dice nada por sí solo. Información: al comparar sucursales aparece algo que se puede leer. Decisión: la acción que alguien puede tomar. Insistir en que toda la sesión (y el curso) se mide contra esta cadena: si no hay decisión al final, el dato guardado no vale nada. Las cifras son un ejemplo inventado para ilustrar.

## 04. Un problema es «grande» cuando una restricción te detiene, no por su peso.

9–13 min. Es la definición de trabajo de big data para todo el curso: no existe un número mágico de GB. Un problema se vuelve de big data cuando lo que exige (volumen, velocidad, variedad, confiabilidad) supera lo que permiten tu memoria, tu plazo, tu gente y tu dinero. Un archivo de 20 GB puede resolverse en una máquina si el plazo es amplio; una aplicación pequeña puede exigir otra arquitectura si hay que responder en segundos. Pausar [pausa 3 s] y pedir un ejemplo de su propia industria donde la restricción sea el plazo y no el tamaño.

## 05. Ocho sesiones: de entender el problema a defender una recomendación.

13–15 min. Una línea con las ocho sesiones, sin explicar ninguna todavía. Cada sesión dura 180 minutos y tiene teoría, un laboratorio guiado con pasos, y cierre. Hoy: concepto y ambiente. Mañana empieza SQL. Cerrar el bloque de apertura y pasar a los conceptos.

## 06. Cinco preguntas miden qué tan «grande» es un problema de datos.

15–18 min. Una V por clic; antes de revelar el ejemplo, preguntar «¿alguien tiene un ejemplo de su propia industria para esta V?». Volumen y velocidad son las que más se citan; variedad y veracidad son las que más duelen en la práctica; valor es la que más se olvida y la más cara de ignorar. Ejemplo de salud para contrastar: un hospital que analiza 500 expedientes en Excel no tiene un problema de big data; una red que cruza millones de expedientes con datos genómicos y de sensores sí. Las cinco preguntas son un marco para conversar, no un examen con puntaje.

## 07. Volumen: un archivo deja de abrirse entero cuando supera tu memoria.

18–21 min. Las barras son un orden de magnitud, no mediciones: 50 MB (reporte del caso), 16 GB (memoria de una laptop típica, supuesto), 20 GB y 100 GB (ejemplos). La idea es sentir cuándo cruzas el límite de memoria. Cruzarlo no hace imposible el trabajo: significa leer por partes, ir a disco o repartir entre máquinas, lo que veremos en tres slides. Dato verificable: una hoja de Excel tiene un máximo de filas por hoja; pasar de ahí obliga a cambiar de herramienta antes de hablar de big data.

## 08. Velocidad: lote o flujo depende de cuándo alguien debe actuar.

21–24 min. Lote: se junta el trabajo y se procesa de una vez (el reporte mensual). Flujo: se procesa cada evento al llegar (la alerta de fraude). Pedir al grupo que diga cuánta demora aceptaría su organización en una decisión concreta. Aclarar un malentendido frecuente: más servicios no hacen los datos más frescos que su fuente; si el archivo llega una vez al día, un flujo continuo no mejora nada. Lote simplifica la recuperación y la repetición; el flujo reacciona antes a cambio de mantener operación continua.

## 09. Antes de distribuir, pregunta si una sola máquina lo resuelve.

24–27 min. Tres preguntas, un clic cada una. Es la herramienta de decisión central de la sesión: no distribuir por prestigio sino por restricción. Si se responde «sí» a las tres, una base de datos normal o incluso una hoja bien usada basta. La sobre-ingeniería no solo cuesta dinero de infraestructura: cuesta el tiempo de un equipo técnico construyendo algo que nadie necesitaba. Pedir al grupo que clasifique un caso de su trabajo antes del último clic.

## 10. Distribuir es repartir el trabajo y luego combinar los resultados.

27–30 min. Pulsar 1, 2, 3, 4 y 6 personas y leer el resultado. Con una persona son 12 minutos; con tres, 4 minutos más el tiempo de sumar los tres conteos; con seis, 2 minutos más combinar. Es el mismo principio de los sistemas distribuidos: dividir el trabajo en partes independientes, procesarlas en paralelo y combinar. Dos matices que importan después: combinar y repartir también cuestan, y si una persona recibe más cajas que las demás, el trabajo termina cuando termina la más lenta. Nada de esto se mide aquí: es un modelo con supuestos.

## 11. Registrar una compra y analizar el año son dos trabajos distintos.

30–33 min. Primero el lado de registrar: una compra es una escritura pequeña y frecuente; lo importante es que no quede a medias (si se cobra, debe quedar guardada). Luego el lado analítico: leer años de historia y resumirla. Por eso la base que registra las compras rara vez es la mejor para analizar todo el historial. Siglas: OLTP (procesamiento transaccional en línea) y OLAP (procesamiento analítico en línea). Más adelante, en SQL, usarás una base relacional con datos de empleados; ahí verás el lado analítico con consultas reales.

## 12. Warehouse, lake y lakehouse: tres formas de guardar datos para analizarlos.

33–36 min. Son definiciones, no un camino obligatorio. Warehouse: tablas ordenadas, ideal para SQL. Lake: lo que llega, tal cual, barato de guardar pero con menos orden. Lakehouse: busca juntar lo mejor de los dos con garantías de gestión de tablas sobre archivos. No decir que cualquier carpeta de archivos más una base ya equivale a un lakehouse. En las siguientes sesiones se verá una forma concreta de ordenar los datos por etapas; hoy solo importa conocer los tres nombres y su idea.

## 13. La nube es alquilar capacidad por uso en lugar de comprarla.

36–38 min. Definición de trabajo primero, luego el contraste. Alquilar permite empezar pequeño y crecer o apagar sin comprar nada; el precio es que el gasto continúa mientras haya recursos encendidos y que algunas decisiones siguen siendo tuyas. Una máquina virtual pequeña también es «nube»: no hace falta un clúster para usarla. En el laboratorio de hoy crearás justamente una máquina pequeña.

## 14. IaaS, PaaS y SaaS: cuánto administras tú.

38–40 min. Un clic por modelo. Cuanto más a la derecha, menos administras y menos control tienes. IaaS: te dan la máquina; instalas el sistema, el software y los datos. PaaS: te dan la plataforma; subes tu aplicación y tus datos. SaaS: usas la aplicación y administras tus datos y accesos. Hoy usarás IaaS (una máquina virtual con una base de datos instalada), porque queremos ver qué hay dentro; más adelante usarás servicios que administran por ti más capas.

## 15. Cuenta de facturación, proyecto y permisos: quién paga y quién puede hacer qué.

40–42 min. Dos ideas separadas: quién paga (la cuenta de facturación) y dónde viven los recursos (el proyecto). Un proyecto agrupa máquinas, discos y almacenamiento, y se identifica por un ID único que suele diferir del nombre que le pones; en los comandos se usa el ID. Después, permisos: un permiso es la combinación de quién, qué rol y sobre qué recurso. Principio de privilegio mínimo: nadie recibe «Propietario» para que algo funcione más rápido. Más adelante, cuando algo falle con «permiso denegado», este es el esquema para buscar la causa.

## 16. Región y zona: dónde corre tu máquina cambia costo, distancia y reglas legales.

42–44 min. Una región es una ubicación geográfica; una zona es un área de despliegue dentro de la región. El nombre completo junta ambas: us-central1-a. Cuatro razones para elegir con cuidado: precio, distancia, regulación y cercanía entre cómputo y datos. En este curso la máquina del laboratorio vive en us-central1-a; el curso no fija una región para todo: se elige según la política de la cuenta. Aclarar que la zona resaltada es la del laboratorio y que las demás existen sin necesidad de detallarlas hoy.

## 17. La nube cobra por lo que usas: tiempo de cómputo, GB guardados y datos que salen.

44–46 min. Tres medidores. Cómputo: se mide por tiempo de uso; una máquina apagada no consume cómputo. Almacenamiento: se paga por GB mientras exista el recurso. Red: la salida de datos tiene tarifa. Luego los tres estados de una máquina: encendida (cobra cómputo y disco), detenida (el cómputo se detiene, el disco sigue existiendo y cobrando según tu cuota) y borrada (todo se va, incluidos los datos). Detener no es borrar. Los precios cambian: se consultan en la calculadora de precios y no se memorizan.

## 18. Un presupuesto avisa; solo detener o borrar recursos frena el gasto.

46–48 min. Tres controles distintos. El presupuesto y sus alertas avisan, no frenan. El crédito de prueba es un medio de financiar práctica, no una mensualidad; según la documentación oficial incluye US$300 para clientes nuevos durante 90 días y un cupo de uso gratuito por producto (una e2-micro por mes en tres regiones de EE. UU., con 30 GB de disco estándar); condiciones, vigencia y elegibilidad deben verificarse en la cuenta de cada persona. Lo que realmente frena es detener o borrar recursos. Hoy configurarás un presupuesto en el laboratorio.

## 19. Cuatro organizaciones, cuatro preguntas de datos distintas.

48–49 min. Cuatro sectores del temario (banca, salud, logística, retail). No prometen ahorros ni garantizan resultados: son publicaciones de cada organización y se leen como ejemplos de qué preguntas se hicieron. Pedir al grupo que ubique cuál de las cinco V pesa más en cada uno (riesgo: volumen y plazo; genómica: volumen y variedad; entregas: velocidad; retail: volumen y valor). Las herramientas que aparecen se irán explicando después; hoy solo importa la pregunta.

## 20. Un mapa del ecosistema: cinco categorías para reconocer nombres.

49–50 min. Mapa de ciudad, no manual de manejo. No hace falta saber operar ninguna pieza hoy; sí reconocer el nombre cuando se mencione en una reunión. Las bases relacionales (MySQL, MariaDB, PostgreSQL) son la categoría con la que empezarás a trabajar en la sesión 2. Cerrar el bloque de conceptos y pasar a aplicarlos.

## 21. Decide tú: tres situaciones, una recomendación cada una.

50–56 min. Ejercicio individual. Dar un minuto por situación para escribir recomendación y razón; luego revelar. No hay una sola respuesta correcta: lo que se evalúa es el razonamiento con las tres preguntas (memoria, plazo, simultaneidad) y con la demora tolerable. A: sobre-ingeniería evitada. B: flujo porque la acción es inmediata. C: es el caso ambiguo y por eso el más valioso: se decide midiendo, no por tamaño. Preguntar a dos personas qué pondrían distinto y por qué.

## 22. Dimensiona un problema con una multiplicación.

56–63 min. Primero seguir el ejemplo en voz alta: filas por día × tamaño por fila = datos por día; luego por mes y por año. Es una estimación de orden de magnitud, no una medición: el tamaño por fila es un supuesto que se mide con una muestra. Tras el ejemplo, dar cinco minutos para que cada persona haga el cálculo del sensor antes del clic final. Resultado: 100 MB por hora, 2.4 GB por día, ≈ 876 GB al año. Conclusión para la discusión: la cifra anual cabe en un disco, así que la pregunta sobre repartir se decide por plazo y simultaneidad, no por tamaño.

## 23. Antes de crear una máquina, responde cinco preguntas.

63–70 min. Es el puente al laboratorio: cada respuesta ya se tomó, y conviene que cada persona entienda por qué. Región y zona por cercanía y cupo gratuito; tamaño pequeño porque basta para practicar SQL; acceso con usuario del curso porque es un entorno desechable con datos públicos (la regla de firewall abierta a internet y la contraseña compartida son prácticas que nunca deben replicarse con datos reales); costo claro; y una disciplina: apagar al terminar. Preguntar qué cambiarían si los datos fueran de clientes reales (acceso restringido por IP, credenciales individuales).

## 24. Pausa. Vuelve con la consola de Google Cloud abierta.

70–80 min. Pausa real, sin avance automático. Antes del laboratorio conviene tener abierta la consola de Google Cloud con la cuenta propia y una pestaña con la guía de laboratorio. Si una cuenta no puede crear un proyecto o activar la facturación, anotar el motivo exacto y seguir la guía como lectura; no activar pagos a ciegas.

## 25. Seis pasos para montar tu ambiente.

80–150 min. Seis pasos, 70 minutos; la guía completa trae dónde hacer clic, cada comando y la salida esperada. El paso 5 es el más largo porque MariaDB se instala sola dentro de la máquina y eso tarda unos 14 minutos en el ensayo; mientras tanto se explora la consola. Avanzar paso a paso y comprobar la salida antes de pasar al siguiente. Los pasos 1 a 4 se hacen en la consola y en Cloud Shell y no se ensayaron desde una cuenta nueva; los pasos 5 y 6 se ensayaron con una máquina real. Al final, detener la máquina para no gastar.

## 26. Tres ejercicios para practicar por tu cuenta.

150–165 min. Tres ejercicios individuales para repetir lo visto sin depender de nadie. Cada uno produce un resultado pequeño y comprobable. Sugerir que se hagan después de la sesión y que guarden las respuestas: sirven como base de comparación cuando más adelante trabajen con datos reales.

## 27. Qué puedes afirmar después de hoy, y qué todavía no.

165–172 min. Cierre honesto: cada columna separa lo que la sesión sí respalda de saltos que conviene evitar. Primera fila: el criterio es la restricción, no el tamaño. Segunda: la nube no es barata ni cara en sí; depende del uso y de lo que dejes encendido. Tercera: detener frena el cómputo, pero el disco sigue existiendo y puede cobrar. Cuarta: los casos son publicaciones de las propias organizaciones. Pedir una frase propia que empiece con «todavía no puedo afirmar que…».

## 28. Glosario mínimo para las próximas sesiones.

172–180 min. Catorce términos que se usarán sin volver a definirse. No hace falta memorizarlos: conviene volver a esta lámina cuando una palabra no se entienda. Cierre: la sesión 2 empieza con SQL sobre la máquina que dejaste lista hoy; antes de irte, comprueba que está detenida o encendida según lo que vayas a hacer, y que tu presupuesto existe.
