from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


@dataclass
class NetworkResult:
    label: str
    value: str
    success: bool = True


def build_results_panel(title, rows):
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold")
    table.add_column()

    for row in rows:
        color = "green" if row.success else "red"
        table.add_row(row.label, f"[{color}]{row.value}[/]")

    return Panel(table, title=f"[bold cyan]{title}[/]", border_style="cyan", expand=False)


def show_results(title, rows):
    console.print(build_results_panel(title, rows))