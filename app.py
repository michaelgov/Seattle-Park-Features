import streamlit as st
import pandas as pd
import pydeck as pdk
import requests

st.title("Seattle Parks Map")

BASE_API_URL = "https://unveiled-freely-defacing.ngrok-free.dev"

st.sidebar.header("Search and Filter")

search_text = st.sidebar.text_input("Search park by name or address").strip()
zip_code = st.sidebar.text_input("Filter by ZIP code, ex: 98144").strip()

if search_text:
    response = requests.get(
        f"{BASE_API_URL}/search",
        params={"q": search_text}
    )
elif zip_code:
    response = requests.get(
        f"{BASE_API_URL}/parks/zip/{zip_code}"
    )
else:
    response = requests.get(
        f"{BASE_API_URL}/parks"
    )

if response.status_code != 200:
    st.error("Could not connect to the Parks API.")
    st.write("Status code:", response.status_code)
    st.write("Response text:", response.text)
    st.stop()

parks_data = response.json()

df = pd.DataFrame(parks_data)

if df.empty:
    st.warning("No parks found.")
    st.stop()

df = df.dropna(subset=["x_coord", "y_coord"])

df["lat"] = pd.to_numeric(df["y_coord"], errors="coerce")
df["lon"] = pd.to_numeric(df["x_coord"], errors="coerce")

df = df.dropna(subset=["lat", "lon"])

if df.empty:
    st.warning("No parks with valid coordinates found.")
    st.stop()

st.write("Number of parks shown:", len(df))

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position="[lon, lat]",
    get_radius=60,
    get_fill_color=[255, 80, 80],
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=df["lat"].mean(),
    longitude=df["lon"].mean(),
    zoom=11,
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "text": "{name}\n{address}\nZIP: {zip_code}\nPark ID: {pmaid}\nFeatures: {features}"
    }
)

st.pydeck_chart(deck)

st.subheader("Park Data")
st.dataframe(df[["name", "address", "zip_code", "pmaid", "features"]])