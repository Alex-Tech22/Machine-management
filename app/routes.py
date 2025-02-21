from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm
from app.models import User

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print("✅ Formulaire soumis !")  # Debug
        user = User.get_by_email(form.email.data)

        if not user:
            print("❌ Utilisateur introuvable !")  # Debug
            flash("Identifiant ou mot de passe incorrect.", "danger")
            return render_template("login.html", form=form)

        if not user.check_password(form.password.data):
            print("❌ Mot de passe incorrect !")  # Debug
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
    flash("Déconnexion réussie!", "info")
    return redirect(url_for("main.login"))
