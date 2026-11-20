gcloud storage ls -l gs://TU_BUCKET/war_tweets.txt
gcloud storage objects describe gs://TU_BUCKET/war_tweets.txt \
  --format="yaml(name,size,storage_class,generation,md5_hash)"
