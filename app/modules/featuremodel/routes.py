from flask import render_template, request, redirect, url_for
from app.modules.featuremodel import featuremodel_bp
from app.modules.featuremodel.services import FeatureModelService

feature_model_service = FeatureModelService()

@featuremodel_bp.route('/featuremodel', methods=['GET'])
def index():
    return render_template('featuremodel/index.html')

@featuremodel_bp.route('/featuremodel/select', methods=['GET'])
def select_feature_models():
    # Utiliza el servicio para obtener todos los modelos
    models = feature_model_service.get_all_feature_models()
    return render_template('featuremodel/select_models.html', models=models)

@featuremodel_bp.route('/featuremodel/add_to_cart', methods=['POST'])
def add_feature_models_to_cart():
    # Obtén los modelos seleccionados desde el formulario
    selected_models = request.form.getlist('models')
    add_to_cart(selected_models)
    return redirect(url_for('dataset.view_cart'))
