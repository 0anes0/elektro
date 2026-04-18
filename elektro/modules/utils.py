from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def format_number(val: float, unit: str = "") -> str:
    """Otomatik SI prefix ekler"""
    if val == 0:
        return f"0 {unit}"
    
    prefixes = [
        (1e12, "T"), (1e9, "G"), (1e6, "M"), (1e3, "k"),
        (1, ""), (1e-3, "m"), (1e-6, "u"), (1e-9, "n"), (1e-12, "p")
    ]
    
    abs_val = abs(val)
    for factor, prefix in prefixes:
        if abs_val >= factor:
            return f"{val/factor:.3f} {prefix}{unit}"
    return f"{val:.3e} {unit}"


def result_panel(title: str, data: dict):
    """Sonuclari duzgun panelde goster"""
    table = Table(show_header=False, box=None)
    table.add_column("Parametre", style="cyan", justify="right")
    table.add_column("Deger", style="bold green")
    
    for key, value in data.items():
        table.add_row(key, str(value))
    
    console.print(Panel(table, title=title, border_style="green"))
