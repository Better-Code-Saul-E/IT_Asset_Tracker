import csv
import json
from typing import List, Dict, Any
from src.it_asset_tracker.interfaces.exporter_interface import IFileExporter

class CsvExporter(IFileExporter):
    def export(self, data: List[Dict[str, Any]], file_path: str) -> str:
        if not file_path.endswith('.csv'):
            file_path += '.csv'
            
        if not data:
            return file_path 
            
        fieldnames = data[0].keys()
        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return file_path

class JsonExporter(IFileExporter):
    def export(self, data: List[Dict[str, Any]], file_path: str) -> str:
        if not file_path.endswith('.json'):
            file_path += '.json'

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return file_path