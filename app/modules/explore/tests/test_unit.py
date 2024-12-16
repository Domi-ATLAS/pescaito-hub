import pytest
from unittest.mock import MagicMock
from app.modules.explore.services import ExploreService

@pytest.fixture
def mock_repository():
    """Fixture para mockear el repositorio."""
    mock_repo = MagicMock()
    mock_repo.filter.return_value = [
        {"id": 1, "title": "Dataset 1", "tags": ["tag1", "tag2"]},
        {"id": 2, "title": "Dataset 2", "tags": ["tag2", "tag3"]}
    ]
    return mock_repo

@pytest.fixture
def explore_service(mock_repository):
    """Fixture para inicializar el servicio con el repositorio mockeado."""
    service = ExploreService()
    service.repository = mock_repository
    return service

def test_filter_combined_filters(explore_service, mock_repository):
    """Prueba: Filtros combinados (query, tags, tipo y orden)."""
    query = "example query"
    tags = ["tag1", "tag3"]
    sorting = "oldest"
    publication_type = "article"

    explore_service.filter(query=query, tags=tags, sorting=sorting, publication_type=publication_type)

    mock_repository.filter.assert_called_once_with(
        query, sorting, publication_type, tags, **{}
    )