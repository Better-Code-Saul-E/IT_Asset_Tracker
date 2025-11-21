from abc import ABC, abstractmethod
from typing import List, Dict

class IAssetService(ABC):
    @abstractmethod
    def get_all_assets(self) -> List[dict]: 
        pass

    @abstractmethod
    def get_asset(self, asset_id: int) -> dict | None:
        pass
    
    @abstractmethod
    def create_asset(self, data: dict) -> int:
        pass
    
    @abstractmethod
    def update_asset(self, asset_id: int, data: dict):
        pass
    
    @abstractmethod
    def remove_asset(self, asset_id: int) -> bool: 
        pass
    
    @abstractmethod
    def get_table_columns(self) -> list[str]:
        pass
    