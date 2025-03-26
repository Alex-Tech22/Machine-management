from flask_login import UserMixin
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app import db
from app import ph

class User(UserMixin, db.Model):
    __tablename__ = 'user_profile'

    # Colonnes
    id = db.Column("ID_user", db.Integer, primary_key=True)
    email = db.Column(db.String(75), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    mobile_number = db.Column(db.String(14), unique=True, nullable=True)

    # Clés étrangères
    access_level = db.Column(db.Integer, db.ForeignKey('role.access_level'), nullable=False)

    # Relations
    role = db.relationship("Role", back_populates="users")

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

class Role(db.Model):
    __tablename__ = 'role'

    # Colonnes
    access_level = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)

    # Relations
    users = db.relationship("User", back_populates="role")

class Machines(db.Model):
    __tablename__ = "machines"

    # Colonnes
    ID_machines = db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(10), unique=True, nullable=False)
    production_date = db.Column(db.Date, nullable=False)
    qrcode = db.Column(db.String(255), unique=True, nullable=True)

    # Clés étrangères
    ID_production_ligne = db.Column(db.Integer, db.ForeignKey("production_ligne.ID_production_ligne"), nullable=True)
    ID_manual_link = db.Column(db.Integer, db.ForeignKey("manual.ID_manual_link"), nullable=True)
    ID_model = db.Column(db.Integer, db.ForeignKey("modele_machine.ID_model"), nullable=False)

    # Relations
    history = db.relationship("History", back_populates="machine", cascade="all, delete-orphan")
    production_ligne = db.relationship("ProductionLigne", back_populates="machines")
    manual = db.relationship("Manual", back_populates="machines")
    modele_machine = db.relationship("ModeleMachine", back_populates="machines")

    def __repr__(self):
        return f"<Machines {self.ID_machines}: {self.machine_name}>"

class ProductionLigne(db.Model):
    __tablename__ = "production_ligne"

    # Colonnes
    ID_production_ligne = db.Column(db.Integer, primary_key=True)
    prod_ligne_name = db.Column(db.String(50), nullable=False)

    # Clé étrangère (corrigée)
    ID_customer = db.Column(db.Integer, db.ForeignKey("customers_list.ID_customer", ondelete="CASCADE"), nullable=False)

    # Relations
    customer = db.relationship("CustomersList", back_populates="production_lignes")
    machines = db.relationship("Machines", back_populates="production_ligne", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ProductionLigne {self.ID_production_ligne}: {self.prod_ligne_name}>"

class CustomersList(db.Model):
    __tablename__ = 'customers_list'

    # Colonnes
    ID_customer = db.Column(db.Integer, primary_key=True)
    customers_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    logo = db.Column(db.String(255))

    # Relations
    production_lignes = db.relationship("ProductionLigne", back_populates="customer", cascade="all, delete-orphan")

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

class ModeleMachine(db.Model):
    __tablename__ = "modele_machine"

    # Colonnes
    ID_model = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(50), nullable=False)

    # Relations
    machines = db.relationship("Machines", back_populates="modele_machine")
    stations = db.relationship("Station", back_populates="modele_machines", cascade="all, delete-orphan")
    def __repr__(self):
        return f"<ModeleMachine {self.ID_model}: {self.model_name}>"

class Station(db.Model):
    __tablename__ = "station"

    # Colonnes
    ID_station = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String(100), nullable=False)

    # Clés étrangères
    ID_model = db.Column(db.Integer, db.ForeignKey("modele_machine.ID_model"), nullable=False)

    # Relations
    modele_machines = db.relationship("ModeleMachine", back_populates="stations")
    settings = db.relationship("Settings", back_populates="station", cascade="all, delete-orphan")
    
class Settings(db.Model):
    __tablename__ = "settings"

    # Colonnes
    ID_settings = db.Column(db.Integer, primary_key=True)
    setting_name = db.Column(db.String(50), nullable=False)
    setting_type = db.Column(db.String(20), nullable=False)
    picture_link = db.Column(db.String(255), nullable=False)

    # Clés étrangères
    ID_station = db.Column(db.Integer, db.ForeignKey("station.ID_station", ondelete="CASCADE"), nullable=False)

    # Relations
    station = db.relationship("Station", back_populates="settings")
    values = db.relationship("SettingValue", back_populates="setting", cascade="all, delete-orphan")
    default_values = db.relationship("SettingDefaultValue", back_populates="setting")

class SettingValue(db.Model):
    __tablename__ = "setting_value"

    # Colonnes
    ID_setting_value = db.Column(db.Integer, primary_key=True)
    row_index = db.Column(db.Integer, nullable=True)
    col_index = db.Column(db.Integer, nullable=True)
    value = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(50), nullable=True)

    # Clés étrangères
    ID_settings = db.Column(db.Integer, db.ForeignKey("settings.ID_settings", ondelete="CASCADE"), nullable=False)
    
    # Relations
    setting = db.relationship("Settings", back_populates="values")

class SettingDefaultValue(db.Model):
    __tablename__ = "setting_default_value"

    # Colonnes
    ID_setting_default_value = db.Column(db.Integer, primary_key=True)
    row_index = db.Column(db.Integer, nullable=True)
    col_index = db.Column(db.Integer, nullable=True)
    default_value = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(50), nullable=True)

    # Clés étrangères
    ID_settings = db.Column(db.Integer, db.ForeignKey("settings.ID_settings"), nullable=False)
    
    # Relations
    setting = db.relationship("Settings", back_populates="default_values")

class Manual(db.Model):
    __tablename__ = "manual"

    # Colonnes
    ID_manual_link = db.Column(db.Integer, primary_key=True)
    manual_version = db.Column(db.String(50), nullable=False)
    manual_link = db.Column(db.String(255), nullable=False)
    manual_title = db.Column(db.String(100), nullable=False)

    # Relations
    machines = db.relationship("Machines", back_populates="manual")
