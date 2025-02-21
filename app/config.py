import os
from dotenv import load_dotenv

# Charger explicitement le fichier .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path, override=True)  # ✅ Force l'utilisation de .env même si des variables système existent

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')

    # Connexion MySQL via .env
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')

    # Vérification que toutes les variables sont bien chargées
    if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
        raise ValueError("❌ Erreur : Une ou plusieurs variables d'environnement sont manquantes dans .env")

    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration des cookies de session
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = True
