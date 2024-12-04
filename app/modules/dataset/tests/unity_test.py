import pytest
from app import create_app, db
from app.modules.dataset.models import DataSet, Rate
from flask_login import login_user
from app.modules.auth.models import User  # Asumo que tienes un modelo de User

@pytest.fixture(scope="module")
def dataset_service():
    """Fixture to get the DataSetService instance."""
    from app.modules.dataset.services import DataSetService
    return DataSetService()

@pytest.fixture(scope="module")
def test_client():
    """Fixture to get the test client."""
    app = create_app() 
    with app.app_context():
        yield app.test_client()
