"""Descargar artefactos GCS para Spark local sin asumir un conector gs://."""
from pathlib import Path
import tempfile
from urllib.parse import urlparse


def local_model(uri):
    if not uri.startswith("gs://"):
        path = Path(uri).resolve()
        if not path.is_dir(): raise ValueError(f"No existe el modelo: {path}")
        return str(path), None
    from google.cloud import storage
    parsed = urlparse(uri)
    prefix = parsed.path.strip("/") + "/"
    staging = tempfile.TemporaryDirectory(prefix="curso-modelo-")
    root = Path(staging.name)
    try:
        blobs = list(storage.Client().list_blobs(parsed.netloc, prefix=prefix))
        if not blobs: raise ValueError(f"Modelo vacío: {uri}")
        for blob in blobs:
            relative = blob.name[len(prefix):]
            if not relative or blob.name.endswith('/'): continue
            target = (root / relative).resolve()
            if not target.is_relative_to(root.resolve()): raise ValueError("Ruta de artefacto inválida")
            target.parent.mkdir(parents=True, exist_ok=True)
            blob.download_to_filename(str(target))
        return str(root), staging
    except Exception:
        staging.cleanup()
        raise
