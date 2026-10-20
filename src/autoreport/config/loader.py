from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class ChartSpec(BaseModel):
    type: str
    title: str = ""
    x: str | None = None
    y: str | None = None
    column: str | None = None
    labels: str | None = None
    values: str | None = None


class SectionSpec(BaseModel):
    name: str
    kind: str  # "summary_stats" | "group_by" | "chart" | "table"
    group_col: str | None = None
    value_col: str | None = None
    agg: str = "sum"
    chart: ChartSpec | None = None


class ReportTemplate(BaseModel):
    title: str
    data_source: str
    sections: list[SectionSpec] = Field(default_factory=list)


def load_template(path: str | Path) -> ReportTemplate:
    with open(path) as f:
        raw = yaml.safe_load(f)
    return ReportTemplate(**raw)
