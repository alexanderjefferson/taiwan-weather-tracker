import requests
import pandas as pd
import os
import numpy as np

LAT = 25.0330
LON = 121.5654

os.makedirs("data/historical", exist_ok=True)

for year in range(2016, 2026):

    start_date = f"{year}-07-22"
    end_date = f"{year}-08-10"

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={LAT}"
        f"&longitude={LON}"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
        "&daily=temperature_2m_max,temperature_2m_min,"
        "precipitation_sum"
        "&hourly=relative_humidity_2m"
        "&temperature_unit=fahrenheit"
        "&timezone=Asia/Taipei"
    )

    data = requests.get(url).json()

# fix humidity to daily value

    humidity_df = pd.DataFrame({
    "time": data["hourly"]["time"],
    "humidity": data["hourly"]["relative_humidity_2m"]
    })

    humidity_df["time"] = pd.to_datetime(humidity_df["time"])
    humidity_df["date"] = humidity_df["time"].dt.date

    daily_humidity = (
    humidity_df
    .groupby("date")["humidity"]
    .mean()
    .reset_index()
    )


    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "high_temp": data["daily"]["temperature_2m_max"],
        "low_temp": data["daily"]["temperature_2m_min"],
        "humidity": humidity_df.groupby("date")["humidity"].mean(),
        "rain": data["daily"]["precipitation_sum"]
    })

    df.to_csv(
        f"data/historical/{year}.csv",
        index=False
    )

    print(f"Saved {year}")
