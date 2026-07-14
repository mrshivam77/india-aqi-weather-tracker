"""
SQLite storage layer. Keeping this in its own module means both the
backfill script and the live-update script write to the exact same schema.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "air_quality.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS air_quality_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            pm2_5 REAL,
            pm10 REAL,
            us_aqi REAL,
            temperature_c REAL,
            UNIQUE(city, timestamp)
        )
        """
    )
    conn.commit()
    return conn


def insert_reading(conn, city, timestamp, pm2_5, pm10, us_aqi, temperature_c):
    conn.execute(
        """
        INSERT OR IGNORE INTO air_quality_readings
            (city, timestamp, pm2_5, pm10, us_aqi, temperature_c)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (city, timestamp, pm2_5, pm10, us_aqi, temperature_c),
    )
