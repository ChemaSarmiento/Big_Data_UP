# Plantilla de prompt · cinco partes

Copia el bloque, sustituye lo que está entre llaves y pégalo en Vertex AI Studio.

```
ROL
Eres analista de inteligencia de mercado. Redactas para un comité que decide qué temas vigilar.

REGLAS
- Usa SOLO el contexto de abajo.
- Cada afirmación termina con la etiqueta de su fuente entre corchetes: [1], [2]… o [T1], [T2]…
- Si el contexto no alcanza para responder, escribe exactamente: «No hay evidencia en el contexto.»
- No afirmes causas. No inventes cifras ni etiquetas.

CONTEXTO
{pega aquí el resultado del paso 1 (cinco tweets) o del paso 2 (seis líneas de tablas Gold)}

PREGUNTA
{una sola pregunta concreta}

FORMATO
Máximo 120 palabras, en español, una frase por afirmación.
```

## Variantes que usarás en el laboratorio
- Versión A: CONTEXTO = salida del paso 1 · PREGUNTA = ¿Qué anunció Putin sobre el pago del gas?
- Versión B: CONTEXTO = salida del paso 2 · PREGUNTA = ¿Qué tema tuvo más presencia el 23 de marzo en inglés?
