from flask import Blueprint, render_template, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app.models import CustomersList, Machines, db
from app.forms import AddClientForm, AddMachineForm
from app.config import UPLOAD_FOLDER

client_bp = Blueprint('client', __name__)

@client_bp.route("/clients")
def clients():
    """Affiche la liste des clients depuis la base de données."""
    clients = CustomersList.query.all()
    return render_template("client/client.html", clients=clients)

@client_bp.route("/client/<int:client_id>")
def get_client(client_id):
    """Récupère les informations d'un client spécifique."""
    client = CustomersList.query.get(client_id)
    if client:
        return jsonify({
            "ID_customer": client.ID_customer,
            "customers_name": client.customers_name,
            "address": client.address,
            "logo": client.logo
        })
    return jsonify({"error": "Client non trouvé"}), 404
@client_bp.route("/machines")
@login_required
def machines():
    return render_template("client/machines.html")

@client_bp.route("/machines/<int:machine_id>")
@login_required
def machine_info(machine_id):
    return render_template("client/machine_info.html", machine_id=machine_id)

@client_bp.route("/clients/add", methods=["GET", "POST"])
def add_client():
    form = AddClientForm()

    if form.validate_on_submit():
        logo_url = "uploads/default_logo.png"  # Image par défaut

        # Gestion du fichier image
        if form.logo.data:
            filename = secure_filename(form.logo.data.filename)  # Sécurise le nom
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            form.logo.data.save(file_path)  # Sauvegarde l'image
            logo_url = f"uploads/{filename}"  # Chemin pour stockage en base

        # Création du client
        new_client = CustomersList(
            customers_name=form.customers_name.data,
            address=form.address.data,
            logo=logo_url
        )

        db.session.add(new_client)
        db.session.commit()
        
        flash(f"✅ Client {new_client.customers_name} ajouté avec succès !", "success")
        return redirect(url_for("client.clients"))  # Retour à la liste des clients

    return render_template("client/add_client.html", form=form)

@client_bp.route("/client/delete/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
    """Supprime un client ainsi que toutes ses données associées."""
    client = CustomersList.query.get(client_id)
    print(client) # Debug

    if client:
        # Supprimer aussi les fichiers logo s'ils existent
        if client.logo and client.logo != "logo_client/default_logo.png":
            file_path = os.path.join("app/static", client.logo)
            if os.path.exists(file_path):
                os.remove(file_path)

        db.session.delete(client)
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Client non trouvé"}), 404
    
@client_bp.route("/client/<int:client_id>/add_machine", methods=["GET", "POST"])
def add_machine(client_id):
    client = CustomersList.query.get_or_404(client_id)
    form = AddMachineForm()

    if form.validate_on_submit():
        new_machine = Machines(
            machine_name=form.machine_name.data,
            serial_number=form.serial_number.data,
            modele=form.modele.data,
            production_date=form.production_date.data,
            customer=client
        )

        db.session.add(new_machine)
        db.session.commit()
        flash("Machine ajoutée avec succès !", "success")
        return redirect(url_for("client.view_client", client_id=client_id))

    return render_template("add_machine.html", form=form, client=client)
