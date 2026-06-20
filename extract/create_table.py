from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secrets/bigquery-key.json"

client = bigquery.Client()

table_id = f"{client.project}.weather.weather_raw"

schema = [
    bigquery.SchemaField("fetched_at", "TIMESTAMP"),
    bigquery.SchemaField("city", "STRING"),
    bigquery.SchemaField("temperature_c", "FLOAT"),
    bigquery.SchemaField("humidity_pct", "FLOAT"),
    bigquery.SchemaField("wind_speed_kmh", "FLOAT"),
]

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table, exists_ok=True)
print(f"Created table {table_id}")