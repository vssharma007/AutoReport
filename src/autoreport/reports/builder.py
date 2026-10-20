from __future__ import annotations

from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from ..analysis import stats as st
from ..charts.factory import ChartFactory
from ..config.loader import ReportTemplate
from ..data.base import get_data_source

TEMPLATE_DIR = Path(__file__).parent / "templates"


def build_report(template: ReportTemplate, output_path: str | Path) -> Path:
    df = get_data_source(template.data_source).load()

    rendered_sections = []
    for section in template.sections:
        entry = {"name": section.name, "table_html": None, "chart_b64": None}

        if section.kind == "summary_stats":
            entry["table_html"] = st.summary_stats(df).round(2).to_html(classes="stats")
        elif section.kind == "group_by":
            result = st.group_by_aggregate(df, section.group_col, section.value_col, section.agg)
            entry["table_html"] = result.to_html(index=False)
        elif section.kind == "table":
            entry["table_html"] = df.to_html(index=False, max_rows=50)
        elif section.kind == "chart" and section.chart:
            chart_kwargs = section.chart.model_dump(exclude={"type"}, exclude_none=True)
            entry["chart_b64"] = ChartFactory.create(section.chart.type, df, **chart_kwargs)

        rendered_sections.append(entry)

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)
    tpl = env.get_template("report.html.j2")
    html = tpl.render(
        title=template.title,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        sections=rendered_sections,
    )

    output_path = Path(output_path)
    output_path.write_text(html, encoding="utf-8")
    return output_path
