import pytest

from app import db
from app.modules.conftest import login, logout
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile
from app.modules.dataset.models import DataSet, DSMetaData


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    for module testing (por example, new users)
    """
    with test_client.application.app_context():
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

    yield test_client


def test_edit_profile_page_get(test_client):
    """
    Tests access to the profile editing page via a GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/profile/edit")
    assert response.status_code == 200, "The profile editing page could not be accessed."
    assert b"Edit profile" in response.data, "The expected content is not present on the page"

    logout(test_client)

def test_me_profile_page_get(test_client):
    """
    Tests access to the profile page via a GET request.
    """
    # Crear el usuario y hacer login
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    # Crear un dataset temporal asociado al usuario de prueba
    with test_client.application.app_context():
        user = User.query.filter_by(email="user@example.com").first()  # Obtener el usuario actual basado en el email
        ds_meta_data = DSMetaData(
            title="Test Dataset",
            description="A test dataset",
            publication_type="OTHER"
        )
        db.session.add(ds_meta_data)
        db.session.commit()

        new_dataset = DataSet(user_id=user.id, ds_meta_data_id=ds_meta_data.id)  # Modelo de ejemplo
        db.session.add(new_dataset)  # Usar SQLAlchemy o similar para añadirlo a la base de datos
        db.session.commit()

    # Acceder a la página de perfil
    response = test_client.get("/profile/me")
    assert response.status_code == 200, "The profile page could not be accessed."
    assert b"Name" in response.data, "The expected profile name is not present on the page"
    assert b"Surname" in response.data, "The expected profile surname is not present on the page"
    assert b"Test Dataset" in response.data, "The expected dataset title is not present on the page"

    # Limpieza: Eliminar dataset temporal después de la prueba
    with test_client.application.app_context():
        db.session.delete(new_dataset)
        db.session.delete(ds_meta_data)
        db.session.commit()

    logout(test_client)
