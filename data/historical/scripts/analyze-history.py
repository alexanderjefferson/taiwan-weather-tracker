import pandas as pd
import glob
import matplotlib.pyplot as plt

# extract csv data and combine

files = glob.glob("data/historical/*.csv")

dfs = []

for file in files:
    df = pd.read_csv(file)
    dfs.append(df)

weather = pd.concat(dfs, ignore_index=True)

weather["date"] = pd.to_datetime(weather["date"])

weather["month_day"] = weather["date"].dt.strftime("%m-%d")

weather["rainy"] = weather["rain"] > 4

rain_prob = (
    weather.groupby("month_day")["rainy"]
    .mean()
    * 100
)

print(weather.head())
print(weather.shape)

print("\nTrip Weather Summary")

# basic analysis

weather["date"] = pd.to_datetime(weather["date"])
weather["month_day"] = weather["date"].dt.strftime("%m-%d")
daily_avg = weather.groupby("month_day").agg(
    avg_high=("high_temp", "mean"),
    avg_low=("low_temp", "mean"),
    avg_hum=("humidity", "mean"),
    avg_rain=("rain", "mean")
)

print(daily_avg)

# plot

daily_avg["avg_high"].plot()
plt.title("Average High Temperature During Trip")
plt.ylabel("Temperature (°F)")
plt.tight_layout()

plt.savefig("data/historical/plots/average_trip_temperatures.png")
plt.clf()

daily_avg["avg_hum"].plot()
plt.title("Average Humidity During Trip")
plt.ylabel("%")
plt.tight_layout()

plt.savefig("data/historical/plots/average_trip_humidity.png")
plt.clf()

rain_prob.plot()
plt.title("Probability of Rain")
plt.ylabel("Percent")
plt.tight_layout()

plt.savefig("data/historical/plots/rain_probability.png")
plt.clf()

# summary

print("\n==== Taiwan Trip Summary ====\n")

print(
    f"Typical High: "
    f"{weather['high_temp'].mean():.1f}°F"
)

print(
    f"Typical Low: "
    f"{weather['low_temp'].mean():.1f}°F"
)

print(
    f"Typical Humidity: "
    f"{weather['humidity'].mean():.1f}%"
)

print(
    f"Rainy Days: "
    f"{(weather['rain'] > 4).mean()*100:.1f}%"
)

print(
    f"Heavy Rain: "
    f"{(weather['rain'] > 10).mean()*100:.1f}%"
)