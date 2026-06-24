import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Taiwan Weather Tracker", layout="wide")

# -----------------------
# Load data
# -----------------------
forecast = pd.read_csv("data/forecasts/forecasts_master.csv")
actual = pd.read_csv("data/observations/daily_actual.csv")
historical_files = "data/historical/"

forecast["forecast_date"] = pd.to_datetime(forecast["forecast_date"])
forecast["run_date"] = pd.to_datetime(forecast["run_date"])
actual["date"] = pd.to_datetime(actual["date"])

# -----------------------
# Merge forecast + actual
# -----------------------
df = forecast.merge(
    actual,
    left_on="forecast_date",
    right_on="date",
    how="inner"
)

df = df[df["run_date"] < df["forecast_date"]]
df["lead_time"] = (df["forecast_date"] - df["run_date"]).dt.days

df["temp_error"] = df["high_temp"] - df["high"]
df["rain_error"] = df["prain"] - df["rain"]

# -----------------------
# Sidebar filters
# -----------------------
st.sidebar.title("Filters")

lead_range = st.sidebar.slider(
    "Lead Time (days before forecast)",
    int(df["lead_time"].min()),
    int(df["lead_time"].max()),
    (1, int(df["lead_time"].max()))
)

df_filtered = df[df["lead_time"].between(*lead_range)]

# -----------------------
# Title
# -----------------------
st.title("🌦 Taiwan Weather Analysis Dashboard")
st.write("Historical + Forecast + Actual Weather for July 22 – Aug 10")

# -----------------------
# Tabs
# -----------------------
tab1, tab2, tab3 = st.tabs(["📊 Forecast Skill", "🌧 Rain Analysis", "📅 Historical Climatology"])

# -----------------------
# TAB 1: Forecast skill
# -----------------------
with tab1:
    st.subheader("Temperature Error vs Lead Time")

    skill = df_filtered.groupby("lead_time")["temp_error"].apply(lambda x: x.abs().mean())

    fig, ax = plt.subplots()
    skill.sort_index(ascending=False).plot(ax=ax)

    ax.set_xlabel("Days Before Event")
    ax.set_ylabel("MAE (°F)")
    ax.set_title("Forecast Error vs Lead Time")

    st.pyplot(fig)

    st.metric("Overall Temp MAE", round(df["temp_error"].abs().mean(), 2))

# -----------------------
# TAB 2: Rain analysis
# -----------------------
with tab2:
    st.subheader("Rain Forecast Bias")

    rain_skill = df_filtered.groupby("lead_time")["rain_error"].mean()

    fig, ax = plt.subplots()
    rain_skill.sort_index(ascending=False).plot(ax=ax)

    ax.set_xlabel("Days Before Event")
    ax.set_ylabel("Bias (Forecast - Actual)")
    ax.set_title("Rain Forecast Bias vs Lead Time")

    st.pyplot(fig)

# -----------------------
# TAB 3: Historical climatology
# -----------------------
with tab3:
    st.subheader("Historical Temperature Pattern (Trip Window)")

    hist = pd.concat(
        [pd.read_csv(f"data/historical/{y}.csv") for y in range(2016, 2026)]
    )

    hist["date"] = pd.to_datetime(hist["date"])
    hist["month_day"] = hist["date"].dt.strftime("%m-%d")

    daily_avg = hist.groupby("month_day")["high_temp"].mean()

    fig, ax = plt.subplots()
    daily_avg.plot(ax=ax)

    ax.set_ylabel("Avg High (°F)")
    ax.set_title("Historical Temperature (July 22 – Aug 10)")

    st.pyplot(fig)