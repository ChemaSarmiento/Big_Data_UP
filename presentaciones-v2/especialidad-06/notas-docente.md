# Sesión 6 · La gráfica también puede torcer la decisión

Gran idea: Un dashboard útil mantiene visible qué comparación sostiene la decisión y qué falta.

Guion para presentar en vivo. [pausa 3 s] indica silencio deliberado. Los controles se activan por el docente; no hay avance automático.

## 01. La gráfica también puede torcer la decisión.

0–5 min. El comité recibe un tablero con54 como mejor compra. Pedir qué información exigirían antes de autorizar. [pausa 3 s] En S5 calculamos bien; hoy la responsabilidad está en cómo se muestra y comparte.

## 02. El título puede prometer más que los datos.

5–10 min. Ejemplo deliberadamente erróneo, no hallazgo sobre C. Antes de pulsar, pedir identificar el supuesto escondido. La corrección debe conservar54 como subtotal, comparar A150/B160 completas y explicitar el alcance histórico. Un título bonito no corrige una población mal definida.

## 03. Una pantalla debe responder a una decisión concreta.

10–15 min. Sustituir «quiero un dashboard» por una pregunta que alguien pueda resolver. En el ejemplo, comparar alternativas históricas; no prometer disponibilidad actual. Pedir audiencia y acción del proyecto propio.

## 04. Cada filtro cambia la interpretación.

15–20 min. Demostración local con los tres resultados conocidos de Gold; no conecta BigQuery. Elegir soloC: ninguna alternativa completa y costo desconocido. ElegirB: es menor solo entre las alternativas visibles, no universalmente. Volver aTodas. Pedir anticipar el título antes de cambiar.

## 05. La mirada necesita una jerarquía visible.

20–24 min. Dibujar dónde mira primero la audiencia. El gráfico sostiene el titular; el detalle permite verificarlo. No colocar seis tarjetas con igual peso visual. El espacio vacío separa funciones y reduce competencia.

## 06. Elige el gráfico por la comparación que necesitas.

24–28 min. No construir una serie de tiempo con el fixture: solo tiene una fecha. No inventar mapa sin geografía. El syllabus propone esos gráficos cuando la fuente los permite; el proyecto debe justificar su selección.

## 07. La longitud de una barra necesita un cero compartido.

28–31 min. Comparación entre completas del fixture, misma unidad y fecha. Truncar el eje de barras cerca de150 exageraría visualmente la diferencia. Etiquetar valores junto a barras evita buscar leyendas. No inferir ahorro futuro a partir de este ejemplo histórico.

## 08. El énfasis funciona cuando el contexto puede descansar.

31–34 min. Aplicar kit: un foco cromático, etiquetas directas y color acompañado de texto. El rojo señala atención, no necesariamente peligro. Evitar leyendas lejanas y efectos3D; las diferencias deben leerse sin depender del color.

## 09. Una tarjeta de total puede sumar alternativas incompatibles.

34–38 min. La suma no es un error aritmético; responde a otra pregunta. En el tablero conservar grano escenario+tienda. COUNT de registros y SUM pueden cambiar con duplicaciones o filtros. Menor costo debe filtrar elegibles y escenario antes de calcularse.

## 10. Un control no garantiza que todas las fuentes respondan.

38–42 min. Canastas y detalle son fuentes distintas; no asumir propagación automática de un control solo por tener columnas con el mismo nombre. Para la ruta base fijar el mismo escenario con filtros explícitos en cada fuente y usar controles separados rotulados por tienda. Probar cruces con SQL. No unir resumen al detalle y sumar costo repetido.

## 11. Una pantalla sin resultados necesita decir qué ocurrió.

42–45 min. RetomarSoloC del tablero local. Una visual vacía puede significar filtro, dato faltante o error de acceso; distinguir estados. En BI añadir mensaje de cobertura y tabla de incompletas. Nunca usar0 como marcador de costo desconocido.

## 12. Un buen título conserva su alcance al filtrar.

45–49 min. El prototipo calcula título dinámico; no promete que Looker Studio tenga el mismo mecanismo automáticamente. En la práctica base elegir título descriptivo que siga siendo verdadero al filtrar, o limitar interacción para una recomendación estática con alcance declarado.

## 13. Mercado Libre conecta la analítica con su consumo.

49–54 min. Caso ya trabajado: uso de BigQuery y Looker. No confundir Looker con Looker Studio ni atribuirle nuestro tablero. El aprendizaje de audiencia es una interpretación docente; no se presenta ROI propio ni se copia su arquitectura interna.

## 14. Compartir el informe también comparte una vía de acceso.

