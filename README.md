# 🌫️ India Air Quality & Weather Tracker

## 🎯 Problem
Track real-time air quality (PM2.5, PM10, US AQI) and weather across 8 Indian cities, with a pipeline that keeps updating itself automatically — not a one-time analysis of a static file.

## 📊 Live Demo
[View the interactive dashboard →](PASTE_YOUR_STREAMLIT_LINK_HERE)

## ⚙️ How the pipeline works
1. **`scripts/backfill_history.py`** — run once locally. Pulls 30 days of hourly historical AQI + weather data per city from Open-Meteo (free, no API key) and loads it into a local SQLite database.
2. **`scripts/fetch_latest.py`** — appends the current reading for every city to the database. Runs automatically every hour via **GitHub Actions** (see `.github/workflows/update_data.yml`), which commits the updated database back to this repo — no server or personal machine needs to stay on.
3. **`dashboard/app.py`** — Streamlit app that reads the database and renders live trend charts, current snapshots, and city comparisons.

## 🔍 Cities Tracked
Bangalore, Mumbai, New Delhi, Gorakhpur, Chennai, Hyderabad, Pune, Kolkata

## 🛠️ Tools
Python, requests, SQLite, Pandas, Streamlit, Plotly, GitHub Actions (scheduled automation)

## 📁 Project Structure
```
├── .github/workflows/
│   └── update_data.yml         # runs fetch_latest.py every hour automatically
├── data/
│   └── air_quality.db          # SQLite database (created by backfill script)
├── scripts/
│   ├── cities.py                # city coordinates config
│   ├── db.py                    # database schema + helpers
│   ├── backfill_history.py      # one-time: load 30 days of history
│   └── fetch_latest.py          # scheduled: append current reading
├── notebooks/
│   └── 01_explore.ipynb         # exploratory analysis on live data
├── dashboard/
│   └── app.py                   # Streamlit dashboard
├── requirements.txt
└── README.md
```

## 🚀 Setup Instructions

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Backfill 30 days of history (run once)
```bash
python scripts/backfill_history.py
```
This creates `data/air_quality.db` with real historical data — no waiting required to have a working dashboard.

### 3. Run the dashboard locally to check it
```bash
streamlit run dashboard/app.py
```

### 4. Push to GitHub (including the database file)
```bash
git init
git add .
git commit -m "Initial pipeline: backfill script, dashboard, GitHub Action"
git remote add origin https://github.com/mrshivam77/india-aqi-weather-tracker.git
git branch -M main
git push -u origin main
```

### 5. Turn on automatic updates
Once pushed, go to your repo's **Actions** tab on GitHub and confirm the "Update Air Quality Data" workflow is enabled. It will run every hour from then on, automatically. You can also click **Run workflow** to trigger it manually and test it immediately.

### 6. Deploy the dashboard
Deploy `dashboard/app.py` on [share.streamlit.io](https://share.streamlit.io) same as the previous project. Since the database is committed to the repo and updated hourly by GitHub Actions, the live dashboard will reflect fresh data automatically.

## 📌 Why this project is different from a typical Kaggle-notebook project
Most fresher portfolios analyze a static CSV once. This one pulls live data through a real API, stores it properly in a database, and keeps itself updated on a schedule with zero manual effort — the actual shape of a real-world data pipeline, not just an analysis.
