# 🌫️ India Air Quality & Weather Tracker

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-red)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automated-success)

An end-to-end data engineering and analytics project that automatically collects live air quality and weather data for major Indian cities, stores historical records in a SQLite database, and visualizes insights through an interactive Streamlit dashboard.

---

## 🎯 Problem

Most air quality dashboards either display only the latest readings or rely on static datasets. This project builds an automated data pipeline that continuously collects live air quality and weather data for major Indian cities, stores historical records in a SQLite database, and powers an interactive dashboard with zero manual intervention.

---

## ✨ Features

- 🌍 Live AQI & weather monitoring for 8 Indian cities
- 🔄 Automatic hourly data updates using GitHub Actions
- 🗄️ Historical data stored in SQLite
- 📊 Interactive Streamlit dashboard
- 📈 Trend analysis with Plotly
- ⚡ Fully automated end-to-end data pipeline
- 🔑 Uses the free Open-Meteo API (no API key required)

---

## 📊 Live Demo

👉 **View the interactive dashboard:**  
https://india-aqi-weather-tracker.streamlit.app/

---

## 🏗️ Project Architecture

```text
                Open-Meteo API
                      │
                      ▼
        backfill_history.py (One-Time)
                      │
                      ▼
             SQLite Database
                      ▲
                      │
     fetch_latest.py (Every Hour)
                      │
          GitHub Actions Scheduler
                      │
                      ▼
        Streamlit Interactive Dashboard
```

---

## ⚙️ How the Pipeline Works

### 1️⃣ Backfill Historical Data

**`scripts/backfill_history.py`**

- Runs only once locally.
- Downloads 30 days of hourly historical AQI and weather data for all cities.
- Stores everything inside a SQLite database.

### 2️⃣ Automatic Hourly Updates

**`scripts/fetch_latest.py`**

- Fetches the latest AQI and weather readings.
- Appends new records to the SQLite database.
- Automatically runs every hour using GitHub Actions.
- Commits the updated database back to GitHub.
- No server or personal computer needs to remain running.

### 3️⃣ Interactive Dashboard

**`dashboard/app.py`**

Reads data directly from the SQLite database and provides:

- Current AQI and weather snapshots
- Historical AQI trends
- PM2.5 trend analysis
- Average AQI comparison across cities
- Temperature vs PM2.5 relationship
- Interactive Plotly visualizations

---

## 🔍 Cities Tracked

- Bangalore
- Mumbai
- New Delhi
- Gorakhpur
- Chennai
- Hyderabad
- Pune
- Kolkata

---

## 🛠️ Tech Stack

- Python
- Pandas
- Requests
- SQLite
- Streamlit
- Plotly
- GitHub Actions
- Open-Meteo API

---

## 📁 Project Structure

```text
├── .github/
│   └── workflows/
│       └── update_data.yml
├── dashboard/
│   └── app.py
├── data/
│   └── air_quality.db
├── notebooks/
│   └── 01_explore.ipynb
├── scripts/
│   ├── backfill_history.py
│   ├── fetch_latest.py
│   ├── db.py
│   └── cities.py
├── requirements.txt
└── README.md
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/mrshivam77/india-aqi-weather-tracker.git
cd india-aqi-weather-tracker
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Backfill Historical Data

Run this only once.

```bash
python scripts/backfill_history.py
```

This creates:

```
data/air_quality.db
```

with 30 days of historical AQI and weather data.

## 4. Launch the Dashboard

```bash
streamlit run dashboard/app.py
```

## 5. Enable Automatic Updates

After pushing the project to GitHub:

- Open the **Actions** tab.
- Enable the **Update Air Quality Data** workflow.
- GitHub Actions will automatically run every hour.
- You can also click **Run workflow** to test it manually.

## 6. Deploy to Streamlit Community Cloud

Deploy the Streamlit application by selecting:

```
dashboard/app.py
```

as the entry point.

Since the SQLite database is updated every hour through GitHub Actions, the dashboard always displays the latest available data automatically.

---

## 📌 Why This Project Stands Out

Most beginner data portfolios stop at analyzing a downloaded CSV.

This project demonstrates a complete end-to-end data pipeline by:

- Collecting live data from real-world APIs
- Automating hourly data ingestion using GitHub Actions
- Storing historical records inside a SQLite database
- Visualizing insights through an interactive dashboard

Unlike a typical Kaggle notebook that performs a one-time analysis on a static dataset, this project simulates a production-style analytics workflow with automated data collection, scheduled updates, persistent storage, and live visualization.

---

## 🚀 Future Improvements

- Support for 100+ Indian cities
- PostgreSQL integration instead of SQLite
- Docker containerization
- AQI alert notifications via Email/SMS
- Machine Learning-based AQI forecasting
- REST API for external integrations

---
