"""
producer_transacciones_stream.py
Simula la llegada en tiempo real de bank_transactions.csv: lee el CSV real (el
mismo de las Sesiones 4 y 5 de Maestría) fila por fila y publica cada una como un
mensaje JSON en Pub/Sub Lite, a una tasa controlada -- para poder probar
07_streaming_scoring.py sin depender de que ocurra un evento real.

pip install google-cloud-pubsublite pandas

Antes de correr, crear el topic y la suscripción (una sola vez):
  gcloud pubsub lite-topics create transacciones-stream \
      --location=us-central1-a --partitions=1 --per-partition-bytes=30GiB
  gcloud pubsub lite-subscriptions create transacciones-stream-sub \
      --location=us-central1-a --topic=transacciones-stream

Correr (desde tu máquina, Cloud Shell, o una VM -- no necesita el cluster de Spark):
  python producer_transacciones_stream.py --project <PROJECT_ID> \
      --csv bank_transactions.csv --tasa 20
"""
import argparse
import json
import time

import pandas as pd
from google.cloud.pubsublite.cloudpubsub import PublisherClient
from google.cloud.pubsublite.types import CloudRegion, CloudZone, TopicPath

parser = argparse.ArgumentParser()
parser.add_argument("--project", required=True)
parser.add_argument("--topic", default="transacciones-stream")
parser.add_argument("--location", default="us-central1-a", help="zona de Pub/Sub Lite")
parser.add_argument("--csv", default="bank_transactions.csv", help="descargado localmente del Drive del curso")
parser.add_argument("--tasa", type=int, default=20, help="mensajes por segundo")
args = parser.parse_args()

zona = CloudZone(CloudRegion(args.location[:-2]), args.location[-1])
topic_path = TopicPath(args.project, zona, args.topic)

# Solo las columnas que 07_streaming_scoring.py necesita -- el resto del esquema
# real de bank_transactions.csv (from_*, to_*, is_suspicious, suspicious_pattern)
# no viaja en el mensaje: en producción, el label (`is_suspicious`) nunca llega
# junto con el evento en tiempo real, se conoce después.
df = pd.read_csv(args.csv, usecols=["transaction_id", "timestamp", "amount", "currency"])

print(f"=== Publicando {len(df)} transacciones a ~{args.tasa} msg/s en {topic_path} ===")

with PublisherClient() as publisher:
    for _, fila in df.iterrows():
        mensaje = json.dumps({
            "transaction_id": str(fila["transaction_id"]),
            "timestamp": str(fila["timestamp"]),
            "amount": float(fila["amount"]),
            "currency": str(fila["currency"]),
        }).encode("utf-8")
        publisher.publish(topic_path, mensaje).result()
        time.sleep(1 / args.tasa)
