# Teoría — Sesión 05: Cómo se ve un pipeline de datos real

> Hasta ahora viste piezas sueltas (SQL, Spark, un cluster). Hoy las juntas en una
> sola historia: de dónde sale un dato hasta que alguien lo usa para decidir algo.

## 1. Qué es un ETL

**ETL** son las siglas de **Extract, Transform, Load** — extraer, transformar, cargar.
Es el patrón más común para mover datos de donde nacen a donde se usan:

- **Extract (extraer):** traer el dato de su origen — una API, un archivo, una base de
  datos operativa. En este punto el dato suele venir "sucio": con nulos, formatos
  inconsistentes, o estructuras anidadas.
- **Transform (transformar):** limpiar, validar, y darle la forma que el destino
  necesita — renombrar columnas, calcular campos derivados, filtrar filas inválidas.
- **Load (cargar):** escribir el resultado ya limpio en su destino final — una base de
  datos, un data warehouse, un archivo listo para un dashboard.

`recursos/etl-tipo-cambio/` es exactamente este patrón, de punta a punta: una API
pública de tipo de cambio → limpieza y validación en Python → carga en MariaDB. El lab
de hoy lo corre sin que tengas que escribir el código — solo llenar la configuración y
observar cada etapa.

## 2. De dónde vienen los datos, a dónde van

La pregunta que cierra el ciclo, y que casi nunca se hace explícita en una
conversación de negocio: **¿quién usa el dato al final, y para qué?** Tres destinos
típicos:

- **Un dashboard** — alguien lo mira para tomar una decisión rápida (¿cómo van las
  ventas hoy?).
- **Un modelo de machine learning** — el dato se convierte en una predicción (¿esta
  transacción es fraude?) — el territorio de Maestría.
- **Un reporte periódico** — un documento formal que se genera y se distribuye (cierre
  mensual, reporte regulatorio).

Sin esta pregunta, es fácil construir un ETL técnicamente correcto que nadie termina
usando. El ejercicio de hoy cierra explícitamente con esta pregunta: correr la celda de
`create_dashboard()` de `recursos/etl-cripto/ETL_Crypto_Dash_mejorado.ipynb` — mismo
patrón E-T-L que ya viste, pero terminando en un dashboard real, la respuesta visual a
"quién consume esto al final".

---

## Referencias

- [AWS — What is ETL? (explicación conceptual, agnóstica de proveedor)](https://aws.amazon.com/what-is/etl/)
- [Google Cloud — ETL vs. ELT: what's the difference?](https://cloud.google.com/learn/etl-vs-elt)
