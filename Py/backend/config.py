import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = "mongodb+srv://mohan07:P8PJtKFiLIhYLx4Z@cluster0.9pykb.mongodb.net/hospital_db?retryWrites=true&w=majority"
    SECRET_KEY = os.getenv("SECRET_KEY", "secret123")
