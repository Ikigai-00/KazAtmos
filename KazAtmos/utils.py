import requests
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor

# -------------------------------
# WAQI API (No key needed)
# -------------------------------
def get_current_data():
    """
    Fetch current AQI + pollutants from WAQI API
    Returns: (aqi, pm25, pm10)
    """
    try:
        url = "https://api.waqi.info/feed/almaty/?token=demo"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("status") == "ok":
            aqi = data["data"].get("aqi", 100)
            iaqi = data["data"].get("iaqi", {})

            pm25 = iaqi.get("pm25", {}).get("v")
            pm10 = iaqi.get("pm10", {}).get("v")

            return aqi, pm25, pm10

    except Exception as e:
        print("API Error:", e)

    # fallback (prevents crash)
    return 100, None, None


# -------------------------------
# AQI Status
# -------------------------------
def aqi_status(aqi):
    if aqi <= 50:
        return "Good 🟢"
    elif aqi <= 100:
        return "Moderate 🟡"
    elif aqi <= 150:
        return "Unhealthy ⚠️"
    else:
        return "Very Unhealthy 🔴"


# -------------------------------
# Generate historical data
# -------------------------------
def generate_data(current_aqi):
    """
    Create realistic past AQI trend (since free APIs don't provide history easily)
    """
    dates = pd.date_range(end=datetime.today(), periods=10)

    noise = np.random.normal(0, 8, size=10)
    trend = np.linspace(current_aqi - 25, current_aqi, 10)

    values = trend + noise

    return pd.DataFrame({
        "date": dates,
        "aqi": values
    })


# -------------------------------
# AI Prediction (Improved)
# -------------------------------
def predict_aqi(df):
    """
    Predict next 2 days AQI using Random Forest
    """
    df = df.copy()
    df["day"] = np.arange(len(df))

    X = df[["day"]]
    y = df["aqi"]

    model = RandomForestRegressor(
        n_estimators=120,
        max_depth=5,
        random_state=42
    )
    model.fit(X, y)

    future_days = np.array([
        [len(df)],
        [len(df) + 1]
    ])

    predictions = model.predict(future_days)

    return predictions