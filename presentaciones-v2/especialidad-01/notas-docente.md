# Sesión 1 · Una compra merece evidencia

Gran idea: Una decisión defendible permite recorrer la evidencia hasta su fuente.

Guion para presentar en vivo. [pausa 3 s] indica silencio deliberado. Los controles se activan por el docente; no hay avance automático.

## 01. Una compra merece evidencia.

0–3 min. Hoy ustedes son el comité que debe autorizar una recomendación de compra. Preguntar qué evidencia exigirían. [pausa 3 s] Escuchar dos respuestas. Abrimos por la decisión; los nombres de los servicios llegarán cuando resuelvan un problema. La imagen es del kit del profesor, no un gráfico de datos.

## 02. El precio menor todavía no resuelve la compra.

3–8 min. Pedir votar A o B y escuchar la razón antes del primer clic. Revelar presentación y fecha. Quien eligió A usó la evidencia disponible; ahora tenemos otra. Preguntar qué compararían para reparar el análisis. No revelar la siguiente gráfica hasta escuchar al menos una propuesta.

## 03. La unidad cambia el orden; la fecha sigue pendiente.

8–12 min. Mostrar la división 24 / 0.5 = 48 en voz alta; B ya está por kg. Las barras parten de cero y usan la misma escala. [pausa 3 s] El orden cambió, pero no basta para recomendar: las fechas difieren. No atribuir estos valores a PROFECO ni a inflación.

## 04. Cada recomendación necesita un camino de vuelta.

12–15 min. Leer el camino desde la decisión hacia la evidencia. Cada clic responde la pregunta anterior. Pedir que expliquen dónde se rompió el ejemplo del arroz: regla de comparabilidad. Esta es la gran idea: podrás defender una decisión si puedes recorrer ese camino.

## 05. La escala empieza cuando una restricción te detiene.

15–19 min. El catálogo reporta tamanio_mb=19706.44; la aproximación no valida filas ni calidad. No hay umbral universal de GB. Un archivo grande puede procesarse por partes en una máquina; una aplicación pequeña puede exigir baja latencia. Preguntar cuál restricción tendría el análisis de su trabajo.

## 06. Las V sirven para interrogar el problema.

19–23 min. Dar una pregunta por clic, sin recitar un glosario. CSV, JSON y texto son ejemplos de variedad, no categorías de calidad. En el precio, veracidad incluye presentación, fecha y procedencia. Cerrar pidiendo a una persona que elija la V que amenaza su proyecto.

## 07. Repartir exige combinar respuestas compatibles.

23–27 min. Rescata la analogía de los documentos del sitio anterior. Cada equipo cuenta observaciones por tienda. Dos resultados con la misma tienda se suman, pero un archivo repetido debe identificarse. Preguntar qué pasa si un archivo es cien veces mayor. No prometer aceleración lineal ni confundir partición con réplica.

## 08. La nube separa guardar datos de ejecutar trabajo.

27–31 min. Cloud entrega recursos bajo demanda. Explicar que servidor administrado sigue teniendo costo y responsabilidades. Una VM pequeña también es cloud. Usaremos GCS/BigQuery; la VM de MariaDB la prepara el docente. No describir GCS como una base transaccional.

## 09. Registrar una compra y analizar historia exigen trabajos distintos.

31–35 min. El dibujo muestra el tipo de trabajo, no un benchmark. OLTP protege operaciones; OLAP permite lecturas y agregaciones amplias. employees es una base relacional usada aquí para aprender SQL; MariaDB también puede agregar. Evitar una falsa prohibición de analítica en motores relacionales.

## 10. El almacenamiento se elige por lo que debe garantizar.

35–40 min. Un warehouse organiza datos analíticos; un lake conserva distintas estructuras; un lakehouse busca garantías de gestión de tablas sobre el lago. Son patrones que pueden coexistir. No vender una evolución obligatoria ni decir que tres carpetas crean un lakehouse. El proyecto justificará una arquitectura; la práctica implementa Medallion con GCS y BigQuery.

## 11. Medallion hace visible qué promete cada capa.

40–45 min. Dibujar las capas con clics. Bronze conserva el original y su origen. Silver aplica reglas explícitas. Gold produce indicadores con una definición. La pregunta del arroz cae en Silver. La línea roja señala la regla, no un servicio preferido. Esto es una implementación docente de capas; no demuestra un lakehouse completo.

## 12. La latencia necesaria cambia la arquitectura.

45–49 min. Recuperar el contraste del banco del sitio anterior: revisión mensual frente a alerta durante la operación. El comité debe decir cuánto demora es aceptable. Batch simplifica repetición y recuperación; streaming mantiene operación y estado. No programaremos streaming en Especialidad.

## 13. Mercado Libre conecta analítica con consumo de negocio.

49–54 min. El caso documenta BigQuery y Looker en su ecosistema de inteligencia. No afirma que esta figura sea toda su arquitectura. Looker no es Looker Studio. Preguntar qué rol consume la evidencia en el proyecto de cada equipo. No prometer ahorros ni atribuir Medallion al caso.

## 14. Otros sectores cambian la evidencia que necesitan.

