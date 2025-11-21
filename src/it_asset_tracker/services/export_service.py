import csv
import json
import os
from dataclasses import asdict
from typing import List, Dict, Any
from src.it_asset_tracker.models.asset import Asset

class ExportService:
    def __init__(self, export_dir: str):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)

    def export_data(self, assets: List[Dict[str, Any]], file_format: str, filename: str) -> str:
        if not filename:
            raise ValueError("Filename cannot be empty")
        data = assets
        
        if file_format == 'csv':
            return self._export_to_csv(data, filename)
        elif file_format == 'json':
            return self._export_to_json(data, filename)
        else:
            raise ValueError(f"Unsupported format: {file_format}")

    def _export_to_csv(self, data: List[dict], filename: str) -> str:
        full_path = os.path.join(self.export_dir, f"{filename}.csv")
        if not data:
            return full_path 
            
        fieldnames = data[0].keys()
        with open(full_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return full_path

    def _export_to_json(self, data: List[dict], filename: str) -> str:
        full_path = os.path.join(self.export_dir, f"{filename}.json")
        with open(full_path, 'w') as f:
            json.dump(data, f, indent=4)
        return full_path