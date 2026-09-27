"""Ortak terminal çıktısı yardımcıları."""

from __future__ import annotations

import json
import math
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from typer.core import TyperGroup

from elektro.i18n import t
from elektro.units import parse_value

console = Console(highlight=False)
err_console = Console(stderr=True, highlight=False)


# --- JSON modu --------------------------------------------------------------------
# `--json` verildiğinde sonuçlar tablo yerine makine okunur JSON olarak yazılır.
_json = False


def set_json(enabled: bool) -> None:
    global _json
    _json = enabled


def json_mode() -> bool:
    return _json


def _clean(value):
    """JSON'a uygun hale getir (inf/nan → null, tuple → list)."""
    if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
        return None
    if isinstance(value, dict):
        return {k: _clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_clean(v) for v in value]
    return value


def print_json(data) -> None:
    print(json.dumps(_clean(data), ensure_ascii=False, indent=2))


def result_panel(title: str, rows: dict, data: Optional[dict] = None, note: Optional[str] = None) -> None:
    """Sonuç panelini yazar; JSON modunda `data`yı (yoksa satırları) JSON olarak basar."""
    if _json:
        print_json(data if data is not None else {k: str(v) for k, v in rows.items()})
        return
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column(style="cyan", justify="right")
    table.add_column(style="bold green")
    for key, value in rows.items():
        table.add_row(key, value if isinstance(value, Text) else str(value))
    console.print(Panel(table, title=f"[bold]{title}[/]", border_style="green",
                        subtitle=note, expand=False))


def emit(renderable, data) -> None:
    """Tablo gibi bir çıktıyı yazar; JSON modunda yerine `data`yı basar."""
    if _json:
        print_json(data)
    else:
        console.print(renderable)


def theory(*lines: str) -> None:
    if _json:
        return
    console.print()
    for line in lines:
        console.print(f"[dim]{line}[/]")


def fail(message: str, code: int = 1) -> "typer.Exit":
    err_console.print(f"[bold red]{t('ui.error')}:[/] {message}")
    raise typer.Exit(code)


def warn(message: str) -> None:
    (err_console if _json else console).print(f"[yellow]{t('ui.warning')}:[/] {message}")


def eng(help_text: str) -> dict:
    """Mühendislik gösterimini (1k, 100n, 4k7) kabul eden seçenekler için ortak ayarlar."""
    return {"parser": parse_value, "metavar": t("ui.metavar.value"), "help": help_text}


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
