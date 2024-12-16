from io import BytesIO
from flask import make_response, render_template, current_app
from flask_login import current_user, login_required
from app.modules.dataset.services import DataSetService
from app.modules.featuremodel.services import FeatureModelService
from app.modules.dashboard import dashboard_bp
from bs4 import BeautifulSoup
from flask import render_template, make_response
from flask_weasyprint import HTML
from flask_login import login_required, current_user
import os
from core.blueprints.base_blueprint import BaseBlueprint

dashboard_bp = BaseBlueprint('dashboard', __name__, template_folder='templates')

@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
def index():
    dataset_service = DataSetService()
    feature_model_service = FeatureModelService()

    if current_user.is_authenticated:
        total_unsynchronized_datasets = dataset_service.count_unsynchronized_datasets(current_user.id)
        user_datasets_count = len(dataset_service.get_synchronized(current_user.id))
    else:
        total_unsynchronized_datasets = 0
        user_datasets_count = 0

    total_synchronized_datasets = dataset_service.count_synchronized_datasets()
    total_feature_models = feature_model_service.count_feature_models()
    total_dataset_downloads = dataset_service.total_dataset_downloads()
    total_authors = dataset_service.count_authors()
    total_feature_model_downloads = feature_model_service.total_feature_model_downloads()
    total_dataset_views = dataset_service.total_dataset_views()
    total_feature_model_views = feature_model_service.total_feature_model_views()
    team_template_path = os.path.join(current_app.root_path, 'modules/team/templates/team/index.html')
    latest_unsynchronized_datasets = dataset_service.latest_unsynchronized()


    try:
        with open(team_template_path, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            total_teams = len(soup.select('div.card.h-100'))
    except Exception:
        total_teams = 0

    return render_template(
        'dashboard.html',
        total_synchronized_datasets=total_synchronized_datasets,
        total_unsynchronized_datasets=total_unsynchronized_datasets,
        user_datasets_count=user_datasets_count,
        total_feature_models=total_feature_models,
        total_dataset_downloads=total_dataset_downloads,
        total_authors = total_authors,
        total_feature_model_downloads=total_feature_model_downloads,
        total_dataset_views=total_dataset_views,
        total_feature_model_views=total_feature_model_views,
        total_teams=total_teams,
        latest_unsynchronized_datasets = latest_unsynchronized_datasets,  
    )




@dashboard_bp.route('/dashboard/export_user_summary', methods=['GET'])
@login_required
def export_user_summary():
    dataset_service = DataSetService()
    feature_model_service = FeatureModelService()
    team_template_path = os.path.join(current_app.root_path, 'modules/team/templates/team/index.html')

    # Datos específicos del usuario
    if current_user.is_authenticated:
        total_unsynchronized_datasets = dataset_service.count_unsynchronized_datasets(current_user.id)
        user_datasets_count = len(dataset_service.get_synchronized(current_user.id))
    else:
        total_unsynchronized_datasets = 0
        user_datasets_count = 0

    try:
        with open(team_template_path, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            total_teams = len(soup.select('div.card.h-100'))
    except Exception:
        total_teams = 0

    # Datos generales
    total_synchronized_datasets = dataset_service.count_synchronized_datasets()
    total_feature_models = feature_model_service.count_feature_models()
    total_dataset_downloads = dataset_service.total_dataset_downloads()
    total_authors = dataset_service.count_authors()
    total_feature_model_downloads = feature_model_service.total_feature_model_downloads()
    total_dataset_views = dataset_service.total_dataset_views()
    total_feature_model_views = feature_model_service.total_feature_model_views()
    latest_unsynchronized_datasets = [
    f"Dataset de modelos seleccionados {dataset.id}" 
    for dataset in dataset_service.latest_unsynchronized() 
    if dataset.ds_meta_data and dataset.ds_meta_data.dataset_doi is None
]



    # Perfil del usuario
    user_profile = current_user.profile
    if user_profile:
        full_name = f"{user_profile.name} {user_profile.surname}"
        orcid = user_profile.orcid or "No ORCID Provided"
        affiliation = user_profile.affiliation or "No Affiliation Provided"
    else:
        full_name = "No Profile Information"
        orcid = "No ORCID Provided"
        affiliation = "No Affiliation Provided"

    # Datos que quieres incluir en el resumen
    user_data = {
        'name': full_name,
        'email': current_user.email,
        'orcid': orcid,
        'affiliation': affiliation,
        'my_unsynchronized_datasets': total_unsynchronized_datasets,
        'user_datasets_count': user_datasets_count,
        'total_synchronized_datasets': total_synchronized_datasets,
        'total_feature_models': total_feature_models,
        'total_dataset_downloads': total_dataset_downloads,
        'total_authors': total_authors,
        'total_teams': total_teams,
        'total_feature_model_downloads': total_feature_model_downloads,
        'total_dataset_views': total_dataset_views,
        'total_feature_model_views': total_feature_model_views,
        'latest_unsynchronized_datasets': latest_unsynchronized_datasets,
    }

    # Renderizar el contenido del PDF
    html = render_template('user_summary.html', user_data=user_data)

    # Generar el PDF usando WeasyPrint
    pdf = HTML(string=html).write_pdf()

    # Retornar el PDF como respuesta descargable
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=user_summary.pdf'
    return response
