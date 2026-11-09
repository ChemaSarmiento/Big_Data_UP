# BigQuery, arquitectura y Medallion · 180 minutos

Fuente: guion.py. Los conteos son de la muestra; ejecución GoogleSQL en GCP pendiente.

## 01. El precio menor necesita contexto.

0–5 min. Preguntar si recomendarían comprar hoy con esta pantalla. [pausa 3 s] La diferencia es real en la muestra; el salto a hoy no está sustentado. El ejecutivo debe identificar la población y la fecha antes de aprobar una decisión.

## 02. La muestra enseña el flujo; no describe todo el archivo.

5–10 min. Se leyeron 6 MiB en total: inicio, mitad y final; se seleccionaron 1500 registros completos por ventana. Las fechas vistas incluyen 2011, 2014 y 2015. No son el mínimo y máximo global. El archivo pesa 20663702126 bytes según Content-Range; tamaño distinto de bytes facturados por BigQuery.

## 03. BigQuery separa los datos del trabajo de consultarlos.

10–15 min. BigQuery es una plataforma analítica administrada: el usuario no dimensiona una VM por consulta. El servicio ejecuta trabajos, coordina cómputo y conserva resultados. El almacenamiento y la ejecución tienen costos y responsabilidades diferentes. No usarlo como sustituto automático de una base transaccional de caja.

## 04. Una consulta ocurre dentro de un proyecto.

15–20 min. Dibujar la ruta proyecto.dataset.tabla. El proyecto de ejecución paga el trabajo según configuración; el propietario del dato administra su almacenamiento. En consola el selector de proyecto y la región importan. Abrir un trabajo permite revisar bytes, tiempos y errores.

## 05. SQL expresa la pregunta; el motor decide cómo ejecutarla.

20–25 min. Lectura guiada: columnas, tabla, filas elegidas y agrupación. Este fragmento es para explicar SQL, no una comparación comercial válida: faltan marca, presentación y geografía. Pedir detectar esos filtros; el archivo05 contiene la versión completa. No se requiere que memoricen sintaxis.

## 06. LIMIT cambia la salida; el filtro puede evitar lectura.

25–30 min. Activar LIMIT: todas las particiones siguen relevantes. Activar un mes: el predicado sobre la columna de partición permite poda. En el laboratorio mediremos bytes reales; clustering puede reducir bloques y la estimación previa puede ser una cota superior. Una tabla pequeña puede no mostrar ahorro facturable.

## 07. La arquitectura depende del uso y del equipo.

30–37 min. Cambiar entre opciones. Warehouse: tablas analíticas gestionadas. Lake+warehouse: archivos originales y tablas curadas; copias y sincronización deben gobernarse. Lakehouse: formatos de tabla abiertos, catálogo y motores compatibles sobre objetos; más decisiones operativas. No afirmar que cualquier bucket más BigQuery ya equivale a un lakehouse abierto.

## 08. Para este taller basta conservar el original y servir tablas.

37–43 min. Propuesta para all_data completo: docente prepara el archivo en GCS, carga una vez en BigQuery y sirve tablas pequeñas. El alumno usa muestra descargable para evitar traslado de 20.7 GB durante clase. Variante warehouse directo viable para el laboratorio; no se requiere contratar BigLake, Spark ni streaming.

## 09. La frecuencia del dato define cómo llega.

43–50 min. QQP en archivos periódicos permite batch. Más servicios no crean datos más frescos que la fuente. CDC y streaming son alternativas para otras fuentes; no forman parte del despliegue del taller. Pedir qué SLA justificaría abandonar el lote.

## 10. Medallion organiza responsabilidades sobre el dato.

50–55 min. Medallion es un patrón de capas de calidad, compatible con varias arquitecturas físicas. No es un servicio de GCP ni exige tres tecnologías diferentes. Aquí son datasets separados; otras organizaciones pueden resolverlo con esquemas, tablas o productos.

## 11. Bronze conserva lo que llegó, incluso sus problemas.

55–59 min. Mantener 15 columnas como STRING en entrada evita inferencias incorrectas de tipos. Bronze conserva los valores y duplicados, con un hash técnico de fila y un lote. La copia CSV original conserva bytes y cabecera; la tabla no es una copia binaria del archivo.

## 12. Silver hace explícitas las reglas de confianza.

59–63 min. La muestra contiene 3000 municipios con espacios finales y cero precios no positivos. No inventar errores para prometer rechazos. SAFE_CAST devuelve NULL ante un dato inválido; definir reglas de negocio después del parseo. Estado histórico se conserva: no convertir Distrito Federal a CDMX sin tabla de equivalencias aprobada.

