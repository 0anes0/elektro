"""Elektro komut satırı giriş noktası."""

from __future__ import annotations

import io
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
import typer.core
import typer.rich_utils
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from elektro import REPO_URL, __version__
from elektro.i18n import (LANGUAGES, config_path, get_language, normalize, save_language,
                          set_language, t)
from elektro.modules import datasheet as datasheet_mod
from elektro.modules import digital, filters, ohm, passive, resistor, rf, timer555
from elektro.ui import console, fail


def _localize_typer() -> None:
    """Typer/Click'in kendi arayüz metinlerini (Options, Commands…) çevirir."""
    ru = typer.rich_utils
    ru.OPTIONS_PANEL_TITLE = t("typer.options")
    ru.ARGUMENTS_PANEL_TITLE = t("typer.arguments")
    ru.COMMANDS_PANEL_TITLE = t("typer.commands")
    ru.ERRORS_PANEL_TITLE = t("typer.error")
    ru.ABORTED_TEXT = t("typer.aborted")
    ru.REQUIRED_LONG_STRING = t("typer.required")
    ru.DEFAULT_STRING = t("typer.default")
    ru.RICH_HELP = t("typer.try_help")

    for cls in (typer.core.TyperCommand, typer.core.TyperGroup):
        original = cls.get_help_option

        def get_help_option(self, ctx, _original=original):
            opt = _original(self, ctx)
            if opt is not None:
                opt.help = t("typer.help_option")
            return opt

        cls.get_help_option = get_help_option


_localize_typer()

app = typer.Typer(
    name="elektro",
    help=t("cli.help"),
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
)

BASIC, PASSIVE, SIGNAL, TOOLS = (t("panel.basic"), t("panel.passive"),
                                 t("panel.signal"), t("panel.tools"))

app.command(rich_help_panel=BASIC, help=t("ohm.help"))(ohm.ohm)
app.add_typer(resistor.app, name="resistor", rich_help_panel=BASIC)
app.add_typer(timer555.app, name="555", rich_help_panel=BASIC)
app.add_typer(digital.app, name="logic", rich_help_panel=BASIC)

app.command(rich_help_panel=PASSIVE, help=t("combine.series.help"))(passive.series)
app.command(rich_help_panel=PASSIVE, help=t("combine.parallel.help"))(passive.parallel)
app.command(rich_help_panel=PASSIVE, help=t("div.help"))(passive.divider)
app.command(rich_help_panel=PASSIVE, help=t("led.help"))(passive.led)
app.command(rich_help_panel=PASSIVE, help=t("eseries.help"))(passive.eseries)
app.command(rich_help_panel=PASSIVE, help=t("cap.help"))(passive.cap)

app.add_typer(filters.app, name="filter", rich_help_panel=SIGNAL)
app.add_typer(rf.app, name="rf", rich_help_panel=SIGNAL)

app.command(rich_help_panel=TOOLS, help=t("ds.help"))(datasheet_mod.datasheet)


MENU = [
    [
        ("ohm", "menu.ohm", "elektro ohm -v 12 -r 1k"),
        ("resistor", "menu.resistor", "elektro resistor bn bk rd gd"),
        ("555", "menu.555", "elektro 555 astable -f 1k --c 10n"),
        ("logic", "menu.logic", 'elektro logic expr "A & ~B"'),
    ],
    [
        ("series/parallel", "menu.combine", "elektro parallel 1k 2k2"),
        ("divider", "menu.divider", "elektro divider --vin 5 --vout 3.3"),
        ("led", "menu.led", "elektro led --vs 5 --vf 2"),
        ("eseries", "menu.eseries", "elektro eseries 4k8"),
        ("cap", "menu.cap", "elektro cap 104"),
    ],
    [
        ("filter", "menu.filter", "elektro filter rc --fc 1k --c 10n"),
        ("rf", "menu.rf", "elektro rf link -f 868 -d 10"),
    ],
    [
        ("datasheet", "menu.datasheet", "elektro datasheet lm358"),
        ("helpall", "menu.helpall", "elektro helpall"),
        ("language", "menu.language", "elektro language en"),
        ("update", "menu.update", "elektro update"),
    ],
]


def show_menu() -> None:
    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    table.add_column(style="bold cyan", no_wrap=True)
    table.add_column()
    table.add_column(style="dim")
    for i, rows in enumerate(MENU):
        if i:
            table.add_row("", "", "")
        for cmd, key, example in rows:
            if cmd == "resistor" and get_language() == "tr":
                example = "elektro resistor k s r a"
            table.add_row(cmd, t(key), example)
    console.print(Panel(table, title=f"[bold yellow]⚡ ELEKTRO {__version__}[/]",
                        subtitle=f"[dim]{t('menu.subtitle')}[/]", border_style="bright_blue",
                        expand=False))


