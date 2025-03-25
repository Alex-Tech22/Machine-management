from flask import Flask
from .auth_routes import auth_bp
from .user_routes import user_bp
from .client_routes import client_bp
from .home_routes import home_bp
from .machine_routes import machine_bp
from .admin_route import admin_bp

def register_blueprints(app: Flask):
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(client_bp, url_prefix="/client")
    app.register_blueprint(machine_bp, url_prefix="/machine")

