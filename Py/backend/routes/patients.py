from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from config import Config

patient_bp = Blueprint("patient_bp", __name__)
client = MongoClient(Config.MONGO_URI)
patient_vitals_db = client["patient_vitals"]

@patient_bp.route("/update-vitals", methods=["POST"])
def update_vitals():
    data = request.json
    patient_id = data.get("patientId", "unknown")
    vitals = data.get("vitals")
    hospital_name = data.get("hospitalName")

    patient_vitals_db.records.insert_one({
        "patient_id": patient_id,
        "vitals": vitals,
        "hospital_name": hospital_name
    })

    return jsonify({"success": True, "message": "Vitals updated"})
