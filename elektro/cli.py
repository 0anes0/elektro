"""Elektro komut satırı giriş noktası."""

from __future__ import annotations

import datetime
import io
import os
import re
import shlex
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

from elektro import REPO_URL, __version__, state
from elektro.i18n import (LANGUAGES, config_path, get_language, normalize, save_language,
                          set_language, t)
from elektro.modules import datasheet as datasheet_mod
from elektro.modules import (analog, digital, embedded, filters, installation, machines, ohm, opamp, passive,
                             pinout, power, resistor, rf, signal, simulate, timer555, tools, wiring)
from elektro.ui import (console, err_console, fail, finish_output, json_mode, print_json, set_command,
                        set_json, set_report)


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

BASIC, PASSIVE, POWER, INSTALL, SIGNAL, EMBEDDED, TOOLS = (
    t("panel.basic"), t("panel.passive"), t("panel.power"), t("panel.install"), t("panel.signal"),
    t("panel.embedded"), t("panel.tools"))

app.command(rich_help_panel=BASIC, help=t("ohm.help"))(ohm.ohm)
app.add_typer(resistor.app, name="resistor", rich_help_panel=BASIC)
app.add_typer(timer555.app, name="555", rich_help_panel=BASIC)
app.add_typer(digital.app, name="logic", rich_help_panel=BASIC)
app.add_typer(analog.switch_app, name="switch", rich_help_panel=BASIC)
app.add_typer(opamp.app, name="opamp", rich_help_panel=BASIC)
app.command(rich_help_panel=BASIC, help=t("chg.help"))(analog.charge)

app.command(rich_help_panel=PASSIVE, help=t("combine.series.help"))(passive.series)
app.command(rich_help_panel=PASSIVE, help=t("combine.parallel.help"))(passive.parallel)
app.command(rich_help_panel=PASSIVE, help=t("div.help"))(passive.divider)
app.command(rich_help_panel=PASSIVE, help=t("led.help"))(passive.led)
app.command(rich_help_panel=PASSIVE, help=t("eseries.help"))(passive.eseries)
app.command(rich_help_panel=PASSIVE, help=t("cap.help"))(passive.cap)
app.command(rich_help_panel=PASSIVE, help=t("coil.help"))(passive.coil)
app.command(rich_help_panel=PASSIVE, help=t("xtal.help"))(passive.crystal)

app.command(rich_help_panel=POWER, help=t("reg.help"))(power.regulator)
app.command(rich_help_panel=POWER, help=t("bat.help"))(power.battery)
app.command(rich_help_panel=POWER, help=t("th.help"))(power.thermal)
app.command(rich_help_panel=POWER, help=t("rect.help"))(power.rectifier)
app.command(rich_help_panel=POWER, help=t("ac.help"))(power.acpower)
app.command(rich_help_panel=POWER, help=t("sd.help"))(power.stardelta)
app.command(rich_help_panel=POWER, help=t("wire.help"))(wiring.wire)
app.command(rich_help_panel=POWER, help=t("trace.help"))(wiring.trace)

app.command(rich_help_panel=INSTALL, help=t("cable.help"))(installation.cable)
app.command(rich_help_panel=INSTALL, help=t("brk.help"))(installation.breaker)
app.command(rich_help_panel=INSTALL, help=t("sc.help"))(installation.shortcircuit)
app.command(rich_help_panel=INSTALL, help=t("tr.help"))(machines.transformer)
app.command(rich_help_panel=INSTALL, help=t("mot.help"))(machines.motor)

app.add_typer(filters.app, name="filter", rich_help_panel=SIGNAL)
app.add_typer(rf.app, name="rf", rich_help_panel=SIGNAL)
app.command(rich_help_panel=SIGNAL, help=t("wave.help"))(signal.wave)
app.command("fft", rich_help_panel=SIGNAL, help=t("fft.help"))(signal.fft_cmd)

app.command(rich_help_panel=EMBEDDED, help=t("uart.help"))(embedded.uart)
app.command(rich_help_panel=EMBEDDED, help=t("pwm.help"))(embedded.pwm)
app.command(rich_help_panel=EMBEDDED, help=t("adc.help"))(embedded.adc)
app.command(rich_help_panel=EMBEDDED, help=t("i2c.help"))(embedded.i2c)
app.command(rich_help_panel=EMBEDDED, help=t("crc.help"))(embedded.crc)

