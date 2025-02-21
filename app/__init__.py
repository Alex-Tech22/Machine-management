from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

# Initialisation des extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "main.login"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialiser les extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Importation différée pour éviter les importations circulaires
    from app.models import User  
    from app.routes import main
    app.register_blueprint(main)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Import différé pour éviter l'erreur
    return User.query.get(int(user_id))
