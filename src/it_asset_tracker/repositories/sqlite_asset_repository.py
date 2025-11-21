import sqlite3

from typing import List, Optional, Dict
from src.it_asset_tracker.interfaces.asset_repository_interface import IAssetRepository
from src.it_asset_tracker.models.asset import Asset

class SQLiteAssetRepository(IAssetRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
        
        if self.db_path == ":memory:":
            self.connection = sqlite3.connect(self.db_path)
            self.connection.execute("PRAGMA foreign_keys = 1")

    def _get_connection(self):
        if self.connection:
            return self.connection
        
        return sqlite3.connect(self.db_path)
    
    def _create_table(self, schema: dict = None):
        with self._get_connection() as conn:
            if schema:
                cols_sql = ", ".join([f"{name} {dtype}" for name, dtype in schema.items()])
                sql = f"CREATE TABLE IF NOT EXISTS assets (asset_id INTEGER PRIMARY KEY AUTOINCREMENT, {cols_sql})"
                conn.execute(sql)
            else:
                conn.execute("""
                CREATE TABLE IF NOT EXISTS assets (
                    asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_type TEXT,
                    manufacturer TEXT,
                    model TEXT,
                    serial_number TEXT NOT NULL UNIQUE
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
    
    def add_dynamic(self, data: dict) -> int:
        """
        Adds a row using a dictionary instead of a strict Asset object.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?"] * len(data))
            values = tuple(data.values())
            
            sql = f"INSERT INTO assets ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, values)
            return cursor.lastrowid
        
    def get_all(self) -> List[Asset]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM assets")
            rows = cursor.fetchall()
            
            column_names = [description[0] for description in cursor.description]
            
            results = []
            for row in rows:
                results.append(dict(zip(column_names, row)))
            
            return results

    def get_columns(self) -> Dict[str, str]:
        """
        Returns a list of column names in the assets table.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(assets)")
            rows = cursor.fetchall()

            return {row[1]: row[2] for row in rows}


    def delete(self, asset_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM assets WHERE asset_id = ?", (asset_id,))
            return cursor.rowcount > 0
        
    def get_by_id(self, asset_id: int) -> Asset:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM assets WHERE asset_id = ?", (asset_id,))
            row = cursor.fetchone()
            
            if row:
                col_names = [d[0] for d in cursor.description]
                return dict(zip(col_names, row))
            return None

    def update(self, asset_id: int, data: dict) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            updatable_cols = [key for key in data.keys() if key != 'asset_id']
            set_clause = ", ".join([f"{col} = ?" for col in updatable_cols])
            
            values = [data[col] for col in updatable_cols]
            values.append(asset_id)
            
            sql = f"UPDATE assets SET {set_clause} WHERE asset_id = ?"
            
            cursor.execute(sql, tuple(values))
            return cursor.rowcount > 0