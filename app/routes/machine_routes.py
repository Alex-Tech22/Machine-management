from flask import Blueprint, render_template, jsonify, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
import os
from app.models import Machines, SettingValue, History, Manual
from app import db
from app.forms import AddClientForm, AddMachineForm, AddProductionLigneForm
from PIL import Image


machine_bp = Blueprint('machine', __name__)

# Route pour afficher la liste des machines
@machine_bp.route('/<int:machine_id>')
def machine_details(machine_id):
    machine = Machines.query.get_or_404(machine_id)

    # Sécurité : vérifier que la machine a bien un modèle
    model = machine.modele_machine
    if not model:
        return redirect(url_for('client_page'))  # ou la page que tu veux

    # Groupement des réglages par station
    settings_by_station = {
        station.station_name: station.settings for station in model.stations
    }

    # Récupération des valeurs
    value_map = {}
    for station in machine.modele_machine.stations:
        for setting in station.settings:
            for val in setting.values:
                if val.ID_machines == machine.ID_machines:
                    key = (setting.ID_settings, val.row_index, val.col_index)
                    value_map[key] = val.value


    column_labels = ["A", "B", "C", "Pression du ressort (Kg)"]
    row_labels = ["ST4", "ST5", "ST6", "ST7", "ST8", "ST9"]

    return render_template(
        "machine/machine.html",
        machine=machine,
        settings_by_station=settings_by_station,
        column_labels=column_labels,
        row_labels=row_labels,
        value_map=value_map
    )

# Route pour ajouter une machine
@machine_bp.route('/<int:machine_id>/add_history', methods=['POST'])
@login_required
def add_history(machine_id):
    remarks = request.form.get("remarks")
    revisions_date = request.form.get("revisions_date")

    if not revisions_date:
        return redirect(url_for("machine.machine_details", machine_id=machine_id))

    from datetime import datetime
    user_name = f"{current_user.first_name} {current_user.last_name}"

    new_entry = History(
        ID_machines=machine_id,
        revisions_date=datetime.strptime(revisions_date, "%Y-%m-%d"),
        tech_name=user_name,
        remarks=remarks
    )
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for("machine.machine_details", machine_id=machine_id))

# Route pour supprimer les ligne sélectioner de l'historique
@machine_bp.route('/<int:machine_id>/delete_history', methods=['POST'])
@login_required
def delete_history(machine_id):
    selected_ids = request.form.getlist("selected_ids")

    for history_id in selected_ids:
        entry = History.query.get(history_id)
        if entry and entry.ID_machines == machine_id:
            db.session.delete(entry)

    db.session.commit()
    return redirect(url_for("machine.machine_details", machine_id=machine_id))

# Route pour mettre a jour les réglages de la machine
@machine_bp.route("/<int:machine_id>/update_setting_value", methods=["POST"])
@login_required
def update_setting_value(machine_id):
    values = request.form.getlist('values')
    for key, val in request.form.items():
        if key.startswith("values["):
            id_setting_value = float(key.split("[")[1].rstrip("]"))
            setting_value = SettingValue.query.get(id_setting_value)
            if setting_value and setting_value.ID_machines == machine_id:
                setting_value.value = float(val)
    db.session.commit()
    flash("Réglages mis à jour avec succès", "success")
    return redirect(url_for("machine.machine_details", machine_id=machine_id))