54–59 min. Casos reportados por las organizaciones en publicaciones de Google Cloud, no auditorías independientes. HSBC integra datos para análisis de riesgo; Mayo presenta analítica genómica; UPS Capital aplica analítica a riesgo de envíos. Pedir qué restricción cambiaría entre salud y retail: privacidad, demora, costo del error. No trasladar los modelos técnicos al laboratorio ejecutivo.

## 15. Una arquitectura pequeña también puede ser una buena decisión.

59–65 min. Hipótesis del curso anterior, no medición. Pedir elegir y justificar antes de pulsar. Si proponen distribuir, escuchar qué nueva condición lo haría necesario. Remate opcional, una sola vez: «El clúster también puede procesar nuestra necesidad de tener un clúster». Cerrar volviendo a memoria, tiempo y usuarios.

## 16. Vuelve con una decisión que necesite evidencia.

65–75 min. Pausa real. No hay avance automático. Mientras regresan, comprobar que se ve la guía. Si una cuenta no tiene crédito, usar acceso docente autorizado y documentar la dependencia; no exigir activar pago para continuar.

## 17. Hoy dejarás una pregunta y un entorno comprobables.

75–80 min. Paso 1 de la guía, 5 min. Esta es la agenda de trabajo, no la infraestructura completa del curso. Confirmar una pestaña para slides y otra para instrucciones. La guía contiene recuperación y restricciones. Si no hay cuenta operativa, registrar exactamente qué acceso prestó el docente.

## 18. Comprueba el proyecto antes de tocar recursos.

80–88 min. Comando de solo lectura. En GCP, crear o seleccionar un proyecto de laboratorio y abrir Cloud Shell según la guía. La respuesta debe ser su ID, no el nombre visible. Si aparece unset o proyecto ajeno, corregir la selección antes de continuar. Verificar elegibilidad del crédito en la cuenta; no asumir que todo participante lo tiene.

## 19. Una alerta avisa; el gasto puede continuar.

88–100 min. Paso 3, 12 min. Abrir facturación, presupuestos y alertas. Verificar alcance del proyecto y tratamiento de créditos según interfaz. Guardar evidencia de configuración; no afirmar haber recibido correo si no llegó. El crédito no es una mensualidad y una alerta no impide gasto. Revisar vigencia real en cuenta.

## 20. El bucket necesita ubicación y acceso definidos.

100–112 min. Seguir opciones detalladas de la guía. Nombre global único, acceso uniforme y prevención de acceso público conforme a política docente. Registrar ubicación; us-central1 es propuesta del laboratorio, no mandato institucional. Un bucket vacío no contiene los datos del Drive. Si no hay permiso, usar un bucket autorizado y declarar quién lo creó.

## 21. El catálogo abre preguntas sobre la fuente.

112–122 min. Paso 5, 10 min. Abrir extracto local. El catálogo inventaría archivos; no verifica columnas, derechos o calidad. No descargar 19 GB a Cloud Shell. El docente debe preparar fuente accesible y muestra perfilada antes de Bronze. Guardar preguntas pendientes para cada candidato.

## 22. Tu mapa debe decir quién responde por cada capa.

122–130 min. Paso 6, 8 min. El esquema es propuesto; no significa que Silver y Gold estén creadas. Asignar responsabilidades, no necesariamente puestos distintos. La fuente propia puede ser de biblioteca, ciudad u otro dominio. Preguntar qué promesa tendrá que comprobarse antes de construir cada capa.

## 23. Cada equipo defenderá una decisión con otro dataset.

130–140 min. No aceptar como datasets distintos dos formatos del mismo origen. El docente confirma asignación después de revisar procedencia y esquema. Ficha local con descarga, no reserva automática. No escribir credenciales ni datos sensibles. El proyecto entrega arquitectura/gobierno, SQL y dashboard; la práctica GenAI complementa la evidencia.

## 24. Una pregunta concreta permite discutir una respuesta.

140–150 min. El ejemplo de biblioteca es una pregunta posible, no un hallazgo ni la fuente asignada. Intercambiar fichas y localizar audiencia, acción, unidad y periodo. El receptor escribe una pregunta de aclaración. Elegir el último año disponible solo después de perfilar fechas.

## 25. La fecha de carga no rejuvenece la observación.

150–160 min. Regresar a las fechas del arroz y transferir el problema al dato propio. Una fecha de modificación no prueba actualidad. Cada equipo escribe una limitación y una acción para comprobarla. Si aún no conoce fechas, declarar pendiente; no inventar un periodo.

## 26. Entrega la pregunta y las pruebas del entorno.

160–170 min. Revisar evidencia con un compañero. Una captura de pantalla aislada no explica qué se verificó. Quien usó acceso docente debe identificarlo. Revisar recursos existentes: cerrar el navegador no detiene una VM. Esta sesión no requiere crear cómputo persistente adicional.

## 27. Exige una regla antes de aceptar el precio.

170–180 min. Retomar el dilema sin repetir toda la clase. Pedir explicar qué falta: unidad y fecha comparables, alcance y disponibilidad no demostrada. Escuchar respuestas de salida y registrar duda para S2. El docente prepara MariaDB y carga employees antes de la próxima clase; nadie instala VM durante el SQL Fast Track.
