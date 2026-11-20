# Cloud Shell: crea tu bucket
gcloud config get-value project
gcloud storage buckets create gs://TU_BUCKET --location=US --uniform-bucket-level-access

# Colab (otra pestaña): celdas del cuaderno del curso
# 1) from google.colab import drive; drive.mount('/content/drive')
# 2) from google.colab import auth; auth.authenticate_user()
# 3) project_id = 'TU_PROYECTO'; bucket_id = 'TU_BUCKET'
#    !gcloud config set project {project_id}
# 4) celda nueva: !gcloud storage cp /content/drive/MyDrive/war_tweets.txt gs://{bucket_id}
# Después: abre el cuaderno de Colab del curso (Drive → Storage), apunta el destino a gs://TU_BUCKET y ejecútalo.
