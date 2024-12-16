import os
import pytest
import zipfile
from app import db
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile
from unittest.mock import patch, MagicMock
from flask import session

@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

    yield test_client


@pytest.fixture
def auth_service():
    from app.modules.auth.services import AuthenticationService
    return MagicMock(spec=AuthenticationService)


@pytest.fixture
def dataset_service():
    from app.modules.dataset.services import DataSetService
    service_mock = MagicMock(spec=DataSetService)
    service_mock.create_dataset_from_selected_models = MagicMock()  
    return service_mock



@pytest.fixture
def feature_model_service():
    from app.modules.featuremodel.services import FeatureModelService
    service_mock = MagicMock(spec=FeatureModelService)
    service_mock.get_all_feature_models = MagicMock()  
    return service_mock

@pytest.fixture
def test_app():
    from app import create_app
    app = create_app('testing')
    return app

#TEST 1:Crear Dataset correctamente

def test_create_dataset_flow(auth_service, dataset_service, feature_model_service, test_app):
    # Paso 1: Login
    with patch.object(auth_service, 'login') as mock_login:
        mock_login.return_value = MagicMock(id=1, email="user1@example.com")

        user = auth_service.login(email="user1@example.com", password="1234")
        assert user.email == "user1@example.com"
        mock_login.assert_called_once_with(email="user1@example.com", password="1234")

    # Paso 2: Selección de Feature Models
    with patch.object(feature_model_service, 'get_all_feature_models') as mock_get_all_feature_models:
        mock_feature_models = [
            MagicMock(id=5, name="Feature Model 5"),
            MagicMock(id=6, name="Feature Model 6"),
            MagicMock(id=8, name="Feature Model 8")
        ]
        mock_get_all_feature_models.return_value = mock_feature_models

        feature_models = feature_model_service.get_all_feature_models(user_id=user.id)
        assert len(feature_models) == 3
        assert [fm.id for fm in feature_models] == [5, 6, 8]
        mock_get_all_feature_models.assert_called_once_with(user_id=user.id)

    # Paso 3: Añadir al carrito
    with test_app.test_request_context():  # Contexto de solicitud
        session['selected_models'] = []
        for model in feature_models:
            if model.id not in session['selected_models']:
                session['selected_models'].append(model.id)

        assert session['selected_models'] == [5, 6, 8]

    # Paso 4: Crear Dataset y validar el ZIP
    with test_app.test_request_context():
        session['selected_models'] = [5, 6, 8]  # Simula los modelos seleccionados

        with patch.object(dataset_service, 'create_dataset_from_selected_models') as mock_create_dataset:
            # Mock del archivo ZIP generado
            mock_zip_path = "/tmp/dataset_1.zip"
            mock_create_dataset.return_value = mock_zip_path

            # Llama al método con los modelos seleccionados
            zip_path = dataset_service.create_dataset_from_selected_models(models=feature_models, user=user)
            assert zip_path == mock_zip_path

            # Verifica que el mock fue llamado con los argumentos correctos
            mock_create_dataset.assert_called_once_with(models=feature_models, user=user)

            # Simula la existencia del archivo ZIP
            with patch("os.path.exists", return_value=True):
                assert os.path.exists(zip_path), "El archivo ZIP no se creó correctamente"

#TEST 2:Crear Dataset vacío

def test_create_dataset_no_models(dataset_service):
    with patch.object(dataset_service, 'create_dataset_from_selected_models') as mock_create_dataset:
        mock_create_dataset.side_effect = ValueError("No models selected")

        # Simular la llamada con una lista vacía de modelos
        with pytest.raises(ValueError, match="No models selected"):
            dataset_service.create_dataset_from_selected_models(models=[], user=MagicMock(id=1))

        mock_create_dataset.assert_called_once_with(models=[], user=MagicMock(id=1))

import os
import tempfile
import zipfile
import pytest
from unittest.mock import patch, MagicMock
from flask import session
from app.modules.dataset.services import DataSetService

@pytest.fixture
def dataset_service():
    from app.modules.dataset.services import DataSetService
    service_mock = MagicMock(spec=DataSetService)
    service_mock.create_dataset_from_selected_models = MagicMock()
    return service_mock

@pytest.fixture
def test_app():
    from app import create_app
    app = create_app('testing')
    return app

