from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.table import Table

console = Console()


@dataclass
class ResourceUsage:
    label: str
    percent: float
    details: str = ""


def usage_color(percent):
    if percent < 50:
        return "green"
    if percent < 80:
        return "yellow"
    return "red"


def build_usage_panel(title, rows):
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold")
    table.add_column()
    table.add_column(justify="right")
    table.add_column(style="dim")

    for row in rows:
        color = usage_color(row.percent)
        bar = ProgressBar(
            total=100,
            completed=row.percent,
            width=30,
            complete_style=color,
            finished_style=color,
        )
        table.add_row(row.label, bar, f"[{color}]{row.percent:5.1f}%[/]", row.details)

    return Panel(table, title=f"[bold cyan]{title}[/]", border_style="cyan", expand=False)


def show_usage(title, rows):
    console.print(build_usage_panel(title, rows))