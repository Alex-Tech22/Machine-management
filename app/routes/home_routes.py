from flask import Blueprint, redirect, url_for, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route("/")
def home():
    return redirect(url_for("auth.login"))

@home_bp.route('/mentions-legales')
def mentions_legales():
    return render_template('mentions_legales.html')