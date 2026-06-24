import requests
import pandas as pd
from datetime import datetime, timedelta
import os

os.makedirs("data/observations", exist_ok=True)

# yesterday
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

LAT = 25.0330
LON = 121.5654

url = (
    "https://archive-api.open-meteo.com/v1/archive"
    f"?latitude={LAT}"
    f"&longitude={LON}"
    f"&start_date={yesterday}"
    f"&end_date={yesterday}"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
    f"&temperature_unit=fahrenheit"
    "&timezone=Asia/Taipei"
)

data = requests.get(url).json()

df = pd.DataFrame({
    "date": data["daily"]["time"],
    "high": data["daily"]["temperature_2m_max"],
    "low": data["daily"]["temperature_2m_min"],
    "rain": data["daily"]["precipitation_sum"]
})

file_path = "data/observations/daily_actual.csv"

# append instead of overwrite
if os.path.exists(file_path):
    old = pd.read_csv(file_path)
    df = pd.concat([old, df], ignore_index=True)

df.to_csv(file_path, index=False)

print(f"Saved actual weather for {yesterday} and added it to total file")
