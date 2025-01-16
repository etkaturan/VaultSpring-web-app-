import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))  # Go up to backend folder
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")  # Instance folder path

class Config:
    SECRET_KEY = "super_jwt_secret"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'app.db')}"  # Absolute path to app.db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super_jwt_secret"
