import streamlit as st

st.set_page_config(page_title="Air Quality AI", layout="wide")


# Custom Styling

st.markdown("""
<style>
body {
    background-color: #f0f8ff;
}
h1, h2, h3 {
    color: #2b7a78;
}
.sidebar .sidebar-content {
    background-color: #d8f3dc;
}
</style>
""", unsafe_allow_html=True)


# Logo + Header

col1, col2 = st.columns([1, 4])

with col1:
    st.image("assets/logo.jpeg", width=120)

with col2:
    st.title("🌍 KazAtmos AQI predictor")


# Description

st.markdown("""
### 📌 About Our Project

This system helps people make safer decisions based on air quality.

👨‍👩‍👧 Families  
🧓 Elderly  
🫁 People with respiratory conditions  

---

### 💡 Innovation

- 📡 Real-time AQI from OpenWeather
- 🤖 AI prediction (Random Forest)
- 📅 2-day forecast
- ⚠️ Health-based recommendations

---

👉 Open the **AQI Dashboard** page to explore live data.
""")