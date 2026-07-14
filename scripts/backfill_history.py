"""
Run this ONCE to populate 30 days of historical air quality + weather data
for every city in cities.py. Open-Meteo's free API allows up to 92 days of
hourly history with no API key, which means the dashboard has real trend
data to show immediately instead of waiting weeks for live updates to build up.

Usage:
    python scripts/backfill_history.py
"""

import requests
import sys
import os

sys.path.append(os.path.dirname(__file__))
from cities import CITIES
from db import get_connection, insert_reading

AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

PAST_DAYS = 30


def fetch_air_quality_history(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm2_5,pm10,us_aqi",
        "past_days": PAST_DAYS,
        "forecast_days": 0,
        "timezone": "auto",
    }
    r = requests.get(AIR_QUALITY_URL, params=params, timeout=30)
    r.raise_for_status()
    return r.json()["hourly"]


def fetch_weather_history(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "past_days": PAST_DAYS,
        "forecast_days": 0,
        "timezone": "auto",
    }
    r = requests.get(WEATHER_URL, params=params, timeout=30)
    r.raise_for_status()
    return r.json()["hourly"]


def main():
    conn = get_connection()
    total_rows = 0

    for city, (lat, lon) in CITIES.items():
        print(f"Fetching {PAST_DAYS} days of history for {city}...")
        try:
            aq = fetch_air_quality_history(lat, lon)
            weather = fetch_weather_history(lat, lon)
        except requests.RequestException as e:
            print(f"  Failed for {city}: {e}")
            continue

        times = aq["time"]
        pm2_5_vals = aq["pm2_5"]
        pm10_vals = aq["pm10"]
        aqi_vals = aq["us_aqi"]
        temp_vals = weather["temperature_2m"]

        for i, ts in enumerate(times):
            insert_reading(
                conn,
                city=city,
                timestamp=ts,
                pm2_5=pm2_5_vals[i],
                pm10=pm10_vals[i],
                us_aqi=aqi_vals[i],
                temperature_c=temp_vals[i] if i < len(temp_vals) else None,
            )
        conn.commit()
        print(f"  Inserted {len(times)} hourly readings for {city}")
        total_rows += len(times)

    conn.close()
    print(f"\nDone. {total_rows} total readings loaded into data/air_quality.db")


if __name__ == "__main__":
    main()
