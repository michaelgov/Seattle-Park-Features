from flask import Flask, jsonify, request
import json

app = Flask(__name__)

with open("data/parks_compiled.json", "r", encoding="utf-8") as file:
    parks = json.load(file)

with open("data/features_index.json", "r", encoding="utf-8") as file:
    features_index = json.load(file)


@app.route("/")
def home():
    return "Seattle Parks API is running!"


@app.route("/parks", methods=["GET"])
def get_parks():
    return jsonify(parks)


@app.route("/parks/zip/<zip_code>", methods=["GET"])
def get_parks_by_zip(zip_code):
    results = []

    for park in parks:
        if str(park.get("zip_code", "")).strip() == str(zip_code).strip():
            results.append(park)

    return jsonify(results)


@app.route("/parks/feature/<feature_name>", methods=["GET"])
def get_parks_by_feature(feature_name):
    results = []

    for park in parks:
        features = park.get("features", [])

        for feature in features:
            if feature_name.lower() in feature.lower():
                results.append(park)
                break

    return jsonify(results)


@app.route("/parks/<pmaid>", methods=["GET"])
def get_park_by_id(pmaid):
    for park in parks:
        if str(park.get("pmaid", "")).strip() == str(pmaid).strip():
            return jsonify(park)

    return jsonify({"error": "Park not found"}), 404


@app.route("/parks/<pmaid>/full", methods=["GET"])
def get_full_park_info(pmaid):
    for park in parks:
        if str(park.get("pmaid", "")).strip() == str(pmaid).strip():
            return jsonify({
                "park": park,
                "features": park.get("features", "None")
            })

    return jsonify({"error": "Park not found"}), 404


@app.route("/search", methods=["GET"])
def search_parks():
    query = request.args.get("q", "").strip().lower()

    results = []

    for park in parks:
        name = park.get("name", "").lower()
        address = park.get("address", "").lower()

        if query in name or query in address:
            results.append(park)

    return jsonify(results)


@app.route("/features", methods=["GET"])
def get_features():
    feature_names = set()

    for park in parks:
        features = park.get("features", [])

        for feature in features:
            feature_names.add(feature)

    return jsonify(sorted(list(feature_names)))