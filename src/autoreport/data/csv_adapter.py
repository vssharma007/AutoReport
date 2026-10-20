from __future__ import annotations

import pandas as pd

from .base import DataSource


class CSVDataSource(DataSource):
    def load(self) -> pd.DataFrame:
        # low_memory=False avoids dtype-guessing issues on large files;
        # for the 100K-row constraint this is fine without chunking.
        return pd.read_csv(self.path, low_memory=False)
