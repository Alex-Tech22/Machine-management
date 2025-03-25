from flask import Flask, Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename 
from app.models import db, ModeleMachine, Station, Settings
from app.forms import ModeleMachineForm, StationForm, SettingsForm
import os
from PIL import Image
from flask import abort

admin_bp = Blueprint('admin', __name__)

#=====================================SUPPRESSION=====================================#

@admin_bp.route('/modele', methods=['GET', 'POST'])
@login_required
def create_model():
    if current_user.access_level < 3:
        return redirect(url_for('index'))

    model_form = ModeleMachineForm()
    station_form = StationForm()
    model = None
    setting_forms = {}

    # Création d’un nouveau modèle
    if model_form.validate_on_submit():
        new_model = ModeleMachine(model_name=model_form.model_name.data)
        db.session.add(new_model)
        db.session.commit()
        return redirect(url_for('admin.create_model', model_id=new_model.ID_model))

    # Récupération du modèle sélectionné
    model_id = request.args.get('model_id', type=int)
    if model_id:
        model = ModeleMachine.query.get(model_id)
        if model:
            setting_forms = {
                station.ID_station: SettingsForm(prefix=f"setting_{station.ID_station}")
                for station in model.stations
            }

    all_models = ModeleMachine.query.all()

    return render_template("admin/add_modele_machine.html",
                           model_form=model_form,
                           station_form=station_form,
                           setting_forms=setting_forms,
                           model=model,
                           all_models=all_models)


@admin_bp.route('/add_station/<int:model_id>', methods=['GET', 'POST'])
@login_required
def add_station(model_id):
    if current_user.access_level < 3:
        return redirect(url_for('index'))

    form = StationForm()
    if form.validate_on_submit():
        station = Station(station_name=form.station_name.data, ID_model=model_id)
        db.session.add(station)
        db.session.commit()
    return redirect(url_for('admin.create_model', model_id=model_id))

@admin_bp.route('/add_settings/<int:station_id>', methods=['POST'])
@login_required
def add_setting(station_id):
    print("📥 Reçu POST pour ajout de réglage pour station", station_id) #DEBUG
    if current_user.access_level < 3:
        return redirect(url_for('index'))

    prefix = f"setting_{station_id}"
    form = SettingsForm(prefix=prefix)

    print("➡ Formulaire soumis")#DEBUG
    print("Contenu brut :", request.form)#DEBUG
    print("Contenu fichiers :", request.files)#DEBUG

    if form.validate_on_submit():
        print("✅ Formulaire validé, enregistrement en cours...")#DEBUG
        image_filename = None

        
        if form.image.data:
            print("📎 Image transmise :", form.image.data)#DEBUG
            image_file = form.image.data[0] if isinstance(form.image.data, list) else form.image.data
            try:
                img = Image.open(image_file)
                img.verify()
                image_file.seek(0)
            except Exception as e:
                flash("❌ Le fichier n’est pas une image valide.", "danger")
                return redirect(url_for('admin.create_model', model_id=Station.query.get_or_404(station_id).ID_model))

            image_filename = secure_filename(image_file.filename)
            save_path = os.path.join(current_app.root_path, "static", "images", "settings")
            os.makedirs(save_path, exist_ok=True)
            image_file.save(os.path.join(save_path, image_filename))

        setting = Settings(
            setting_name=form.setting_name.data,
            setting_type=form.setting_type.data,
            picture_link=image_filename,
            ID_station=station_id
        )
        db.session.add(setting)
        db.session.commit()
        flash("✅ Réglage ajouté avec succès !", "success")
    else:
        print("❌ Formulaire invalide :", form.errors)#DEBUG

    station = Station.query.get_or_404(station_id)
    return redirect(url_for('admin.create_model', model_id=station.ID_model))



#=====================================SUPPRESSION=====================================#

@admin_bp.route('/delete/<string:obj_type>/<int:obj_id>', methods=['POST'])
@login_required
def delete_dynamic(obj_type, obj_id):
    if current_user.access_level < 3:
        flash("🚫 Action non autorisée", "danger")
        return redirect(url_for('index'))

    model_id = None
    try:
        if obj_type == "station":
            obj = Station.query.get_or_404(obj_id)
            model_id = obj.ID_model
        elif obj_type == "setting":
            obj = Settings.query.get_or_404(obj_id)
            model_id = Station.query.get_or_404(obj.ID_station).ID_model
        elif obj_type == "model":
            obj = ModeleMachine.query.get_or_404(obj_id)
        else:
            abort(404)

        db.session.delete(obj)
        db.session.commit()
        flash(f"✅ {obj_type.capitalize()} supprimé avec succès", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"❌ Erreur lors de la suppression : {str(e)}", "danger")

    if model_id:
        return redirect(url_for('admin.create_model', model_id=model_id))
    else:
        return redirect(url_for('admin.create_model'))
