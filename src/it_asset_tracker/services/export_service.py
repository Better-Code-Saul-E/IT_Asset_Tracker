import os
from typing import List, Dict, Any
from src.it_asset_tracker.interfaces.exporter_interface import IFileExporter

class ExportService:
    def __init__(self, export_dir: str, exporters: Dict[str, IFileExporter]):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)
        
        self._exporters = exporters

    def export_data(self, assets: List[Dict[str, Any]], file_format: str, filename: str) -> str:
        if not filename:
            raise ValueError("Filename cannot be empty")
        
        exporter = self._exporters.get(file_format)
        if not exporter:
            raise ValueError(f"Unsupported format: {file_format}")
            
        full_path = os.path.join(self.export_dir, filename)
        return exporter.export(assets, full_path)