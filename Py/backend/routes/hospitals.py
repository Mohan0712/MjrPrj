from flask import Blueprint, request, jsonify
from utils.geo_utils import haversine_distance 
import pandas as pd
import os

hospitals_bp = Blueprint("hospitals", __name__)

# Corrected path to CSV
DATA_PATH = os.path.join(os.path.dirname(__file__), "bangalore_200_hospitals.csv")
# Alternatively, you can use forward slashes:
# DATA_PATH = "C:/Users/Lenovo/OneDrive/Desktop/Py/bangalore_hospitals.csv"

# Load hospitals dataset
hospitals_df = pd.read_csv(DATA_PATH)

@hospitals_bp.route("/nearest-hospitals", methods=["POST"])
def nearest_hospitals():
    try:
        data = request.json
        lat, lon = data.get("latitude"), data.get("longitude")

        if lat is None or lon is None:
            return jsonify({"success": False, "message": "Missing location"}), 400

        # Calculate distance from user location to each hospital
        hospitals_df["distance"] = hospitals_df.apply(
            lambda row: haversine_distance(lat, lon, row["latitude"], row["longitude"]), axis=1
        )

        # Sort by nearest distance
        nearest = hospitals_df.sort_values("distance").head(5)

        return jsonify({
            "success": True,
            "hospitals": nearest.to_dict(orient="records")
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
