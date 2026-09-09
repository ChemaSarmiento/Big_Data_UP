# Teoría — Sesión 07: Datos en tiempo real

> El objetivo hoy es reconocer una pregunta muy concreta en tu propio negocio: "¿esto
> necesita saberse ahora mismo, o basta con saberlo mañana?" — y entender que la
> respuesta cambia radicalmente el costo y la complejidad de la solución.

## 1. Batch vs. tiempo real

- **Batch (por lotes):** los datos se procesan en bloques, en intervalos programados
  — cada hora, cada noche, cada mes. Un reporte de ventas mensual es batch: no importa
  si el dato de la venta de hoy se procesa en este momento o esta noche, mientras esté
  listo a fin de mes.
- **Tiempo real (streaming):** los datos se procesan *conforme llegan*, uno por uno o
  en microlotes de segundos — sin esperar a acumular un lote completo. Detectar fraude
  mientras la transacción está ocurriendo (no al día siguiente en un reporte) es
  tiempo real: el valor de la detección depende de que llegue a tiempo para actuar.

La pregunta que separa un caso de otro no es técnica — es de negocio: **¿alguien va a
actuar de forma distinta si la respuesta llega en segundos en vez de en horas?** Si la
respuesta es no, batch es más simple, más barato, y no pierde nada.

## 2. Trade-offs de optar por tiempo real

Tiempo real no es "mejor" — es una decisión con costos concretos que hay que
justificar con el valor de negocio que aporta:

| | Batch | Tiempo real |
|---|---|---|
| **Costo de infraestructura** | Más bajo — se procesa en ventanas, el sistema puede estar apagado el resto del tiempo | Más alto — el sistema tiene que estar corriendo (o listo para responder) todo el tiempo |
| **Complejidad de desarrollo** | Menor — si algo falla a medianoche, se corrige y se vuelve a correr el lote | Mayor — hay que diseñar para fallas parciales sin perder ni duplicar eventos, mientras el sistema sigue corriendo |
| **Cuándo se justifica** | La mayoría de reportes, análisis históricos, entrenamiento de modelos | Fraude en el momento, alertas de seguridad, precios dinámicos |

El error común (mencionado ya en la Sesión 1) es elegir tiempo real por prestigio
técnico, no por necesidad de negocio — construir un sistema de streaming para un
reporte que de todas formas nadie mira hasta la mañana siguiente es pagar la
complejidad de arriba sin ganar nada del lado derecho de la tabla.

---

## Referencias

- [Google Cloud — Batch vs. stream processing](https://cloud.google.com/learn/what-is-stream-processing)
- [Confluent — Batch vs. Real-Time Data Processing](https://www.confluent.io/learn/batch-vs-real-time-data-processing/)
