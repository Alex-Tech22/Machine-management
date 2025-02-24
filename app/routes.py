from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from app.forms import UserForm
from app.models import User,db
from flask_mail import Mail, Message
from app import db, mail, app
from itsdangerous import URLSafeTimedSerializer
from argon2 import PasswordHasher

ph = PasswordHasher()  # Hashage du mot de passe

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

@main.route("/", methods=["GET", "POST"])
@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print("✅ Formulaire soumis !")  # Debug
        user = User.query.filter_by(email=form.email.data).first()

        if not user or not user.check_password(form.password.data):
            print("❌ Identifiant ou mot de passe incorrect !")  # Debug
            flash("Identifiant ou mot de passe incorrect.", "danger")
            return render_template("login.html", form=form)

        print("✅ Connexion réussie !")  # Debug
        login_user(user, remember=form.remember.data)
        flash(f"Bienvenue {user.first_name}!", "success")

        return redirect(url_for("main.client_page"))

    return render_template("login.html", form=form)

@main.route("/client")
@login_required
def client_page():
    print("✅ Redirection vers /client réussie !")  # Debug
    return render_template("client.html", user=current_user)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie!", "info") # Debug
    return redirect(url_for("main.login"))

@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@main.route("/create_user", methods=["GET", "POST"])
@login_required
def create_user():
    # ✅ Vérification du niveau d'accès
    if current_user.access_level not in [2, 3]:
        flash("❌ Vous n'avez pas l'autorisation de créer un utilisateur.", "danger")
        return redirect(url_for("main.client_page"))

    form = UserForm()

    if form.validate_on_submit():
        new_user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            mobile_number=form.mobile_number.data,
            access_level=form.access_level.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("✅ Utilisateur créé avec succès !", "success")
        return redirect(url_for("main.client_page"))

    return render_template("create_user.html", form=form)

# 🔹 Générer un token sécurisé pour la réinitialisation
def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

# 🔹 Vérifier le token et récupérer l'email
def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
        return email
    except:
        return None

# 🔹 Envoyer un email de réinitialisation
def send_reset_email(email, token):
    reset_link = url_for("auth.reset_password", token=token, _external=True)
    subject = "🔐 Réinitialisation de votre mot de passe"
    body = f"""
Bonjour,

Cliquez sur le lien suivant pour réinitialiser votre mot de passe :
{reset_link}

Si vous n'avez pas demandé de réinitialisation, ignorez cet email.

Cordialement,
L'équipe Mayekawa
"""

    with app.app_context():
        msg = Message(subject, 
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email])
        msg.body = body

        try:
            mail.send(msg)
            print(f"📨 Email de réinitialisation envoyé à {email}")
        except Exception as e:
            print(f"❌ Erreur d'envoi : {str(e)}")

# Route pour demander la réinitialisation
@auth.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = generate_reset_token(user.email)
            send_reset_email(user.email, token)
        flash("📩 Un email de réinitialisation vous a été envoyé.", "info")
        return redirect(url_for("auth.login"))
    return render_template("reset_request.html", form=form)

# Route pour réinitialiser le mot de passe (avec token)
@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash("❌ Lien de réinitialisation invalide ou expiré.", "danger")
        return redirect(url_for("auth.reset_request"))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("❌ Utilisateur introuvable.", "danger")
        return redirect(url_for("auth.reset_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = ph.hash(form.password.data)
        db.session.commit()
        flash("✅ Votre mot de passe a été réinitialisé !", "success")
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", form=form)