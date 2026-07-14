"""
Run this periodically (e.g. every hour via cron or Windows Task Scheduler)
to keep appending the CURRENT reading for every city into the database.
This is what turns the project from a one-time notebook into a real,
ongoing ETL pipeline.

Usage:
    python scripts/fetch_latest.py

To schedule on Windows: Task Scheduler -> Create Basic Task -> Trigger: Daily,
repeat every 1 hour -> Action: start a program -> point it at python.exe with
this script's full path as the argument.

To schedule on Mac/Linux: add a line to `crontab -e`:
    0 * * * * cd /full/path/to/aqi-project && python3 scripts/fetch_latest.py
"""

import requests
import sys
import os
from datetime import datetime, timezone

sys.path.append(os.path.dirname(__file__))
from cities import CITIES
from db import get_connection, insert_reading

AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_current(lat, lon):
    aq_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "pm2_5,pm10,us_aqi",
        "timezone": "auto",
    }
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m",
        "timezone": "auto",
    }
    aq = requests.get(AIR_QUALITY_URL, params=aq_params, timeout=30).json()["current"]
    weather = requests.get(WEATHER_URL, params=weather_params, timeout=30).json()["current"]
    return aq, weather


def main():
    conn = get_connection()
    run_time = datetime.now(timezone.utc).isoformat(timespec="minutes")

    for city, (lat, lon) in CITIES.items():
        try:
            aq, weather = fetch_current(lat, lon)
        except requests.RequestException as e:
            print(f"Failed to fetch {city}: {e}")
            continue

        insert_reading(
            conn,
            city=city,
            timestamp=aq.get("time", run_time),
            pm2_5=aq.get("pm2_5"),
            pm10=aq.get("pm10"),
            us_aqi=aq.get("us_aqi"),
            temperature_c=weather.get("temperature_2m"),
        )
        print(f"{city}: AQI={aq.get('us_aqi')} PM2.5={aq.get('pm2_5')} Temp={weather.get('temperature_2m')}C")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
