# Pruebas para Vertex AI Studio

El texto del modelo cambia en cada ejecución. No compares palabras: comprueba que se cumplan las reglas.

## Prueba A · contexto = los cinco tweets del paso 1
- **P1 (se puede responder):** ¿Qué anunció Putin sobre el pago del gas?
  Debe citar [3] y/o [4].
- **P2 (no se puede responder):** ¿Cuántos tweets hablaron de energía ese día?
  Debe escribir «No hay evidencia en el contexto.» El contexto solo tiene cinco tweets.

## Prueba B · contexto = las seis líneas del paso 2
- **P3:** ¿Qué tema tuvo más presencia el 23 de marzo en inglés? Debe citar [T1]: energía, 10530 tweets (3.382 %).
- **P4:** ¿Quién concentra la interacción? Debe citar [T3] y hablar de porcentajes de tweets y de likes por segmento.
- **P5:** ¿Por qué subió la energía? Debe escribir «No hay evidencia en el contexto.» Ninguna tabla trae causas.

## Cómo juzgar cada respuesta
1. ¿Cada afirmación termina con una etiqueta que existe en tu contexto?
2. ¿Cada cifra aparece, tal cual, en esa etiqueta?
3. ¿Dice «No hay evidencia en el contexto.» donde debe?
Si alguna respuesta falla, anótalo: esa afirmación pasa a la auditoría del paso 5 como «inventada».
