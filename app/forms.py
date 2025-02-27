from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileAllowed, FileRequired

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

class AddClientForm(FlaskForm):
    customers_name = StringField("Nom du client", validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField("Adresse", validators=[DataRequired(), Length(min=5, max=255)])

    logo = FileField("Logo du client", validators=[
        FileAllowed(["jpg", "png", "jpeg"], "Seuls les fichiers JPG et PNG sont autorisés !")
    ])

    submit = SubmitField("Ajouter le client")