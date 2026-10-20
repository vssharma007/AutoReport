from __future__ import annotations

import sqlite3

import pandas as pd

from .base import DataSource


class SQLiteDataSource(DataSource):
    def __init__(self, path, table: str | None = None, query: str | None = None):
        super().__init__(path)
        self.table = table
        self.query = query

    def load(self) -> pd.DataFrame:
        conn = sqlite3.connect(self.path)
        try:
            if self.query:
                return pd.read_sql_query(self.query, conn)
            table = self.table or self._first_table(conn)
            return pd.read_sql_query(f"SELECT * FROM {table}", conn)
        finally:
            conn.close()

    @staticmethod
    def _first_table(conn: sqlite3.Connection) -> str:
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1;")
        row = cur.fetchone()
        if not row:
            raise ValueError("No tables found in SQLite database")
        return row[0]
