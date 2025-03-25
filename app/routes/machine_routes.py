from flask import Blueprint, render_template, jsonify, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
import os
from app.models import Machines
from app import db
from app.forms import AddClientForm, AddMachineForm, AddProductionLigneForm
from PIL import Image


machine_bp = Blueprint('machine', __name__)

@machine_bp.route('/<int:machine_id>')
def machine_details(machine_id):
    machine = Machines.query.get_or_404(machine_id)
    return render_template('machine.html', machine=machine)