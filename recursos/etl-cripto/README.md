# ETL Cripto: mercado + tipo de cambio + noticias → MariaDB (4 tablas)

Versión mejorada de un ejercicio hecho por el instructor en Colab. Mismo propósito que
`recursos/etl-tipo-cambio/`, pero con dos diferencias deliberadas que lo hacen un buen
segundo ejemplo en el curso (no un duplicado):

> Ver [`FLUJO.md`](FLUJO.md) para el diagrama del flujo completo.


1. **Enriquecimiento en dos rondas de Extract-Transform.** El primer Extract trae mercado
   (CoinGecko) y tipo de cambio (Frankfurter). El primer Transform decide cuáles monedas
   son "top movers". Solo entonces hay un **segundo Extract** (NewsAPI) que pregunta
   específicamente por esas monedas. Es el patrón real de un pipeline de enriquecimiento,
   y se dejó marcado con encabezados 🟦 EXTRACT / 🟨 TRANSFORM / 🟩 LOAD para que sea
   imposible confundir en qué etapa está cada celda.

2. **Carga en 4 tablas normalizadas**, no una sola tabla ancha:
   - `dim_moneda_cripto` (catálogo, no se repite en cada snapshot)
   - `hechos_mercado_cripto` (el snapshot de precio/volumen/cambio %)
   - `noticias_cripto` (solo monedas con noticia real, no placeholders)
   - `tipo_cambio` (comparte tabla con `recursos/etl-tipo-cambio/` — mismo esquema)

## Requiere

- Una **NewsAPI key** gratuita (https://newsapi.org/register, tier gratuito ~100 req/día).
- La misma instancia de MariaDB de `environment/mariadb-vscode-setup.md`.

Ambas credenciales se piden en tiempo de ejecución (Colab Secrets o `getpass`) — nunca
quedan escritas en el notebook.

## Nota de seguridad

Si trabajas a partir de una versión anterior de este ejercicio que tenía la API key o el
password de la base escritos directamente en una celda: **rótalos**. Un valor de API key
o password que estuvo alguna vez en texto plano en un notebook compartido debe tratarse
como comprometido, aunque ya no esté visible en la versión actual.
