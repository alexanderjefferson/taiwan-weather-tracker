# Taiwan Weather Tracker 🌦️

A data-driven weather analysis project that explores historical and real-time weather patterns in Taiwan, focused on the travel window of **July 22 – August 10**. The project builds a multi-year climate dataset, analyzes trends, and compares historical conditions to forecasted and observed weather.

---

## 📌 Project Goals

- Collect historical weather data for Taipei during a fixed travel window across multiple years
- Analyze long-term climate patterns (temperature, rainfall, humidity)
- Build daily climatology for trip planning
- Compare yearly variability and identify extreme conditions
- Prepare a framework to compare **forecast vs actual weather** (in progress)

---

## 📊 Data Sources

This project uses the Open-Meteo API:

- Historical weather archive data
- Hourly humidity data
- Daily temperature and precipitation summaries

---

## ⚙️ Features

### 📥 Data Collection
- Downloads historical weather for each year (July 22 – August 10)
- Extracts:
  - Daily high temperature (°F)
  - Daily low temperature (°F)
  - Precipitation
  - Relative humidity (daily average from hourly data)

### 📊 Analysis
- Combines multiple years into a single dataset
- Computes:
  - Average trip conditions
  - Rain probability by date
  - Year-to-year variability
- Identifies:
  - Hottest / coolest years
  - Wettest / driest patterns

### 📈 Visualization
- Temperature trends across years
- Rain probability by day of trip window
- Climate variability plots

---

## 🌡️ Example Insights

- Typical Taipei summer highs: ~90–95°F
- High humidity: often 75–90%
- Rain probability varies significantly by day
- Strong year-to-year variability due to monsoon and typhoon season

---
