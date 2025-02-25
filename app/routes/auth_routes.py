from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user
from app.forms import LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, db
from app.utils.email_utils import send_reset_email
from itsdangerous import URLSafeTimedSerializer
from argon2 import PasswordHasher

ph = PasswordHasher()
auth_bp = Blueprint('auth', __name__)

# Générer un token sécurisé pour la réinitialisation
def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

# Vérifier le token et récupérer l'email
def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
        return email
    except:
        return None

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            flash("Identifiant ou mot de passe incorrect.", "danger")
            return render_template("auth/login.html", form=form)
        login_user(user, remember=form.remember.data)
        flash(f"Bienvenue {user.first_name}!", "success")
        return redirect(url_for("client.client_page"))
    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Déconnexion réussie!", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = generate_reset_token(user.email)
            send_reset_email(user.email, token)
        flash("📩 Un email de réinitialisation vous a été envoyé.", "info")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_request.html", form=form)

@auth_bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash("❌ Lien invalide ou expiré.", "danger")
        return redirect(url_for("auth.reset_request"))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("❌ Utilisateur introuvable.", "danger")
        return redirect(url_for("auth.reset_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = ph.hash(form.password.data)
        db.session.commit()
        flash("✅ Mot de passe réinitialisé!", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", form=form)
