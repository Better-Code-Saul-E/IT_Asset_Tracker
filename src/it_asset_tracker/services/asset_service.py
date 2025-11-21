from typing import List, Dict, Any
from src.it_asset_tracker.interfaces.asset_repository_interface import IAssetRepository
from src.it_asset_tracker.interfaces.asset_service_interface import IAssetService

class AssetService(IAssetService):
    def __init__(self, repo: IAssetRepository):
        self.repo = repo
    
    def get_all_assets(self) -> List[Dict[str, Any]]:
        return self.repo.get_all()
    
    def get_asset(self, asset_id: int) -> Dict[str, Any]:
        return self.repo.get_by_id(asset_id)
        
    def create_asset(self, data: Dict[str, Any]) -> int:
        return self.repo.add(data)

    def update_asset(self, asset_id: int, data: Dict[str, Any]) -> bool:
        return self.repo.update(asset_id, data)
    
    def remove_asset(self, asset_id: int) -> bool:
        return self.repo.delete(asset_id)    
        
    def get_table_columns(self) -> Dict[str, str]:
        return self.repo.get_columns()