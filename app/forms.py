from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length

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

class UserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    first_name = StringField("Prénom", validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField("Nom", validators=[DataRequired(), Length(min=2, max=30)])
    mobile_number = StringField("Téléphone", validators=[Length(min=10, max=14)])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=6)])
    access_level = IntegerField("Niveau d'accès (1, 2 ou 3)", validators=[DataRequired()])
    submit = SubmitField("Créer l'utilisateur")

# Formulaire pour demander un reset de mot de passe
class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Envoyer l'email de réinitialisation")

# Formulaire pour entrer le nouveau mot de passe
class ResetPasswordForm(FlaskForm):
    password = PasswordField("Nouveau mot de passe", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirmer le mot de passe", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Réinitialiser le mot de passe")