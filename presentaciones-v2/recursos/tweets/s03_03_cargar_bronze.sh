gcloud services enable bigquery.googleapis.com
bq --location=US mk --dataset tweets_bronze
bq --location=US load --replace --source_format=CSV \
  --field_delimiter='þ' --quote='' --max_bad_records=0 \
  tweets_bronze.entrada "gs://TU_BUCKET/war_tweets.txt" value:STRING
