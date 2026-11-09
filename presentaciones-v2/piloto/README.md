# Piloto local · Especialidad, sesión 1

Diez pantallas del storyboard, implementadas con HTML/CSS/JS sin build ni dependencias de red para presentarlas. Usa fuentes del sistema como respaldo de la identidad serif/sans/mono del curso. No modifica `presentaciones/`, su generador ni Firebase.

Desde la raíz del repositorio:

```bash
python3 -m http.server 4183 --bind 127.0.0.1 --directory presentaciones-v2/piloto
```

Abre **http://localhost:4183**. También puedes abrir `index.html` directamente: la navegación funciona; algunas funciones del navegador, como copiar o guardar localmente, pueden estar restringidas bajo `file://`.

## Cómo recorrerlo

- Clic en espacio libre, → o espacio: revelar el siguiente paso; después avanzar a la siguiente slide.
- ←: retroceder un paso. Al volver a otra slide, muestra su último paso.
- Inicio / Fin: primera / última pantalla. `O`: índice; `F`: pantalla completa; `L`: guía de laboratorio.
- Mostrar todo / Reiniciar pasos: revelar o reiniciar la pantalla actual.
- Enlaces profundos: `#6/2` es slide 6, paso 2. La URL conserva la posición al recargar y funciona con historial.
- Controles, formularios, código seleccionable y enlaces no hacen avanzar la slide.
- La preferencia de movimiento reducido elimina transiciones y animación. Revelar sigue siendo explícito por clic.
- Índice → Imprimir todas las slides: muestra también los pasos aún no revelados. La guía se imprime por separado.

## Contenido e interacciones

1. Dilema de decisión: archivo → evidencia → recomendación.
2. Contexto: unidad y fecha de un precio, con revelado progresivo.
3. Paralelismo: repartir, combinar y discutir coordinación.
4. Almacenamiento/cómputo: interruptor ilustrativo; no controla GCP.
5. OLTP/OLAP: propósito, patrón de trabajo y herramientas docentes.
6. Medallion: rastrear una observación ilustrativa entre capas.
7. Canasta: excluir alternativas incompletas sin alterar los precios del ejemplo.
8. Mercado Libre: caso documentado con fuente y diferencia Looker/Looker Studio.
9. Laboratorio: proyecto y presupuesto, comando descargable y guía de recuperación.
10. Ficha de decisión: almacenamiento local y descarga JSON con mapa propuesto.

La ficha se guarda solo en este navegador, sin backend ni envío a terceros. No escribas credenciales. El JSON descargado permite conservarla si el almacenamiento local está bloqueado.

## Qué validar con el docente

Ritmo del clic, legibilidad en proyección, equilibrio teoría/laboratorio, densidad y utilidad de las interacciones. El piloto no representa las tres horas completas de S1.

Los precios, productos y coberturas de las demostraciones son **ilustrativos**. El archivo `all_data.csv` todavía necesita perfilado. No hay SQL de PROFECO ni una ejecución cloud probada; no se desplegaron recursos ni el sitio.

## Archivos y comprobación

`index.html` es la fuente única del contenido; `app.js` controla navegación/interacciones; `styles.css` contiene presentación, responsive e impresión. `laboratorio.html` es la guía extensa, y `verificar-proyecto.sh` solo consulta la configuración de gcloud.

Con el servidor en marcha y las dependencias del repo existentes:

```bash
node presentaciones-v2/piloto/verify.mjs
```

El script usa Chromium de `slides_maestria/node_modules/playwright-chromium`. Genera capturas y un PDF en `/tmp/bigdata-plan3-piloto/` y comprueba navegación, interacciones, descarga, persistencia, impresión, responsive y movimiento reducido. Puede requerir permiso para lanzar Chromium en un entorno restringido. No valida la ejecución en GCP ni la recepción de correo.
