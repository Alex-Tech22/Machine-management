from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from config import Config
from app.routes import register_blueprints

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    register_blueprints(app)  # Enregistre les Blueprints

    return app
