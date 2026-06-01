import streamlit as st
import pandas as pd
import pydeck as pdk
import requests
import re

st.set_page_config(
    page_title="Seattle Park Feature Explorer",
    layout="wide"
)

st.title("Seattle Park Feature Explorer")

BASE_API_URL = "https://unveiled-freely-defacing.ngrok-free.dev"

st.sidebar.header("Search and Filter")

search_text = st.sidebar.text_input("Search park by name or address").strip()
zip_code = st.sidebar.text_input("Filter by ZIP code, ex: 98144").strip()

features_response = requests.get(f"{BASE_API_URL}/features")

if features_response.status_code == 200:
    feature_options = ["All"] + features_response.json()
else:
    feature_options = ["All"]
    st.sidebar.warning("Could not load feature options from API.")

selected_features = st.sidebar.multiselect(
    "Filter by features",
    feature_options[1:]
)

response = requests.get(f"{BASE_API_URL}/parks")

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

df["features"] = df["features"].apply(
    lambda x: ", ".join(x) if isinstance(x, list) and len(x) > 0 else "None"
)

if search_text:
    df = df[
        df["name"].str.contains(search_text, case=False, na=False) |
        df["address"].str.contains(search_text, case=False, na=False)
    ]

if zip_code:
    df = df[
        df["zip_code"].astype(str).str.strip() == zip_code
    ]

if selected_features:
    for feature in selected_features:
        df = df[
            df["features"].str.contains(re.escape(feature), case=False, na=False, regex=True)
        ]

if df.empty:
    st.warning("No parks match your search and filters.")
    st.stop()

df = df.dropna(subset=["x_coord", "y_coord"])

df["lat"] = pd.to_numeric(df["y_coord"], errors="coerce")
df["lon"] = pd.to_numeric(df["x_coord"], errors="coerce")

df = df.dropna(subset=["lat", "lon"])

if df.empty:
    st.warning("No parks with valid coordinates found.")
    st.stop()

st.write(
    "This application utilizes data from Seattle's Open Data program to display parks on an interactive map. "
    "Search for parks by name or address, filter by ZIP code, or explore parks based on their features and amenities."
)

st.caption(
    "Data source: [Park Features](https://data.seattle.gov/Community-and-Culture/Park-Features-By-PMAID/xrnu-8eiq/about_data) "
    "& [Park Addresses](https://data.seattle.gov/Community-and-Culture/Seattle-Parks-And-Recreation-Park-Addresses/v5tj-kqhc/about_data)"
)

st.write("Number of parks shown:", len(df))

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position="[lon, lat]",
    get_radius=40,
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
        "text": "{name}\n{address}\nZIP: {zip_code}\nPMA ID: {pmaid}\nFeatures: {features}"
    }
)

st.pydeck_chart(deck, use_container_width=True)

st.subheader("Park Data")

st.data_editor(
    df[["name", "address", "zip_code", "pmaid", "features"]],
    use_container_width=True,
    hide_index=True,
    disabled=True,
    row_height=90,
    column_config={
        "name": st.column_config.TextColumn("Park Name", width="medium"),
        "address": st.column_config.TextColumn("Address", width="medium"),
        "zip_code": st.column_config.TextColumn("ZIP Code", width="small"),
        "pmaid": st.column_config.TextColumn("PMA ID", width="small"),
        "features": st.column_config.TextColumn("Features / Amenities", width="large"),
    }
)