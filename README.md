# AutoReport

Automated report & analytics generator — reads data from CSV/Excel/JSON/SQLite,
runs analysis, and produces HTML/PDF reports from YAML templates.

## What's built here (Days 1–4 of the brief)

- Project skeleton (`pyproject.toml`, `pip install -e .`)
- CLI with `generate`, `validate`, `list-templates` (Typer)
- Data adapters for CSV, Excel, JSON, SQLite — all behind one `DataSource` interface
  (this is the **Adapter pattern** the rubric asks for)
- Statistical analysis: summary stats, group-by aggregation, correlations,
  Z-score and IQR anomaly detection, moving average, growth rate
- Chart factory (bar, line, pie, scatter, histogram, heatmap) — the **Factory pattern**
- YAML → Jinja2 → HTML report pipeline, working end to end
- Pydantic-validated report templates
- 9 passing pytest tests
- A sample dataset + sample template that actually generates a report

## Quickstart

```bash
pip install -e .
autoreport validate templates/sales_template.yaml
autoreport generate templates/sales_template.yaml -o sample_data/sample_report.html
```

Open `sample_data/sample_report.html` in a browser — it has real stats tables and
matplotlib charts embedded as base64 PNGs.

## Run tests

```bash
pip install -e ".[dev]"
pytest -v
```

## Writing your own template

```yaml
title: "My Report"
data_source: "path/to/data.csv"
sections:
  - name: "Summary Statistics"
    kind: "summary_stats"
  - name: "Revenue by Region"
    kind: "group_by"
    group_col: "region"
    value_col: "revenue"
    agg: "sum"          # sum | mean | count | min | max
  - name: "Trend"
    kind: "chart"
    chart:
      type: "line"       # bar | line | pie | scatter | histogram | heatmap
      x: "month"
      y: "revenue"
      title: "Revenue over time"
  - name: "Raw Data"
    kind: "table"
```

## What's NOT built yet — your remaining roadmap (Days 5–15)

This scaffold covers roughly the first 3–4 days. Here's what's left, mapped to the
original brief, plus where in this codebase each piece plugs in:

| Day(s) | Task | Where it goes |
|---|---|---|
| 5 | Trend detection (moving avg, growth rate) — **functions already exist** in `analysis/stats.py`, just wire them into report sections | `reports/builder.py` |
| 6 | Anomaly detection in reports — Z-score/IQR functions **already exist**, add an `"anomalies"` section kind | `reports/builder.py`, `config/loader.py` |
| 8 | Interactive Plotly charts for HTML variant | new `charts/plotly_factory.py`, swap in `report.html.j2` |
| 11 | PDF generation — convert the HTML template output using WeasyPrint (`pip install autoreport[pdf]`) | new `reports/pdf_builder.py` |
| 13 | Scheduler — wrap `generate()` in an APScheduler job, add `autoreport schedule` command | new `scheduler.py`, register in `cli.py` |
| 14 | Push pytest coverage past 70%, add edge-case tests (empty CSV, huge dataset, malformed YAML) | `tests/` |
| 15 | Package for distribution (this pyproject.toml already supports `pip install`), write full user guide, prep 5-min demo | `README.md`, `pyproject.toml` |

### Concrete next step
Add PDF export — since HTML is already working, WeasyPrint can render it directly:

```python
from weasyprint import HTML
HTML(string=html_string).write_pdf(output_path)
```

That's a ~10-line addition to `reports/builder.py` and knocks out Day 11.
