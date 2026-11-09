# Sesión 5 · Una canasta incompleta parece una ganga

Gran idea: Una comparación justa conserva el mismo contrato, población y denominador.

Guion para presentar en vivo. [pausa 3 s] indica silencio deliberado. Los controles se activan por el docente; no hay avance automático.

## 01. Una canasta incompleta parece una ganga.

0–5 min. Retomar las dos exclusiones de Silver. Preguntar si54 permite comparar una compra completa. [pausa 3 s] La cifra es correcta como subtotal y engañosa como costo completo. No faltan ceros: faltan observaciones.

## 02. Exigir la misma canasta cambia el ranking.

5–10 min. Pedir elegir antes del botón. Las barras comparten cero y escala. Al exigir cobertura, C se conserva como información pero deja de participar en el ranking. A es la alternativa de menor costo completo del fixture, no una recomendación de compra actual.

## 03. Gold traduce una decisión en reglas de comparación.

10–15 min. Silver valida observaciones; Gold decide cómo usarlas para una pregunta. Pedir nombrar el cambio de grano: de observación a tienda y escenario. El contrato de negocio acompaña al número.

## 04. El catálogo fija qué debe contener la compra.

15–19 min. Cinco productos de demostración, no una canasta oficial de PROFECO. El catálogo define denominador antes de ver resultados. No sustituir un producto faltante por otro ni sumar mínimos de tiendas distintas: cambiaría la pregunta.

## 05. Una fila de Gold necesita una identidad precisa.

19–23 min. El producto se identifica junto con marca y presentación. El escenario incluye catálogo, cantidades y ventana. Dos filas con el mismo grano son un conflicto que se investiga; no se suman para ocultarlo.

## 06. El modelo une observaciones con el catálogo que las interpreta.

23–27 min. Explicar dimensión y hecho sobre estas piezas concretas. No afirmar que una tabla ancha sea la única verdad de una empresa. El catálogo y la regla temporal aportan contexto a una observación de precio. El fixture no tiene geografía; una fuente real puede necesitarla.

## 07. Elegir la última observación exige resolver los empates.

27–31 min. Fragmento de QUALIFY de06_gold.sql. El alumno interpreta, no implementa una ventana desde cero. Un ID repetido con misma fecha y datos distintos no queda resuelto semánticamente por esta regla: validar antes. Una ventana ampliada puede mezclar días; último no significa simultáneo.

## 08. El catálogo debe conservar los productos sin precio.

31–35 min. Mostrar primero solo coincidencias. Al usar LEFT desde catálogo aparecen las ausencias. Un INNER no demuestra cobertura100%: cambió el denominador a lo observado. En SQL se usa tienda×catálogo y LEFT a precios elegidos. El universo de tiendas del fixture proviene de Silver; una tienda sin ninguna observación aceptada requeriría un padrón externo para seguir presente.

## 09. Cobertura divide lo encontrado entre lo requerido.

35–39 min. Son tipos de producto requeridos, no número de envases comprados. Con cantidades diferentes, el denominador de cobertura sigue siendo el catálogo según este contrato. Distinguir cobertura de calidad, disponibilidad e inventario.

## 10. Un subtotal conocido no completa un precio desconocido.

39–42 min. SUM ignora valores NULL; por eso puede devolver54 sin que la compra esté completa. La condición de completitud debe envolver el resultado. No usar COALESCE(precio,0) para fabricar una canasta barata.

## 11. Un indicador debe declarar cómo puede agregarse.

42–45 min. Un promedio de porcentajes no siempre corresponde a cobertura total; necesita denominadores compatibles. Sumar tiendas es sumar alternativas de compra, no ventas. El dato de precios no contiene ingresos ni demanda.

## 12. Una unión duplicada puede inflar el costo sin avisar.

45–49 min. Miniatura hipotética del problema de cardinalidad. No son dos unidades autorizadas por catálogo sino una observación replicada por la unión. El script comprueba unicidad de precios elegidos; también comprobar catálogo y detalle. DISTINCT al final puede ocultar el defecto.

## 13. Una tabla Gold necesita una política de actualización.

49–53 min. En el laboratorio usamos CTAS y reemplazo explícito. No traducir automáticamente el ejemplo del syllabus a vista materializada con ventanas: soporte depende de modalidad y restricciones. Las tablas de este script guardan solo el escenario recién ejecutado; no se promete histórico multiescenario. Conservar exportación/versión si se necesita comparar ejecuciones.

