from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IAssetRepository(ABC):
    @abstractmethod
    def add(self, data: Dict[str, Any]) -> int:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete(self, asset_id: int) -> bool:
        pass

    @abstractmethod
    def update(self, asset_id: int, data: Dict[str, Any]) -> bool:
        pass
    
    @abstractmethod
    def get_by_id(self, asset_id: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_columns(self) -> Dict[str, str]:
        pass