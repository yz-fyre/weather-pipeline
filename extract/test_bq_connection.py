from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secrets/bigquery-key.json"

client = bigquery.Client()

# List datasets to prove the connection works
datasets = list(client.list_datasets())
for d in datasets:
    print(d.dataset_id)