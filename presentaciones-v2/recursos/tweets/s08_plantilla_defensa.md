# Defensa del proyecto propio · Especialidad (S8)

Dataset / fuente distinta:
Equipo / integrantes:
Audiencia y decisión:

## Siete minutos (1-1-3-1-1)
1. **Problema y audiencia (1 min).** Una frase: quién decide qué.
2. **Arquitectura y gobierno (1 min).** Capas ejecutadas con sus conteos; separar lo preparado por el docente y lo propuesto.
3. **Evidencia (3 min).** Una cifra, su denominador, su grano y la consulta que la reconstruye. Gold, gráfica y control SQL.
4. **Límites e IA (1 min).** Qué no se puede afirmar; una frase de la IA que corregiste.
5. **Decisión (1 min).** Recomendación y siguiente comprobación.

## Tres minutos de preguntas
Anota la pregunta del comité y responde con un dato o una consulta, no con una opinión.

## Modelo de referencia (war_tweets, marzo de 2022; uso académico)
- Problema: qué temas satélite de la guerra vigilar primero.
- Arquitectura: archivo (22.04 GiB) -> Bronze 6,798,932 -> Silver 6,798,932 -> Gold 216 filas.
- Evidencia: energía en 2.0 % de los tweets; 3.382 % el 23 de marzo en inglés (10,530 / 311,363); consulta en s08_control_cifra.sql.
- Límites: un mes; el 16 de marzo es día parcial; palabras clave de precisión no medida; no hay causa en el dato.
- Decisión: vigilar primero energía y sanciones; confirmar con datos de mercado antes de actuar.

## Paquete de entrega
SQL ejecutado; conteos Bronze/Silver/Gold; tabla de reglas; KPI definidos; dashboard; memo con evidencia; límites; costo (bytes, jobs y cierre).
No entregar credenciales ni datos crudos sensibles.
