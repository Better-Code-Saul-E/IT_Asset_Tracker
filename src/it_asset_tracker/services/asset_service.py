from typing import List, Dict
from src.it_asset_tracker.interfaces.asset_repository_interface import IAssetRepository
from src.it_asset_tracker.models.asset import Asset

class AssetService:
    def __init__(self, repo: IAssetRepository):
        self.repo = repo
    
    def create_asset(self, device_type: str, manufacturer: str, model: str, serial: str) -> int:
        new_asset = Asset(None, device_type, manufacturer, model, serial)
        return self.repo.add(new_asset)
    
    def create_dynamic_asset(self, data: dict) -> int:
        return self.repo.add_dynamic(data)
    
    def get_all_assets(self) -> List[dict]:
        return self.repo.get_all()
    
    def remove_asset(self, asset_id: int) -> bool:
        return self.repo.delete(asset_id)
    
    def get_table_columns(self) -> Dict[str, str]:
        return self.repo.get_columns()
    
    def get_asset(self, asset_id: int) -> dict:
        return self.repo.get_by_id(asset_id)

    def update_asset_details(self, asset_id: int, data: dict) -> bool:
        return self.repo.update(asset_id, data)