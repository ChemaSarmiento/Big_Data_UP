gcloud services enable dataproc.googleapis.com
gcloud dataproc batches submit pyspark json_a_parquet.py \
  --region=us-central1 \
  --batch=json-a-parquet-001 \
  --deps-bucket=TU_BUCKET \
  --properties=spark.dynamicAllocation.maxExecutors=4
