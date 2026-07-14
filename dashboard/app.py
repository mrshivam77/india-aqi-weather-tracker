import sqlite3
import os
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="India Air Quality Tracker", layout="wide")

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "air_quality.db")


def aqi_category(aqi):
    if aqi is None or pd.isna(aqi):
        return "Unknown"
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Moderate"
    if aqi <= 150:
        return "Unhealthy (Sensitive Groups)"
    if aqi <= 200:
        return "Unhealthy"
    if aqi <= 300:
        return "Very Unhealthy"
    return "Hazardous"


@st.cache_data(ttl=600)
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM air_quality_readings", conn)
    conn.close()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp")
    return df


st.title("🌫️ India Air Quality & Weather Tracker")
st.caption("Live-updating pipeline pulling PM2.5, PM10, US AQI, and temperature for 8 Indian cities via Open-Meteo.")

if not os.path.exists(DB_PATH):
    st.error("No database found yet. Run `python scripts/backfill_history.py` first to populate historical data.")
    st.stop()

df = load_data()

if df.empty:
    st.warning("Database exists but has no rows yet. Run the backfill script first.")
    st.stop()

cities = sorted(df["city"].unique())
selected_cities = st.sidebar.multiselect("Cities", cities, default=cities)

filtered = df[df["city"].isin(selected_cities)]

# Latest reading per city
latest = filtered.sort_values("timestamp").groupby("city").tail(1)

st.subheader("Current Snapshot")
cols = st.columns(len(latest)) if len(latest) > 0 else [st]
for col, (_, row) in zip(cols, latest.iterrows()):
    with col:
        st.metric(
            label=row["city"],
            value=f"AQI {row['us_aqi']:.0f}" if pd.notna(row["us_aqi"]) else "N/A",
            delta=aqi_category(row["us_aqi"]),
            delta_color="off",
        )
        st.caption(f"PM2.5: {row['pm2_5']:.1f} µg/m³ | Temp: {row['temperature_c']:.1f}°C" if pd.notna(row['pm2_5']) else "No data")

st.divider()

c1, c2 = st.columns(2)

with c1:
    st.subheader("AQI Trend Over Time")
    fig = px.line(filtered, x="timestamp", y="us_aqi", color="city", labels={"us_aqi": "US AQI", "timestamp": "Time"})
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("PM2.5 Trend Over Time")
    fig2 = px.line(filtered, x="timestamp", y="pm2_5", color="city", labels={"pm2_5": "PM2.5 (µg/m³)", "timestamp": "Time"})
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Average AQI by City (selected period)")
avg_aqi = filtered.groupby("city")["us_aqi"].mean().sort_values(ascending=False)
fig3 = px.bar(avg_aqi, orientation="h", labels={"value": "Average US AQI", "city": "City"})
fig3.update_layout(showlegend=False, yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Temperature vs PM2.5")
fig4 = px.scatter(filtered, x="temperature_c", y="pm2_5", color="city",
                   labels={"temperature_c": "Temperature (°C)", "pm2_5": "PM2.5 (µg/m³)"})
st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.caption("Data source: Open-Meteo (free, no API key). Pipeline: Python + requests → SQLite → Streamlit.")
