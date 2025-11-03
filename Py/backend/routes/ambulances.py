from flask import Blueprint, jsonify
from pymongo import MongoClient
from config import Config

ambulance_bp = Blueprint("ambulance_bp", __name__)
client = MongoClient(Config.MONGO_URI)
hospital_db = client["hospital_db"]

@ambulance_bp.route("/", methods=["GET"])
def get_ambulances():
    ambulances = list(hospital_db["ambulances"].find({}, {"_id": 0}))
    return jsonify(ambulances)
