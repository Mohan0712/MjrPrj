# backend/routes/incidents.py
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

incident_bp = Blueprint("incident_bp", __name__)

@incident_bp.route("/report", methods=["POST"])
def report_incident():
    """
    POST /api/incidents/report
    body: { latitude, longitude, type, severity, description }
    """
    try:
        data = request.json or {}
        lat = data.get("latitude")
        lon = data.get("longitude")
        e_type = data.get("type")
        severity = data.get("severity")
        desc = data.get("description", "")

        if lat is None or lon is None or not e_type or not severity:
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        db = current_app.config["MONGO_CLIENT"]["hospital_db"]
        doc = {
            "location": {"latitude": lat, "longitude": lon},
            "emergency_type": e_type,
            "severity": severity,
            "description": desc,
            "created_at": datetime.utcnow()
        }
        res = db["incidents"].insert_one(doc)
        return jsonify({"success": True, "incident_id": str(res.inserted_id)}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
