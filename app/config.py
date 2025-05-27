import os
from dotenv import load_dotenv

# Charger explicitement le fichier .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path, override=True)

UPLOAD_FOLDER = "app/static/logo_client"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("❌ SECRET_KEY non définie !")
    
    # Sel pour flask-security
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    if not SECURITY_PASSWORD_SALT:
        raise ValueError("❌ SECURITY_PASSWORD_SALT non défini dans .env !")

    # Connexion MySQL via .env
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')

    # lien vers les logo client
    UPLOAD_FOLDER = UPLOAD_FOLDER
    
    # Vérification que toutes les variables sont bien chargées
    if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
        raise ValueError("❌ Erreur : Une ou plusieurs variables d'environnement sont manquantes dans .env")

    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration des cookies de session
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = True

    # 🔹 Configuration SMTP pour l'envoi d'email (Modifie avec tes infos)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # Configuration de l'url du serveur
    PREFERRED_URL_SCHEME = "https"
    SERVER_NAME = "mayekawa_service"
