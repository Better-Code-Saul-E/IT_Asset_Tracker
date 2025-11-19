from src.it_asset_tracker.models.asset import Asset

def test_create_asset():
    """Test that we can create an Asset object correctly."""
    asset = Asset(
        id=1, 
        device_type="Laptop", 
        manufacturer="Dell", 
        model="XPS 13", 
        serial_number="SN123"
    )
    
    assert asset.id == 1
    assert asset.device_type == "Laptop"
    assert asset.serial_number == "SN123"