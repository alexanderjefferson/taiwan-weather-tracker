import requests
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib as mpl

url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=25.0330"
    "&longitude=121.5654"
    "&current=temperature_2m,relative_humidity_2m"
)

data = requests.get(url).json()

row = {
    "timestamp": datetime.now(),
    "temperature_c": data["current"]["temperature_2m"],
    "humidity": data["current"]["relative_humidity_2m"]
}

try:
    df = pd.read_csv("taipei_weather.csv")
except FileNotFoundError:
    df = pd.DataFrame()

df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

df.to_csv("taipei_weather.csv", index=False)

print("Data added")