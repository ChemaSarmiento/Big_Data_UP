"""Reproduce una muestra del CSV en Pub/Sub estándar, sin cargarlo en RAM."""
import argparse
import csv
import json
import math
import time
from datetime import datetime


def event_from_row(row):
    event = {key: row[key] for key in ("transaction_id", "timestamp", "amount", "currency")}
    event["amount"] = float(event["amount"])
    if not event["transaction_id"] or not event["currency"] or not math.isfinite(event["amount"]):
        raise ValueError("Evento inválido: identificador, moneda o monto")
    datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
    return event


def main():
    from google.cloud import pubsub_v1
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--topic", default="transacciones-stream")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--tasa", type=float, default=20)
    parser.add_argument("--max-events", type=int, default=1200)
    args = parser.parse_args()
    if args.tasa <= 0 or args.max_events <= 0:
        parser.error("tasa y max-events deben ser positivos")
    publisher = pubsub_v1.PublisherClient()
    topic = publisher.topic_path(args.project, args.topic)
    try:
        with open(args.csv, newline="", encoding="utf-8") as handle:
            for i, row in enumerate(csv.DictReader(handle)):
                if i >= args.max_events:
                    break
                event = event_from_row(row)
                publisher.publish(topic, json.dumps(event).encode("utf-8")).result(timeout=30)
                time.sleep(1 / args.tasa)
        print(f"Publicación completada: hasta {args.max_events} eventos; timestamps originales, sin labels")
    finally:
        publisher.stop()


if __name__ == "__main__":
    main()
