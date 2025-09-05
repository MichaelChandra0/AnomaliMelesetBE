import os
from dotenv import load_dotenv

# load variabel dari .env (kalau ada)
load_dotenv()


class Config:
    # Secret key Flask (wajib ada buat session / CSRF)
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")

    # Database (contoh pakai SQLite default)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cloudinary
    CLOUD_NAME = os.getenv("CLOUD_NAME")
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
