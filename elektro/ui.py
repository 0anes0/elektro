"""Ortak terminal çıktısı yardımcıları."""

from __future__ import annotations

from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typer.core import TyperGroup

from elektro.units import parse_value

console = Console(highlight=False)
err_console = Console(stderr=True, highlight=False)


def result_panel(title: str, rows: dict, note: Optional[str] = None) -> None:
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column(style="cyan", justify="right")
    table.add_column(style="bold green")
    for key, value in rows.items():
        table.add_row(key, str(value))
    console.print(Panel(table, title=f"[bold]{title}[/]", border_style="green",
                        subtitle=note, expand=False))


def theory(*lines: str) -> None:
    console.print()
    for line in lines:
        console.print(f"[dim]{line}[/]")


def fail(message: str, code: int = 1) -> "typer.Exit":
    err_console.print(f"[bold red]Hata:[/] {message}")
    raise typer.Exit(code)


def warn(message: str) -> None:
    console.print(f"[yellow]Uyarı:[/] {message}")


def eng(help_text: str) -> dict:
    """Mühendislik gösterimini (1k, 100n, 4k7) kabul eden seçenekler için ortak ayarlar."""
    return {"parser": parse_value, "metavar": "DEĞER", "help": help_text}


class DefaultCommandGroup(TyperGroup):
    """İlk argüman bir alt komut değilse `default_command`'ı çalıştırır.

    Böylece `elektro resistor k s r a` ile `elektro resistor decode k s r a` aynı işi yapar.
    """

    default_command: str = ""

    def parse_args(self, ctx, args):
        if args and self.default_command and args[0] not in self.commands and not args[0].startswith("-"):
            args.insert(0, self.default_command)
        return super().parse_args(ctx, args)


def default_group(command: str) -> type:
    return type(f"DefaultGroup_{command}", (DefaultCommandGroup,), {"default_command": command})
