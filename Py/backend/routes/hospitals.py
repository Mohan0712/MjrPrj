# backend/routes/hospitals.py
from flask import Blueprint, request, jsonify, current_app
from math import radians, sin, cos, atan2, sqrt

hospital_bp = Blueprint("hospital_bp", __name__)

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return 2 * R * atan2(sqrt(a), sqrt(1 - a))

@hospital_bp.route("/nearest", methods=["POST"])
def nearest_hospitals():
    """
    POST /api/hospitals/nearest
    body: { latitude, longitude }
    """
    try:
        data = request.json or {}
        lat = float(data.get("latitude"))
        lon = float(data.get("longitude"))
        if lat is None or lon is None:
            return jsonify({"success": False, "message": "latitude/longitude required"}), 400

        db = current_app.config["MONGO_CLIENT"]["hospital_db"]
        hospitals = list(db["bangalore_hospitals"].find({}))

        enriched = []
        for h in hospitals:
            hlat = h.get("latitude")
            hlon = h.get("longitude")
            if hlat is None or hlon is None:
                continue
            dist = haversine_km(lat, lon, float(hlat), float(hlon))
            enriched.append({
                "id": str(h.get("_id")),
                "name": h.get("name"),
                "address": h.get("address"),
                "latitude": hlat,
                "longitude": hlon,
                "specialties": h.get("specialties", []),
                "beds": (h.get("current_availability") or {}).get("emergency", 0),
                "distance": round(dist, 2)
            })

        enriched.sort(key=lambda x: x["distance"])
        top5 = enriched[:5]

        return jsonify({"success": True, "hospitals": top5}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
