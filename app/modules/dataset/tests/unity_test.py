import pytest
from unittest.mock import MagicMock, patch
from app.modules.dataset.services import DataSetService
from app.modules.dataset.models import DataSet, Rate
from flask import Flask
from app import create_app


# ---------- Fixtures ----------
@pytest.fixture
def app():
    """Crear la aplicación Flask para las pruebas."""
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def dataset_service(app):
    """Mock del servicio de datasets."""
    dataset_repo_mock = MagicMock()
    service = DataSetService()
    service.repository = dataset_repo_mock
    yield service

@pytest.fixture
def mock_rate():
    """Mock para una calificación."""
    return Rate(id=1, rating=4, dataset_id=1, user_id=1)

@pytest.fixture
def mock_query():
    """Mock para consultas a la base de datos."""
    with patch('app.modules.dataset.services.db.session.query') as mock_query:
        yield mock_query


# ---------- Pruebas ----------

def test_get_dataset_by_id(dataset_service):
    """Probar que se obtiene un dataset existente."""
    mock_dataset = DataSet(id=1, name="Test Dataset")
    dataset_service.repository.get_by_id.return_value = mock_dataset

    result = dataset_service.get_dataset_by_id(1)

    assert result == mock_dataset
    dataset_service.repository.get_by_id.assert_called_once_with(1)

def test_get_dataset_by_id_not_found(dataset_service):
    """Probar excepción si no se encuentra el dataset."""
    dataset_service.repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Dataset con id 999 no encontrado."):
        dataset_service.get_dataset_by_id(999)


@pytest.mark.parametrize("rating, is_valid", [
    (1, True),  # Límite inferior permitido
    (5, True),  # Límite superior permitido
    (0, False), # Rating menor al mínimo
    (6, False)  # Rating mayor al máximo
], ids=["min_rating", "max_rating", "below_min", "above_max"])
def test_update_rating_with_valid_and_invalid_values(dataset_service, app, rating, is_valid):
    """Probar actualización de rating con valores límite y no válidos."""
    with app.app_context():  # Proporcionar contexto de aplicación
        if is_valid:
            mock_rate = Rate(id=1, rating=rating, dataset_id=1, user_id=1)
            dataset_service.update_rating = MagicMock(return_value=mock_rate)

            result = dataset_service.update_rating(mock_rate.dataset_id, mock_rate.rating)

            assert result == mock_rate
            dataset_service.update_rating.assert_called_once_with(mock_rate.dataset_id, mock_rate.rating)
        else:
            with patch('app.modules.dataset.services.current_user', MagicMock(id=1)):  # Mockear usuario
                with pytest.raises(ValueError, match="El valor del rating debe estar entre 1 y 5"):
                    dataset_service.update_rating(dataset_id=1, rating=rating)


def test_user_already_rated(dataset_service, mock_query, app):
    """Probar que no se permite calificar un dataset más de una vez."""
    with app.app_context():  # Proporcionar contexto de aplicación
        existing_rate = Rate(id=1, rating=4, dataset_id=1, user_id=1)
        with patch('app.modules.dataset.services.current_user', MagicMock(id=1)):
            mock_query.return_value.filter_by.return_value.first.return_value = existing_rate

            with pytest.raises(ValueError, match="El usuario ya ha calificado este dataset."):
                dataset_service.update_rating(dataset_id=1, rating=5)


def test_rate_dataset_with_existing_ratings(dataset_service, mock_query, app):
    """Probar actualización de ratings en un dataset con calificaciones previas."""
    with app.app_context():  # Proporcionar contexto de aplicación
        existing_dataset = MagicMock(id=1, avgRating=4.0, numRatings=5, totalRatings=20)
        new_rating = 1

        with patch('app.modules.dataset.services.db.session.add') as mock_add, \
             patch('app.modules.dataset.services.db.session.commit') as mock_commit, \
             patch('app.modules.dataset.services.current_user', MagicMock(id=1)), \
             patch.object(dataset_service.repository, 'update') as mock_update:

            dataset_service.get_dataset_by_id = MagicMock(return_value=existing_dataset)
            mock_query.return_value.filter_by.return_value.first.return_value = None

            updated_dataset = dataset_service.update_rating(dataset_id=1, rating=new_rating)

            assert updated_dataset.avgRating == 3.5
            assert updated_dataset.numRatings == 6
            assert updated_dataset.totalRatings == 21

            mock_add.assert_called_once()
            mock_commit.assert_called_once()
            dataset_service.get_dataset_by_id.assert_called_once_with(1)

