from itsdangerous import URLSafeTimedSerializer
from app import app

def generate_reset_token(email):
    """Génère un token sécurisé pour la réinitialisation de mot de passe"""
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def verify_reset_token(token, expiration=3600):
    """Vérifie un token de réinitialisation"""
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
        return email
    except:
        return None
