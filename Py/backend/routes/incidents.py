from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from config import Config
from utils.geo_utils import nearest_hospitals

incident_bp = Blueprint("incident_bp", __name__)

# Connect to Atlas
client = MongoClient(Config.MONGO_URI)

# Use hospital_db from Atlas
hospital_db = client["hospital_db"]
incidents_col = hospital_db["incidents"]

@incident_bp.route("/report", methods=["POST"])
def report_incident():
    try:
        data = request.json
        location = data.get("location")
        emergency_type = data.get("emergencyType")
        severity = data.get("severity")
        description = data.get("description", "")

        if not location or not emergency_type:
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # Save incident
        incident = {
            "location": location,
            "emergency_type": emergency_type,
            "severity": severity,
            "description": description
        }
        incidents_col.insert_one(incident)

        # Get hospitals collection from Atlas
        hospitals = list(hospital_db["bangalore_hospitals"].find())

        # Find nearest hospitals
        nearest = nearest_hospitals(location, hospitals, 5)

        return jsonify({"success": True, "hospitals": nearest})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