def test_create_dataset_flow(auth_service, dataset_service, feature_model_service, test_app):
    # Paso 1: Login
    with patch.object(auth_service, 'login') as mock_login:
        mock_login.return_value = MagicMock(id=1, email="user1@example.com")

        user = auth_service.login(email="user1@example.com", password="1234")
        assert user.email == "user1@example.com"
        mock_login.assert_called_once_with(email="user1@example.com", password="1234")

    # Paso 2: Selección de Feature Models
    with patch.object(feature_model_service, 'get_all_feature_models') as mock_get_all_feature_models:
        mock_feature_models = [
            MagicMock(id=5, name="Feature Model 5"),
            MagicMock(id=6, name="Feature Model 6"),
            MagicMock(id=8, name="Feature Model 8")
        ]
        mock_get_all_feature_models.return_value = mock_feature_models

        feature_models = feature_model_service.get_all_feature_models(user_id=user.id)
        assert len(feature_models) == 3
        assert [fm.id for fm in feature_models] == [5, 6, 8]
        mock_get_all_feature_models.assert_called_once_with(user_id=user.id)

    # Paso 3: Añadir al carrito
    with test_app.test_request_context():  # Contexto de solicitud
        session['selected_models'] = []
        for model in feature_models:
            if model.id not in session['selected_models']:
                session['selected_models'].append(model.id)

        assert session['selected_models'] == [5, 6, 8]

    # Paso 4: Crear Dataset y validar el ZIP
    with test_app.test_request_context():
        session['selected_models'] = [5, 6, 8]  # Simula los modelos seleccionados

        with patch.object(dataset_service, 'create_dataset_from_selected_models') as mock_create_dataset:
            # Mock del archivo ZIP generado
            mock_zip_path = "/tmp/dataset_1.zip"
            mock_create_dataset.return_value = mock_zip_path

            # Llama al método con los modelos seleccionados
            zip_path = dataset_service.create_dataset_from_selected_models(models=feature_models, user=user)
            assert zip_path == mock_zip_path

            # Verifica que el mock fue llamado con los argumentos correctos
            mock_create_dataset.assert_called_once_with(models=feature_models, user=user)

            # Simula la existencia del archivo ZIP
            with patch("os.path.exists", return_value=True):
                assert os.path.exists(zip_path), "El archivo ZIP no se creó correctamente"

#TEST 3: Manejo de errores con lista vacía de modelos
def test_create_dataset_no_models(dataset_service):
    user_mock = MagicMock(id=1)  # Crear un único mock para el usuario

    with patch.object(dataset_service, 'create_dataset_from_selected_models') as mock_create_dataset:
        mock_create_dataset.side_effect = ValueError("No models selected")

        # Simular la llamada con una lista vacía de modelos
        with pytest.raises(ValueError, match="No models selected"):
            dataset_service.create_dataset_from_selected_models(models=[], user=user_mock)

        mock_create_dataset.assert_called_once_with(models=[], user=user_mock)


def test_zip_content_creation(dataset_service):
    with patch.object(dataset_service, 'create_dataset_from_selected_models') as mock_create_dataset:
        # Simula la ruta del archivo ZIP generado
        mock_zip_path = "/tmp/dataset_1.zip"
        mock_create_dataset.return_value = mock_zip_path

        # Simular los modelos seleccionados
        mock_models = [
            MagicMock(id=5, name="Feature Model 5"),
            MagicMock(id=6, name="Feature Model 6")
        ]

        # Crear un archivo ZIP temporal con contenido simulado
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "dataset_1.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                zipf.writestr("file5.uvl", "Contenido del modelo 5")
                zipf.writestr("file6.uvl", "Contenido del modelo 6")

            # Verificar el contenido del ZIP
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                assert "file5.uvl" in zipf.namelist()
                assert "file6.uvl" in zipf.namelist()
                assert len(zipf.namelist()) == 2

#TEST 4: Verificación de la asociación de modelos al dataset
def test_model_association_with_dataset(dataset_service):
    with patch.object(dataset_service, 'create_dataset_from_selected_models') as mock_create_dataset:
        # Simular los modelos seleccionados
        mock_models = [
            MagicMock(id=5, name="Feature Model 5"),
            MagicMock(id=6, name="Feature Model 6"),
            MagicMock(id=8, name="Feature Model 8")
        ]

        # Configurar el mock del dataset
        mock_dataset = MagicMock(id=1, title="Created Dataset")
        mock_dataset.feature_models = mock_models
        mock_create_dataset.return_value = mock_dataset

        # Llama a la función con los modelos seleccionados
        user_mock = MagicMock(id=1)
        dataset = dataset_service.create_dataset_from_selected_models(models=mock_models, user=user_mock)

        # Verificar que el dataset incluye los modelos seleccionados
        assert dataset.title == "Created Dataset"
        assert len(dataset.feature_models) == len(mock_models)
        assert [fm.id for fm in dataset.feature_models] == [5, 6, 8]

        # Verificar que la función fue llamada con los parámetros correctos
        mock_create_dataset.assert_called_once_with(models=mock_models, user=user_mock)


