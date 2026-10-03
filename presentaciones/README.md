# Big Data · Aula

Un sitio de presentaciones para el track de Especialidad, el de Maestría y la introducción compartida. Se genera a partir de los archivos Markdown existentes: 25 decks independientes, con una identidad visual común y enlaces directos a cada diapositiva.

## Construir y presentar

Desde `slides_maestria/`:

```bash
npm ci
npm run build:web
npm run serve:web
```

Abre **http://localhost:4173**. Selecciona un track y una sesión. Para compartir una posición concreta, copia la URL, por ejemplo `http://localhost:4173/#maestria-01/5`.

- Clic en la diapositiva, flecha derecha o espacio: siguiente diapositiva.
- Flecha izquierda: anterior. Inicio / Fin: primera / última.
- `O`: índice de la sesión. `F`: pantalla completa.
- Las entradas se animan automáticamente en secuencia al cambiar de slide. El clic avanza a la siguiente diapositiva; no es necesario hacer clic para revelar cada elemento.
- Las animaciones respetan la preferencia del sistema de reducir movimiento.
- En pantallas pequeñas o slides extensas, el contenido permite desplazamiento para no recortarse.

## Editar el contenido

| Contenido | Fuente |
|---|---|
| Introducción | `intro-big-data/slides.md` |
| Especialidad | `especialidad/sesion-XX/slides.md` |
| Maestría | `slides_maestria/sesion-XX.md` |
| Rutas de aprendizaje | `especialidad/TEMARIO.md`, `maestria/TEMARIO.md` |
| Práctica y evidencia de aprendizaje | `sesion-XX/README.md` de cada track |
| Temas complementarios | `presentaciones/complementos/TRACK-XX.md` |
| Identidad visual | `presentaciones/styles.css` |
| Navegación y animaciones | `presentaciones/app.js` |

Después de editar, ejecuta `npm run build:web`. No edites `dist/`: es salida generada e ignorada por Git. Los originales PPTX se conservan como referencia; el sitio usa la versión estructurada en Markdown, no una conversión visual uno a uno del PowerPoint.

El generador elimina metadatos de Marp/Slidev y convierte sus elementos a HTML. Los `v-click` originales pasan a entradas temporizadas. Incluye rutas de aprendizaje, una práctica inicial cuando el README la especifica y un checkpoint de cierre. Los complementos añaden las distinciones y controles de decisión que faltaban en los decks. La edición es independiente del flujo normal de Slidev y de la exportación de los decks originales.

## Alojamiento estático

Publica el contenido de `presentaciones/dist/` en cualquier servidor estático. No requiere backend ni claves. Incluye Mermaid y las imágenes locales; la presentación no depende de un CDN. Los enlaces a fuentes externas sí requieren conexión. Las rutas de sesión usan fragmentos, por lo que no necesitan reglas de redirección del servidor.

## Verificación

Desde `slides_maestria/`, con el servidor anterior corriendo y Chromium de Playwright instalado:

```bash
node verify-web.mjs
```

El recorrido comprueba los 25 decks, cada diapositiva, diagramas Mermaid, filtros, navegación por clic y teclado, el índice, las imágenes, el catálogo móvil y reducción de movimiento. Reporta los slides con desplazamiento para facilitar su revisión editorial.

## Infográficos y narrativa de clase

Ocho SVG editables en `infograficos/`, embebidos por el generador en los complementos de las sesiones: mapa de rutas, decisión de arquitectura, presupuesto US$300, controles ETL, shuffle/skew, separación sin fuga, watermark y ciclo MLOps. Sus grupos entran en secuencia y respetan reducción de movimiento. En móvil los diagramas se desplazan horizontalmente para conservar legibilidad. Los cuatro PNG originales permanecen como referencia.

Los títulos explican la conclusión; color y etiquetas enfocan lo relevante. Los números esquemáticos están identificados como ejemplos y la asignación presupuestaria no se presenta como tarifa. Se añaden ejercicios de visualización dentro de S5/S8 de Especialidad y S2/S6/S11 de Maestría, sin incrementar horas del programa.

Referencias: [Cole Nussbaumer Knaflic: comunicar el hallazgo](https://www.storytellingwithdata.com/blog/2017/3/22/so-what), [evidencia y anotaciones](https://www.storytellingwithdata.com/blog/2021/1/14/data-doesnt-speak-for-itself).

## Big Data y cloud computing

Cada sesión incluye una diapositiva que distingue Big Data (escala y procesamiento), cloud computing (recursos y servicios bajo demanda) y conocimientos complementarios (SQL, ML, visualización, gobernanza o MLOps). Las etiquetas del catálogo y de la sesión muestran los ámbitos presentes, sin equiparar el uso de GCP con Big Data. La clasificación editorial se mantiene en `ambitos.json`. Las presentaciones se dirigen al alumnado y no incluyen referencias al presentador.
