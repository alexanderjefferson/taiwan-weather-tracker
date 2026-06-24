import requests
import pandas as pd
from datetime import datetime
import os

os.makedirs("data/forecasts", exist_ok=True)

LAT = 25.0330
LON = 121.5654

data = requests.get(
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
    f"&temperature_unit=fahrenheit"
    f"&timezone=Asia/Taipei"
).json()

run_date = datetime.now().strftime("%Y-%m-%d")

df = pd.DataFrame({
    "forecast_date": data["daily"]["time"],
    "run_date": run_date,
    "high_temp": data["daily"]["temperature_2m_max"],
    "low_temp": data["daily"]["temperature_2m_min"],
    "prain": data["daily"]["precipitation_sum"]
})

file = "data/forecasts/forecasts_master.csv"

if os.path.exists(file):
    old = pd.read_csv(file)
    df = pd.concat([old, df], ignore_index=True)

# remove duplicates (only include farout forecasts)

df = df.drop_duplicates(subset=["forecast_date", "run_date"])

df.to_csv(file, index=False)

print("Forecast updated")