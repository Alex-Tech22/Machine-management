from flask import Flask, Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename 
from app.models import db, ModeleMachine, Station, Settings, SettingValue, SettingDefaultValue, Manual, Machines
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

    manual_folder = os.path.join(current_app.static_folder, 'manuel')
    manuals = [f for f in os.listdir(manual_folder) if f.endswith('.pdf')]



    # Création d’un nouveau modèle
    if model_form.validate_on_submit():
        filename = None
        if model_form.manual_file.data:
            file = model_form.manual_file.data
            filename = secure_filename(file.filename)
            pdf_path = os.path.join(current_app.static_folder, "manuel", filename)
            file.save(pdf_path)

        new_model = ModeleMachine(
            model_name=model_form.model_name.data,
            manual_filename=filename
        )
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
        if request.method == 'POST' and model_form.manual_file.data:
            file = model_form.manual_file.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.static_folder, "manuel", filename))
            model.manual_filename = filename
            db.session.commit()


    all_models = ModeleMachine.query.all()
    column_labels = ["A", "B", "C", "Pression du ressort (Kg)"]
    row_labels = ["ST4", "ST5", "ST6", "ST7", "ST8", "ST9"]

    value_map = {}

    if model:
        for station in model.stations:
            for setting in station.settings:
                if setting.setting_type == "Tab":
                    for val in setting.default_values:
                        key = (setting.ID_settings, val.row_index, val.col_index)
                        value_map[key] = val.default_value


    return render_template(
        "admin/add_modele_machine.html",
        model_form=model_form,
        manuals=manuals,
        station_form=station_form,
        setting_forms=setting_forms,
        model=model,
        all_models=all_models,
        column_labels=column_labels,
        row_labels=row_labels,
        value_map=value_map
)


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
    else:
        print("❌ Formulaire invalide :", form.errors)#DEBUG

    station = Station.query.get_or_404(station_id)
    return redirect(url_for('admin.create_model', model_id=station.ID_model))

@admin_bp.route('/add_value/<int:setting_id>', methods=['POST'])
@login_required
def add_setting_value(setting_id):
    setting = Settings.query.get_or_404(setting_id)
    setting_type = request.form.get("setting_type")
    name = request.form.get("name")
    default_value = request.form.get("value", type=float)

    if setting_type == "Tab":
        row = request.form.get("row_index", type=int)
        col = request.form.get("col_index", type=int)
        setting_value = SettingDefaultValue(
            default_value=default_value,
            row_index=row,
            col_index=col,
            ID_settings=setting_id
        )
    else:
        name = request.form.get("name")
        setting_value = SettingDefaultValue(
            default_value=default_value,
            name=name,
            ID_settings=setting_id
        )

    db.session.add(setting_value)
    db.session.commit()

    return redirect(url_for('admin.create_model', model_id=setting.station.ID_model))



@admin_bp.route('/update_table/<int:setting_id>', methods=['POST'])
@login_required
def update_table_values(setting_id):
    setting = Settings.query.get_or_404(setting_id)
    
    # Nettoyer les anciennes valeurs si nécessaire
    SettingDefaultValue.query.filter_by(ID_settings=setting_id).delete()

    for key, value in request.form.items():
        if key.startswith("value_") and value:
            _, row, col = key.split("_")
            new_val = SettingDefaultValue(
                ID_settings=setting_id,
                row_index=int(row),
                col_index=int(col),
                default_value=float(value)
            )
            db.session.add(new_val)

    db.session.commit()
    return redirect(url_for('admin.create_model', model_id=setting.station.ID_model))

@admin_bp.route('/assign_manual/<int:model_id>', methods=['POST'])
@login_required
def assign_manual(model_id):
    selected_manual = request.form.get("manual_file")
    if selected_manual:
        manual = Manual.query.filter_by(manual_link=f"manuel/{selected_manual}").first()
        if not manual:
            manual = Manual(
                manual_version="Auto",
                manual_link=f"manuel/{selected_manual}",
                manual_title=selected_manual.rsplit(".", 1)[0]
            )
            db.session.add(manual)
            db.session.commit()

        model = ModeleMachine.query.get_or_404(model_id)
        machines = Machines.query.filter_by(ID_model=model.ID_model).all()
        for machine in machines:
            machine.ID_manual_link = manual.ID_manual_link
        db.session.commit()

    return redirect(url_for('admin.create_model', model_id=model_id))

@admin_bp.route('/update_numeric/<int:setting_id>', methods=['POST'])
@login_required
def update_numeric_values(setting_id):
    setting = Settings.query.get_or_404(setting_id)

    # Supprimer les anciennes valeurs
    SettingDefaultValue.query.filter_by(ID_settings=setting_id).delete()

    for i in range(len(request.form) // 2):
        name = request.form.get(f"name_{i}")
        value = request.form.get(f"value_{i}", type=float)
        if name is not None and value is not None:
            new_val = SettingDefaultValue(
                ID_settings=setting_id,
                name=name,
                default_value=value
            )
            db.session.add(new_val)

    db.session.commit()
    return redirect(url_for('admin.create_model', model_id=setting.station.ID_model))

#=====================================SUPPRESSION=====================================#

@admin_bp.route('/delete/<string:obj_type>/<int:obj_id>', methods=['POST'])
@login_required
def delete_dynamic(obj_type, obj_id):
    if current_user.access_level < 3:
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

    except Exception as e:
        db.session.rollback()

    if model_id:
        return redirect(url_for('admin.create_model', model_id=model_id))
    else:
        return redirect(url_for('admin.create_model'))
