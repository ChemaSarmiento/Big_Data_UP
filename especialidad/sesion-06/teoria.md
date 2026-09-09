# Teoría — Sesión 06: Data Lakes y gobierno del dato

> Esta sesión es puramente conceptual — no hay lab de código. El objetivo es que
> puedas evaluar si un proyecto de datos está bien gobernado, sin necesitar leer una
> sola línea de configuración.

## 1. Qué es un data lake

**Analogía — bodega vs. archivero organizado:** un data warehouse tradicional es como
un archivero: todo lo que entra ya está clasificado en carpetas con etiqueta, listo
para buscar. Un **data lake** es más como una bodega grande: se puede meter cualquier
cosa (cajas, muebles, documentos sueltos) sin clasificar de entrada, porque no siempre
sabes de antemano cómo vas a necesitar usar ese contenido después.

Esto no es un defecto — es la razón por la que existen los data lakes: guardar datos
"tal cual llegan" (texto, imágenes, logs, tablas) sin forzar una estructura rígida
desde el principio, porque estructurar de más *antes* de saber para qué se va a usar
el dato es, en sí mismo, una forma de sobre-ingeniería (ver Sesión 1).

## 2. Arquitectura medallion, en términos simples

La forma más común de organizar un data lake sin que se vuelva un caos es por capas de
madurez — el patrón **medallion**:

| Capa | Analogía | Qué contiene |
|---|---|---|
| 🟤 **Bronze** (cruda) | La bodega tal cual llega el camión | Datos exactamente como llegaron — sin limpiar, sin validar |
| ⚪ **Silver** (limpia) | La bodega ya ordenada por categoría | Datos limpios, con tipos correctos, sin duplicados |
| 🟡 **Gold** (lista para usar) | El escaparate, listo para vender | Datos agregados y listos para un dashboard o reporte, sin que nadie tenga que procesarlos más |

`recursos/etl-tipo-cambio/` implementa exactamente este patrón: `data/raw/` (bronze) →
`data/processed/` (silver) → la tabla final en MariaDB (gold). Verlo sin correr código
— solo mirando cómo cambia el archivo de una carpeta a otra — es suficiente para esta
sesión.

## 3. Por qué importa el gobierno del dato

Gobierno del dato es, en esencia, **quién puede tocar qué, y quién es responsable de
que el dato sea correcto**. No es burocracia por burocracia — es lo que evita fallas
costosas:

- **Sin control de acceso:** cualquiera puede modificar datos sensibles (financieros,
  de salud, personales) sin registro de quién lo hizo.
- **Sin validación de calidad:** un error en el dato bronze se propaga silenciosamente
  hasta el dashboard que un ejecutivo usa para decidir — sin que nadie note el error a
  tiempo.
- **Sin documentación de origen (linaje):** cuando algo sale mal, nadie puede rastrear
  de dónde vino el dato ni qué transformaciones sufrió.

El caso de estudio de hoy (una falla real por mal manejo de datos, con costo de
negocio medible) es el vehículo para discutir esto sin necesitar jerga técnica — el
gobierno del dato se evalúa por sus consecuencias, no por su configuración.

---

## Referencias

- [Databricks — What is a Data Lake?](https://www.databricks.com/discover/data-lakes)
- [Databricks — Medallion Architecture explained](https://www.databricks.com/glossary/medallion-architecture)
- [Google Cloud — Data governance overview](https://cloud.google.com/learn/what-is-data-governance)
