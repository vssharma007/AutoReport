import pandas as pd
import pytest

from autoreport.analysis import stats as st


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "region": ["N", "N", "S", "S"],
        "revenue": [100, 200, 300, 100000],  # last value is an outlier
    })


def test_summary_stats_has_expected_columns(sample_df):
    result = st.summary_stats(sample_df)
    assert "mean" in result.columns
    assert "revenue" in result.index


def test_group_by_aggregate_sums_correctly(sample_df):
    result = st.group_by_aggregate(sample_df, "region", "revenue", "sum")
    n_total = result.loc[result["region"] == "N", "revenue"].iloc[0]
    assert n_total == 300


def test_zscore_flags_outlier(sample_df):
    flags = st.detect_anomalies_zscore(sample_df["revenue"], threshold=1.0)
    assert flags.iloc[3]  # the 100000 value should be flagged
    assert not flags.iloc[0]


def test_iqr_flags_outlier(sample_df):
    flags = st.detect_anomalies_iqr(sample_df["revenue"])
    assert flags.iloc[3]


def test_growth_rate_first_value_is_zero(sample_df):
    rates = st.growth_rate(sample_df["revenue"])
    assert rates.iloc[0] == 0
