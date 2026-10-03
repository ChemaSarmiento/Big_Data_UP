"""Checks meaningful failure paths without creating billable cloud resources."""
import csv
import importlib
import importlib.util
import json
import math
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
for relative in ['recursos/spark', 'recursos/streaming', 'recursos/serving']:
    sys.path.insert(0, str(ROOT / relative))


def test_psi_constant_repeated_quantiles_and_empty():
    from monitor_drift import calcular_psi
    assert calcular_psi([10] * 100, [10] * 100) == pytest.approx(0)
    assert calcular_psi([10] * 100, [30] * 100) > 0.25
    assert math.isfinite(calcular_psi([1, 1, 1, 2], [1, 2, 2, 2]))
    with pytest.raises(ValueError): calcular_psi([], [1])
    with pytest.raises(ValueError): calcular_psi([1], [float('nan')])


def test_events_validate_and_never_publish_label():
    from producer_transacciones_stream import event_from_row
    row = {'transaction_id': 't1', 'timestamp': '2026-01-01T12:00:00Z', 'amount': '10', 'currency': 'MXN', 'is_suspicious': '1'}
    assert set(event_from_row(row)) == {'transaction_id','timestamp','amount','currency'}
    with pytest.raises(ValueError): event_from_row({**row, 'amount': 'nan'})
    with pytest.raises(ValueError): event_from_row({**row, 'timestamp': 'not-a-date'})


def test_bridge_immutable_retries_and_failure():
    from pubsub_to_gcs import persist_batch
    from google.api_core.exceptions import PreconditionFailed
    items = [SimpleNamespace(message=SimpleNamespace(message_id='p1', data=json.dumps({'transaction_id':'t1','timestamp':'2026-01-01T00:00:00Z','amount':10,'currency':'MXN'}).encode()))]
    calls = []
    class Blob:
        def upload_from_string(self, payload, **kwargs):
            calls.append((payload,kwargs))
    bucket = SimpleNamespace(blob=lambda name: Blob())
    name1 = persist_batch(items, bucket, 'stream/test/entrada')
    assert name1 == persist_batch(items, bucket, 'stream/test/entrada')
    assert calls[0][1]['if_generation_match'] == 0
    class Existing:
        def upload_from_string(self, *args, **kwargs): raise PreconditionFailed('already written')
    assert persist_batch(items, SimpleNamespace(blob=lambda name: Existing()), 'stream/test/entrada') == name1
    class Failed:
        def upload_from_string(self, *args, **kwargs): raise RuntimeError('write failed')
    with pytest.raises(RuntimeError): persist_batch(items, SimpleNamespace(blob=lambda name: Failed()), 'stream/test/entrada')


def test_local_spark_training_stream_and_api(tmp_path, monkeypatch):
    monkeypatch.setenv('PYSPARK_PYTHON', sys.executable)
    from pyspark.sql import SparkSession, functions as F
    from pyspark.ml import PipelineModel
    from stream_common import events
    from ml_common import read_transactions, temporal_split
    training = importlib.import_module('04_pipeline_ml')
    spark = SparkSession.builder.master('local[2]').appName('course-smoke').config('spark.ui.enabled','false').config('spark.sql.shuffle.partitions','2').getOrCreate()
    spark.conf.set('spark.sql.session.timeZone','UTC')
    spark.sparkContext.setLogLevel('ERROR')
    data = tmp_path / 'bank.csv'
    start = datetime(2026,1,1)
    with data.open('w',newline='') as handle:
        writer = csv.writer(handle); writer.writerow(['transaction_id','timestamp','amount','currency','is_suspicious'])
        for n in range(240): writer.writerow([f't{n}',(start+timedelta(minutes=n)).isoformat(),10+n%50,'MXN' if n%3 else 'USD',int(n%7==0)])
    output = str(tmp_path/'model')
    try:
        metrics = training.train(spark,str(data),output,'2026-01-01T03:00:00')
        assert metrics['train_rows']==180 and metrics['test_rows']==60
        assert Path(output,'metrics.json').exists() and 0<=metrics['pr_auc']<=1
        model = PipelineModel.load(metrics['model_uri'])
        raw = read_transactions(spark,str(data))
        train, test = temporal_split(raw,'2026-01-01T03:00:00')
        assert model.transform(test).count()==60
        with pytest.raises(ValueError): temporal_split(raw,'2030-01-01')
        duplicate = tmp_path/'dup.csv'; duplicate.write_text(data.read_text()+data.read_text().splitlines()[1]+'\n')
        with pytest.raises(ValueError, match='único'): read_transactions(spark,str(duplicate))
        # File stream processes duplicate IDs once inside the watermark horizon.
        incoming = tmp_path/'incoming'; incoming.mkdir()
        event = {'transaction_id':'same','timestamp':'2026-01-01T04:00:00','amount':55.,'currency':'NEW'}
        (incoming/'batch.json').write_text('\n'.join([json.dumps(event)]*2)+'\n')
        stream = model.transform(events(spark,str(incoming))).select('transaction_id','prediction')
        query = stream.writeStream.format('memory').queryName('course_scores').outputMode('append').option('checkpointLocation',str(tmp_path/'checkpoint')).start()
        try:
            query.processAllAvailable()
            assert spark.table('course_scores').count()==1
        finally: query.stop()
        counts = events(spark,str(incoming)).groupBy(F.window('timestamp','1 minute'),'currency').count()
        count_query = counts.writeStream.format('memory').queryName('course_counts').outputMode('append').option('checkpointLocation',str(tmp_path/'count-checkpoint')).start()
        try:
            count_query.processAllAvailable()
            later = {**event, 'transaction_id':'later', 'timestamp':'2026-01-01T04:10:00'}
            (incoming/'later.json').write_text(json.dumps(later)+'\n')
            count_query.processAllAvailable()
            assert spark.table('course_counts').filter('count = 1').count() >= 1
        finally: count_query.stop()
        monkeypatch.setenv('MODELO', metrics['model_uri']); monkeypatch.setenv('MODELO_ROOT',str(tmp_path))
        monkeypatch.setenv('RELOAD_TOKEN','test-only-token')
        import serve_fraude
        from fastapi.testclient import TestClient
        with TestClient(serve_fraude.app) as client:
            response = client.post('/score',json={'transaction_id':'api','timestamp':'2026-01-01T04:00:00Z','amount':55,'currency':'NEW'})
            assert response.status_code==200, response.text
            assert 0<=response.json()['prob_sospechosa']<=1
            assert client.post('/reload',json={'model_uri':metrics['model_uri']}).status_code==403
            assert client.post('/reload',headers={'X-Reload-Token':'test-only-token'},json={'model_uri':'/outside/model'}).status_code==400
            assert client.post('/reload',headers={'X-Reload-Token':'test-only-token'},json={'model_uri':metrics['model_uri']}).status_code==200
    finally:
        spark.stop()
