---
marp: true
theme: default
paginate: true
style: |
  section { font-family: 'Helvetica Neue', Arial, sans-serif; }
  h1, h2 { color: #1d4ed8; }
  .accent { color: #1d4ed8; font-weight: bold; }
  .box { border-left: 4px solid #1d4ed8; padding: 0.5em 1em; background: rgba(29,78,216,0.05); }
---

# Sesión 05
## Cómo se ve un pipeline de datos real

Especialidad — Big Data

---

## ETL: extraer, transformar, cargar

| Etapa | Qué pasa | Qué puede fallar |
|---|---|---|
| **Extract** | Traer el dato de su origen | La API no responde, el archivo no existe |
| **Transform** | Limpiar, validar, darle forma | Un valor viene en formato inesperado |
| **Load** | Escribir en el destino final | Sin espacio o permisos en la base |

---

## La pregunta que casi nunca se hace

<div class="box" style="font-size:1.3em; text-align:center;">
¿Quién usa el dato al final, y para qué?
</div>

- Un **dashboard** — decisión rápida
- Un **modelo** — se convierte en predicción (territorio de Maestría)
- Un **reporte periódico** — cierre mensual, regulatorio

Sin esta pregunta, es fácil construir un ETL técnicamente correcto que nadie
termina usando.

---

# Lab guiado

## Paso 1 — Correr el ETL en Colab

`recursos/etl-tipo-cambio/etl_tipo_cambio_colab.ipynb` — solo llenas la celda
de configuración:

```python
SIMBOLOS = ["MXN", "EUR"]
```

<div class="box">
<b>Deberías ver:</b> el notebook corre extract → transform → load, terminando
con una confirmación de filas cargadas en MariaDB.
</div>

---

## Paso 2 — El dashboard, sin tocar código

```python
# recursos/etl-cripto/ETL_Crypto_Dash_mejorado.ipynb
create_dashboard(df_resultado)
```

Mismo patrón E-T-L que el paso anterior, pero termina en algo que el ETL de
tipo de cambio no muestra: un **dashboard real**, la respuesta visual a
"quién consume esto al final".

---

## Paso 3 — Diagrama del flujo

Con tu pareja: dibuja (a mano o en una herramienta simple) el flujo que
acabas de correr — origen → transformación → destino → **consumo final**.

---

## Entregable de hoy

Diagrama del flujo + captura del resultado, **incluyendo la captura del
dashboard**.

---

# → Sesión 06

Data Lakes y gobierno del dato
