from flask import Flask, jsonify, request
import json

app = Flask(__name__)

with open("data/park.json", "r", encoding="utf-8") as file:
    parks = json.load(file)

with open("data/park_amen.json", "r", encoding="utf-8") as file:
    amenities = json.load(file)


@app.route("/")
def home():
    return "Seattle Parks API is running!"


@app.route("/parks", methods=["GET"])
def get_parks():
    return jsonify(parks)


@app.route("/amenities", methods=["GET"])
def get_amenities():
    return jsonify(amenities)


@app.route("/parks/<pmaid>", methods=["GET"])
def get_park_by_id(pmaid):
    for park in parks:
        if str(park["pmaid"]) == str(pmaid):
            return jsonify(park)

    return jsonify({"error": "Park not found"}), 404


@app.route("/parks/<pmaid>/amenities", methods=["GET"])
def get_park_amenities(pmaid):
    matching_amenities = []

    for amenity in amenities:
        if str(amenity["pmaid"]) == str(pmaid):
            matching_amenities.append(amenity)

    if len(matching_amenities) == 0:
        return jsonify({"error": "No amenities found for this park"}), 404

    return jsonify(matching_amenities)


@app.route("/parks/<pmaid>/full", methods=["GET"])
def get_full_park_info(pmaid):
    matching_park = None

    for park in parks:
        if str(park["pmaid"]) == str(pmaid):
            matching_park = park
            break

    if matching_park is None:
        return jsonify({"error": "Park not found"}), 404

    matching_amenities = []

    for amenity in amenities:
        if str(amenity["pmaid"]) == str(pmaid):
            matching_amenities.append(amenity)

    return jsonify({
        "park": matching_park,
        "amenities": matching_amenities
    })


@app.route("/search", methods=["GET"])
def search_parks():
    query = request.args.get("q", "").lower()

    results = []

    for park in parks:
        name = park.get("name", "").lower()
        address = park.get("address", "").lower()

        if query in name or query in address:
            results.append(park)

    return jsonify(results)