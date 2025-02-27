from flask_login import UserMixin
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask_sqlalchemy import SQLAlchemy
from app import db

ph = PasswordHasher()

class User(UserMixin, db.Model):
    __tablename__ = 'user_profile'

    # Colonnes
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
        except Exception as e:
            print(f"⚠ Erreur lors de la vérification du mot de passe : {e}")
            return False
        except Exception as e:
            print(f"⚠ Erreur lors de la vérification du mot de passe : {e}")
            return False

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

class Machines(db.Model):
    __tablename__ = 'machines'
    ID_machines = db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(10), unique=True, nullable=False)
    modele = db.Column(db.String(50))
    production_date = db.Column(db.DateTime)
    qrcode = db.Column(db.String(255))
    ID_production_ligne = db.Column(db.Integer, db.ForeignKey('production_ligne.ID_production_ligne'))
    ID_manual_link = db.Column(db.Integer, db.ForeignKey('manual.ID_manual_link'))
    ID_customer = db.Column(db.Integer, db.ForeignKey('customers_list.ID_customer'))

class CustomersList(db.Model):
    __tablename__ = 'customers_list'
    ID_customer = db.Column(db.Integer, primary_key=True)
    customers_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    logo = db.Column(db.String(255))

class History(db.Model):
    __tablename__ = 'history'
    ID_history = db.Column(db.Integer, primary_key=True)
    révisions_date = db.Column(db.DateTime)
    tech_name = db.Column(db.String(50))
    Remarks = db.Column(db.Text)
    ID_machines = db.Column(db.Integer, db.ForeignKey('machines.ID_machines'))