## 14. Mercado Libre conecta el análisis con sus consumidores.

53–58 min. Retomar caso documentado de BigQuery y Looker. La recomendación de contrato de KPI es nuestra transferencia pedagógica; no afirmar que esta figura describe su modelo interno ni que usa nuestra canasta. Looker no es Looker Studio. No atribuir ROI sin evidencia.

## 15. La recomendación debe sobrevivir a una pregunta incómoda.

58–65 min. Cada pareja elige una objeción al ranking y dice qué evidencia la resuelve. Un resultado SQL válido puede incumplir el contrato de la decisión. Si se amplía fecha o catálogo, repetir controles y revisar comparabilidad.

## 16. Vuelve con Silver reconciliada y el catálogo a la vista.

65–75 min. Pausa. Confirmar Silver del fixture:13 aceptadas. Si falta, usar restauración docente de Bronze y Silver, registrando dependencia. No improvisar la fuente real durante la práctica.

## 17. Define el escenario antes de ejecutar el script.

75–80 min. Paso1,5 min. Leer parámetros dentro de06_gold.sql, no ejecutarlos como consulta independiente. Confirmar proyecto y región. El fixture carece de geografía; no inventar un filtro territorial. Cambiar ventana requiere una nueva revisión de comparabilidad.

## 18. Localiza la observación que puede alimentar cada producto.

80–88 min. Paso2,8 min. Leer JOIN y QUALIFY del script. Anticipar13 precios elegidos. No aplicar el esquema del fixture a cualquier dataset propio. Revisar la política temporal y los empates con docente antes de modificarla.

## 19. Ejecuta Gold completo en el proyecto de laboratorio.

88–100 min. Paso3,12 min. Ejecutar script entero porque las variables pertenecen al script. Reemplaza tablas curso_gold, no Silver. Guardar errores si falla; no presentar salida parcial como Gold terminado. La ejecución conserva solo el escenario actual.

## 20. Contrasta la salida con el contrato de cobertura.

100–112 min. Paso4,12 min. Consultar canastas, contrastar gold-esperado.csv y el detalle de C. No confundir formato vacío del CSV esperado con un cero. Confirmar ASSERT y comprobar15 filas de detalle y ausencia de repetición en el grano.

## 21. Recalcula una tienda antes de presentar el ranking.

112–122 min. Paso5,10 min. Usar07_control_dashboard.sql para rastrear detalle y escenario. Comparar A conB160: diferencia10 MXN para la misma canasta ficticia. Registrar job, bytes y caché; la salida pequeña no prueba costo pequeño.

## 22. Guarda la definición que acompañará cada KPI.

122–130 min. Paso6,8 min. Guardar SQL, catálogo, escenario, controles y definición. Conservar Gold para BI y revisar política de actualización/retención. La tabla no se refresca sola. Registrar qué se ejecutó y qué sigue pendiente.

## 23. Tu proyecto necesita su propio contrato analítico.

130–140 min. Cada equipo usa otra fuente y métricas acordes. Elegir tres KPIs, no copiar canastas a dominios incompatibles. El docente proporciona esquema y SQL adaptado; si todavía no están preparados, entregar diseño y declarar ejecución pendiente.

## 24. Otro equipo debe poder reconstruir una cifra.

140–150 min. Intercambiar una cifra y su contrato. El receptor sigue la evidencia y comprueba denominador, filtros y grano. No basta una captura de pantalla. Devolver una discrepancia o una condición que aún necesita prueba.

## 25. Cambiar el denominador puede cambiar la historia.

150–160 min. Mismos tres precios, distinta definición. En el proyecto propio revisar universo de entidades, no solo filas presentes. Una tienda sin ninguna fila Silver no aparece en el script actual; requeriría dimensión/padrón de tiendas. Registrar límite en H5.

## 26. Entrega un indicador que pueda auditarse.

160–170 min. Separar práctica ficticia del hito sobre dataset propio. Adjuntar SQL, resultados, job y límites. Conservar Gold para S6; revisar expiración y consultas programadas si existen. No publicar crudos ni credenciales.

## 27. El dashboard tendrá que mostrar lo que falta.

170–180 min. Cerrar el dilema. Pregunta de salida: cómo mostraría C para que nadie lea54 como canasta completa. Preparar S6: escenario, cobertura, fecha y costos deben permanecer visibles. No prometer precio o inventario actual.
