#!/usr/bin/env python3
"""Añade la sección editorial al build existente de Firebase Hosting."""
from pathlib import Path
import shutil
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'presentaciones-v2'
DEST = ROOT / 'presentaciones/dist/refactor_especialidad'
# Solo materiales públicos; nunca scripts de build, cachés o notas internas del repo.
EXTENSIONS = {'.sh', '.html', '.css', '.js', '.json', '.md', '.sql', '.txt', '.csv', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.woff', '.woff2', '.ttf', '.otf'}
FOLDERS = ['compartido', 'editorial', 'identidad', 'recursos', 'piloto'] + [f'especialidad-{n:02d}' for n in range(1, 9)]
if not (DEST.parent / 'index.html').is_file():
    raise SystemExit('Falta build del sitio principal: npm run build:web en slides_maestria.')
if DEST.exists():
    shutil.rmtree(DEST)
DEST.mkdir()
for name in ['index.html', 'manifest.json', 'README.md']:
    shutil.copy2(SOURCE / name, DEST / name)
count = 3
for folder in FOLDERS:
    for src in (SOURCE / folder).rglob('*'):
        if not src.is_file() or src.suffix.lower() not in EXTENSIONS or any(p.startswith('.') or p == '__pycache__' for p in src.relative_to(SOURCE).parts):
            continue
        target = DEST / src.relative_to(SOURCE)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        count += 1
print(f'Sección /refactor_especialidad/: {count} archivos. Sitio principal intacto.')
