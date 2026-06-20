# Weather Pipeline

A small end-to-end data engineering pipeline that pulls live weather data, lands it in a cloud data warehouse, and runs on an automated schedule - built entirely on free-tier tools. I built this to explore and develop my understanding of data engineering with Python and the cloud using the help of Generative AI Tools.

## What Does this project do?

Every 6 hours, a Python script will fetch current weather data for Belfast from the [Open-Meteo API](https://open-meteo.com/) and write a new row into a Google BigQuery table. The whole thing runs automatically via GitHub Actions.

```
Open-Meteo API → Python extract script → BigQuery (weather.weather_raw)
                        ↑
              GitHub Actions (scheduled, every 6h)
```

## Tech stack

| Layer | Tool |
|---|---|
| Data source | Open-Meteo API (free, no API key) |
| Extraction | Python (`requests`, `pandas`) |
| Storage / Warehouse | Google BigQuery (free sandbox tier) |
| Orchestration / Scheduling | GitHub Actions (cron schedule) |
| Secrets management | GitHub Actions Secrets |

## Project structure

```
weather-pipeline/
├── .github/workflows/
│   └── extract.yml          # scheduled GitHub Action, runs every 6 hours
├── extract/
│   ├── fetch_weather.py     # pulls weather data, writes to BigQuery
│   ├── create_table.py      # one-off script to create the BigQuery table/schema
│   └── test_bq_connection.py # sanity check for BigQuery auth
├── requirements.txt
├── .gitignore
└── README.md
```

## How it works

1. **Extract**: `fetch_weather.py` calls the Open-Meteo API for current temperature, humidity, and wind speed.
2. **Load**: the result is loaded into a BigQuery table (`weather.weather_raw`) using `google-cloud-bigquery`.
3. **Schedule**: a GitHub Actions workflow (`.github/workflows/extract.yml`) runs this script automatically every 6 hours using a cron trigger, authenticating to Google Cloud via a service account key stored as a GitHub Secret.

## Running it locally

```bash
git clone https://github.com/yz-fyre/weather-pipeline.git
cd weather-pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You also need:
- A Google Cloud project with BigQuery enabled (free sandbox tier, no card required)
- A service account JSON key with `BigQuery Data Editor` and `BigQuery Job User` roles, saved locally at `secrets/bigquery-key.json` (never committed — see `.gitignore`)

Then run:
```bash
python extract/fetch_weather.py
```

## Roadmap

- [x] Extract weather data from a public API
- [x] Load into BigQuery
- [x] Automate with GitHub Actions on a schedule
- [ ] Transform raw data with dbt (daily aggregates, rolling averages)
- [ ] Build a dashboard (Streamlit / Looker Studio) on top of the transformed data
- [ ] Add data quality tests

