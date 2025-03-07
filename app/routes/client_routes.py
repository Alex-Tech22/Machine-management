from flask import Blueprint, render_template, jsonify, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app.models import CustomersList, Machines, ProductionLigne
from app import db
from app.forms import AddClientForm, AddMachineForm, AddProductionLigneForm
from app.config import UPLOAD_FOLDER

client_bp = Blueprint('client', __name__)

@client_bp.route("/clients")
def clients():
    """Affiche la liste des clients avec leurs lignes de production."""
    clients = CustomersList.query.all()
    selected_client = clients[0] if clients else None  # Sélection automatique du premier client
    production_lignes = ProductionLigne.query.filter_by(ID_customer=selected_client.ID_customer).all() if selected_client else []
    form = AddProductionLigneForm()
    machine_form = AddMachineForm()

    return render_template(
    "client/client.html",
    clients=clients,
    selected_client=selected_client,
    production_lignes=production_lignes,
    form=form,
    machine_form=machine_form)

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

@client_bp.route("/clients/add", methods=["GET", "POST"])
def add_client():
    form = AddClientForm()

    if form.validate_on_submit():
        logo_url = "logo_client/default_logo.png"  # Image par défaut

        # Gestion du fichier image
        if form.logo.data:
            filename = secure_filename(form.logo.data.filename)  # Sécurise le nom
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            form.logo.data.save(file_path)  # Sauvegarde l'image
            logo_url = f"logo_client/{filename}"  # Chemin pour stockage en base

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
        ligne_id = request.form.get("ligne_id", type=int)
        print(f"DEBUG: ligne_id reçu = {ligne_id}")  # Ajoute ce log pour voir la valeur reçue

        if not ligne_id:
            flash("❌ Erreur : Ligne de production non spécifiée.", "danger")
            return redirect(url_for("client.clients"))

        new_machine = Machines(
            machine_name=form.machine_name.data,
            serial_number=form.serial_number.data,
            modele=form.modele.data,
            production_date=form.production_date.data,
            ID_production_ligne=ligne_id
        )

        db.session.add(new_machine)
        db.session.commit()
        flash("✅ Machine ajoutée avec succès !", "success")
        return redirect(url_for("client.clients"))

    return render_template("client/add_machine.html", form=form, client=client)



@client_bp.route("/client/<int:client_id>/production_lignes", methods=["GET"])
def get_production_lignes(client_id):
    """Récupère les lignes de production d'un client."""
    client = CustomersList.query.get(client_id)
    
    if not client:
        return jsonify({"error": "Client non trouvé"}), 404

    lignes = ProductionLigne.query.filter_by(ID_customer=client_id).all()
    lignes_data = [{"id": ligne.ID_production_ligne, "name": ligne.prod_ligne_name} for ligne in lignes]

    return jsonify(lignes_data)

@client_bp.route("/client/<int:client_id>/production_ligne/<int:ligne_id>")
def get_machines(client_id, ligne_id):
    """Récupère les machines affectées à une ligne de production."""
    machines = Machines.query.filter_by(ID_production_ligne=ligne_id).all()

    if not machines:
        return jsonify({"message": "Aucune machine trouvée"}), 200

    return jsonify([{"id": machine.ID_machines, "name": machine.machine_name} for machine in machines])

@client_bp.route("/client/<int:client_id>/add_production_ligne", methods=["POST"])
def add_production_ligne(client_id):
    """Ajoute une ligne de production à un client."""
    form = AddProductionLigneForm()
    if form.validate_on_submit():
        new_ligne = ProductionLigne(
            prod_ligne_name=form.prod_ligne_name.data,
            ID_customer=client_id
        )
        db.session.add(new_ligne)
        db.session.commit()
        flash("✅ Ligne de production ajoutée avec succès !", "success")
        return redirect(url_for("client.clients"))
    return render_template("client/client.html", clients=CustomersList.query.all(), form=form)

@client_bp.route("/delete_machine/<int:machine_id>", methods=["POST"])
def delete_machine(machine_id):
    machine = Machines.query.get(machine_id)
    if machine:
        db.session.delete(machine)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})

@client_bp.route("/delete_production_ligne/<int:ligne_id>", methods=["POST"])
def delete_production_ligne(ligne_id):
    ligne = ProductionLigne.query.get(ligne_id)
    if ligne:
        db.session.delete(ligne)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})
