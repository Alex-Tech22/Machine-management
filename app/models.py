from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'user_profile'

    id = db.Column("ID_user", db.Integer, primary_key=True)
    email = db.Column(db.String(75), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    mobile_number = db.Column(db.String(14), unique=True, nullable=True)
    access_level = db.Column(db.Integer, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
