import sqlite3
from typing import Optional

class SQLiteContext:
    """
    Handles the SQLite connection.
    """
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None
        
        if self.db_path == ":memory:":
            self._connection = sqlite3.connect(self.db_path)
            self._connection.execute("PRAGMA foreign_keys = 1")

    def get_connection(self) -> sqlite3.Connection:
        if self._connection:
            return self._connection

        return sqlite3.connect(self.db_path)