-- BigQuery Studio
SELECT COUNT(*) AS tweets FROM tweets_bronze.entrada;

# Cloud Shell (sin costo de consulta)
gcloud storage cat -r 0-5000 gs://TU_BUCKET/war_tweets.txt | head -n 1