def _version_callback(value: bool):
    if value:
        console.print(f"elektro {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True, help=t("cli.help_long"))
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(None, "--version", "-V", callback=_version_callback,
                                           is_eager=True, help=t("cli.opt.version")),
    lang: Optional[str] = typer.Option(None, "--lang", metavar="en|tr|de|ru",
                                       help=t("cli.opt.lang")),
):
    # Dil, yardım metinleri üretilmeden önce elektro.i18n tarafından argv'den okunur;
    # burada yalnızca geçerliliği kontrol edilir.
    if lang is not None and normalize(lang) is None:
        fail(t("lang.unknown", code=lang, options=", ".join(LANGUAGES)))
    if ctx.invoked_subcommand is None:
        show_menu()


# --- language ------------------------------------------------------------------------

@app.command(rich_help_panel=TOOLS, help=t("lang.help"))
def language(code: Optional[str] = typer.Argument(None, metavar="en|tr|de|ru", help=t("lang.arg"))):
    if code is None:
        current = get_language()
        table = Table(show_header=False, box=None, padding=(0, 2))
        for c, name in LANGUAGES.items():
            mark = "[bold green]●[/]" if c == current else " "
            table.add_row(mark, f"[cyan]{c}[/]", name)
        console.print(table)
        console.print(f"\n[dim]{t('lang.usage')}[/]")
        return

    lang = normalize(code)
    if lang is None:
        fail(t("lang.unknown", code=code, options=", ".join(LANGUAGES)))
    try:
        path = save_language(lang)
    except OSError as e:
        fail(t("lang.save_failed", path=config_path(), error=e))
    set_language(lang)
    console.print(f"[bold green]✓[/] {t('lang.saved', name=LANGUAGES[lang])} [dim]({path})[/]")
    if os.environ.get("ELEKTRO_LANG"):
        console.print(f"[yellow]{t('lang.env_override')}[/]")


# Kolaylık için gizli takma adlar
app.command("languages", hidden=True)(language)
app.command("lang", hidden=True)(language)


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


def render_manual(out: Console) -> None:
    root = typer.main.get_command(app)
    out.rule(f"[bold yellow]ELEKTRO {__version__} — {t('manual.title')}")
    out.print(t("manual.values") + " [cyan]4k7  100n  2.2u  10M  1meg  1R5[/]")
    for path, cmd in _walk(root, ["elektro"]):
        if path[-1] == "helpall":
            continue
        out.print(f"\n[bold cyan]{' '.join(path)}[/]")
        help_text = (cmd.help or "").split("\f")[0].strip()
        for line in help_text.splitlines():
            out.print(f"    {line}", markup=False)
        params = [_param_line(p) for p in cmd.params if p.name != "help"]
        if params:
            out.print()
            tbl = Table(show_header=False, box=None, padding=(0, 2, 0, 4))
            tbl.add_column(style="green", no_wrap=True)
            tbl.add_column()
            for names, h in params:
                tbl.add_row(names, h)
            out.print(tbl)
    out.print(f"\n[dim]{REPO_URL}[/]")


@app.command(rich_help_panel=TOOLS, help=t("manual.help"))
def helpall():
    less = shutil.which("less")
    if not (sys.stdout.isatty() and less):
        render_manual(console)
        return
    # MANPAGER/PAGER kullanıcının man sayfaları için ayarlanmış olabilir (col -b, bat…)
    # ve renk kodlarını bozar; bu yüzden doğrudan `less -R` kullanılır.
    buf = io.StringIO()
    render_manual(Console(file=buf, force_terminal=True, color_system=console.color_system,
                          width=console.width, highlight=False))
    env = {**os.environ, "LESS": "-R", "LESSCHARSET": "utf-8"}
    try:
        subprocess.run([less, "-R"], input=buf.getvalue(), text=True, env=env)
    except (OSError, KeyboardInterrupt):
        pass


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


@app.command(rich_help_panel=TOOLS, help=t("upd.help"))
def update(force: bool = typer.Option(False, "--force", help=t("upd.opt.force"))):
    import requests

    try:
        r = requests.get(INIT_URL, timeout=10)
        r.raise_for_status()
        latest = re.search(r'__version__\s*=\s*"([^"]+)"', r.text).group(1)
    except Exception:
        fail(t("upd.fetch_failed"))

    console.print(f"{t('upd.installed')}: [cyan]{__version__}[/]   GitHub: [cyan]{latest}[/]")
    if _version_tuple(latest) <= _version_tuple(__version__) and not force:
        console.print(f"[green]{t('upd.up_to_date')}[/]")
        return

    kind = _install_kind()
    if kind == "pipx":
        console.print(t("upd.pipx") + "\n"
                      f"  [cyan]pipx uninstall elektro && curl -fsSL {REPO_URL}/raw/main/install.sh | bash[/]")
        raise typer.Exit(1)
    if kind != "installer":
        console.print(t("upd.dev"))
        raise typer.Exit(1)

    console.print(t("upd.updating"))
    cmd = [sys.executable, "-m", "pip", "install", "--quiet", "--disable-pip-version-check",
           "--upgrade", "--force-reinstall", TARBALL_URL]
    if subprocess.call(cmd) != 0:
        fail(t("upd.failed"))
    console.print(f"[bold green]✓ {t('upd.done', version=latest)}[/]")


if __name__ == "__main__":
    app()
