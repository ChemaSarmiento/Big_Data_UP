# Big Data · Especialidad · ocho sesiones de 180 minutos

Material interactivo de Especialidad (perfil ejecutivo): cada sesión tiene un deck HTML, una guía de laboratorio de 6 pasos (70 min) y notas. Es una versión pensada para repetirse: cada alumno trabaja solo, en su propio proyecto de Google Cloud, con sus propios datos.

| Sesión | Tema | Herramienta principal |
|---|---|---|
| 1 | Introducción a big data y a la nube; monta tu ambiente | Consola, Cloud Shell, VM con MariaDB |
| 2 | SQL con MariaDB y `employees` | MariaDB |
| 3 | Del JSON a una tabla: Bronze, formatos, costos y primer Spark | Cloud Storage, BigQuery, Dataproc |
| 4 | Silver: calidad y tablas con significado | BigQuery, PySpark |
| 5 | Gold: del dato al indicador | BigQuery |
| 6 | Dashboard con varias tablas Gold | Data Studio (antes Looker Studio) |
| 7 | IA generativa con evidencia | Vertex AI Studio |
| 8 | Comité de decisión (pendiente de rehacer) | — |

El hilo de datos empieza en S3 con `war_tweets.txt` (tweets de 12 días de marzo de 2022; uso académico). Cifras de referencia: `recursos/tweets/verdad.json`.

## Ver el material en local

```bash
python3 -m http.server 4183 --bind 127.0.0.1 --directory presentaciones-v2
```

Abrir `http://localhost:4183/`. Servir la carpeta completa: todas las sesiones usan `compartido/`, `editorial/` y `recursos/`.

Navegación: clic en espacio libre, flecha derecha o espacio avanza; izquierda retrocede; `O` índice, `L` guía, `F` pantalla completa. Imprimir desde el índice muestra todo el contenido revelado.

## Dónde se edita cada cosa (los HTML generados no se editan)

| Qué | Fuente |
|---|---|
| Slides y notas S1–S7 | `editorial/sNN.py` (+ `sNN.css`, `sNN.js` si la sesión los necesita); ayudantes en `editorial/guion.py` |
| Guía de laboratorio S2–S8 | `especialidad-0N/contenido.json` (S3 lo sincroniza desde `s03.py`) |
| Guía de S1 | `especialidad-01/laboratorio.html` (escrita a mano) |
| S8 | `especialidad-08/contenido.json` |
| Scripts y datos del laboratorio | `recursos/tweets/`, `../recursos/mariadb/` |
| Estilo común | `editorial/editorial.css`, `compartido/` |

```bash
python3 presentaciones-v2/scripts/build-editorial.py [N]   # decks y notas S1–S7 (N = solo esa sesión)
python3 presentaciones-v2/scripts/build.py [N]             # guías S2–S8 y deck S8
python3 presentaciones-v2/scripts/catalogo.py              # índice y manifiesto
```

## Verificación

Con el servidor en marcha en el puerto 4183:

```bash
python3 presentaciones-v2/scripts/verify-resources.py            # verdad, guías, recursos y texto prohibido
node presentaciones-v2/scripts/verify-editorial.mjs               # S1–S7 en 3 tamaños; ONLY=N limita la sesión
node presentaciones-v2/scripts/verify-course.mjs                  # S8
node presentaciones-v2/scripts/verify-hosting.mjs                 # paquete publicable (puerto 4184)
```

Las comprobaciones usan Chromium de `slides_maestria/node_modules/playwright-chromium`. Verifican layout, enlaces, demos y recursos; no demuestran una ejecución en Google Cloud.

## Límites conocidos

- Sin ensayar con una cuenta de alumno: copia Drive → Storage (Colab del curso), pasos de consola de S1, carga completa desde un bucket propio, scripts de Spark de conteo, Data Studio y Vertex AI Studio.
- S8 conserva la versión anterior y habla de equipos y de un dataset compartido; pendiente de rehacer con los criterios de S1–S7.
- La clase independiente `clase-bigquery/` no forma parte de las ocho sesiones.
