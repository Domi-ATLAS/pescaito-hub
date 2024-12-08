import logging
import os
import json
import shutil
import tempfile
import uuid
from datetime import datetime, timezone
from zipfile import ZipFile
from app import db  

from flask import (
    flash,
    send_file,
    session,
    redirect,
    render_template,
    request,
    jsonify,
    send_from_directory,
    make_response,
    abort,
    url_for,
)
from flask_login import login_required, current_user

from app.modules.dataset.forms import DataSetForm
from app.modules.dataset.models import DSDownloadRecord, DSMetaData, DataSet, PublicationType
from app.modules.dataset import dataset_bp
from app.modules.dataset.services import (
    AuthorService,
    DSDownloadRecordService,
    DSMetaDataService,
    DSViewRecordService,
    DataSetService,
    DOIMappingService,
    add_to_cart,
    get_cart,
    create_dataset_from_selected_models,
)
from app.modules.hubfile.services import HubfileService
from app.modules.zenodo.services import ZenodoService
from app.modules.featuremodel.models import FeatureModel

logger = logging.getLogger(__name__)

# Instanciamos los servicios
dataset_service = DataSetService()
author_service = AuthorService()
dsmetadata_service = DSMetaDataService()
zenodo_service = ZenodoService()
doi_mapping_service = DOIMappingService()
ds_view_record_service = DSViewRecordService()


