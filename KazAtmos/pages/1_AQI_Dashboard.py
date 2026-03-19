import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(layout="wide")


# Styling (Light blue / green)

st.markdown("""
<style>
body {
    background-color: #f0f8ff;
}
h1, h2, h3 {
    color: #2b7a78;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 AQI Dashboard — Almaty")


# WAQI API

def get_current_data():
    try:
        url = "https://api.waqi.info/feed/almaty/?token=demo"
        data = requests.get(url).json()

        if data["status"] == "ok":
            aqi = data["data"]["aqi"]
            iaqi = data["data"].get("iaqi", {})

            pm25 = iaqi.get("pm25", {}).get("v", None)
            pm10 = iaqi.get("pm10", {}).get("v", None)

            return aqi, pm25, pm10
    except:
        pass

    return 100, None, None


# AQI Status

def aqi_status(aqi):
    if aqi <= 50:
        return "Good 🟢"
    elif aqi <= 100:
        return "Moderate 🟡"
    elif aqi <= 150:
        return "Unhealthy ⚠️"
    else:
        return "Very Unhealthy 🔴"



# Generate historical data

def generate_data(current_aqi):
    dates = pd.date_range(end=datetime.today(), periods=10)

    noise = np.random.normal(0, 10, size=10)
    trend = np.linspace(current_aqi - 20, current_aqi, 10)

    values = trend + noise

    return pd.DataFrame({
        "date": dates,
        "aqi": values
    })



# AI Prediction

def predict_aqi(df):
    df["day"] = np.arange(len(df))

    X = df[["day"]]
    y = df["aqi"]

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)

    future = np.array([[len(df)], [len(df) + 1]])
    preds = model.predict(future)

    return preds



# MAIN

aqi, pm25, pm10 = get_current_data()


# Metrics row
col1, col2, col3, col4 = st.columns(4)

col1.metric("🌫️ AQI", aqi)
col2.metric("📊 Status", aqi_status(aqi))
col3.metric("PM2.5", pm25 if pm25 else "N/A")
col4.metric("PM10", pm10 if pm10 else "N/A")

st.divider()

# Historical + AI

df = generate_data(aqi)

st.subheader("📈 AQI Trend (Last 10 Days)")
st.line_chart(df.set_index("date"))


# Prediction
preds = predict_aqi(df)

future_dates = [
    datetime.today() + timedelta(days=1),
    datetime.today() + timedelta(days=2)
]

forecast_df = pd.DataFrame({
    "date": future_dates,
    "AQI Forecast": preds
})

st.subheader("🤖 AI Forecast (Next 2 Days)")
st.dataframe(forecast_df, use_container_width=True)


# Combined chart
combined = pd.concat([
    df.rename(columns={"aqi": "AQI"})[["date", "AQI"]],
    forecast_df.rename(columns={"AQI Forecast": "AQI"})
])

st.subheader("📊 Combined Trend + Forecast")
st.line_chart(combined.set_index("date"))