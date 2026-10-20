from __future__ import annotations

import pandas as pd

from .base import DataSource


class JSONDataSource(DataSource):
    def load(self) -> pd.DataFrame:
        return pd.read_json(self.path)