app.command(rich_help_panel=TOOLS, help=t("ds.help"))(datasheet_mod.datasheet)
app.command(rich_help_panel=TOOLS, help=t("pin.help"))(pinout.pinout)
app.command(rich_help_panel=TOOLS, help=t("sim.help"))(simulate.sim)
app.command("examples", rich_help_panel=TOOLS, help=t("ex.help"))(simulate.examples_cmd)
app.command(rich_help_panel=TOOLS, help=t("calc.help"))(tools.calc)
app.command(rich_help_panel=TOOLS, help=t("unit.help"))(tools.unit)


MENU = [
    [
        ("ohm", "menu.ohm", "elektro ohm -v 12 -r 1k"),
        ("resistor", "menu.resistor", "elektro resistor bn bk rd gd"),
        ("555", "menu.555", "elektro 555 astable -f 1k --c 10n"),
        ("logic", "menu.logic", 'elektro logic expr "A & ~B"'),
        ("switch", "menu.switch", "elektro switch bjt --ic 500m -v 3.3"),
        ("charge", "menu.charge", "elektro charge --r 10k --c 100u --v 5"),
        ("opamp", "menu.opamp", "elektro opamp noninv --gain 11"),
    ],
    [
        ("series/parallel", "menu.combine", "elektro parallel 1k 2k2"),
        ("divider", "menu.divider", "elektro divider --vin 5 --vout 3.3"),
        ("led", "menu.led", "elektro led --vs 5 --vf 2"),
        ("eseries", "menu.eseries", "elektro eseries 4k8"),
        ("cap", "menu.cap", "elektro cap 104"),
        ("coil", "menu.coil", "elektro coil --l 1u --d 10"),
        ("crystal", "menu.crystal", "elektro crystal --cl 12p"),
    ],
    [
        ("regulator", "menu.regulator", "elektro regulator lm317 --vout 5"),
        ("battery", "menu.battery", "elektro battery 2000 -i 15m"),
        ("thermal", "menu.thermal", "elektro thermal -p 2 --rth-jc 5"),
        ("wire", "menu.wire", "elektro wire --awg 22 -l 3 -i 2"),
        ("trace", "menu.trace", "elektro trace -i 3"),
        ("rectifier", "menu.rectifier", "elektro rectifier --vac 12 -i 1 --ripple 1"),
        ("acpower", "menu.acpower", "elektro acpower --i 10 --pf 0.8 --target-pf 0.95"),
    ],
    [
        ("cable", "menu.cable", "elektro cable -p 9k --phases 3 -l 40"),
        ("breaker", "menu.breaker", "elektro breaker -i 14 --iz 21 --mm2 2.5 -l 30"),
        ("shortcircuit", "menu.shortcircuit", "elektro shortcircuit --kva 630 --mm2 95 -l 50"),
        ("transformer", "menu.transformer", "elektro transformer --v1 230 --v2 12 --va 50"),
        ("motor", "menu.motor", "elektro motor -p 7.5k --rpm 1450"),
    ],
    [
        ("filter", "menu.filter", "elektro filter rc --fc 1k --c 10n"),
        ("rf", "menu.rf", "elektro rf lora --sf 9 -p 20"),
        ("wave", "menu.wave", "elektro wave pwm --vp 5 -d 25"),
        ("fft", "menu.fft", "elektro fft scope.csv --plot fft.svg"),
    ],
    [
        ("uart", "menu.uart", "elektro uart -c 16M -b 115200"),
        ("pwm", "menu.pwm", "elektro pwm -c 72M -f 20k -m stm32"),
        ("adc", "menu.adc", "elektro adc -b 12 --vref 3.3 --code 2048"),
        ("i2c", "menu.i2c", "elektro i2c --cb 200p"),
        ("crc", "menu.crc", 'elektro crc "01 03 00 00 00 0A"'),
    ],
    [
        ("tui", "menu.tui", "elektro tui"),
        ("sim", "menu.sim", "elektro sim devre.json"),
        ("examples", "menu.examples", "elektro examples rc_lowpass"),
        ("shell", "menu.shell", "elektro shell"),
        ("set / vars", "menu.vars", "elektro set vin 12  →  -v @vin"),
        ("history", "menu.history", "elektro history"),
        ("calc", "menu.calc", 'elektro calc "230∠0 / (10 + j5)"'),
        ("unit", "menu.unit", "elektro unit 25 c"),
        ("datasheet", "menu.datasheet", "elektro datasheet lm358"),
        ("pinout", "menu.pinout", "elektro pinout ne555"),
        ("--md / --report", "menu.report", "elektro ohm -v 12 -r 1k --report lab.md"),
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
    json_out: bool = typer.Option(False, "--json", help=t("cli.opt.json")),
    md: bool = typer.Option(False, "--md", help=t("cli.opt.md")),
    latex: bool = typer.Option(False, "--latex", help=t("cli.opt.latex")),
    report: Optional[Path] = typer.Option(None, "--report", metavar=t("plot.metavar"), help=t("cli.opt.report")),
    copy: bool = typer.Option(False, "--copy", help=t("cli.opt.copy")),
):
    # Dil, yardım metinleri üretilmeden önce elektro.i18n tarafından argv'den okunur;
    # burada yalnızca geçerliliği kontrol edilir.
    if lang is not None and normalize(lang) is None:
        fail(t("lang.unknown", code=lang, options=", ".join(LANGUAGES)))
    if md and latex or json_out and (md or latex or report):
        fail(t("report.conflict"))
    # her çağrıda sıfırdan: kabukta bir önceki komuttan kalmasın
    set_json(json_out)
    fmt = "md" if md else "latex" if latex else None
    if report is not None and fmt is None:
        fmt = "latex" if report.suffix.lower() in (".tex", ".latex") else "md"
    set_report(fmt, to_stdout=md or latex, file=report, copy=copy)
    ctx.call_on_close(finish_output)
    if ctx.invoked_subcommand is None:
        show_menu()


# Geçmişe yazılmayan komutlar (yönetim komutları)
NOT_RECORDED = {"history", "shell", "tui", "helpall", "manpage", "language", "languages", "lang", "update",
                "set", "unset", "vars"}


def _strip_global(args) -> list:
    """--lang X ve --lang=X'i çıkarır (geçmiş, o anki dille tekrar çalışsın)."""
    out, skip = [], False
    for a in args:
        if skip:
            skip = False
        elif a == "--lang":
            skip = True
        elif not a.startswith("--lang="):
            out.append(a)
    return out


def _recordable(args) -> bool:
    words = [a for a in args if not a.startswith("-")]
    return bool(words) and words[0] not in NOT_RECORDED and not {"-h", "--help"} & set(args)


ROOT_FLAGS = ("--json", "--md", "--latex", "--copy")


def _hoist_root_options(args) -> list:
    """--json, --md, --report X … komutun sonunda da yazılabilsin: kök seçeneği olarak başa alınır."""
    front, rest, i = [], [], 0
    while i < len(args):
        a = args[i]
        if a in ROOT_FLAGS or a.startswith("--report="):
            front.append(a)
        elif a == "--report" and i + 1 < len(args):
            front += args[i:i + 2]
            i += 1
        else:
            rest.append(a)
        i += 1
    return front + rest


def execute(args, record: bool = True) -> int:
    """Bir komut satırını çalıştırır: @değişkenleri açar, --json'u işler, geçmişe yazar.

    Hem normal çağrı hem `elektro shell` hem de `elektro history --run` bunu kullanır.
    """
    try:
        expanded = state.expand_vars(list(args))
    except KeyError as e:
        err_console.print(f"[bold red]{t('ui.error')}:[/] {t('vars.unknown', name=e.args[0])}")
        return 1
    if "--" in expanded:
        cut = expanded.index("--")
        head, tail = expanded[:cut], expanded[cut:]
    else:
        head, tail = expanded, []
    set_command(expanded)
    try:
        app(args=_hoist_root_options(head) + tail, prog_name="elektro")
        code = 0
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    finally:
        set_command(None)
    clean = _strip_global(args)
    if code == 0 and record and _recordable(clean):
        state.add_history(clean)
    return code


def run() -> None:
    """Konsol giriş noktası."""
    sys.exit(execute(sys.argv[1:]))


# --- değişkenler -----------------------------------------------------------------------------

@app.command("set", rich_help_panel=TOOLS, help=t("vars.set.help"))
def set_cmd(
    name: str = typer.Argument(..., help=t("vars.arg.name")),
    value: str = typer.Argument(..., help=t("vars.arg.value")),
    local: bool = typer.Option(False, "--local", help=t("vars.opt.local")),
):
    try:
        path = state.set_var(name, value, local)
    except ValueError as e:
        fail(str(e))
    console.print(f"[bold green]✓[/] @{name} = {value}  [dim]({path})[/]")


@app.command("unset", rich_help_panel=TOOLS, help=t("vars.unset.help"))
def unset_cmd(name: str = typer.Argument(..., help=t("vars.arg.name"))):
    if not state.unset_var(name):
        fail(t("vars.unknown", name=name))
    console.print(f"[bold green]✓[/] @{name} {t('vars.removed')}")


@app.command("vars", rich_help_panel=TOOLS, help=t("vars.help"))
def vars_cmd():
    global_vars, local_vars = state.load_vars()
    if json_mode():
        print_json({"global": global_vars, "local": local_vars})
        return
    if not global_vars and not local_vars:
        console.print(f"[dim]{t('vars.empty')}[/]")
        return
    tbl = Table(header_style="bold")
    tbl.add_column(t("vars.col.name"), style="cyan")
    tbl.add_column(t("vars.col.value"), style="bold green")
    tbl.add_column(t("vars.col.scope"), style="dim")
    for name, value in sorted(global_vars.items()):
        mark = f" [yellow]({t('vars.overridden')})[/]" if name in local_vars else ""
        tbl.add_row(f"@{name}", str(value), t("vars.global") + mark)
    for name, value in sorted(local_vars.items()):
        tbl.add_row(f"@{name}", str(value), t("vars.local"))
    console.print(tbl)
    local = state.local_file()
    console.print(f"[dim]{config_path()}" + (f"\n{local}" if local else "") + "[/]")


# --- geçmiş ------------------------------------------------------------------------------------

@app.command(rich_help_panel=TOOLS, help=t("hist.help"))
def history(
    count: int = typer.Option(20, "-n", help=t("hist.opt.n")),
    search: Optional[str] = typer.Option(None, "--search", "-s", help=t("hist.opt.search")),
    run_id: Optional[int] = typer.Option(None, "--run", "-r", help=t("hist.opt.run")),
    clear: bool = typer.Option(False, "--clear", help=t("hist.opt.clear")),
):
    if clear:
        state.clear_history()
        console.print(f"[bold green]✓[/] {t('hist.cleared')}")
        return
    entries = state.read_history()
    if run_id is not None:
        if not 1 <= run_id <= len(entries):
            fail(t("hist.bad_id", max=len(entries)))
        args = entries[run_id - 1]["args"]
        console.print(f"[dim]$ elektro {' '.join(shlex.quote(a) for a in args)}[/]")
        raise typer.Exit(execute(args, record=True))
    indexed = list(enumerate(entries, 1))
    if search:
        indexed = [(i, e) for i, e in indexed if search.lower() in " ".join(e["args"]).lower()]
    indexed = indexed[-count:]
    if json_mode():
        print_json([{"id": i, "time": e["time"], "args": e["args"]} for i, e in indexed])
        return
    if not indexed:
        console.print(f"[dim]{t('hist.empty')}[/]")
        return
    tbl = Table(box=None, header_style="bold")
    tbl.add_column("#", justify="right", style="dim")
    tbl.add_column(t("ds.col.date"), style="dim")
    tbl.add_column(t("hist.col.command"))
    for i, e in indexed:
        when = datetime.datetime.fromtimestamp(e["time"]).strftime("%m-%d %H:%M")
        tbl.add_row(str(i), when, "elektro " + " ".join(shlex.quote(a) for a in e["args"]))
    console.print(tbl)
    console.print(f"[dim]{t('hist.rerun')}[/]")


# --- etkileşimli kabuk (REPL) ----------------------------------------------------------------

def _command_words() -> dict:
    root = typer.main.get_command(app)
    words = {}
    for name, cmd in root.commands.items():
        if not cmd.hidden:
            words[name] = sorted(getattr(cmd, "commands", {}) or [])
    return words


def _setup_readline(words: dict):
    try:
        import readline
    except ImportError:
        return None
    hist = state.state_dir() / "shell_history"
    try:
        readline.read_history_file(hist)
    except OSError:
        pass
    readline.set_history_length(1000)

    def complete(text, index):
        line = readline.get_line_buffer().split()
        if not line or (len(line) == 1 and not readline.get_line_buffer().endswith(" ")):
            options = [w for w in list(words) + ["exit", "help", "clear"] if w.startswith(text)]
        else:
            options = [w for w in words.get(line[0], []) if w.startswith(text)]
        return options[index] + " " if index < len(options) else None

    readline.set_completer(complete)
    readline.set_completer_delims(" \t")
    readline.parse_and_bind("tab: complete")
    return readline, hist


@app.command(rich_help_panel=TOOLS, help=t("shell.help"))
def shell():
    rl = _setup_readline(_command_words())
    console.print(f"[bold yellow]⚡ ELEKTRO {__version__}[/] — {t('shell.welcome')}")
    while True:
        try:
            line = input("elektro> ").strip()
        except EOFError:
            console.print()
            break
        except KeyboardInterrupt:
            console.print()
            continue
        if not line:
            continue
        if line in ("exit", "quit", "q"):
            break
        if line in ("help", "?"):
            show_menu()
            continue
        if line == "clear":
            console.clear()
            continue
        try:
            args = shlex.split(line)
        except ValueError as e:
            err_console.print(f"[bold red]{t('ui.error')}:[/] {e}")
            continue
        if args and args[0] == "elektro":
            args = args[1:]
        if not args or args[0] == "shell":
            continue
        execute(args)
    if rl:
        readline, hist = rl
        try:
            hist.parent.mkdir(parents=True, exist_ok=True)
            readline.write_history_file(hist)
        except OSError:
            pass


# --- terminal arayüzü --------------------------------------------------------------------

@app.command(rich_help_panel=TOOLS, help=t("tui.help"))
def tui(file: Optional[Path] = typer.Argument(None, exists=True, dir_okay=False, help=t("tui.arg"))):
    try:
        from elektro.tui import run_app
    except ImportError:
        fail(t("tui.need_textual", pip=f"{sys.executable} -m pip install textual"))
    set_command(None)
    run_app(file)


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


# --- man sayfası ------------------------------------------------------------------------

def _roff(text: str) -> str:
    text = text.replace("\\", "\\e").replace("-", "\\-")
    return "\n".join(("\\&" + line) if line[:1] in (".", "'") else line for line in text.splitlines())


def render_manpage() -> str:
    root = typer.main.get_command(app)
    date = datetime.date.today().isoformat()
    out = [
        f'.TH ELEKTRO 1 "{date}" "elektro {__version__}" "{t("manual.title")}"',
        ".SH NAME",
        f"elektro \\- {_roff(t('cli.help'))}",
        ".SH SYNOPSIS",
        ".B elektro",
        "[\\fB\\-\\-lang\\fR \\fICODE\\fR] [\\fB\\-\\-json\\fR] \\fICOMMAND\\fR [\\fIOPTIONS\\fR]",
        ".SH DESCRIPTION",
        _roff(t("cli.help_long")),
        ".SH COMMANDS",
    ]
    for path, cmd in _walk(root, ["elektro"]):
        if path[-1] == "helpall":
            continue
        out.append(f".SS {_roff(' '.join(path))}")
        out += [".nf", _roff((cmd.help or "").split("\f")[0].strip()), ".fi"]
        for p in cmd.params:
            if p.name == "help":
                continue
            names, h = _param_line(p)
            out += [".TP", f"\\fB{_roff(names)}\\fR", _roff(h) or "\\&"]
    out += [".SH FILES", "~/.config/elektro/config.json, ~/.cache/elektro/datasheets/",
            ".SH SEE ALSO", REPO_URL]
    return "\n".join(out) + "\n"


@app.command(hidden=True)
def manpage():
    """Man sayfasını (roff) yazdırır: elektro manpage > elektro.1"""
    sys.stdout.write(render_manpage())


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


def _refresh_manpage() -> None:
    """Kurulu man sayfası varsa yeni sürümle yeniler."""
    base = os.environ.get("XDG_DATA_HOME") or os.path.join(os.path.expanduser("~"), ".local", "share")
    page = Path(base) / "man" / "man1" / "elektro.1"
    if page.exists():
        try:
            out = subprocess.run([sys.executable, "-m", "elektro", "manpage"], capture_output=True, text=True)
            if out.returncode == 0:
                page.write_text(out.stdout, encoding="utf-8")
        except OSError:
            pass


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
    pip = [sys.executable, "-m", "pip", "--disable-pip-version-check"]
    # 0.4 öncesi paket adı "elektro" idi; aynı dosyaları paylaştıkları için önce eskisi kaldırılır.
    try:
        from importlib.metadata import PackageNotFoundError, distribution
        distribution("elektro")
        subprocess.call(pip + ["uninstall", "--quiet", "--yes", "elektro"])
    except PackageNotFoundError:
        pass
    if subprocess.call(pip + ["install", "--quiet", "--upgrade", "--force-reinstall", TARBALL_URL]) != 0:
        fail(t("upd.failed"))
    _refresh_manpage()
    console.print(f"[bold green]✓ {t('upd.done', version=latest)}[/]")


if __name__ == "__main__":
    app()
