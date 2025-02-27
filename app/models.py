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

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

class Machines(db.Model):
    __tablename__ = "machines"

    # Colonnes
    ID_machines = db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(10), unique=True, nullable=False)
    modele = db.Column(db.String(50), nullable=False)
    production_date = db.Column(db.Date, nullable=False)
    qrcode = db.Column(db.String(255), unique=True, nullable=True)

    # Clés étrangères
    ID_customer = db.Column(db.Integer, db.ForeignKey("customers_list.ID_customer", ondelete="CASCADE"), nullable=False)
    ID_production_ligne = db.Column(db.Integer, db.ForeignKey("production_ligne.ID_production_ligne"), nullable=True)
    ID_manual_link = db.Column(db.Integer, db.ForeignKey("manual.ID_manual_link"), nullable=True)

    # Relations
    customer = db.relationship("CustomersList", back_populates="machines")
    history = db.relationship("History", back_populates="machine", cascade="all, delete-orphan")
    settings = db.relationship("Settings", back_populates="machine", cascade="all, delete-orphan")

class CustomersList(db.Model):
    __tablename__ = 'customers_list'

    # Colonnes
    ID_customer = db.Column(db.Integer, primary_key=True)
    customers_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    logo = db.Column(db.String(255))

    # Relations
    machines = db.relationship("Machines", back_populates="customer", cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return f"<Client {self.ID_customer}: {self.customers_name}>"


class History(db.Model):
    __tablename__ = "history"
    
    # Colonnes
    ID_history = db.Column(db.Integer, primary_key=True)
    revisions_date = db.Column("revisions_date", db.DateTime, nullable=False)
    tech_name = db.Column(db.String(50), nullable=False)
    remarks = db.Column(db.Text, nullable=True)

    # Clés étrangères
    ID_machines = db.Column(db.Integer, db.ForeignKey("machines.ID_machines", ondelete="CASCADE"), nullable=False)

    # Relations
    machine = db.relationship("Machines", back_populates="history")


class Settings(db.Model):
    __tablename__ = "settings"

    ID_settings = db.Column(db.Integer, primary_key=True)
    setting_name = db.Column(db.String(50), nullable=False)
    setting_data = db.Column(db.String(255), nullable=False)

    ID_machines = db.Column(db.Integer, db.ForeignKey("machines.ID_machines", ondelete="CASCADE"), nullable=False)
    ID_station = db.Column(db.Integer, db.ForeignKey("station.ID_station", ondelete="CASCADE"), nullable=False)

    machine = db.relationship("Machines", back_populates="settings")
    station = db.relationship("Station", back_populates="settings")

class Station(db.Model):
    __tablename__ = "station"

    # colonnes
    ID_station = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String(100), nullable=False)

    # Relation
    settings = db.relationship("Settings", back_populates="station", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Station {self.ID_station}: {self.station_name}>"
