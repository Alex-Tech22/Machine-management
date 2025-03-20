from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FileField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileAllowed, FileRequired
from app import db
from app.models import ModeleMachine

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

# Formulaire pour créer un nouvel utilisateur
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

# Formulaire pour ajouter un client
class AddClientForm(FlaskForm):
    customers_name = StringField("Nom du client", validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField("Adresse", validators=[DataRequired(), Length(min=5, max=255)])

    logo = FileField("Logo du client", validators=[
        FileAllowed(["jpg", "png", "jpeg"], "Seuls les fichiers JPG et PNG sont autorisés !")
    ])

    submit = SubmitField("Ajouter le client")

# Formulaire pour ajouter une machine
class AddMachineForm(FlaskForm):
    machine_name = StringField("Nom de la machine", validators=[DataRequired()])
    serial_number = StringField("Numéro de série", validators=[DataRequired()])
    production_date = DateField("Date de production", format='%Y-%m-%d', validators=[DataRequired()])
    model_id = SelectField("Modèle de la machine", validators=[DataRequired()], coerce=int)

    submit = SubmitField("Ajouter la machine")

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.model_id.choices = [(m.ID_model, m.model_name) for m in db.session.query(ModeleMachine).all()]

class AddProductionLigneForm(FlaskForm):
    prod_ligne_name = StringField("Nom de la ligne de production", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Ajouter la ligne")