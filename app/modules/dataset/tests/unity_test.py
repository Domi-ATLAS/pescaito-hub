import pytest
from unittest.mock import MagicMock
from app.modules.dataset.services import DataSetService
from app.modules.dataset.models import DataSet, DSMetaData, Rate
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def dataset_service():
    # Mock del repositorio de dataset
    dataset_repo_mock = MagicMock()
    service = DataSetService()
    service.repository = dataset_repo_mock
    yield service

def test_get_dataset_by_id(dataset_service):
    mock_dataset = DataSet(id=1, name="Test Dataset")
    dataset_service.repository.get_by_id.return_value = mock_dataset

    result = dataset_service.get_dataset_by_id(1)

    assert result == mock_dataset
    dataset_service.repository.get_by_id.assert_called_once_with(1)

def test_get_dataset_by_id_not_found(dataset_service):
    dataset_service.repository.get_by_id.return_value = None

    with pytest.raises(ValueError) as exc_info:
        dataset_service.get_dataset_by_id(999)

    assert "Dataset con id 999 no encontrado." in str(exc_info.value)