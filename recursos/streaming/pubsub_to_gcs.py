"""Puente docente Pub/Sub -> objetos JSON inmutables -> Spark file stream.
ACK después de persistir; deduplicar transaction_id en Spark. No garantiza
exactly-once end-to-end: un reintento puede reagrupar mensajes en otro objeto.
"""
import argparse
import hashlib
import json
import time
from producer_transacciones_stream import event_from_row


def persist_batch(messages, bucket, prefix):
    from google.api_core.exceptions import PreconditionFailed
    ids = sorted(m.message.message_id for m in messages)
    name = f"{prefix.rstrip('/')}/{hashlib.sha256('|'.join(ids).encode()).hexdigest()}.json"
    payload = []
    for item in messages:
        event = event_from_row(json.loads(item.message.data))
        payload.append(json.dumps(event))
    blob = bucket.blob(name)
    try:
        blob.upload_from_string("\n".join(payload) + "\n", content_type="application/x-ndjson", if_generation_match=0, timeout=30)
    except PreconditionFailed:
        # Same Pub/Sub IDs identify the same durable batch; never overwrite it.
        pass
    return name


def main():
    from google.cloud import pubsub_v1, storage
    from google.api_core.exceptions import DeadlineExceeded
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--subscription", default="transacciones-stream-sub")
    parser.add_argument("--bucket", required=True, help="Nombre del bucket, sin gs://")
    parser.add_argument("--prefix", required=True, help="streaming/<run-id>/entrada")
    parser.add_argument("--seconds", type=int, default=180)
    parser.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args()
    if args.seconds <= 0 or not 1 <= args.batch_size <= 1000:
        parser.error("seconds positivo y batch-size entre 1 y 1000")
    client = pubsub_v1.SubscriberClient()
    subscription = client.subscription_path(args.project, args.subscription)
    bucket = storage.Client(project=args.project).bucket(args.bucket)
    until = time.monotonic() + args.seconds
    try:
        while time.monotonic() < until:
            try:
                response = client.pull(request={"subscription": subscription, "max_messages": args.batch_size}, timeout=10)
            except DeadlineExceeded:
                continue
            messages = response.received_messages
            if not messages:
                continue
            ack_ids = [item.ack_id for item in messages]
            client.modify_ack_deadline(request={"subscription": subscription, "ack_ids": ack_ids, "ack_deadline_seconds": 120})
            name = persist_batch(messages, bucket, args.prefix)
            client.acknowledge(request={"subscription": subscription, "ack_ids": ack_ids})
            print(f"Persistidos {len(messages)} eventos: gs://{args.bucket}/{name}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
