from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField(
        "Email", 
        validators=[DataRequired(), Email()], 
        render_kw={"autocomplete": "email", "class": "input-field", "placeholder": "Votre email"}
    )
    password = PasswordField(
        "Mot de passe", 
        validators=[DataRequired()], 
        render_kw={"autocomplete": "current-password", "class": "input-field", "placeholder": "Mot de passe"}
    )
    remember = BooleanField("Se souvenir de moi")
    submit = SubmitField("Se connecter", render_kw={"class": "login-button"})
