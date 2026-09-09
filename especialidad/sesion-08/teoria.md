# Teoría — Sesión 08: Costos, gobernanza y cómo evaluar un proyecto de datos

> Esta es la sesión más directamente útil para tu rol: no vas a construir nada, vas a
> salir con un framework concreto para hacer las preguntas correctas cuando tu equipo
> te presente una propuesta técnica.

## 1. Cómo se cobra la nube

Tres modelos de cobro que vas a encontrar una y otra vez, sin importar el proveedor:

- **Por uso (on-demand):** pagas exactamente por lo que consumes — bytes escaneados
  en BigQuery, horas de cómputo de un cluster. Sin compromiso, pero impredecible si
  nadie está vigilando el consumo.
- **Por hora (mientras está encendido):** un cluster de Spark cobra por cada hora que
  está activo, sin importar si está procesando datos o "esperando" — por eso
  `environment/gcp-setup.md` insiste en apagar el cluster al terminar cada lab
  (`--max-idle=1h --max-age=3h` lo hace automáticamente si alguien se olvida).
- **Por almacenamiento:** un costo pequeño pero constante, por cada GB guardado, cada
  mes, indefinidamente — a diferencia del cómputo, este costo no se apaga solo.

## 2. Qué preguntas hacer para evitar sorpresas de costo

Cinco preguntas que cualquier perfil de negocio puede hacer, sin necesitar
conocimiento técnico, y que exponen riesgos reales:

1. **¿Este sistema se apaga solo cuando no se usa, o hay que apagarlo manualmente?**
   (un cluster olvidado prendido es la causa #1 de sorpresas de facturación en
   cualquier equipo que empieza con la nube)
2. **¿Hay una alerta configurada si el gasto se sale de lo esperado?**
3. **¿El costo escala con el uso, o hay un componente fijo alto sin importar cuánto se
   use?**
4. **¿Quién tiene permiso para crear recursos nuevos, y hay límite de gasto por
   persona/equipo?**
5. **¿Qué pasa si el proveedor cambia sus precios? ¿Cuánto dependemos de un solo
   proveedor (vendor lock-in)?**

## 3. Framework para evaluar una propuesta técnica

Cuatro dimensiones, en el orden en que vale la pena preguntarlas:

| Dimensión | Pregunta central |
|---|---|
| **Arquitectura** | ¿Los componentes propuestos corresponden al problema real, o hay sobre-ingeniería (ver Sesión 1)? |
| **Costo** | ¿Cuál es el costo estimado mensual, y qué pasa si el uso crece 10x? |
| **Riesgo** | ¿Qué pasa si un componente falla? ¿Hay un plan de respaldo, o todo depende de que nada salga mal? |
| **Tiempo** | ¿El cronograma propuesto incluye tiempo de prueba y ajuste, o asume que todo funciona a la primera? |

El caso de `recursos/mariadb/README.md` (tabla "Qué cambió respecto al original") es
un ejemplo real de por qué esto importa: la versión original exponía la base de datos
a internet completo (`0.0.0.0/0`) con contraseñas escritas directamente en el código —
"barato y rápido" de construir, pero un riesgo de seguridad real que ninguna de las
cuatro preguntas de arriba habría dejado pasar sin respuesta.

---

## Referencias

- [Google Cloud — Cost management overview](https://cloud.google.com/cost-management)
- [Google Cloud — Set up budgets and alerts](https://cloud.google.com/billing/docs/how-to/budgets)
- [Google Cloud — Well-Architected Framework (las cuatro dimensiones de arriba, versión oficial extendida)](https://cloud.google.com/architecture/framework)