@dataset_bp.route('/dataset/<int:dataset_id>/update_rating/<int:rating>', methods=['POST', 'PUT','GET'])
@login_required
def update_rating(dataset_id, rating):    
    try:
        if rating < 1 or rating > 5:
            raise ValueError("El valor del rating debe estar entre 1 y 5.")

        updated_dataset = dataset_service.update_rating(dataset_id, rating)
        return jsonify({"message": "Rating updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@dataset_bp.route("/dataset/upload", methods=["GET", "POST"])
@login_required
def create_dataset():
    form = DataSetForm()
    if request.method == "POST":
        dataset = None

        if not form.validate_on_submit():
            return jsonify({"message": form.errors}), 400

        try:
            logger.info("Creating dataset...")
            dataset = dataset_service.create_from_form(form=form, current_user=current_user)
            logger.info(f"Created dataset: {dataset}")
            dataset_service.move_feature_models(dataset)
        except Exception as exc:
            logger.exception(f"Exception while creating dataset data locally {exc}")
            return jsonify({"Exception while creating dataset data locally: ": str(exc)}), 400

        # Send dataset as deposition to Zenodo
        data = {}
        try:
            zenodo_response_json = zenodo_service.create_new_deposition(dataset)
            response_data = json.dumps(zenodo_response_json)
            data = json.loads(response_data)
        except Exception as exc:
            data = {}
            zenodo_response_json = {}
            logger.exception(f"Exception while creating dataset data in Zenodo {exc}")

        if data.get("conceptrecid"):
            deposition_id = data.get("id")

            # Update dataset with deposition id in Zenodo
            dataset_service.update_dsmetadata(dataset.ds_meta_data_id, deposition_id=deposition_id)

            try:
                # Iterate for each feature model (one feature model = one request to Zenodo)
                for feature_model in dataset.feature_models:
                    zenodo_service.upload_file(dataset, deposition_id, feature_model)

                # Publish deposition
                zenodo_service.publish_deposition(deposition_id)

                # Update DOI
                deposition_doi = zenodo_service.get_doi(deposition_id)
                dataset_service.update_dsmetadata(dataset.ds_meta_data_id, dataset_doi=deposition_doi)
            except Exception as e:
                msg = f"It has not been possible to upload feature models to Zenodo and update the DOI: {e}"
                return jsonify({"message": msg}), 200

        # Delete temp folder
        file_path = current_user.temp_folder()
        if os.path.exists(file_path) and os.path.isdir(file_path):
            shutil.rmtree(file_path)

        msg = "Everything works!"
        return jsonify({"message": msg}), 200

    return render_template("dataset/upload_dataset.html", form=form)


@dataset_bp.route("/dataset/list", methods=["GET", "POST"])
@login_required
def list_dataset():
    return render_template(
        "dataset/list_datasets.html",
        datasets=dataset_service.get_synchronized(current_user.id),
        local_datasets=dataset_service.get_unsynchronized(current_user.id),
    )


# **Rutas del Carrito**
@dataset_bp.route("/cart/select_models", methods=["GET", "POST"])
@login_required
def select_models():
    # Limpiar el carrito antes de mostrar la selección de modelos
    session['selected_models'] = []
    session.modified = True
    models = FeatureModel.query.all()  # Obtenemos todos los modelos disponibles
    if request.method == "POST":
        model_ids = request.form.getlist("models")  # Recuperamos los modelos seleccionados
        
        if not model_ids:  # Validar que haya al menos un modelo seleccionado
            flash("Por favor, selecciona al menos un modelo para continuar.", "error")
            return render_template('dataset/select_models.html', models=models)  # Renderizar con el mensaje

        add_to_cart(model_ids)  # Agregar al carrito
        return redirect(url_for('dataset.view_cart'))  # Redirigir al carrito

    return render_template('dataset/select_models.html', models=models)


@dataset_bp.route("/cart/view", methods=["GET"])
@login_required
def view_cart():
    selected_model_ids = get_cart()
    selected_models = FeatureModel.query.filter(FeatureModel.id.in_(selected_model_ids)).all()
    return render_template('dataset/view_cart.html', models=selected_models)


@dataset_bp.route("/cart/create_dataset", methods=["POST"])
@login_required
def create_dataset_from_cart():
    selected_model_ids = get_cart()
    selected_models = FeatureModel.query.filter(FeatureModel.id.in_(selected_model_ids)).all()

    if not selected_models:
        return jsonify({"message": "No hay modelos seleccionados para crear el dataset"}), 400

    zip_path = create_dataset_from_selected_models(selected_models, current_user) # Creo el dataset
    
    return send_file(
        zip_path,
        as_attachment=True,
        download_name='selected_models.zip',
        mimetype='application/zip'
    )


@dataset_bp.route("/cart/move_and_create_dataset", methods=["POST"])
@login_required
def move_and_create_dataset():
    selected_model_ids = get_cart()
    selected_models = FeatureModel.query.filter(FeatureModel.id.in_(selected_model_ids)).all()

    if not selected_models:
        return jsonify({"message": "No hay modelos seleccionados para crear el dataset"}), 400

    # Crear el dataset en la base de datos
    new_dataset = DataSet(
        user_id=current_user.id,
        feature_models=selected_models,
        ds_meta_data=DSMetaData(
            title=f"Dataset de modelos seleccionados {len(selected_models)}",
            description="Incluye modelos seleccionados por el usuario.",
            publication_type=PublicationType.DATA_MANAGEMENT_PLAN
        )
    )
    db.session.add(new_dataset)
    db.session.commit()

    print(f"Dataset creado: {new_dataset}")

    # Crear el directorio para guardar los archivos
    dataset_dir = os.path.join(
        os.getenv('WORKING_DIR', ''),
        'uploads',
        f'user_{current_user.id}',
        f'dataset_{new_dataset.id}'
    )
    os.makedirs(dataset_dir, exist_ok=True)

    # Mover los archivos seleccionados al directorio
    for feature_model in selected_models:
        for hubfile in feature_model.files:
            source_path = HubfileService().get_path_by_hubfile(hubfile)  # Ruta original del archivo
            dest_path = os.path.join(dataset_dir, hubfile.name)

            if os.path.exists(source_path):
                shutil.copy(source_path, dest_path)
                print(f"Archivo copiado: {dest_path}")
            else:
                print(f"Archivo no encontrado: {source_path}")

    return jsonify({"message": f"Dataset creado y archivos movidos al directorio {dataset_dir}."}), 200



# **Rutas de archivos**
@dataset_bp.route("/dataset/file/upload", methods=["POST"])
@login_required
def upload():
    file = request.files["file"]
    temp_folder = current_user.temp_folder()

    if not file or not file.filename.endswith(".uvl"):
        return jsonify({"message": "No valid file"}), 400

    # create temp folder
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    file_path = os.path.join(temp_folder, file.filename)

    if os.path.exists(file_path):
        # Generate unique filename (by recursion)
        base_name, extension = os.path.splitext(file.filename)
        i = 1
        while os.path.exists(
            os.path.join(temp_folder, f"{base_name} ({i}){extension}")
        ):
            i += 1
        new_filename = f"{base_name} ({i}){extension}"
        file_path = os.path.join(temp_folder, new_filename)
    else:
        new_filename = file.filename

    try:
        file.save(file_path)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    return (
        jsonify(
            {
                "message": "UVL uploaded and validated successfully",
                "filename": new_filename,
            }
        ),
        200,
    )


@dataset_bp.route("/dataset/file/delete", methods=["POST"])
@login_required
def delete():
    data = request.get_json()
    filename = data.get("file")
    temp_folder = current_user.temp_folder()
    filepath = os.path.join(temp_folder, filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({"message": "File deleted successfully"})

    return jsonify({"error": "Error: File not found"})


@dataset_bp.route("/dataset/download/<int:dataset_id>", methods=["GET"])
def download_dataset(dataset_id):
    dataset = dataset_service.get_or_404(dataset_id)

    file_path = f"uploads/user_{dataset.user_id}/dataset_{dataset.id}/"

    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, f"dataset_{dataset_id}.zip")

    with ZipFile(zip_path, "w") as zipf:
        for subdir, dirs, files in os.walk(file_path):
            for file in files:
                full_path = os.path.join(subdir, file)
                relative_path = os.path.relpath(full_path, file_path)
                zipf.write(
                    full_path,
                    arcname=os.path.join(
                        os.path.basename(zip_path[:-4]), relative_path
                    ),
                )

    user_cookie = request.cookies.get("download_cookie")
    if not user_cookie:
        user_cookie = str(uuid.uuid4())  # Generate a new unique identifier if it does not exist
        # Save the cookie to the user's browser
        resp = make_response(
            send_from_directory(
                temp_dir,
                f"dataset_{dataset_id}.zip",
                as_attachment=True,
                mimetype="application/zip",
            )
        )
        resp.set_cookie("download_cookie", user_cookie)
    else:
        resp = send_from_directory(
            temp_dir,
            f"dataset_{dataset_id}.zip",
            as_attachment=True,
            mimetype="application/zip",
        )

    # Check if the download record already exists for this cookie
    existing_record = DSDownloadRecord.query.filter_by(
        user_id=current_user.id if current_user.is_authenticated else None,
        dataset_id=dataset_id,
        download_cookie=user_cookie
    ).first()

    if not existing_record:
        # Record the download in your database
        DSDownloadRecordService().create(
            user_id=current_user.id if current_user.is_authenticated else None,
            dataset_id=dataset_id,
            download_date=datetime.now(timezone.utc),
            download_cookie=user_cookie,
        )

    return resp


# **Rutas Relacionadas con DOI**
@dataset_bp.route("/doi/<path:doi>/", methods=["GET"])
def subdomain_index(doi):
    new_doi = doi_mapping_service.get_new_doi(doi)
    if new_doi:
        return redirect(url_for('dataset.subdomain_index', doi=new_doi), code=302)

    ds_meta_data = dsmetadata_service.filter_by_doi(doi)

    if not ds_meta_data:
        abort(404)

    dataset = ds_meta_data.data_set
    user_cookie = ds_view_record_service.create_cookie(dataset=dataset)
    resp = make_response(render_template("dataset/view_dataset.html", dataset=dataset))
    resp.set_cookie("view_cookie", user_cookie)

    return resp


@dataset_bp.route("/dataset/unsynchronized/<int:dataset_id>/", methods=["GET"])
@login_required
def get_unsynchronized_dataset(dataset_id):
    dataset = dataset_service.get_unsynchronized_dataset(current_user.id, dataset_id)

    if not dataset:
        abort(404)

    if not dataset.ds_meta_data.tags:
        dataset.ds_meta_data.tags = "No tags"
    if not dataset.ds_meta_data.publication_doi:
        dataset.ds_meta_data.publication_doi = "N/A"

    return render_template("dataset/view_dataset.html", dataset=dataset)

@dataset_bp.route('/dataset/unsynchronized/download/<int:dataset_id>', methods=['GET'])
@login_required
def download_unsynchronized_dataset(dataset_id):
    # Obtener el dataset correspondiente
    dataset = DataSet.query.filter_by(id=dataset_id, user_id=current_user.id).first()
    if not dataset:
        return jsonify({"error": "Dataset no encontrado o acceso no autorizado."}), 404

    # Crear un archivo ZIP temporal
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, f"dataset_{dataset.id}.zip")

    try:
        with ZipFile(zip_path, 'w') as zipf:
            # Iterar sobre los FeatureModels y sus Hubfiles asociados
            for feature_model in dataset.feature_models:
                for hubfile in feature_model.files:
                    # Obtener la ruta del archivo desde el servicio HubfileService
                    source_path = HubfileService().get_path_by_hubfile(hubfile)

                    if os.path.exists(source_path):
                        # Agregar el archivo al ZIP
                        zipf.write(source_path, os.path.basename(source_path))
                        print(f"Archivo añadido al ZIP: {source_path}")
                    else:
                        print(f"Archivo no encontrado: {source_path}")

        # Enviar el archivo ZIP al cliente
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=f'dataset_{dataset.id}.zip',
            mimetype='application/zip'
        )
    except Exception as e:
        print(f"Error al generar el ZIP: {e}")
        return jsonify({"error": "Error al generar el ZIP del dataset."}), 500
    finally:
        # Limpiar el directorio temporal
        shutil.rmtree(temp_dir)

