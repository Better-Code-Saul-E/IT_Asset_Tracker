from abc import ABC, abstractmethod
from typing import List, Dict
from src.it_asset_tracker.models.asset import Asset

class IAssetRepository(ABC):
    @abstractmethod
    def add(self, asset: Asset) -> int:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Asset]:
        pass

    @abstractmethod
    def delete(self, asset_id: int) -> bool:
        pass

    @abstractmethod
    def update(self, asset: Asset) -> bool:
        pass
    
    @abstractmethod
    def get_by_id(self, asset_id: int) -> Asset:
        pass