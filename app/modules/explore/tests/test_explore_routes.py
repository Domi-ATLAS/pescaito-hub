import os
from flask import Flask
from flask.templating import DispatchingJinjaLoader
import pytest  # Asegúrate de que pytest esté importado
from unittest.mock import patch
from app.modules.explore.routes import index
from jinja2 import FileSystemLoader, Environment


@pytest.fixture
def client():
    """Crear una aplicación Flask para pruebas."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'  # Clave secreta para pruebas

    # Configurar múltiples rutas de búsqueda para las plantillas
    module_template_path = os.path.abspath('app/modules/explore/templates')
    global_template_path = os.path.abspath('app/templates')
    app.jinja_loader = FileSystemLoader([module_template_path, global_template_path])

    print("Search paths for templates:", app.jinja_loader.searchpath)

    with app.test_client() as client:
        app.add_url_rule('/explore', view_func=index, methods=['GET', 'POST'])
        yield client

def test_explore_get_valid_query(client):
    """Prueba positiva: GET /explore con query válida."""
    response = client.get('/explore?query=example')
    assert response.status_code == 200
    assert b'Explore' in response.data
    assert b'example' in response.data  # La query debe estar reflejada
   