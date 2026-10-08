"""Terminal arayüzü (Textual): komut ağacı, otomatik form, çıktı paneli, devre tuvali, geçmiş.

Formlar komutların Click parametrelerinden üretilir; yeni bir komut eklendiğinde arayüzde
ayrıca bir şey yapmak gerekmez. Devre sekmesi ileride şema editörü + simülatör olacak.
"""

from __future__ import annotations

import contextlib
import datetime
import io
import shlex
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import typer
from rich.text import Text
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widget import Widget
from textual.widgets import (Button, Checkbox, Collapsible, DataTable, Footer, Header, Input, Label, RichLog, Select, Static,
                             TabbedContent, TabPane, Tree)

from elektro import __version__, cli, state, ui
from elektro.circuit.editor import CircuitEditor
from elektro.circuit.plotview import PlotView
from elektro.i18n import t

# Arayüzden çalıştırılmayan komutlar (etkileşimli, sayfalayıcı, kurulum…)
HIDDEN = {"tui", "shell", "helpall", "manpage", "update", "language", "languages", "lang", "history"}
BLOCKED = HIDDEN - {"history", "language"}


# --- Komut ağacı ve parametreler -------------------------------------------------------------

def command_groups() -> List[Tuple[str, List[Tuple[Tuple[str, ...], Any]]]]:
    """[(panel adı, [(yol, komut), …]), …] — menüdeki panel sırasıyla."""
    root = typer.main.get_command(cli.app)
    order = [cli.BASIC, cli.PASSIVE, cli.POWER, cli.INSTALL, cli.SIGNAL, cli.EMBEDDED, cli.TOOLS]
    groups: Dict[str, list] = {name: [] for name in order}
    for name, cmd in root.commands.items():
        panel = getattr(cmd, "rich_help_panel", None)
        if cmd.hidden or name in HIDDEN or not isinstance(panel, str):
            continue
        groups.setdefault(panel, []).append(((name,), cmd))
    return [(panel, items) for panel, items in groups.items() if items]


def find_command(path: Tuple[str, ...]) -> Optional[Any]:
    cmd = typer.main.get_command(cli.app)
    for part in path:
        cmd = getattr(cmd, "commands", {}).get(part)
        if cmd is None:
            return None
    return cmd


def summary(cmd: Any) -> str:
    return (cmd.help or "").split("\f")[0].strip().split("\n\n")[0].replace("\n", " ")


def form_params(cmd: Any) -> List[Any]:
    return [p for p in cmd.params if p.name != "help" and not getattr(p, "hidden", False)]


def _is_option(param) -> bool:
    # Typer yeni sürümlerde click'i kendi içinde taşır; sınıf yerine türe bakılır
    return param.param_type_name == "option"


def option_flag(param) -> str:
    """En açıklayıcı seçenek adı: --current, yoksa -i."""
    longs = [o for o in param.opts if o.startswith("--")]
    return longs[0] if longs else param.opts[0]


def build_args(path: Tuple[str, ...], values: List[Tuple[Any, object]]) -> List[str]:
    """Form değerlerinden komut satırı argümanları."""
    args, positional = list(path), []
    for param, value in values:
        if _is_option(param):
            if param.is_flag:
                if value:
                    args.append(option_flag(param))
                continue
            text = str(value or "").strip()
            if not text:
                continue
            if param.multiple:
                for item in shlex.split(text):
                    args += [option_flag(param), item]
            else:
                args += [option_flag(param), text]
        else:
            text = str(value or "").strip()
            if text:
                positional += shlex.split(text) if param.nargs != 1 else [text]
    if any(a.startswith("-") for a in positional):      # negatif sayılar seçenek sanılmasın
        positional = ["--", *positional]
    return args + positional


def run_captured(args: List[str], width: int) -> Tuple[int, str]:
    """Komutu çalıştırır, tüm çıktısını (renkli ANSI) metin olarak döndürür."""
    buf = io.StringIO()
    with ui.capture(buf, width), contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        old_stdin = sys.stdin
        sys.stdin = io.StringIO("")              # sihirbaz soruları beklemesin
        try:
            code = cli.execute(args)
        except Exception as e:                   # arayüz hiçbir hatada kapanmasın
            buf.write(f"{type(e).__name__}: {e}\n")
            code = 1
        finally:
            sys.stdin = old_stdin
    return code, buf.getvalue()


