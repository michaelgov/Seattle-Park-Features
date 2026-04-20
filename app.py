import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import csv

def read_json_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

park_list = read_json_file("data/park.json")

features = []
with open("data/park_amen.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        features.append(row)

def add_features_to_parks(parks, features):
    for park in parks:
        park_id = str(park.get("pmaid")).strip()
        park_features_list = []

        for feature in features:
            feature_park_id = str(feature.get("PMAID")).strip()
            if feature_park_id == park_id:
                park_features_list.append(feature.get("feature desc"))

        park["features"] = park_features_list

    return parks

my_parks_with_features = add_features_to_parks(park_list, features)

data = []
for park in my_parks_with_features:
    if park.get("x_coord") and park.get("y_coord"):
        data.append({
            "name": park.get("name"),
            "address": park.get("address"),
            "pmaid": park.get("pmaid"),
            "lat": float(park.get("y_coord")),
            "lon": float(park.get("x_coord")),
            "features": ", ".join(park.get("features", []))
        })

df = pd.DataFrame(data)

st.title("Seattle Parks Map")

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[lon, lat]',
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
    tooltip={"text": "{name}\n{address}\nPark ID: {pmaid}\nFeatures: {features}"}
)

st.pydeck_chart(deck)