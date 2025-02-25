from flask_login import UserMixin
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

ph = PasswordHasher()

class User(UserMixin, db.Model):
    __tablename__ = 'user_profile'

    id = db.Column("ID_user", db.Integer, primary_key=True)
    email = db.Column(db.String(75), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    mobile_number = db.Column(db.String(14), unique=True, nullable=True)
    access_level = db.Column(db.Integer, nullable=False)

    def set_password(self, password):
        """Hash le mot de passe avec Argon2."""
        self.password = ph.hash(password)

    def check_password(self, password):
        """Vérifie le mot de passe avec Argon2"""
        try:
            return ph.verify(self.password, password)
        except VerifyMismatchError:
            print("❌ Mot de passe incorrect !")
            return False

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