# --- Uygulama ---------------------------------------------------------------------------------

class ElektroApp(App):
    TITLE = f"⚡ ELEKTRO {__version__}"
    CSS = """
    #sidebar { width: 32; border-right: tall $panel; }
    #search { margin: 0 0 0 0; }
    #commands { height: 1fr; }
    #main { width: 1fr; }
    #form { height: 1fr; padding: 0 1; }
    #help { color: $text-muted; }
    #form Collapsible { margin: 0 0 1 0; }
    #cmdtitle { text-style: bold; color: $accent; padding: 0 1; }
    .field { height: auto; }
    .field Label { width: 20; padding: 1 1 0 0; text-align: right; color: $secondary; }
    .field Input, .field Select { width: 1fr; }
    .field Checkbox { width: 1fr; }
    #cmdbar { height: 3; padding: 0 1; }
    #cmdline { width: 1fr; }
    #run { min-width: 14; }
    #output { height: 1fr; border: round $primary; margin: 0 1; }
    #circuit-keys { padding: 0 1; color: $text-muted; height: auto; }
    #editor { width: 1fr; height: 1fr; border: round $primary; }
    #editor:focus { border: round $accent; }
    #circuit-side { width: 46; height: 1fr; padding: 0 1; border-left: tall $panel; }
    #circuit-top { height: 1fr; }
    #plot { height: 40%; border: round $primary; }
    #plot:focus { border: round $accent; }
    #plot.big { height: 70%; }
    #plot.hidden { display: none; }
    #history-table { height: 1fr; }
    """
    BINDINGS = [
        Binding("ctrl+r", "run", t("tui.key.run")),
        Binding("ctrl+l", "clear", t("tui.key.clear")),
        Binding("f2", "show_tab('calc')", t("tui.tab.calc")),
        Binding("f3", "show_tab('circuit')", t("tui.tab.circuit")),
        Binding("f4", "show_tab('history')", t("tui.tab.history")),
        Binding("f6", "plot_size", t("plot.key.size")),
        Binding("ctrl+f", "focus_search", t("tui.key.search")),
        Binding("ctrl+q", "quit", t("tui.key.quit")),
    ]

    def __init__(self, circuit_path: Optional[Path] = None) -> None:
        super().__init__()
        self.circuit_path = circuit_path
        self.path: Optional[Tuple[str, ...]] = None
        self.fields: List[Tuple[Any, Widget]] = []
        self._building = False

    # --- düzen ---
    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(initial="calc"):
            with TabPane(t("tui.tab.calc"), id="calc"):
                with Horizontal():
                    with Vertical(id="sidebar"):
                        yield Input(placeholder=t("tui.search"), id="search")
                        yield Tree(t("tui.commands"), id="commands")
                    with Vertical(id="main"):
                        yield Static(t("tui.pick"), id="cmdtitle")
                        yield VerticalScroll(id="form")
                        with Horizontal(id="cmdbar"):
                            yield Input(placeholder=t("tui.cmdline"), id="cmdline")
                            yield Button(t("tui.run"), id="run", variant="success")
                        yield RichLog(id="output", wrap=True, markup=False, highlight=False)
            with TabPane(t("tui.tab.circuit"), id="circuit"):
                yield Static(t("tui.circuit.keys"), id="circuit-keys")
                with Horizontal(id="circuit-top"):
                    yield CircuitEditor(self.circuit_path, id="editor")
                    with VerticalScroll(id="circuit-side"):
                        yield Static(id="circuit-info")
                yield PlotView(id="plot")
            with TabPane(t("tui.tab.history"), id="history"):
                yield Static(t("tui.hist.hint"), id="history-hint")
                yield DataTable(id="history-table", cursor_type="row", zebra_stripes=True)
        yield Footer()

    def on_mount(self) -> None:
        self.sub_title = t("cli.help")
        self.fill_tree("")
        table = self.query_one("#history-table", DataTable)
        table.add_columns("#", t("tui.col.time"), t("tui.col.command"))
        self.query_one("#output", RichLog).write(Text(t("tui.welcome"), style="dim"))
        self._circuit_changed()
        self.query_one("#circuit-side").can_focus = False      # Tab editörden doğrudan grafiğe geçsin
        if self.circuit_path is not None:
            self.action_show_tab("circuit")
        else:
            self.query_one("#commands", Tree).focus()

    # --- komut ağacı ---
    def fill_tree(self, query: str) -> None:
        tree = self.query_one("#commands", Tree)
        tree.clear()
        tree.root.expand()
        q = query.strip().lower()

        def match(name: str, cmd: Any) -> bool:
            return not q or q in name.lower() or q in summary(cmd).lower()

        for panel, items in command_groups():
            node = None
            for (name,), cmd in items:
                subs = getattr(cmd, "commands", None)
                if subs:
                    hits = [(s, c) for s, c in subs.items() if not c.hidden and (match(name, cmd) or match(s, c))]
                    if not hits:
                        continue
                    node = node or tree.root.add(panel, expand=bool(q))
                    group = node.add(name, expand=bool(q))
                    for sub, sub_cmd in hits:
                        group.add_leaf(sub, data=(name, sub))
                elif match(name, cmd):
                    node = node or tree.root.add(panel, expand=bool(q))
                    node.add_leaf(name, data=(name,))
        if not q:
            for child in tree.root.children[:1]:
                child.expand()

    @on(Input.Changed, "#search")
    def _search(self, event: Input.Changed) -> None:
        self.fill_tree(event.value)

    @on(Input.Submitted, "#search")
    def _search_done(self) -> None:
        self.query_one("#commands", Tree).focus()

    @on(Tree.NodeSelected, "#commands")
    def _select(self, event: Tree.NodeSelected) -> None:
        if event.node.data:
            self.load_command(tuple(event.node.data))

    # --- form ---
    def load_command(self, path: Tuple[str, ...]) -> None:
        cmd = find_command(path)
        if cmd is None:
            return
        self.path = path
        self.query_one("#cmdtitle", Static).update(f"elektro {' '.join(path)} — {summary(cmd)}")
        form = self.query_one("#form", VerticalScroll)
        form.remove_children()
        self.fields = []
        self._building = True
        widgets: List[Widget] = [Collapsible(Static(Text((cmd.help or "").split("\f")[0].strip()), id="help"),
                                             title=t("tui.help_examples"), collapsed=True)]
        for i, param in enumerate(form_params(cmd)):
            label, widget = self._field(param, i)
            self.fields.append((param, widget))
            widgets.append(Horizontal(Label(label), widget, classes="field"))
        form.mount_all(widgets)
        form.scroll_home(animate=False)
        self._building = False
        self.update_cmdline()

    def _field(self, param: Any, index: int) -> Tuple[str, Widget]:
        help_text = getattr(param, "help", "") or ""
        wid = f"param-{index}"
        if _is_option(param):
            label = option_flag(param) + (" *" if param.required else "")
            if param.is_flag:
                return label, Checkbox(help_text, value=bool(param.default), id=wid)
        else:
            label = (param.metavar or param.name or "").split("|")[0].upper() + (" *" if param.required else "")
        if getattr(param.type, 'choices', None):
            options = [(c, c) for c in param.type.choices]
            return label, Select(options, allow_blank=not param.required, id=wid)
        default = param.default if param.default not in (None, (), []) and not callable(param.default) else None
        placeholder = help_text + (f"  [{default}]" if default is not None and not isinstance(default, bool) else "")
        widget = Input(placeholder=placeholder, id=wid)
        widget.tooltip = help_text or None
        return label, widget

    def form_values(self) -> List[Tuple[Any, object]]:
        out = []
        for param, widget in self.fields:
            value = widget.value
            if isinstance(widget, Select) and value == Select.BLANK:
                value = None
            out.append((param, value))
        return out

    def update_cmdline(self) -> None:
        if self.path is None:
            return
        args = build_args(self.path, self.form_values())
        self.query_one("#cmdline", Input).value = "elektro " + " ".join(shlex.quote(a) for a in args)

    @on(Input.Changed, "#form Input")
    @on(Checkbox.Changed, "#form Checkbox")
    @on(Select.Changed, "#form Select")
    def _form_changed(self) -> None:
        if not self._building:
            self.update_cmdline()

    @on(Input.Submitted, "#form Input")
    @on(Input.Submitted, "#cmdline")
    @on(Button.Pressed, "#run")
    def _submit(self) -> None:
        self.action_run()

    # --- çalıştırma ---
    def action_run(self) -> None:
        line = self.query_one("#cmdline", Input).value.strip()
        try:
            args = shlex.split(line)
        except ValueError as e:
            self._write_error(str(e))
            return
        if args and args[0] == "elektro":
            args = args[1:]
        if not args:
            return
        if args[0] in BLOCKED:
            self._write_error(t("tui.blocked", cmd=args[0]))
            return
        log = self.query_one("#output", RichLog)
        log.write(Text(f"$ elektro {' '.join(shlex.quote(a) for a in args)}", style="bold cyan"))
        self._run_worker(args, max(60, log.size.width - 4))

    @work(thread=True, exclusive=True, group="run")
    def _run_worker(self, args: List[str], width: int) -> None:
        code, output = run_captured(args, width)
        self.call_from_thread(self._show_output, code, output)

    def _show_output(self, code: int, output: str) -> None:
        log = self.query_one("#output", RichLog)
        if output.strip():
            log.write(Text.from_ansi(output.rstrip("\n"), no_wrap=True))
        if code:
            log.write(Text(f"✗ exit {code}", style="bold red"))
        log.write(Text(""))

    def _write_error(self, message: str) -> None:
        self.query_one("#output", RichLog).write(Text(f"{t('ui.error')}: {message}", style="bold red"))

    def action_clear(self) -> None:
        self.query_one("#output", RichLog).clear()

    def action_focus_search(self) -> None:
        self.action_show_tab("calc")
        self.query_one("#search", Input).focus()

    def action_show_tab(self, tab: str) -> None:
        self.query_one(TabbedContent).active = tab

    # --- devre tuvali ---
    @on(CircuitEditor.Changed)
    def _circuit_changed(self) -> None:
        self.query_one("#circuit-info", Static).update(self.query_one("#editor", CircuitEditor).info())

    @on(CircuitEditor.SweepStarted)
    def _sweep_started(self) -> None:
        plot_view = self.query_one("#plot", PlotView)
        plot_view.busy = True
        plot_view.refresh()

    @on(CircuitEditor.SweepReady)
    def _sweep_ready(self, event: CircuitEditor.SweepReady) -> None:
        plot_view = self.query_one("#plot", PlotView)
        plot_view.busy = False
        if event.sweep is not None:
            plot_view.show(event.sweep, event.traces, event.title)
        else:
            plot_view.show_message(event.error or t("plot.hint"))

    @on(PlotView.CursorMoved)
    def _plot_cursor(self, event: PlotView.CursorMoved) -> None:
        self.query_one("#editor", CircuitEditor).set_plot_cursor(event.index)

    def action_plot_size(self) -> None:
        """Grafik paneli: normal → büyük → gizli → normal."""
        plot_view = self.query_one("#plot", PlotView)
        if plot_view.has_class("hidden"):
            plot_view.remove_class("hidden")
        elif plot_view.has_class("big"):
            plot_view.remove_class("big")
            plot_view.add_class("hidden")
        else:
            plot_view.add_class("big")

    # --- geçmiş ---
    @on(TabbedContent.TabActivated)
    def _tab(self, event: TabbedContent.TabActivated) -> None:
        pane = event.pane.id if event.pane is not None else None
        if pane == "history":
            self.fill_history()
            self.query_one("#history-table", DataTable).focus()
        elif pane == "circuit":
            self.query_one("#editor", CircuitEditor).focus()

    def fill_history(self) -> None:
        table = self.query_one("#history-table", DataTable)
        table.clear()
        entries = list(enumerate(state.read_history(), 1))
        for i, e in reversed(entries[-200:]):
            when = datetime.datetime.fromtimestamp(e["time"]).strftime("%m-%d %H:%M")
            table.add_row(str(i), when, "elektro " + " ".join(shlex.quote(a) for a in e["args"]),
                          key=" ".join(shlex.quote(a) for a in e["args"]))

    @on(DataTable.RowSelected, "#history-table")
    def _history_pick(self, event: DataTable.RowSelected) -> None:
        self.action_show_tab("calc")
        cmdline = self.query_one("#cmdline", Input)
        cmdline.value = "elektro " + str(event.row_key.value)
        cmdline.focus()


def run_app(circuit_path: Optional[Path] = None) -> None:
    ElektroApp(circuit_path).run()
