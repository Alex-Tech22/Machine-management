from flask_login import UserMixin
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app import db

ph = PasswordHasher()  # ✅ Création d'une instance Argon2

class User(UserMixin, db.Model):
    __tablename__ = 'user_profile'

    id = db.Column("ID_user", db.Integer, primary_key=True)
    email = db.Column(db.String(75), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # ✅ Compatibilité Argon2
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    mobile_number = db.Column(db.String(14), unique=True, nullable=True)
    access_level = db.Column(db.Integer, nullable=False)

    def set_password(self, password):
        """Hash le mot de passe avec Argon2."""
        self.password = ph.hash(password)

    def check_password(self, password):
        """Vérifie le mot de passe avec Argon2. Gère aussi PBKDF2 pour migration automatique."""
        try:
            return ph.verify(self.password, password)
        except VerifyMismatchError:
            print("❌ Mot de passe incorrect (Argon2) !")
            return False
        except Exception:
            # Vérifier si c'est un ancien hash PBKDF2 et migrer vers Argon2
            from werkzeug.security import check_password_hash
            if check_password_hash(self.password, password):
                print("🔄 Migration du hash PBKDF2 vers Argon2...")
                self.set_password(password)
                db.session.commit()  # Sauvegarder le nouveau hash
                return True
            print("❌ Mot de passe incorrect (Ancien format) !")
            return False

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
