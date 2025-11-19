import pytest

from unittest.mock import MagicMock
from src.it_asset_tracker.services.asset_service import AssetService
from src.it_asset_tracker.interfaces.asset_repository_interface import IAssetRepository
from src.it_asset_tracker.models.asset import Asset

@pytest.fixture
def mock_repo():
    """Creates a fake repository that looks like IAssetRepository."""
    return MagicMock(spec=IAssetRepository)

@pytest.fixture
def asset_service(mock_repo):
    """Creates the service with the fake repo injected."""
    return AssetService(mock_repo)

def test_create_asset_calls_repo(asset_service, mock_repo):
    """
    Test that creating an asset actually calls the repository's add method.
    """
    mock_repo.add.return_value = 10
    new_id = asset_service.create_asset("Mouse", "Logitech", "MX", "SN999")

    assert new_id == 10

    mock_repo.add.assert_called_once() 

def test_get_all_assets(asset_service, mock_repo):
    """
    Test that the service returns whatever the repo gives it.
    """
    fake_assets = [
        Asset(1, "Laptop", "Dell", "XPS", "123"),
        Asset(2, "Phone", "Apple", "iPhone", "456")
    ]

    mock_repo.get_all.return_value = fake_assets
    results = asset_service.get_all_assets()

    assert len(results) == 2
    assert results[0].manufacturer == "Dell"