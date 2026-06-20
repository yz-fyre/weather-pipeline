import requests
import pandas as pd
import os
from google.cloud import bigquery

# Big Query 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secrets/bigquery-key.json"

#  API Request
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 54.5973,
    "longitude": -5.9301,
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
}

# request and store in JSON Format
response = requests.get(url, params=params)
data = response.json()
current = data["current"]

row = {
    "fetched_at": pd.Timestamp.now(tz="UTC"),
    "city": "Belfast",
    "temperature_c": current["temperature_2m"],
    "humidity_pct": current["relative_humidity_2m"],
    "wind_speed_kmh": current["wind_speed_10m"]
}

df = pd.DataFrame([row])

client = bigquery.Client()
table_id = f"{client.project}.weather.weather_raw"

job = client.load_table_from_dataframe(df, table_id)
job.result()  # wait for it to finish

print(f"Inserted row into {table_id}: {row}")