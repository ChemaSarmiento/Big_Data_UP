# Publicación independiente de Especialidad

Ruta: https://bigdata-up.web.app/refactor_especialidad/

Firebase Hosting sirve `presentaciones/dist`. El sitio principal conserva sus rutas. `scripts/package-refactor.py` añade una carpeta separada con los materiales públicos de `presentaciones-v2`; no copia generadores Python ni cachés. Las rutas internas son relativas, por lo que slides, fuentes, prácticas y guías funcionan bajo ese prefijo.

## Build reproducible

Desde la raíz:

```sh
npm ci --ignore-scripts --prefix slides_maestria
npm run build:web --prefix slides_maestria
python3 presentaciones-v2/scripts/build.py
python3 presentaciones-v2/scripts/build-editorial.py
python3 presentaciones-v2/scripts/catalogo.py
python3 scripts/package-refactor.py
python3 -m http.server 4184 --bind 127.0.0.1 --directory presentaciones/dist
```

Abrir `/refactor_especialidad/`. La salida dist no se guarda en Git.

## Automatización

El workflow `.github/workflows/deploy-curso.yml` publica el canal live de Hosting en cada push a `plan3`, usando el secret de servicio existente. No despliega reglas Firestore. El disparo manual también está limitado a `plan3`. Los despliegues se serializan.

La versión antigua del workflow permanece en `plan2`: un push a esa rama podría volver a publicar un sitio sin la sección nueva. Usar `plan3` como rama de publicación desde este cambio; retirar el disparo antiguo al integrar las ramas. No se ha modificado la rama plan2 remotamente.

S1–S7 tienen rediseño editorial; S8 mantiene la base. Publicar el material no significa que los laboratorios cloud hayan sido ensayados.
