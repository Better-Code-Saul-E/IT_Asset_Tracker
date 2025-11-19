import sqlite3

from typing import List, Optional
from src.it_asset_tracker.interfaces.asset_repository_interface import IAssetRepository
from src.it_asset_tracker.models.asset import Asset

class SQLiteAssetRepository(IAssetRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._create_table()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def _create_table(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS assets (
                    asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_type TEXT,
                    manufacturer TEXT,
                    model TEXT,
                    serial_number TEXT
                )""")
            
    def add(self, asset: Asset) -> int:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                "INSERT INTO assets (device_type, manufacturer, model, serial_number) VALUES (?, ?, ?, ?)",
                (asset.device_type, asset.manufacturer, asset.model, asset.serial_number))
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"Asset with serial number '{asset.serial_number}' already exists.")
            else:
                raise e

        
    def get_all(self) -> List[Asset]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT asset_id, device_type, manufacturer, model, serial_number FROM assets")
            rows = cursor.fetchall()

        return [Asset(id=row[0], device_type=row[1], manufacturer=row[2], model=row[3], serial_number=row[4]) for row in rows]        
    
    def delete(self, asset_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM assets WHERE asset_id = ?", (asset_id,))
            return cursor.rowcount > 0
        
    def get_by_id(self, asset_id: int) -> Asset:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT asset_id, device_type, manufacturer, model, serial_number FROM assets WHERE asset_id = ?", (asset_id,))            
            row = cursor.fetchone()
            if row:
                return Asset(id=row[0], device_type=row[1], manufacturer=row[2], model=row[3], serial_number=row[4])
            
        return None

    def update(self, asset: Asset) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE assets 
                SET device_type = ?, manufacturer = ?, model = ?, serial_number = ?
                WHERE asset_id = ?
                """,
                (asset.device_type, asset.manufacturer, asset.model, asset.serial_number, asset.id)
            )
            return cursor.rowcount > 0