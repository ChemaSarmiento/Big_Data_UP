# Sesión 4 · Un cero puede decidir la compra por ti

Gran idea: Cada exclusión necesita una regla explícita, evidencia y un responsable.

Guion para presentar en vivo. [pausa 3 s] indica silencio deliberado. Los controles se activan por el docente; no hay avance automático.

## 01. Un cero puede decidir la compra por ti.

0–4 min. Retomar C4 del archivo Bronze. Pedir que el comité explique si aprobaría la compra. [pausa 3 s] El cero podría ser promoción, error u otra convención; hoy la regla docente exige precio positivo y se tiene que justificar. No convertimos la regla en una ley universal ni inventamos el precio que falta.

## 02. La regla de precio cambia quién puede compararse.

4–10 min. Pedir predecir el efecto antes del botón. Barras con origen cero y escala común. El cero se muestra como punto, sin fabricar una barra de longitud positiva. Aplicar regla excluye C; entre las observaciones válidas de este ejemplo, A es menor. No implica disponibilidad, precio actual ni que C sea una tienda cara. El botón filtra una miniatura local, no consulta GCP.

## 03. Silver hace explícitas las condiciones para usar una fila.

10–15 min. La pregunta central es qué condiciones necesita el análisis, no si un dato es bueno en abstracto. Conservar la versión cruda hace posible revisar una regla y reconstruir el resultado. Aceptar una fila solo certifica las reglas aplicadas, no todas las condiciones de comparación.

## 04. Cero, ausencia y texto inválido piden tratamientos distintos.

15–19 min. El fixture contiene un cero, no necesariamente los otros dos ejemplos. NULL no vale cero. Reemplazar valores ausentes con0 puede fabricar una oferta. Preguntar qué harían en préstamos o reseñas: el cero puede ser perfectamente válido en otro dominio. La regla nace del significado del dato.

## 05. SAFE_CAST revela un fallo de conversión sin arreglarlo.

19–23 min. Consulta completa de demostración. SAFE_CAST convierte errores de ejecución de la conversión en NULL; no corrige el contenido. Conversiones imposibles entre tipos todavía pueden fallar en análisis estático. En nuestro script se conservan campos crudos en la tabla de rechazadas. Nunca rellenar fecha de hoy para ocultar el fallo.

## 06. Normalizar texto no demuestra que dos productos sean iguales.

23–27 min. Fragmento de expresión, no consulta completa aislada. UPPER/TRIM reduce variaciones de formato de la tienda; no prueba equivalencia de productos. Solo normalizamos establecimiento en el fixture. La unidad y presentación requieren reglas de negocio y posible conversión validada; S5 definirá la canasta.

## 07. Una copia exacta y otra observación no son lo mismo.

27–31 min. SELECT DISTINCT * implementa la política acotada de copias exactas del fixture. Dos filas con mismo ID y contenido distinto seguirían existiendo: hay que detectarlas e investigarlas. En fuentes reales, incluso registros idénticos pueden ser eventos legítimos; decidir clave y política con el responsable. Bronze permanece intacta.

## 08. Cada regla necesita una prueba y una consecuencia.

31–35 min. Este contrato mínimo coincide con el CASE suministrado. Marca y presentación son necesarias para comparar en Gold, pero este script no las valida plenamente: señalar esa limitación. Una regla no aplicada no debe aparecer como garantía. El CASE registra el primer motivo según prioridad, no todas las incidencias de la fila.

## 09. Clasificar conserva tanto el resultado como la explicación.

35–39 min. Separar tres destinos contables sin superposición. La copia se retira del trabajo, no del original. Rechazadas conserva datos originales y motivo; no es una papelera. El linaje mínimo del fixture usa archivo_origen e id; una fuente real necesita versión/lote para resolver IDs reutilizados.

## 10. Ninguna fila debe desaparecer sin explicación.

39–45 min. Pedir anticipar destinos antes de pulsar. La prima solo distingue visualmente la copia; no cambia el ID real A1. Señalar C4 precio inválido y C5 fecha inválida. Cada fila entra en un destino; no sumar incidencias múltiples como filas. [pausa 3 s] Una cuenta que no cierra bloquea la publicación del resultado.

## 11. Gobernar es decidir quién puede cambiar la regla.

45–49 min. No hacen falta tres puestos distintos; sí responsabilidades explícitas. Si alguien solicita aceptar precios0, se necesita una decisión documentada y una versión de regla, no un cambio silencioso en SQL. Retención debe tener responsable, criterio y revisión. No inventar un plazo legal universal.

## 12. El permiso técnico no determina el uso permitido.

49–53 min. Referencias del syllabus para reconocer contextos, no asesoría de aplicabilidad legal. GDPR tiene alcance y principios propios; HIPAA se aplica a entidades cubiertas y asociados, no a todo archivo que mencione salud. Precios ficticios no son datos clínicos. Para el proyecto identificar origen, datos personales y revisión pertinente; no afirmar cumplimiento por usar GCP.

## 13. Carrefour vincula colaboración con controles sobre los datos.

53–57 min. Carrefour reportó usar BigQuery data clean rooms para colaborar con socios manteniendo protección de datos de clientes y estratégicos. Es testimonio publicado por Google Cloud, sin ROI cuantificado aquí. La plataforma admite reglas de análisis; este dibujo es conceptual. Transferencia: escribir restricciones de consumo. No desplegamos una clean room ni asumimos que el laboratorio ofrece sus garantías.

