from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .config.loader import load_template
from .reports.builder import build_report

app = typer.Typer(help="AutoReport — automated report & analytics generator")
console = Console()


@app.command()
def generate(
    template: Path = typer.Argument(..., help="Path to a YAML report template"),
    output: Path = typer.Option("report.html", "--output", "-o", help="Output file path"),
):
    """Generate a single report from a template."""
    tpl = load_template(template)
    out_path = build_report(tpl, output)
    console.print(f"[bold green]Report generated:[/bold green] {out_path}")


@app.command()
def validate(template: Path = typer.Argument(..., help="Path to a YAML report template")):
    """Validate a report template without generating a report."""
    try:
        tpl = load_template(template)
    except Exception as exc:
        console.print(f"[bold red]Invalid template:[/bold red] {exc}")
        raise typer.Exit(code=1)
    console.print(f"[bold green]Valid.[/bold green] {len(tpl.sections)} section(s) defined.")


@app.command("list-templates")
def list_templates(directory: Path = typer.Option("templates", "--dir", "-d")):
    """List available report templates in a directory."""
    table = Table(title="Available Templates")
    table.add_column("File")
    table.add_column("Title")
    for path in sorted(directory.glob("*.yaml")):
        try:
            tpl = load_template(path)
            table.add_row(path.name, tpl.title)
        except Exception:
            table.add_row(path.name, "[red]invalid[/red]")
    console.print(table)


if __name__ == "__main__":
    app()
