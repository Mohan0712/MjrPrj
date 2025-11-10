# backend/routes/patients.py
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

patient_bp = Blueprint("patient_bp", __name__)

@patient_bp.route("/vitals", methods=["POST"])
def save_vitals():
    """
    POST /api/patients/vitals
    body: {
      patient_id, hospital_name,
      vitals: { heart_rate, blood_pressure_systolic, ... },
      incident_id (optional)
    }
    """
    try:
        data = request.json or {}
        patient_id = data.get("patient_id")
        hospital_name = data.get("hospital_name")
        vitals = data.get("vitals")
        incident_id = data.get("incident_id")

        if not patient_id or not hospital_name or not vitals:
            return jsonify({"success": False, "message": "patient_id, hospital_name, vitals required"}), 400

        db = current_app.config["MONGO_CLIENT"]["patient_vitals"]
        doc = {
            "patient_id": patient_id,
            "hospital_name": hospital_name,
            "vital_signs": vitals,
            "incident_id": incident_id,
            "created_at": datetime.utcnow()
        }
        db["records"].insert_one(doc)
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
