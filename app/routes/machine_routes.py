from flask import Blueprint, render_template, jsonify, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
import os
from app.models import Machines, SettingValue, History, Manual
from app import db
from app.forms import AddClientForm, AddMachineForm, AddProductionLigneForm
from PIL import Image


machine_bp = Blueprint('machine', __name__)

@machine_bp.route('/<int:machine_id>')
def machine_details(machine_id):
    machine = Machines.query.get_or_404(machine_id)

    # Sécurité : vérifier que la machine a bien un modèle
    model = machine.modele_machine
    if not model:
        flash("⚠ Cette machine n'a pas de modèle associé.", "warning")
        return redirect(url_for('client_page'))  # ou la page que tu veux

    # Groupement des réglages par station
    settings_by_station = {
        station.station_name: station.settings for station in model.stations
    }

    # Récupération des valeurs
    value_map = {}
    for station in model.stations:
        for setting in station.settings:
            for val in setting.default_values:
                key = (setting.ID_settings, val.row_index, val.col_index)
                value_map[key] = val.default_value

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

