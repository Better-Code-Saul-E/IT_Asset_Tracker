from abc import ABC, abstractmethod
from typing import List, Dict

class IView(ABC):
    @abstractmethod
    def display_assets(self, assets: List[dict]): 
        pass
    
    @abstractmethod
    def show_message(self, message: str): 
        pass
    
    @abstractmethod
    def show_error(self, message: str):
        pass
    
    @abstractmethod
    def show_menu(self) -> str:
        pass
    
    @abstractmethod
    def prompt_for_asset_data(self, columns: list) -> dict: 
        pass
    
    @abstractmethod
    def prompt_for_update(self, current: dict) -> dict: 
        pass
    
    @abstractmethod
    def prompt_for_id(self, action="delete") -> int: 
        pass
    
    @abstractmethod
    def prompt_for_export(self) -> tuple[str, str]: 
        pass
