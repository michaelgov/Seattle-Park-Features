from flask import Flask, jsonify, request
import json

app = Flask(__name__)

with open("data/park.json", "r", encoding="utf-8") as file:
    parks = json.load(file)

with open("data/park_amen.json", "r", encoding="utf-8") as file:
    amenities = json.load(file)

def add_features_to_park(park):
    park_id = str(park.get("pmaid", "")).strip()

    park_features = []

    for amenity in amenities:
        amenity_park_id = str(amenity.get("pmaid", "")).strip()

        if amenity_park_id == park_id:
            park_features.append(amenity.get("feature_desc"))

    park_copy = park.copy()

    if len(park_features) == 0:
        park_copy["features"] = "None"
    else:
        park_copy["features"] = ", ".join(park_features)

    return park_copy

@app.route("/")
def home():
    return "Seattle Parks API is running!"


@app.route("/parks", methods=["GET"])
def get_parks():
    parks_with_features = []

    for park in parks:
        parks_with_features.append(add_features_to_park(park))

    return jsonify(parks_with_features)


@app.route("/parks/zip/<zip_code>", methods=["GET"])
def get_parks_by_zip(zip_code):
    results = []

    for park in parks:
        if str(park.get("zip_code", "")).strip() == str(zip_code).strip():
            results.append(add_features_to_park(park))

    return jsonify(results)


@app.route("/parks/<pmaid>", methods=["GET"])
def get_park_by_id(pmaid):
    for park in parks:
        if str(park.get("pmaid", "")).strip() == str(pmaid).strip():
            return jsonify(add_features_to_park(park))

    return jsonify({"error": "Park not found"}), 404


@app.route("/parks/<pmaid>/amenities", methods=["GET"])
def get_park_amenities(pmaid):
    matching_amenities = []

    for amenity in amenities:
        if str(amenity.get("pmaid", "")).strip() == str(pmaid).strip():
            matching_amenities.append(amenity)

    if len(matching_amenities) == 0:
        return jsonify({"error": "No amenities found for this park"}), 404

    return jsonify(matching_amenities)


@app.route("/parks/<pmaid>/full", methods=["GET"])
def get_full_park_info(pmaid):
    matching_park = None

    for park in parks:
        if str(park.get("pmaid", "")).strip() == str(pmaid).strip():
            matching_park = park
            break

    if matching_park is None:
        return jsonify({"error": "Park not found"}), 404

    matching_amenities = []

    for amenity in amenities:
        if str(amenity.get("pmaid", "")).strip() == str(pmaid).strip():
            matching_amenities.append(amenity)

    return jsonify({
        "park": matching_park,
        "amenities": matching_amenities
    })

@app.route("/search", methods=["GET"])
def search_parks():
    query = request.args.get("q", "").strip().lower()

    results = []

    for park in parks:
        name = park.get("name", "").lower()
        address = park.get("address", "").lower()

        if query in name or query in address:
            results.append(add_features_to_park(park))

    return jsonify(results)