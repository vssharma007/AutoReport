"""Adapter pattern: every data source exposes the same .load() -> DataFrame interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class DataSource(ABC):
    """Common interface all data adapters must implement."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"Data source not found: {self.path}")

    @abstractmethod
    def load(self) -> pd.DataFrame:
        """Return the data as a pandas DataFrame."""
        raise NotImplementedError

    def validate_schema(self, required_columns: list[str] | None = None) -> None:
        """Basic schema check — extend per-adapter as needed."""
        if required_columns is None:
            return
        df = self.load()
        missing = set(required_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")


def get_data_source(path: str | Path) -> DataSource:
    """Factory-ish helper: pick the right adapter based on file extension."""
    from .csv_adapter import CSVDataSource
    from .excel_adapter import ExcelDataSource
    from .json_adapter import JSONDataSource
    from .sqlite_adapter import SQLiteDataSource

    ext = Path(path).suffix.lower()
    mapping = {
        ".csv": CSVDataSource,
        ".xlsx": ExcelDataSource,
        ".xls": ExcelDataSource,
        ".json": JSONDataSource,
        ".db": SQLiteDataSource,
        ".sqlite": SQLiteDataSource,
    }
    if ext not in mapping:
        raise ValueError(f"Unsupported data source type: {ext}")
    return mapping[ext](path)
