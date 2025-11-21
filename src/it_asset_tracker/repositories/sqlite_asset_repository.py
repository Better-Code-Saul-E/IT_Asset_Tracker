import sqlite3
from typing import List, Dict, Any, Optional
from src.it_asset_tracker.interfaces.asset_repository_interface import IAssetRepository
from src.it_asset_tracker.repositories.db_context import SQLiteContext

class SQLiteAssetRepository(IAssetRepository):
    def __init__(self, context: SQLiteContext, table_name: str = "assets"):
        self.context = context
        self.table_name = table_name

    def _get_connection(self):
        return self.context.get_connection()
    
    def create_table(self, schema: Dict[str, str] = None):
        if not schema:
            return

        cols_sql = ", ".join([f"{name} {dtype}" for name, dtype in schema.items()])
        sql = f"CREATE TABLE IF NOT EXISTS {self.table_name} (asset_id INTEGER PRIMARY KEY AUTOINCREMENT, {cols_sql})"

        with self._get_connection() as conn:
                conn.execute(sql)

    def get_all(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM assets {self.table_name}")
            rows = cursor.fetchall()
            
            column_names = [description[0] for description in cursor.description]
            return [dict(zip(column_names, row)) for row in rows]

    def get_by_id(self, asset_id: int) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE asset_id = ?", (asset_id,))
            row = cursor.fetchone()
            
            if row:
                col_names = [d[0] for d in cursor.description]
                return dict(zip(col_names, row))
            
            return None
                    
    def add(self, data: Dict[str, Any]) -> int:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                columns = ", ".join(data.keys())
                placeholders = ", ".join(["?"] * len(data))
                values = tuple(data.values())
                
                sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, values)
                return cursor.lastrowid
            
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"Duplicate entry found for {str(e).split('.')[-1]}.")            
            raise e

    def update(self, asset_id: int, data: Dict[str, Any]) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            updatable_cols = [key for key in data.keys() if key != 'asset_id']
            set_clause = ", ".join([f"{col} = ?" for col in updatable_cols])
            
            values = [data[col] for col in updatable_cols]
            values.append(asset_id)
            
            sql = f"UPDATE {self.table_name} SET {set_clause} WHERE asset_id = ?"
            
            cursor.execute(sql, tuple(values))
            return cursor.rowcount > 0
        
    def delete(self, asset_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(f"DELETE FROM {self.table_name} WHERE asset_id = ?", (asset_id,))
            return cursor.rowcount > 0
            
    def get_columns(self) -> Dict[str, str]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({self.table_name})")

            rows = cursor.fetchall()
            return {row[1]: row[2] for row in rows}