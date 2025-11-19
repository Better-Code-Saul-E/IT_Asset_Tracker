import pytest

from src.it_asset_tracker.repositories.sqlite_asset_repository import SQLiteAssetRepository
from src.it_asset_tracker.models.asset import Asset

@pytest.fixture
def repo():
    """
    Creates a repository connected to a temporary in-memory database.
    """
    repo = SQLiteAssetRepository(":memory:")
    return repo

def test_add_and_get_asset(repo):
    """
    Test adding an asset and retrieving it from the DB.
    """
    asset = Asset(None, "Tablet", "Samsung", "Galaxy", "TAB-123")
    
    new_id = repo.add(asset)
    assets = repo.get_all()
    
    assert len(assets) == 1
    assert assets[0].id == new_id
    assert assets[0].serial_number == "TAB-123"

def test_delete_asset(repo):
    """
    Test deleting an asset.
    """
    asset = Asset(None, "Screen", "LG", "Ultrafine", "LG-555")
    new_id = repo.add(asset)

    success = repo.delete(new_id)
    
    assert success is True
    assert len(repo.get_all()) == 0

def test_unique_serial_constraint(repo):
    """
    Test that adding duplicate serials fails (if you implemented error handling).
    """
    import sqlite3
    
    asset1 = Asset(None, "A", "B", "C", "UNIQUE-SN")
    repo.add(asset1)
    asset2 = Asset(None, "X", "Y", "Z", "UNIQUE-SN")
    
    with pytest.raises(ValueError):
        repo.add(asset2)