## 13. Gold conserva el grano de la comparación.

63–67 min. No sumar precios como ventas. Gold produce precio por producto/tienda/día y luego comparación por producto/día/municipio. Si hay más de un precio en el grupo, se marca conflicto y se excluye ese valor del ranking. S/M significa marca no especificada: no demuestra equivalencia entre marcas desconocidas.

## 14. Cada capa necesita un dueño y una regla de acceso.

67–70 min. El ejecutivo exige responsable de actualización, acceso y retención. Los datasets separados permiten asignar permisos; el taller no configura políticas de producción automáticamente. La trazabilidad acompaña cada entrega.

## 15. Pausa. Abriremos el dato que acabamos de discutir.

70–80 min. Confirmar acceso al proyecto docente, facturación y permisos antes de continuar. No crear cuentas o recursos de pago a ciegas durante clase. Si falta acceso, seguir el perfil y consultas como revisión, dejando ejecución pendiente.

## 16. Carga la muestra con un esquema explícito.

80–95 min. Paso1: abrir BigQuery Studio, ejecutar 00 y cargar CSV local en emergente_bronze.entrada. Cabecera1, comillas dobles, UTF8, sin autodetección. Esquema descargable. Seguir guía si el asistente cambia de nombre.

## 17. Registra un lote que puedas reconocer mañana.

95–105 min. Paso2: ejecutar 01 completo. La protección es serial por ID de lote; no es un sistema transaccional multiusuario. Mantener proyecto aislado por equipo. Para el archivo completo cambiar ID y fuente, no el contrato de campos.

## 18. Perfila antes de aceptar una regla.

105–115 min. Paso3:02_perfil.sql. Revisar mínimo/máximo de la muestra, duplicados exactos y conversiones. La falta de errores en una muestra no garantiza calidad global. Identificar el par deREFRESCO/SPRITE con el mismo periodo y presentación.

## 19. Tipa, clasifica y conserva los rechazos.

115–130 min. Paso4: ejecutar 03 completo. Reconstruye Silver desde Bronze y crea copia plana parabenchmark. Filtra fechas al consultar la particionada. Los hashes derivados no son IDs oficiales ni resuelven cambios de dirección. No confundir limpieza textual con identidad comercial.

## 20. Publica una comparación con sus condiciones.

130–140 min. Paso5:04_gold.sql. Abrir detalle y agregado. Explicar que no existe cobertura de todas las tiendas ni inventario. Se construyeGold pequeña para consultas repetidas, pagando la transformación y el almacenamiento correspondientes.

## 21. Optimiza la misma pregunta, no una respuesta distinta.

140–150 min. Paso6: ejecutar cada SELECT de 05 por separado, caché desactivada. Registrarjob ID, bytes estimados/procesados/facturados y tiempo. A/B comparan organización física. C solo es equivalente si no hay conflictos. La muestra puede quedar bajo mínimos de facturación; no prometer porcentajes.

## 22. Conserva la prueba y retira la copia temporal.

150–160 min. Paso7: entregar controles y registro-optimizacion.csv. Revisar expiraciones. Cerrar pestaña no elimina almacenamiento; no borrar datasets ajenos niBronze por comodidad. El ensayo del archivo completo queda a cargo del docente antes de impartir.

## 23. La tarea comienza cuando llega otro archivo.

160–165 min. Descargar un corte oficial QQP acotado. No reemplazar all_data ni mezclar todo el histórico antes de revisar esquema. Es una tarea posterior, no descarga masiva en la última parte de clase. La página oficial y checklist están en tarea.html.

## 24. Un nombre de columna nuevo exige una decisión explícita.

165–170 min. Ejemplos de mapeo condicionales, no esquema ya verificado de2026. Abrir cabecera real del nuevo archivo y registrar tipo, unidad, codificación y fecha. No fabricar marca o presentación para que el flujo pase. Si no es compatible, detener ese lote y documentar.

## 25. Reprocesar el mismo lote no debe duplicar Silver.

170–175 min. Ruta inicial: reconstrucción completaSilver/Gold; simple y comprobable, pero vuelve a leerBronze. La optimización futura es procesar lotes nuevos y recalcular particiones afectadas, con revisiones y llegadas tardías. Nunca llamar incremental a nuestro03. La tarea exige prueba de repetición y conflictos.

## 26. Entrega una actualización que otra persona pueda auditar.

175–180 min. Cada equipo justifica arquitectura, forma de actualización y una decisión que sí permite la fuente. Pedir una limitación por escrito. Entregar original,SQL y evidencia; no solo captura del precio menor.
