from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms import UserForm
from app.models import User, db

user_bp = Blueprint('user', __name__)

@user_bp.route("/profile")
@login_required
def profile():
    return render_template("user/profile.html", user=current_user)

@user_bp.route("/create_user", methods=["GET", "POST"])
@login_required
def create_user():
    if current_user.access_level not in [2, 3]:
        return redirect(url_for("client.client_page"))

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
        return redirect(url_for("client.client_page"))

    return render_template("user/create_user.html", form=form)
