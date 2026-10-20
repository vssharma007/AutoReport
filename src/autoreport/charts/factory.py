"""Factory pattern: one entry point that dispatches to the right chart builder."""
from __future__ import annotations

import base64
from io import BytesIO

import matplotlib

matplotlib.use("Agg")  # headless rendering, cross-platform, no display needed
import matplotlib.pyplot as plt
import pandas as pd


class ChartFactory:
    _builders = {}

    @classmethod
    def register(cls, name: str):
        def decorator(fn):
            cls._builders[name] = fn
            return fn
        return decorator

    @classmethod
    def create(cls, chart_type: str, df: pd.DataFrame, **kwargs) -> str:
        """Build a chart and return it as a base64 PNG string (easy to embed in HTML/PDF)."""
        if chart_type not in cls._builders:
            raise ValueError(f"Unknown chart type: {chart_type}. Available: {list(cls._builders)}")
        fig, ax = plt.subplots(figsize=kwargs.pop("figsize", (7, 4)))
        cls._builders[chart_type](df, ax, **kwargs)
        fig.tight_layout()
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=110)
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("ascii")


@ChartFactory.register("bar")
def _bar(df, ax, x: str, y: str, title: str = ""):
    ax.bar(df[x], df[y])
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=45)


@ChartFactory.register("line")
def _line(df, ax, x: str, y: str, title: str = ""):
    ax.plot(df[x], df[y], marker="o")
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=45)


@ChartFactory.register("pie")
def _pie(df, ax, labels: str, values: str, title: str = ""):
    ax.pie(df[values], labels=df[labels], autopct="%1.1f%%")
    ax.set_title(title)


@ChartFactory.register("scatter")
def _scatter(df, ax, x: str, y: str, title: str = ""):
    ax.scatter(df[x], df[y])
    ax.set_title(title)


@ChartFactory.register("histogram")
def _histogram(df, ax, column: str, bins: int = 20, title: str = ""):
    ax.hist(df[column].dropna(), bins=bins)
    ax.set_title(title)


@ChartFactory.register("heatmap")
def _heatmap(df, ax, title: str = ""):
    corr = df.select_dtypes(include="number").corr()
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns)
    ax.figure.colorbar(im, ax=ax)
    ax.set_title(title)
