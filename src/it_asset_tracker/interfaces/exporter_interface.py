from abc import ABC, abstractmethod
from typing import List, Dict, Any   

class IFileExporter(ABC):
    @abstractmethod
    def export(self, assets: List[Dict[str, Any]], file_path: str) -> str:
        pass
    
