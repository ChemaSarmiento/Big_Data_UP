# Storyboard de sesión 1 — Una decisión necesita una arquitectura

**Estado:** borrador para revisión; no es una presentación implementada. Sesión total: 180 min. El piloto visual será un subconjunto de 8–12 slides de este guion.

**Audiencia:** ejecutivos que deben comprender, consultar y decidir. **Promesa:** terminar con una pregunta acotada, mapa de datos y entorno GCP listo. **Tensión:** dos precios pueden parecer comparables y esconder productos, fechas o coberturas diferentes.

## Recorrido propuesto

| # | Mensaje / pantalla | Visual o interacción | Propósito y evidencia |
|---|---|---|---|
| 1 | ¿Confiarías esta compra a un archivo que no puedes revisar? | Archivo → recomendación, con la conexión aún incompleta | Abrir el dilema sin vender una herramienta |
| 2 | La misma cifra puede contestar preguntas distintas | Tres tarjetas: precio, fecha, presentación; revelar campos por clic | Identificar contexto faltante |
| 3 | Antes de comparar, acuerda qué estás comprando | Mini-canasta; elegir «misma tienda» o «varias tiendas» | Mostrar que el objetivo cambia el KPI |
| 4 | Al terminar podrás rastrear una recomendación hasta su fuente | Dashboard → KPI → regla → observación | Mostrar el producto final, como mockup rotulado |
| 5 | La escala cambia cómo lees y procesas la información | Laptop y motor distribuido; repartir bloques por clic | Explicar paralelismo y coordinación; no declarar un umbral universal de GB |
| 6 | El volumen no compensa datos incomparables | Cinco V conectadas al caso PROFECO | Dar teoría con un problema por V |
| 7 | La nube separa el recurso que guardas del que usas | Storage persistente; cómputo que se enciende y apaga | Diferenciar Big Data y cloud |
| 8 | Registrar operaciones y analizar historia son trabajos distintos | OLTP/OLAP con dos preguntas concretas | Preparar puente MariaDB → BigQuery |
| 9 | Warehouse, lake y lakehouse resuelven necesidades diferentes | Tres arquitecturas pequeñas; revelar consumidor y contrato | Explicar ventajas y límites sin catálogo de marcas |
| 10 | Cada capa de Medallion agrega una promesa verificable | Una observación viaja Bronze → Silver → Gold | Mantener registro visible; calidad no es solo cambiar de carpeta |
| 11 | Bronze guarda lo recibido y su procedencia | Tarjeta de manifiesto, archivo y fecha de ingestión | Diferenciar fecha de ingestión y fecha observada |
| 12 | Silver hace explícitas las reglas de aceptación | Precio imposible va a rechazados; valor válido continúa | Datos de ejemplo rotulados como ilustrativos |
| 13 | Gold define qué significa una comparación justa | Canasta completa vs. incompleta | No concluir «más barato» sin cobertura |
| 14 | La latencia importa cuando cambia la acción | Elegir batch/streaming según decisión; revelar trade-off | Mantener tiempo real dentro del mapa moderno sin programarlo |
| 15 | Mercado Libre conecta el almacén con productos de análisis | Diagrama propio basado en la fuente, con fecha y enlace | Caso real; no atribuir Medallion ni Looker Studio si la fuente no lo dice |
| 16 | Nuestra primera entrega es una pregunta y un mapa | Ruta de ocho sesiones e hitos | Explicar qué se construye hoy y qué después |
| — | Pausa | — | Fin de primeros 65 min; 10 min de descanso |
| 17 | Laboratorio: verifica tu cuenta y el proyecto activo | Checklist de elegibilidad, proyecto, permisos y crédito | Ningún secreto en capturas; alternativa docente si no hay acceso |
| 18 | Un presupuesto avisa; no detiene el consumo | Diagrama gasto → aviso → acción responsable | Paso exacto en Billing con ubicación de UI por verificar |
| 19 | El bucket conservará la evidencia original | Esquema de nombre y ubicación compatible con BigQuery | Ruta UI + parámetros resueltos; no nombres globales idénticos |
| 20 | El inventario te dice qué existe, no si sirve | Extracto real de `metadata.json`; resaltar lo que no contiene | Distinguir tamaño de esquema, licencia y calidad |
| 21 | Una muestra útil conserva el contexto de la decisión | Muestra docente + manifiesto y reglas de selección | No fingir representatividad ni cargar el archivo completo en laptop |
| 22 | Define una compra que puedas justificar | Ficha con periodo, zona, canasta, alternativa y audiencia | Actividad de equipo; el periodo se elige tras perfilar fuente |
| 23 | Asigna un responsable a cada promesa del dato | Mapa de origen, validación, acceso y consumo | Primer borrador de gobernanza |
| 24 | Dibuja de dónde saldrá cada KPI | Diagrama editable con Bronze/Silver/Gold | H1: explicación por el equipo, no memoria de nombres de servicio |
| 25 | Comprueba que otro equipo entiende tu pregunta | Tres preguntas de revisión entre pares | Audiencia, comparabilidad, evidencia faltante |
| 26 | Hoy preparamos el entorno; la próxima vez consultaremos | Checklist H1, cierre y avance a SQL `employees` | Evidencia de acceso, mapa, pregunta y recursos que quedan activos |

Los mensajes interrogativos abren una exploración; las conclusiones se revelan cuando la evidencia las sostiene. No usar porcentajes o precios aparentando un hallazgo real hasta ejecutar los datos.

## Piloto visual propuesto

Probar 10 pantallas representativas: 1, 2, 5, 7, 8, 10, 13, 15, 18 y 24. Incluyen portada, contexto, teoría, diagrama, comparación, fuente externa, paso de laboratorio y entregable. El código descargable y las instrucciones extensas irán en la guía, no en bloques ilegibles sobre la proyección.

**Revisión del piloto:** proyección 16:9, un portátil, móvil para consulta, teclado, selección de texto/código, controles interactivos, regresar tras un revelado, enlaces profundos, fade y movimiento reducido. No dar por aprobado el estilo solo porque el build termine.
