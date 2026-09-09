---
marp: true
theme: default
paginate: true
style: |
  section { font-family: 'Helvetica Neue', Arial, sans-serif; }
  h1, h2 { color: #1d4ed8; }
  .accent { color: #1d4ed8; font-weight: bold; }
---

# Sesión 05
## Cómo se ve un pipeline de datos real

Especialidad — Big Data

---

# ETL: extraer, transformar, cargar

| Etapa | Qué pasa |
|---|---|
| **Extract** | Traer el dato de su origen — suele venir "sucio" |
| **Transform** | Limpiar, validar, darle forma |
| **Load** | Escribir el resultado en su destino final |

---

# La pregunta que casi nunca se hace

**¿Quién usa el dato al final, y para qué?**

- Un dashboard — decisión rápida
- Un modelo — se convierte en predicción (territorio de Maestría)
- Un reporte periódico — cierre mensual, regulatorio

---

# Sin esta pregunta...

Es fácil construir un ETL técnicamente correcto que nadie termina usando.

<span class="accent">El ejercicio de hoy cierra explícitamente con esta pregunta.</span>

---

# Lab guiado

`recursos/etl-tipo-cambio/` en Colab — solo llenar la configuración, ver extract → transform → load funcionando de principio a fin.

Después: correr (sin modificar) el dashboard de `recursos/etl-cripto/` — la respuesta visual a "quién consume esto al final".

---

# Entregable

Diagrama del flujo armado + captura del resultado, **incluyendo el dashboard final**.

---

# → Sesión 06

Data Lakes y gobierno del dato
