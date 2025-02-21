from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm
from app.forms import UserForm
from app.models import User,db

main = Blueprint('main', __name__)

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
        new_user.set_password(form.password.data)  # Hash du mot de passe
        db.session.add(new_user)
        db.session.commit()
        flash("✅ Utilisateur créé avec succès !", "success")
        return redirect(url_for("main.client_page"))

    return render_template("create_user.html", form=form)
