"""Core statistical analysis functions. Pure functions: DataFrame in, dict/DataFrame out."""
from __future__ import annotations

import numpy as np
import pandas as pd


def summary_stats(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Mean, median, std, min, max, percentiles for numeric columns."""
    numeric = df.select_dtypes(include="number")
    if columns:
        numeric = numeric[columns]
    return numeric.describe(percentiles=[0.25, 0.5, 0.75, 0.9]).T


def group_by_aggregate(
    df: pd.DataFrame, group_col: str, value_col: str, agg: str = "sum"
) -> pd.DataFrame:
    return df.groupby(group_col, dropna=False)[value_col].agg(agg).reset_index()


def correlations(df: pd.DataFrame) -> pd.DataFrame:
    return df.select_dtypes(include="number").corr()


def detect_anomalies_zscore(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    """Boolean mask flagging values whose |z-score| exceeds threshold."""
    mean, std = series.mean(), series.std(ddof=0)
    if std == 0 or np.isnan(std):
        return pd.Series(False, index=series.index)
    z = (series - mean) / std
    return z.abs() > threshold


def detect_anomalies_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    """Boolean mask flagging values outside [Q1 - k*IQR, Q3 + k*IQR]."""
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - k * iqr, q3 + k * iqr
    return (series < lower) | (series > upper)


def moving_average(series: pd.Series, window: int = 3) -> pd.Series:
    return series.rolling(window=window, min_periods=1).mean()


def growth_rate(series: pd.Series) -> pd.Series:
    """Period-over-period % growth."""
    return series.pct_change().fillna(0) * 100
