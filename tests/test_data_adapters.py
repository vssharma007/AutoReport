from pathlib import Path

import pytest

from autoreport.data.base import get_data_source
from autoreport.data.csv_adapter import CSVDataSource

SAMPLE_CSV = Path(__file__).parent.parent / "sample_data" / "sales.csv"


def test_csv_adapter_loads_dataframe():
    df = CSVDataSource(SAMPLE_CSV).load()
    assert not df.empty
    assert "revenue" in df.columns


def test_get_data_source_dispatches_by_extension():
    source = get_data_source(SAMPLE_CSV)
    assert isinstance(source, CSVDataSource)


def test_get_data_source_rejects_unknown_extension(tmp_path):
    bad_file = tmp_path / "data.txt"
    bad_file.write_text("hello")
    with pytest.raises(ValueError):
        get_data_source(bad_file)


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        CSVDataSource("does_not_exist.csv")
