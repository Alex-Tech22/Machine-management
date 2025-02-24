from flask import Blueprint, render_template
from flask_login import login_required, current_user

client_bp = Blueprint('client', __name__)

@client_bp.route("/client")
@login_required
def client_page():
    return render_template("client/client.html", user=current_user)

@client_bp.route("/machines")
@login_required
def machines():
    return render_template("client/machines.html")

@client_bp.route("/machines/<int:machine_id>")
@login_required
def machine_info(machine_id):
    return render_template("client/machine_info.html", machine_id=machine_id)
