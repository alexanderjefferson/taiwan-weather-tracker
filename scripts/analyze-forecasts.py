import pandas as pd
import matplotlib.pyplot as plt

forecast = pd.read_csv("data/forecasts/forecasts_master.csv")
actual = pd.read_csv("data/observations/daily_actual.csv")

forecast["forecast_date"] = pd.to_datetime(forecast["forecast_date"])
forecast["run_date"] = pd.to_datetime(forecast["run_date"])
actual["date"] = pd.to_datetime(actual["date"])

df = forecast.merge(
    actual,
    left_on="forecast_date",
    right_on="date",
    how="inner"
)

df = df[df["run_date"] < df["forecast_date"]]

# days ahead forecast predicted
df["lead_time"] = (df["forecast_date"] - df["run_date"]).dt.days
df["temp_error"] = df["high_temp"] - df["high"]

skill = df.groupby("lead_time")["temp_error"].apply(lambda x: x.abs().mean())

print(skill)

skill.plot()
plt.title("Forecast Temperature Error vs Lead Time")
plt.ylabel("Mean Absolute Error (°F)")
plt.xlabel("Days Before Event")
plt.gca().invert_xaxis()
plt.tight_layout()

plt.savefig("plots/forecast_skill_temp.png")

df["rain_error"] = df["rain"] - df["rain"]

rain_skill = df.groupby("lead_time")["rain_error"].mean()

print(rain_skill)

rain_skill.plot()
plt.title("Rain Forecast Bias vs Lead Time")
plt.ylabel("Bias (Forecast - Actual)")
plt.xlabel("Days Before Event")
plt.gca().invert_xaxis()
plt.tight_layout()

plt.savefig("plots/rain_bias.png")

print("\n=== OVERALL MODEL PERFORMANCE ===")

print("Temp MAE:", df["temp_error"].abs().mean())
print("Rain MAE:", df["rain_error"].abs().mean())

print("\nMost predictable lead time:")
print(skill.idxmin(), "days out")