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

def test_filter_no_results(explore_service, mock_repository):
    """Prueba negativa: No se encuentran resultados para los filtros dados."""
    mock_repository.filter.return_value = []  # Simula que no hay resultados

    result = explore_service.filter(query="no match", tags=["unknown"], sorting="newest")

    assert result == []
    mock_repository.filter.assert_called_once_with(
        "no match", "newest", "any", ["unknown"], **{}
    )

def test_filter_invalid_sorting(explore_service):
    """Prueba negativa: Orden (sorting) inválido."""
    with pytest.raises(ValueError, match="Invalid sorting value"):
        explore_service.filter(sorting="invalid_order")

def test_filter_error_handling(explore_service, mock_repository):
    """Prueba negativa: Simular que el repositorio lanza una excepción."""
    mock_repository.filter.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        explore_service.filter(query="example")