## 14. Particionar ayuda cuando la consulta puede descartar fechas.

57–61 min. El dibujo agrupa días por mes; PARTITION BY fecha_observada crea particiones diarias. Un filtro elegible permite pruning; medir en el job. El fixture real solo tiene enero y es pequeño: no demostraría este ahorro. Clustering organiza bloques por otras columnas; no es lo mismo que partición.

## 15. Rechazar registros también reduce la cobertura.

61–65 min. Conteos del fixture aceptado: A5,B5,C3; cada tienda tenía cinco productos previstos. La copia de A no era otro producto. El gráfico comunica cobertura, no que C sea barata o cara. ¿Se concentran exclusiones por zona o periodo en su fuente? Esa pérdida puede sesgar una comparación incluso con reglas correctas.

## 16. Vuelve con Bronze y sus 16 filas identificadas.

65–75 min. Pausa. Confirmar tabla curso_bronze.observaciones_raw de S3. Si falta, la guía tiene restauración ilustrativa, que debe declararse. No preparar transformaciones contra un proyecto ajeno.

## 17. Mide la entrada antes de ejecutar una transformación.

75–80 min. Revisar proyecto y región. Si falta Bronze, volver a S3 o ejecutar01_fixture_bronze.sql en laboratorio autorizado y señalar recuperación. El resultado16 incluye copia y errores. No modificar fuente para forzar el conteo; localizar el archivo correcto.

## 18. Anticipa el motivo antes de ejecutar el CASE.

80–88 min. Fragmento para leer; ejecutar el script completo en el paso siguiente, no este CASE aislado. Una fila que falle fecha y precio recibe fecha_invalida por prioridad; no se cuenta dos veces. Leer también identidad_incompleta del script. Marcar qué no valida aún el contrato.

## 19. Ejecuta el script completo para conservar sus tablas temporales.

88–100 min. Copiar script completo en el editor de BigQuery y ejecutar como script. Las tablas temporales no son tablas persistentes para nuevas consultas independientes. Reemplaza solo destinos curso_silver; conserva Bronze. Si falla, guardar error, revisar permisos y proyecto; volver a ejecutar completo tras resolverlo. No prometer transacción atómica entre todos los destinos.

## 20. La reconciliación debe cerrar antes de continuar.

100–112 min. Comprobar con consulta a tablas persistentes. Una reconciliación correcta no valida todas las reglas, pero una incorrecta bloquea Gold. Si el ASSERT falla, no editar los números del reporte: investigar versión de entrada, scripts parciales y categorías. El reporte de fixture tiene únicas15 además de esos cuatro conteos.

## 21. Acota la fecha y registra lo que leyó BigQuery.

112–122 min. Consulta incluida en05_control_silver.sql. Ejecutar también control de IDs repetidos. El fixture no mide beneficio de particionar porque tiene poco volumen y una fecha; comparar sobre fuente docente preparada solo si costo y acceso están autorizados. Una salida correcta no prueba pruning por sí sola.

## 22. El responsable y el acceso deben quedar por escrito.

122–130 min. Completar matriz por capa, sin contraseñas. Si existe segunda identidad autorizada, comprobar lectura acordada; no cambiar permisos para hacer pasar la práctica. Si no existe, marcar pendiente. Conservar destinos para Gold y revisar recursos temporales, retención y costos con docente.

## 23. Otro equipo debe poder explicar por qué salió C4.

130–140 min. Transferencia al dataset distinto del equipo. La cadena C4 es modelo, no entregable obligatorio para todos. Identificar versión, fila, regla, motivo y responsable; prestar el registro al compañero para comprobar que puede reconstruirlo. Si falta linaje, registrarlo como pendiente.

## 24. Tu dominio decide qué significa un valor aceptable.

140–150 min. Adaptar reglas a biblioteca, reseñas u otra fuente asignada. No copiar validaciones de precio a todos los proyectos. El paquete y SQL base de cada dominio deben prepararse con docente. Si el esquema no está validado, documentar contrato propuesto y no presentar Silver como ejecutada.

## 25. Un dato que pasa las reglas todavía puede no compararse.

150–160 min. Retomar exactamente el problema del intro. Las reglas de tipos y precio positivo no establecen comparabilidad temporal. Pedir que un compañero nombre una condición faltante del proyecto y qué evidencia permitiría comprobarla. Eso será parte del contrato de Gold.

## 26. Entrega filas explicadas y responsabilidades verificables.

160–170 min. H4 del proyecto usa fuente propia; separar práctica guiada, ejecución propia y recursos preparados por docente. Adjuntar SQL y evidencia sin secretos. Si falta cuenta, declarar que se revisó el diseño o resultados suministrados. No dar por ensayado GCP desde una simulación HTML.

## 27. El cero salió; ahora tendrás que explicar lo que falta.

170–180 min. Volver a la tiendaC sin convertir ausencia en cero. Aun con13 filas aceptadas, una canasta incompleta no se compara como completa. Próxima sesión: catálogo y cobertura. Guardar evidencia y conservar capas necesarias; cerrar navegador no detiene otros recursos de la cuenta.
