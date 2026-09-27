"""Elektro komut satırı giriş noktası."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
from rich import box
from rich.panel import Panel
from rich.table import Table

from elektro import REPO_URL, __version__
from elektro.modules import datasheet as datasheet_mod
from elektro.modules import digital, filters, ohm, passive, resistor, rf, timer555
from elektro.ui import console, fail

app = typer.Typer(
    name="elektro",
    help="Terminal tabanlı Elektrik-Elektronik Mühendisliği aracı.",
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
)

TEMEL, PASIF, SINYAL, ARAC = "Temel", "Pasif elemanlar", "Sinyal & RF", "Araçlar"

app.command(rich_help_panel=TEMEL)(ohm.ohm)
app.add_typer(resistor.app, name="resistor", rich_help_panel=TEMEL)
app.add_typer(timer555.app, name="555", rich_help_panel=TEMEL)
app.add_typer(digital.app, name="logic", rich_help_panel=TEMEL)

app.command(rich_help_panel=PASIF)(passive.series)
app.command(rich_help_panel=PASIF)(passive.parallel)
app.command(rich_help_panel=PASIF)(passive.divider)
app.command(rich_help_panel=PASIF)(passive.led)
app.command(rich_help_panel=PASIF)(passive.eseries)
app.command(rich_help_panel=PASIF)(passive.cap)

app.add_typer(filters.app, name="filter", rich_help_panel=SINYAL)
app.add_typer(rf.app, name="rf", rich_help_panel=SINYAL)

app.command(rich_help_panel=ARAC)(datasheet_mod.datasheet)


MENU = [
    ("Temel", [
        ("ohm", "Ohm kanunu ve güç", "elektro ohm -v 12 -r 1k"),
        ("resistor", "Renk kodu, SMD kodu", "elektro resistor k s r a"),
        ("555", "NE555 zamanlayıcı", "elektro 555 astable -f 1k --c 10n"),
        ("logic", "Tabanlar, kapılar, ifadeler", 'elektro logic expr "A & ~B"'),
    ]),
    ("Pasif", [
        ("series/parallel", "Seri/paralel eşdeğer", "elektro parallel 1k 2k2"),
        ("divider", "Gerilim bölücü", "elektro divider --vin 5 --vout 3.3"),
        ("led", "LED ön direnci", "elektro led --vs 5 --vf 2"),
        ("eseries", "Standart değerler", "elektro eseries 4k8"),
        ("cap", "Kondansatör kodu", "elektro cap 104"),
    ]),
    ("Sinyal", [
        ("filter", "RC/RL/LC/RLC filtreler", "elektro filter rc --fc 1k --c 10n"),
        ("rf", "FSPL, link bütçesi, anten", "elektro rf link -f 868 -d 10"),
    ]),
    ("Araç", [
        ("datasheet", "Datasheet bul ve indir", "elektro datasheet lm358"),
        ("helpall", "Tüm komutların kılavuzu", "elektro helpall"),
        ("update", "Son sürüme güncelle", "elektro update"),
    ]),
]


def show_menu() -> None:
    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    table.add_column(style="bold cyan", no_wrap=True)
    table.add_column()
    table.add_column(style="dim")
    for i, (_, rows) in enumerate(MENU):
        if i:
            table.add_row("", "", "")
        for cmd, desc, example in rows:
            table.add_row(cmd, desc, example)
    console.print(Panel(table, title=f"[bold yellow]⚡ ELEKTRO {__version__}[/]",
                        subtitle="[dim]elektro KOMUT --help[/]", border_style="bright_blue", expand=False))


def _version_callback(value: bool):
    if value:
        console.print(f"elektro {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(None, "--version", "-V", callback=_version_callback,
                                           is_eager=True, help="Sürümü göster"),
):
    """⚡ Elektrik-Elektronik Mühendisliği hesaplamaları için terminal aracı.

    Değerler mühendislik gösterimiyle yazılabilir: 4k7, 100n, 2.2u, 10M, 1meg
    """
    if ctx.invoked_subcommand is None:
        show_menu()


# --- helpall -------------------------------------------------------------------------

def _walk(cmd, path: list):
    subcommands = getattr(cmd, "commands", None)
    if subcommands is None:
        yield path, cmd
        return
    for name, sub in subcommands.items():
        if not sub.hidden:
            yield from _walk(sub, path + [name])


def _param_line(p) -> tuple:
    if p.param_type_name == "option":
        names = ", ".join(p.opts + p.secondary_opts)
        if p.metavar:
            names += f" {p.metavar}"
    else:
        names = (p.metavar or p.name).upper()
        if p.nargs == -1 and not names.endswith("..."):
            names += "..."
    return names, getattr(p, "help", "") or ""


@app.command(rich_help_panel=ARAC)
def helpall():
    """Tüm komutların ayrıntılı kılavuzu (sayfalayıcıda)."""
    root = typer.main.get_command(app)
    os.environ.setdefault("LESS", "-R")
    with console.pager(styles=True):
        console.rule(f"[bold yellow]ELEKTRO {__version__} — Kullanım Kılavuzu")
        console.print("Değerler mühendislik gösterimiyle yazılabilir: "
                      "[cyan]4k7  100n  2.2u  10M  1meg  1R5[/]\n")
        for path, cmd in _walk(root, ["elektro"]):
            if path[-1] in ("helpall",):
                continue
            console.print(f"\n[bold cyan]{' '.join(path)}[/]")
            help_text = (cmd.help or "").split("\f")[0].strip()
            for line in help_text.splitlines():
                console.print(f"    {line}", markup=False)
            params = [_param_line(p) for p in cmd.params if p.name not in ("help",)]
            if params:
                t = Table(show_header=False, box=None, padding=(0, 2))
                t.add_column(style="green", no_wrap=True)
                t.add_column()
                for names, h in params:
                    t.add_row("    " + names, h)
                console.print(t)
        console.print(f"\n[dim]{REPO_URL}[/]")


# --- update ----------------------------------------------------------------------------

INIT_URL = REPO_URL.replace("github.com", "raw.githubusercontent.com") + "/main/elektro/__init__.py"
TARBALL_URL = REPO_URL + "/archive/refs/heads/main.tar.gz"


def _version_tuple(v: str) -> tuple:
    return tuple(int(x) for x in re.findall(r"\d+", v)[:3])


def _install_kind() -> str:
    prefix = Path(sys.prefix)
    if (prefix / ".elektro-install").exists():
        return "installer"
    if "pipx" in prefix.parts:
        return "pipx"
    return "other"


@app.command(rich_help_panel=ARAC)
def update(force: bool = typer.Option(False, "--force", help="Sürüm aynı olsa da yeniden kur")):
    """Elektro'yu GitHub'daki son sürüme günceller."""
    import requests

    try:
        r = requests.get(INIT_URL, timeout=10)
        r.raise_for_status()
        latest = re.search(r'__version__\s*=\s*"([^"]+)"', r.text).group(1)
    except Exception:
        fail("GitHub'dan sürüm bilgisi alınamadı. İnternet bağlantını kontrol et.")

    console.print(f"Kurulu: [cyan]{__version__}[/]   GitHub: [cyan]{latest}[/]")
    if _version_tuple(latest) <= _version_tuple(__version__) and not force:
        console.print("[green]Zaten güncel.[/]")
        return

    kind = _install_kind()
    if kind == "pipx":
        console.print("pipx ile kurulmuş. Yeni kurulum betiğine geçmek için:\n"
                      f"  [cyan]pipx uninstall elektro && curl -fsSL {REPO_URL}/raw/main/install.sh | bash[/]")
        raise typer.Exit(1)
    if kind != "installer":
        console.print("Geliştirme kurulumu görünüyor; repo klasöründe [cyan]git pull[/] yeterli.")
        raise typer.Exit(1)

    console.print("Güncelleniyor…")
    cmd = [sys.executable, "-m", "pip", "install", "--quiet", "--disable-pip-version-check",
           "--upgrade", "--force-reinstall", TARBALL_URL]
    if subprocess.call(cmd) != 0:
        fail("güncelleme başarısız")
    console.print(f"[bold green]✓ elektro {latest} kuruldu.[/]")


if __name__ == "__main__":
    app()