54–59 min. Configuración real depende de política y conector. En modo propietario, un lector puede ver gráficos sin acceso propio directo a BigQuery; compartir el enlace es relevante. En modo lector, cada lector necesita permisos apropiados. No usar publicación pública para sortear errores. Documentar modalidad y audiencia.

## 15. Cada consulta del tablero puede consumir recursos.

59–65 min. Interacciones y actualización pueden consultar BigQuery. Cerrar el informe no elimina fuentes ni tareas programadas existentes. No prometer que cada clic genera job ni que todo se sirve de caché. Revisar costos observados y política de refresco. Ensayar una pregunta de comité antes del laboratorio.

## 16. Vuelve con Gold y su consulta de control abiertas.

65–75 min. Pausa. Confirmar acceso y canastas del escenario previsto. Ruta principal Looker Studio según syllabus; documentación actual puede decir Data Studio. Si no hay acceso, usar prototipo local y CSV declarando que no se ensayó conexión cloud.

## 17. Conecta la tabla que ya responde a tu pregunta.

75–80 min. Paso1,5 min. Crear informe, añadir conector BigQuery y seleccionar tabla canastas. Confirmar proyecto de facturación y modalidad de credenciales con docente. No introducir contraseñas en la guía. Permisos faltantes se resuelven por responsable autorizado.

## 18. Fija el escenario y revisa los tipos antes de graficar.

80–88 min. Paso2,8 min. Revisar campos en fuente. Antes de agregación confirmar una fila por escenario/tienda. Para barras usar establecimiento y MAX(costo_completo_mxn), solo como valor de esa fila única; MAX no repara duplicados. Añadir filtro elegible=true a comparación, no a tabla de cobertura.

## 19. Muestra costo y cobertura en lugares distintos.

88–100 min. Paso3,12 min. Insertar barras horizontales, dimensión establecimiento, métricaMAX(costo_completo_mxn), escenario fijo y elegible=true; eje mínimo0 y etiquetas. Tabla de cobertura sin filtro de elegibilidad. Tarjeta opcional MIN del costo sobre completas y COUNT_DISTINCT de tiendas elegibles; etiquetar población.

## 20. El detalle debe conservar la misma población que el resumen.

100–112 min. Paso4,12 min. Añadir fuente curso_gold.detalle, tabla producto/cantidad/fecha/importe. Fijar mismo escenario directamente en cada fuente/gráfico. Controles de tienda separados y rotulados para evitar una sincronización no comprobada. No mezclar fuentes con joins improvisados que dupliquen costos.

## 21. Escribe la conclusión con sus condiciones visibles.

112–122 min. Paso5,10 min. Revisar título, etiquetas, moneda y fecha. ProbarTodo,A,B,C y caso sin filas si la UI lo permite. Si la conclusión es texto fijo, que no contradiga filtros; usar título descriptivo o escenario bloqueado. Guardar discrepancias antes de compartir.

## 22. Prueba el acceso con la identidad que recibirá el informe.

122–130 min. Paso6,8 min. Compartir solo con la audiencia autorizada y probar en cuenta distinta cuando exista. Exportar respaldo, anotar escenario y fecha de ejecución. No afirmar acceso probado desde la misma cuenta propietaria. No hacer público el informe para superar permisos.

## 23. Tu audiencia necesita un mensaje sobre su propia decisión.

130–140 min. Conservar fuente distinta por equipo y contrato de Gold. La biblioteca puede comparar formatos; reseñas no equivalen a ventas. No imponer mapas o líneas cuando faltan variables necesarias. Definir qué dato obligaría a cambiar la recomendación.

## 24. Otro equipo debe interpretar el tablero sin tu explicación.

140–150 min. Prueba de lectura en parejas, no cronómetro de rendimiento. Guardar una interpretación errónea y corregir jerarquía, título o etiqueta. No culpar a quien leyó: el diseño debe hacer visibles las condiciones.

## 25. El filtro más incómodo es una prueba del mensaje.

150–160 min. Aplicar pruebas al dominio propio. Confirmar fuente, escenario y agregación en cada visual. Si una condición contradice el titular, corregirlo antes de la entrega. Documentar límites del prototipo si no hay BI conectado.

## 26. Entrega el tablero junto con su evidencia.

160–170 min. Separar diseño local, conexión real y acceso probado. Adjuntar evidencia sin secretos. Revisar permiso y refresco; conservar Gold para la siguiente sesión. No publicar crudos por comodidad.

## 27. La IA recibirá el mismo límite que ve tu audiencia.

170–180 min. Cerrar el ciclo: indicador, visual y relato deben conservar la misma población y límites. Pregunta de salida: qué información enviarías al LLM para que no llamara54 una compra completa. No introducir entrenamiento de ML; S7 se centra en evidencia y generación.
