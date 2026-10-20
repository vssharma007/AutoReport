from __future__ import annotations

import pandas as pd

from .base import DataSource


class ExcelDataSource(DataSource):
    def __init__(self, path, sheet_name: str | int = 0):
        super().__init__(path)
        self.sheet_name = sheet_name

    def load(self) -> pd.DataFrame:
        return pd.read_excel(self.path, sheet_name=self.sheet_name, engine="openpyxl")
