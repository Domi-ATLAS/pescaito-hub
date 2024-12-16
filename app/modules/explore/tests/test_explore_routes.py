import pytest
from flask import Flask
from unittest.mock import patch
from app.modules.explore.routes import index

@pytest.fixture
def client():
    """Crear una aplicación Flask para pruebas."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'  # Clave secreta para pruebas
   
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
    print(app.jinja_loader.searchpath)
