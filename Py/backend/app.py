from flask import Flask, render_template
from flask_cors import CORS
from pymongo import MongoClient
from config import Config


# Flask App
app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
CORS(app)

# MongoDB Connection
client = MongoClient(Config.MONGO_URI)
hospital_db = client["hospital_db"]
patient_vitals_db = client["patient_vitals"]

# Blueprints
from routes.hospitals import hospitals_bp
from routes.patients import patient_bp
from routes.incidents import incident_bp
from routes.ambulances import ambulance_bp

app.register_blueprint(hospitals_bp, url_prefix="/api/hospitals")
app.register_blueprint(patient_bp, url_prefix="/api/patients")
app.register_blueprint(incident_bp, url_prefix="/api/incidents")
app.register_blueprint(ambulance_bp, url_prefix="/api/ambulances")

# Frontend Routes
@app.route("/")
def dashboard():
    hospital_count = hospital_db["bangalore_hospitals"].count_documents({})
    patient_count = patient_vitals_db["records"].count_documents({})
    incident_count = hospital_db["incidents"].count_documents({})
    ambulance_count = hospital_db["ambulances"].count_documents({})
    return render_template("dashboard.html",
                           hospital_count=hospital_count,
                           patient_count=patient_count,
                           incident_count=incident_count,
                           ambulance_count=ambulance_count)

@app.route("/report")
def report():
    return render_template("report_emergency.html")

@app.route("/hospitals")
def hospitals():
    hospitals = list(hospital_db["bangalore_hospitals"].find({}, {"_id": 0}))
    return render_template("hospitals.html", hospitals=hospitals)

@app.route("/patients")
def patients():
    patients = list(patient_vitals_db["records"].find({}, {"_id": 0}))
    return render_template("patients.html", patients=patients)

@app.route("/incidents")
def incidents():
    incidents = list(hospital_db["incidents"].find({}, {"_id": 0}))
    return render_template("incidents.html", incidents=incidents)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
