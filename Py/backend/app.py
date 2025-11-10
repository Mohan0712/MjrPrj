# backend/app.py
from flask import Flask, render_template
from flask_cors import CORS
from pymongo import MongoClient

from backend.config import Config
from backend.routes.hospitals import hospital_bp
from backend.routes.incidents import incident_bp
from backend.routes.patients import patient_bp

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)
CORS(app)

# Mongo client attached to app config
mongo_client = MongoClient(Config.MONGO_URI)
app.config["MONGO_CLIENT"] = mongo_client

# APIs
app.register_blueprint(hospital_bp, url_prefix="/api/hospitals")
app.register_blueprint(incident_bp, url_prefix="/api/incidents")
app.register_blueprint(patient_bp, url_prefix="/api/patients")

# Pages
@app.route("/")
def dashboard():
    db_h = mongo_client["hospital_db"]
    db_p = mongo_client["patient_vitals"]
    hospital_count = db_h["bangalore_hospitals"].count_documents({})
    incident_count = db_h["incidents"].count_documents({})
    patient_count = db_p["records"].count_documents({})
    ambulance_count = db_h["ambulances"].count_documents({}) if "ambulances" in db_h.list_collection_names() else 0
    return render_template("dashboard.html",
                           hospital_count=hospital_count,
                           incident_count=incident_count,
                           patient_count=patient_count,
                           ambulance_count=ambulance_count)

@app.route("/report")
def report():
    return render_template("report_emergency.html")

@app.route("/hospitals")
def hospitals_page():
    db = mongo_client["hospital_db"]
    hospitals = list(db["bangalore_hospitals"].find({}, {"_id": 0}))
    return render_template("hospitals.html", hospitals=hospitals)

@app.route("/patients")
def patients_page():
    db = mongo_client["patient_vitals"]
    patients = list(db["records"].find({}, {"_id": 0}))
    return render_template("patients.html", patients=patients)

@app.route("/incidents")
def incidents_page():
    db = mongo_client["hospital_db"]
    incidents = list(db["incidents"].find({}, {"_id": 0}))
    return render_template("incidents.html", incidents=incidents)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
