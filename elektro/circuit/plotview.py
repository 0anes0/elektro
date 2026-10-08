"""Grafik paneli (Textual) ve analiz ayar penceresi."""

from __future__ import annotations

from typing import List, Optional

from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Button, Input, Label, Select

from elektro.circuit import plot
from elektro.circuit.model import CircuitError, spice_number
from elektro.circuit.sources import Analysis, parse_directive
from elektro.i18n import t


class PlotView(Widget, can_focus=True):
    """Analiz sonucunu çizer. ←/→ imleci gezdirir, m AC'de genlik/faz değiştirir."""

    BINDINGS = [
        Binding("left", "cursor(-1)", show=False), Binding("right", "cursor(1)", show=False),
        Binding("shift+left", "cursor(-10)", show=False), Binding("shift+right", "cursor(10)", show=False),
        Binding("home", "cursor_to(0)", show=False), Binding("end", "cursor_to(-1)", show=False),
        Binding("m", "toggle_mode", t("plot.key.mode")),
    ]

    class CursorMoved(Message):
        """Grafik imleci değişti: şemadaki değerler ve probe tablosu o ana göre yenilensin."""

        def __init__(self, index: Optional[int]) -> None:
            super().__init__()
            self.index = index

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.sweep = None
        self.traces: List = []
        self.mode = "mag"
        self.cursor: Optional[int] = None
        self.title = ""
        self.message = t("plot.hint")
        self.busy = False

    def show(self, sweep, traces, title: str) -> None:
        same_axis = self.sweep is not None and sweep is not None and self.sweep.kind == sweep.kind
        self.sweep, self.traces, self.title = sweep, traces, title
        if sweep is None or not same_axis or self.cursor is None or self.cursor >= len(sweep.x):
            self.cursor = len(sweep.x) // 2 if sweep else None
        self.message = ""
        self.refresh()
        self.post_message(self.CursorMoved(self.cursor))

    def show_message(self, text: str) -> None:
        self.sweep, self.traces, self.message = None, [], text
        self.refresh()
        self.post_message(self.CursorMoved(None))

    def render(self) -> Text:
        w, h = max(self.size.width, 30), max(self.size.height, 6)
        if self.sweep is None:
            return Text("\n" + self.message, style="dim")
        series = plot.series_from(self.traces, self.mode)
        errors = [tr for tr in self.traces if tr.error]
        title = self.title + ("  …" if self.busy else "")
        lines = plot.render(series, self.sweep.x, w, h - (1 if errors else 0), log_x=self.sweep.kind == "ac",
                            x_unit=self.sweep.x_unit, cursor=self.cursor, title=title)
        if errors:
            lines.append(Text("  ".join(f"{tr.expr}: {tr.error}" for tr in errors), style="red"))
        return Text("\n").join(lines)

    def action_cursor(self, step: int) -> None:
        if self.sweep is None:
            return
        n = len(self.sweep.x)
        # bir adım ≈ bir sütun genişliği
        stride = max(n // max((self.size.width - plot.LEFT - plot.RIGHT) * 2, 1), 1)
        self.cursor = min(max((self.cursor or 0) + step * stride, 0), n - 1)
        self.refresh()
        self.post_message(self.CursorMoved(self.cursor))

    def action_cursor_to(self, k: int) -> None:
        if self.sweep is not None:
            self.cursor = k % len(self.sweep.x)
            self.refresh()
            self.post_message(self.CursorMoved(self.cursor))

    def action_toggle_mode(self) -> None:
        self.mode = "phase" if self.mode == "mag" else "mag"
        self.refresh()


KINDS = ("op", "tran", "ac", "dc")


class AnalysisDialog(ModalScreen):
    """Analiz ayarı: üstte LTspice komut satırı, altında form; biri değişince diğeri güncellenir."""

    BINDINGS = [Binding("escape", "cancel", show=False)]
    DEFAULT_CSS = """
    AnalysisDialog { align: center middle; }
    AnalysisDialog > Vertical { width: 76; height: auto; border: round $accent; background: $panel; padding: 1 2; }
    AnalysisDialog .row { height: auto; }
    AnalysisDialog .row Label { width: 22; padding: 1 1 0 0; text-align: right; color: $secondary; }
    AnalysisDialog .row Input, AnalysisDialog .row Select { width: 1fr; }
    AnalysisDialog #an-error { color: $error; height: auto; margin: 1 0 0 0; }
    AnalysisDialog #an-buttons { height: auto; align: right middle; margin: 1 0 0 0; }
    AnalysisDialog .hidden { display: none; }
    """

    def __init__(self, directive: str, sources: List[str]) -> None:
        super().__init__()
        self.directive = directive or ".op"
        self.sources = sources
        self._sync = False

    def compose(self) -> ComposeResult:
        try:
            an = parse_directive(self.directive)
        except CircuitError:
            an = Analysis()
        src_options = [(s, s) for s in self.sources] or [("-", "-")]
        with Vertical():
            yield Label(t("an.title"))
            yield Input(self.directive, id="an-directive", placeholder=".tran 10m")
            yield self._row(t("an.kind"), Select([(t(f"an.kind.{k}"), k) for k in KINDS], value=an.kind,
                                                 allow_blank=False, id="an-kind"))
            yield self._row(t("an.tstop"), Input(_n(an.tstop, "10m"), id="an-tstop"), "tran")
            yield self._row(t("an.tstep"), Input(_n(an.tstep, ""), id="an-tstep", placeholder=t("an.auto")), "tran")
            yield self._row(t("an.sweep"), Select([("dec", "dec"), ("oct", "oct"), ("lin", "lin")], value=an.sweep,
                                                  allow_blank=False, id="an-sweep"), "ac")
            yield self._row(t("an.points"), Input(str(an.points), id="an-points"), "ac")
            yield self._row(t("an.fstart"), Input(_n(an.fstart, "10"), id="an-fstart"), "ac")
            yield self._row(t("an.fstop"), Input(_n(an.fstop, "100k"), id="an-fstop"), "ac")
            yield self._row(t("an.source"), Select(src_options, value=an.source if an.source in self.sources
                                                   else src_options[0][1], allow_blank=False, id="an-source"), "dc")
            yield self._row(t("an.start"), Input(_n(an.start, "0"), id="an-start"), "dc")
            yield self._row(t("an.stop"), Input(_n(an.stop, "5"), id="an-stop"), "dc")
            yield self._row(t("an.step"), Input(_n(an.step, "0.1"), id="an-step"), "dc")
            yield Label("", id="an-error")
            with Horizontal(id="an-buttons"):
                yield Button(t("an.ok"), id="an-ok", variant="success")
                yield Button(t("an.cancel"), id="an-cancel")

    @staticmethod
    def _row(label: str, widget, group: str = "") -> Horizontal:
        return Horizontal(Label(label), widget, classes=f"row {('group-' + group) if group else ''}")

    def on_mount(self) -> None:
        self._show_groups()
        self.query_one("#an-directive", Input).focus()

    def _show_groups(self) -> None:
        kind = self.query_one("#an-kind", Select).value
        for g in ("tran", "ac", "dc"):
            for row in self.query(f".group-{g}"):
                row.set_class(g != kind, "hidden")

    def _value(self, wid: str) -> str:
        return str(self.query_one(f"#{wid}").value).strip()

    def _form_directive(self) -> str:
        kind = self._value("an-kind")
        if kind == "tran":
            step = self._value("an-tstep")
            return f".tran {step} {self._value('an-tstop')}" if step else f".tran {self._value('an-tstop')}"
        if kind == "ac":
            return (f".ac {self._value('an-sweep')} {self._value('an-points')} {self._value('an-fstart')} "
                    f"{self._value('an-fstop')}")
        if kind == "dc":
            return (f".dc {self._value('an-source')} {self._value('an-start')} {self._value('an-stop')} "
                    f"{self._value('an-step')}")
        return ".op"

    def on_input_changed(self, event: Input.Changed) -> None:
        if self._sync:
            return
        if event.input.id == "an-directive":
            try:
                an = parse_directive(event.value)
            except CircuitError as e:
                self.query_one("#an-error", Label).update(str(e))
                return
            self.query_one("#an-error", Label).update("")
            self._sync = True
            try:
                self.query_one("#an-kind", Select).value = an.kind
                if an.kind == "tran":
                    self.query_one("#an-tstop", Input).value = _n(an.tstop, "")
                    self.query_one("#an-tstep", Input).value = _n(an.tstep, "")
                elif an.kind == "ac":
                    self.query_one("#an-sweep", Select).value = an.sweep
                    self.query_one("#an-points", Input).value = str(an.points)
                    self.query_one("#an-fstart", Input).value = _n(an.fstart, "")
                    self.query_one("#an-fstop", Input).value = _n(an.fstop, "")
                elif an.kind == "dc":
                    if an.source in self.sources:
                        self.query_one("#an-source", Select).value = an.source
                    self.query_one("#an-start", Input).value = _n(an.start, "0")
                    self.query_one("#an-stop", Input).value = _n(an.stop, "")
                    self.query_one("#an-step", Input).value = _n(an.step, "")
            finally:
                self._sync = False
            self._show_groups()
        else:
            self._from_form()

    def on_select_changed(self, event: Select.Changed) -> None:
        self._show_groups()
        if not self._sync:
            self._from_form()

    def _from_form(self) -> None:
        text = self._form_directive()
        self._sync = True
        try:
            self.query_one("#an-directive", Input).value = text
        finally:
            self._sync = False
        try:
            parse_directive(text)
            self.query_one("#an-error", Label).update("")
        except CircuitError as e:
            self.query_one("#an-error", Label).update(str(e))

    def _submit(self) -> None:
        text = self._value("an-directive")
        try:
            an = parse_directive(text)
        except CircuitError as e:
            self.query_one("#an-error", Label).update(str(e))
            return
        if an.kind == "dc" and an.source not in self.sources:
            self.query_one("#an-error", Label).update(t("an.no_source", ref=an.source))
            return
        self.dismiss(an.directive())

    def on_input_submitted(self) -> None:
        self._submit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "an-ok":
            self._submit()
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)


def _n(value: float, default: str) -> str:
    return spice_number(value) if value else default
