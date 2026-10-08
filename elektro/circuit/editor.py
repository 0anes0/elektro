"""Klavyeyle şema editörü (Textual widget'ı) ve değer/dosya pencereleri."""

from __future__ import annotations

import copy
import math
from pathlib import Path
from typing import List, Optional

from rich.console import Group
from rich.table import Table
from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Input, Label

from elektro.circuit import render as rnd
from elektro.circuit.plotview import AnalysisDialog
from elektro.circuit import probes as prb
from elektro.circuit.model import KINDS, Circuit, CircuitError, Point, addr, parse_addr, valid_value
from elektro.circuit.solver import OpResult, dc_operating_point, run_analysis
from elektro.i18n import t
from elektro.units import format_si

DEFAULT_ROT = {"R": 0, "L": 0, "C": 90, "V": 90, "I": 90, "GND": 0, "N": 0, "D": 90, "Q": 0, "M": 0, "U": 0}
UNDO_LIMIT = 200


class PromptDialog(ModalScreen):
    """Tek satırlık giriş penceresi: Enter onaylar, Esc vazgeçer."""

    BINDINGS = [Binding("escape", "cancel", show=False)]
    DEFAULT_CSS = """
    PromptDialog { align: center middle; }
    PromptDialog > Vertical { width: 60; height: auto; border: round $accent; background: $panel; padding: 1 2; }
    PromptDialog Label { margin: 0 0 1 0; }
    PromptDialog #prompt-error { color: $error; margin: 1 0 0 0; height: auto; }
    """

    def __init__(self, title: str, value: str = "", validate=None) -> None:
        super().__init__()
        self.title_text, self.value, self.validate = title, value, validate

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(self.title_text)
            yield Input(value=self.value, id="prompt-input")
            yield Label("", id="prompt-error")

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        value = event.value.strip()
        error = self.validate(value) if self.validate else None
        if error:
            self.query_one("#prompt-error", Label).update(error)
            return
        self.dismiss(value)

    def action_cancel(self) -> None:
        self.dismiss(None)


class ExampleDialog(ModalScreen):
    """Hazır örnekler: kategorilere ayrılmış liste; Enter açar, Esc vazgeçer."""

    BINDINGS = [Binding("escape", "cancel", show=False)]
    DEFAULT_CSS = """
    ExampleDialog { align: center middle; }
    ExampleDialog > Vertical { width: 64; height: auto; max-height: 90%; border: round $accent;
                               background: $panel; padding: 1 2; }
    ExampleDialog OptionList { height: auto; max-height: 30; }
    """

    def compose(self) -> ComposeResult:
        from textual.widgets import OptionList
        from textual.widgets.option_list import Option
        from elektro.circuit import examples
        items = []
        for cat in examples.CATEGORIES:
            items.append(Option(Text(t(f"ex.cat.{cat}"), style="bold yellow"), disabled=True))
            for name, (c, _) in examples.EXAMPLES.items():
                if c == cat:
                    items.append(Option(f"  {t(f'ex.{name}')}", id=name))
        with Vertical():
            yield Label(t("ex.title"))
            yield OptionList(*items, id="examples")

    def on_mount(self) -> None:
        options = self.query_one("#examples")
        options.focus()
        options.highlighted = 1

    def on_option_list_option_selected(self, event) -> None:
        self.dismiss(event.option.id)

    def action_cancel(self) -> None:
        self.dismiss(None)


class CircuitEditor(Widget, can_focus=True):
    """Izgara üzerinde bileşen yerleştirme, kablolama ve DC çözüm."""

    BINDINGS = [
        Binding("up", "move(0, -1)", show=False), Binding("down", "move(0, 1)", show=False),
        Binding("left", "move(-1, 0)", show=False), Binding("right", "move(1, 0)", show=False),
        Binding("shift+up", "move(0, -4)", show=False), Binding("shift+down", "move(0, 4)", show=False),
        Binding("shift+left", "move(-4, 0)", show=False), Binding("shift+right", "move(4, 0)", show=False),
        Binding("r", "place('R')", show=False), Binding("c", "place('C')", show=False),
        Binding("l", "place('L')", show=False), Binding("v", "place('V')", show=False),
        Binding("i", "place('I')", show=False), Binding("g", "place('GND')", show=False),
        Binding("d", "place('D')", show=False), Binding("q", "place('Q')", show=False),
        Binding("f", "place('M')", show=False), Binding("u", "place('U')", show=False),
        Binding("n", "label", show=False),
        Binding("w", "wire", t("ckt.key.wire")),
        Binding("enter", "enter", show=False),
        Binding("e", "edit", show=False),
        Binding("ctrl+r", "rotate", t("ckt.key.rotate")),
        Binding("m", "grab", show=False),
        Binding("x,delete", "delete", show=False),
        Binding("escape", "cancel", show=False),
        Binding("ctrl+z", "undo", t("ckt.key.undo")),
        Binding("f5", "simulate", t("ckt.key.simulate")),
        Binding("ctrl+s", "save", t("ckt.key.save")),
        Binding("ctrl+o", "open", t("ckt.key.open")),
        Binding("ctrl+n", "new", show=False),
        Binding("p", "probe", t("ckt.key.probe")),
        Binding("a", "two_point('I')", show=False),
        Binding("o", "two_point('R')", show=False),
        Binding("P", "probe_prompt", show=False),
        Binding("s", "analysis", t("ckt.key.analysis")),
        Binding("ctrl+e", "examples", t("ckt.key.examples")),
    ]

    class Changed(Message):
        """Durum değişti: yan panel yenilensin."""

    class SweepStarted(Message):
        """Arka planda bir analiz başladı."""

    class SweepReady(Message):
        """Analiz bitti (ya da analiz yok): grafik paneli yenilensin."""

        def __init__(self, sweep, traces, error: Optional[str], title: str) -> None:
            super().__init__()
            self.sweep, self.traces, self.error, self.title = sweep, traces, error, title

    def __init__(self, path: Optional[Path] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.circuit = Circuit()
        self.cursor: Point = (2, 2)
        self.ox = self.oy = 0
        self.mode = "normal"                 # normal | wire | move | probe
        self.wire_start: Optional[Point] = None
        self.probe_start: Optional[Point] = None
        self.probe_func = "I"                # iki noktalı probe: I (akım) veya R (eşdeğer direnç)
        self.grab: Optional[tuple] = None    # (bileşen, eski x, eski y, dx, dy)
        self.undo_stack: List[Circuit] = []
        self.path: Optional[Path] = None
        self.dirty = False
        self.live = False                    # F5'ten sonra her değişiklikte yeniden çöz
        self.result: Optional[OpResult] = None
        self.error: Optional[str] = None
        self.message: str = ""
        self.sweep = None                    # son analiz sonucu (tran/ac/dc)
        self.traces: List = []               # o analizdeki probe eğrileri
        self.plot_cursor: Optional[int] = None   # grafik imlecinin örnek numarası
        self.sweep_error: Optional[str] = None
        self.busy = False
        self._generation = 0                 # eski arka plan sonuçlarını yok saymak için
        if path is not None:
            self.load(Path(path))

    # --- çizim ---
    def render(self) -> Text:
        self._scroll_to_cursor()
        preview = []
        if self.mode == "wire" and self.wire_start and self.wire_start != self.cursor:
            tmp = Circuit()
            tmp.add_wire(self.wire_start, self.cursor)
            preview = tmp.wires
        under = self.circuit.component_at(self.cursor)
        points, parts = self._probe_marks()
        view = rnd.View(self.ox, self.oy, max(self.size.width, 1), max(self.size.height, 1), self.cursor,
                        under.ref if under and under.kind != "GND" else None, preview,
                        self._label_voltages(),
                        points, parts, {self.probe_start} if self.probe_start else set())
        return Text("\n").join(rnd.render(self.circuit, view))

    def _probe_marks(self):
        """Şemada işaretlenecek probe noktaları (◉) ve akım probe'lu bileşenler."""
        points, parts = set(), set()
        for expr in self.circuit.probes:
            m = prb.PROBE_RE.match(expr)
            if not m:
                continue
            func, a, b = m.group(1).upper(), m.group(2).upper(), m.group(3)
            if func == "V" or b:
                for name in (a, b or ""):
                    labels = [c.pins()[0] for c in self.circuit.components
                              if c.kind == "N" and c.value.upper() == name.upper()]
                    pt = parse_addr(name)
                    points |= set(labels) if labels else ({pt} if pt is not None else set())
            else:
                parts.add(a.split(".")[0])
        return points, {c.ref for c in self.circuit.components if c.ref.upper() in parts}

    def _at_cursor(self):
        """Grafik imlecindeki sonuç (OpResult) — analiz yoksa None."""
        if self.sweep is None or self.plot_cursor is None or not 0 <= self.plot_cursor < len(self.sweep.x):
            return None
        return self.sweep.point(self.plot_cursor)

    def _label_voltages(self) -> dict:
        """Şemadaki düğüm etiketleri: analiz varsa grafik imlecindeki değer (AC'de genlik), yoksa DC."""
        point = self._at_cursor()
        if point is not None:
            out = {}
            for n, v in point.voltages.items():
                v = abs(v) if isinstance(v, complex) else v
                peak = max((abs(x) for x in self.sweep.voltages.get(n, [])), default=0.0)
                out[n] = 0.0 if abs(v) < peak * 1e-9 else v           # sayısal artık
            return out
        return self.result.voltages if self.result and not self.error else {}

    def set_plot_cursor(self, index: Optional[int]) -> None:
        self.plot_cursor = index
        self.refresh()
        self.post_message(self.Changed())

    def _scroll_to_cursor(self) -> None:
        view = rnd.View(self.ox, self.oy, max(self.size.width, 1), max(self.size.height, 1))
        cols, rows = view.cols(), view.rows()
        x, y = self.cursor
        if x < self.ox:
            self.ox = x
        elif x > self.ox + cols - 1:
            self.ox = x - cols + 1
        if y < self.oy:
            self.oy = y
        elif y > self.oy + rows - 1:
            self.oy = y - rows + 1

    def add_probe(self, expr: str) -> None:
        expr = prb.normalize(expr)
        self.snapshot()
        if expr in self.circuit.probes:
            self.circuit.probes.remove(expr)
            self.say(t("ckt.msg.probe_removed", expr=expr))
        else:
            self.circuit.probes.append(expr)
            self.say(t("ckt.msg.probe_added", expr=expr))
            self.live = True                   # probe koymak simülasyonu da başlatır
        self.changed(edited=True)

    def changed(self, edited: bool = False) -> None:
        if edited:
            self.dirty = True
            if self.live:
                self.run_simulation(quiet=True)
        self.refresh()
        self.post_message(self.Changed())

    # --- düzenleme yardımcıları ---
    def snapshot(self) -> None:
        self.undo_stack.append(copy.deepcopy(self.circuit))
        del self.undo_stack[:-UNDO_LIMIT]

    def say(self, text: str) -> None:
        self.message = text

    # --- eylemler ---
    def action_move(self, dx: int, dy: int) -> None:
        x, y = self.cursor
        self.cursor = (max(x + dx, 0), max(y + dy, 0))
        if self.mode == "move" and self.grab:
            comp, _, _, gx, gy = self.grab
            comp.x, comp.y = self.cursor[0] - gx, self.cursor[1] - gy
            self.changed(edited=True)
            return
        self.changed()

    def action_place(self, kind: str) -> None:
        if self.mode != "normal":
            return
        self.snapshot()
        comp = self.circuit.add(kind, *self.cursor, rot=DEFAULT_ROT[kind])
        self.say(t("ckt.msg.placed", ref=comp.ref))
        self.changed(edited=True)

    def action_label(self) -> None:
        """Düğüm etiketi: imleçteki noktaya ad ver (aynı adlı noktalar birbirine bağlıdır)."""
        if self.mode != "normal":
            return

        def validate(value: str) -> Optional[str]:
            return None if valid_value("N", value) else t("ckt.bad_label", name=value)

        def done(value: Optional[str]) -> None:
            if value:
                self.snapshot()
                self.circuit.add("N", *self.cursor, value=value)
                self.say(t("ckt.msg.label", name=value))
                self.changed(edited=True)

        self.app.push_screen(PromptDialog(t("ckt.prompt.label"), "", validate), done)

    def action_wire(self) -> None:
        if self.mode == "wire":
            self.action_enter()
            return
        if self.mode != "normal":
            return
        self.mode, self.wire_start = "wire", self.cursor
        self.say(t("ckt.msg.wire"))
        self.changed()

    def action_enter(self) -> None:
        if self.mode == "probe":
            self.action_two_point(self.probe_func)
            return
        if self.mode == "wire":
            if self.wire_start == self.cursor:
                self.action_cancel()
                return
            self.snapshot()
            self.circuit.add_wire(self.wire_start, self.cursor)
            self.wire_start = self.cursor           # zincir: kaldığın yerden devam
            self.changed(edited=True)
        elif self.mode == "move":
            self.mode, self.grab = "normal", None
            self.say("")
            self.changed()
        else:
            self.action_edit()

    def action_edit(self) -> None:
        comp = self.circuit.component_at(self.cursor)
        if comp is None or comp.kind == "GND" or self.mode != "normal":
            return

        def validate(value: str) -> Optional[str]:
            if comp.kind == "N":
                return None if valid_value("N", value) else t("ckt.bad_label", name=value)
            return None if value and valid_value(comp.kind, value) else t("ckt.bad_value", ref=comp.ref)

        def done(value: Optional[str]) -> None:
            if value and value != comp.value:
                self.snapshot()
                comp.value = value
                self.changed(edited=True)

        unit = KINDS[comp.kind].unit
        if comp.kind == "N":
            title = t("ckt.prompt.label")
        elif comp.kind in ("D", "Q", "M", "U"):
            from elektro.circuit.devices import models_for
            title = t(f"ckt.prompt.model.{comp.kind}", ref=comp.ref, models=" · ".join(models_for(comp.kind)))
        else:
            key = "ckt.prompt.source" if comp.kind in ("V", "I") else "ckt.prompt.value"
            title = t(key, ref=comp.ref, unit=unit)

        def validate_model(value: str) -> Optional[str]:
            if comp.kind not in ("D", "Q", "M", "U"):
                return validate(value)
            from elektro.circuit.devices import parse_model
            try:
                parse_model(comp.kind, value)
            except CircuitError as e:
                return str(e)
            return None

        self.app.push_screen(PromptDialog(title, comp.value, validate_model), done)

    def action_rotate(self) -> None:
        comp = self.grab[0] if self.grab else self.circuit.component_at(self.cursor)
        if comp is None or comp.kind == "GND":
            return
        self.snapshot()
        comp.rot = (comp.rot + 90) % 360
        self.changed(edited=True)

    def action_grab(self) -> None:
        if self.mode == "move":
            self.action_enter()
            return
        comp = self.circuit.component_at(self.cursor)
        if comp is None or self.mode != "normal":
            return
        self.snapshot()
        self.mode = "move"
        self.grab = (comp, comp.x, comp.y, self.cursor[0] - comp.x, self.cursor[1] - comp.y)
        self.say(t("ckt.msg.move", ref=comp.ref))
        self.changed()

    def action_delete(self) -> None:
        if self.mode != "normal":
            return
        self.snapshot()
        if self.circuit.delete_at(self.cursor):
            self.changed(edited=True)
        else:
            self.undo_stack.pop()

    def action_cancel(self) -> None:
        reverted = False
        if self.mode == "move" and self.grab:
            comp, x, y, _, _ = self.grab
            comp.x, comp.y = x, y
            self.undo_stack.pop()
            reverted = True
        self.mode, self.wire_start, self.grab, self.probe_start = "normal", None, None, None
        self.say("")
        self.changed(edited=reverted)

    def action_undo(self) -> None:
        if self.mode != "normal" or not self.undo_stack:
            return
        self.circuit = self.undo_stack.pop()
        self.say(t("ckt.msg.undone"))
        self.changed(edited=True)

    def action_probe(self) -> None:
        """İmleç bir elemandaysa akımını, bir düğümdeyse gerilimini ölçer (tekrar basınca kaldırır)."""
        if self.mode != "normal":
            return
        comp = self.circuit.component_at(self.cursor)
        if comp is not None and comp.kind == "N":
            self.add_probe(f"V({comp.value.upper()})")
        elif comp is not None and comp.is_part and self.cursor not in comp.pins():
            self.add_probe(f"I({comp.ref})")
        elif self.circuit.net_at(self.cursor) is not None:
            self.add_probe(f"V({addr(self.cursor)})")
        else:
            self.say(t("ckt.msg.nothing"))
            self.changed()

    def action_two_point(self, func: str) -> None:
        """İki noktalı probe: başlangıçta a (akım) ya da o (direnç), bitişte aynı tuş/Enter.

        I(başlangıç, bitiş) akımı, R(başlangıç, bitiş) eşdeğer direnci ölçer.
        """
        if self.mode == "normal":
            if self.circuit.net_at(self.cursor) is None:
                self.say(t("ckt.msg.nothing"))
                self.changed()
                return
            self.mode, self.probe_start, self.probe_func = "probe", self.cursor, func
            self.say(t("ckt.msg.probe_from" if func == "I" else "ckt.msg.req_from", a=addr(self.cursor)))
            self.changed()
        elif self.mode == "probe":
            start, func = self.probe_start, self.probe_func
            self.mode, self.probe_start = "normal", None
            if start == self.cursor:
                self.say("")
                self.changed()
                return
            self.add_probe(f"{func}({addr(start)},{addr(self.cursor)})")

    def action_probe_prompt(self) -> None:
        if self.mode != "normal":
            return

        def validate(value: str) -> Optional[str]:
            if value.startswith("-") or not value:
                return None
            try:
                prb.normalize(value)
            except CircuitError as e:
                return str(e)
            return None

        def done(value: Optional[str]) -> None:
            if value is None:
                return
            if value == "-":                                  # hepsini sil
                self.snapshot()
                self.circuit.probes.clear()
                self.changed(edited=True)
            elif value.startswith("-") and value[1:].isdigit():
                n = int(value[1:])
                if 1 <= n <= len(self.circuit.probes):
                    self.snapshot()
                    removed = self.circuit.probes.pop(n - 1)
                    self.say(t("ckt.msg.probe_removed", expr=removed))
                    self.changed(edited=True)
            elif value:
                self.add_probe(value)

        self.app.push_screen(PromptDialog(t("ckt.prompt.probe"), "", validate), done)

    def action_simulate(self) -> None:
        self.live = True
        self.run_simulation()
        self.changed()

    def run_simulation(self, quiet: bool = False) -> None:
        if not any(c.kind in ("V", "I") for c in self.circuit.components):
            # Kaynak yok: DC çözümün anlamı yok; yalnızca direnç probe'ları hesaplanır
            self.result, self.error = None, None
            if not quiet:
                self.say(t("ckt.msg.no_source"))
            self.start_analysis(skip=True)
            return
        try:
            self.result = dc_operating_point(self.circuit)
            self.error = None
            if not quiet:
                self.say(t("ckt.msg.solved"))
        except CircuitError as e:
            self.result, self.error = None, str(e)
        self.start_analysis(skip=self.error is not None)

    def start_analysis(self, skip: bool = False) -> None:
        """.tran/.ac/.dc komutunu arka planda çalıştırır; arayüz donmaz.

        Devrenin kopyası kullanılır; bu sırada yapılan düzenleme yeni bir çözüm başlatır ve
        eski çözümün sonucu (nesil numarası tutmadığı için) yok sayılır.
        """
        self._generation += 1
        gen = self._generation
        directive = self.circuit.analysis.strip()
        if skip or not directive or directive.lower().startswith(".op"):
            self.sweep, self.sweep_error, self.busy, self.traces = None, None, False, []
            self.post_message(self.SweepReady(None, [], None, directive))
            return
        snapshot = copy.deepcopy(self.circuit)
        self.busy = True
        self.post_message(self.SweepStarted())

        def job() -> None:
            try:
                sweep = run_analysis(snapshot, directive)
                traces = prb.traces(snapshot, sweep) if sweep is not None else []
                error = None
            except CircuitError as e:
                sweep, traces, error = None, [], str(e)
            except Exception as e:                        # arayüz hiçbir hatada çökmesin
                sweep, traces, error = None, [], f"{type(e).__name__}: {e}"
            self.app.call_from_thread(self._sweep_done, gen, sweep, traces, error, directive)

        self.run_worker(job, thread=True, exclusive=True, group="analysis")

    def _sweep_done(self, gen: int, sweep, traces, error: Optional[str], directive: str) -> None:
        if gen != self._generation:
            return
        self.busy, self.sweep, self.sweep_error, self.traces = False, sweep, error, traces
        self.post_message(self.SweepReady(sweep, traces, error, directive))
        self.post_message(self.Changed())

    def action_analysis(self) -> None:
        if self.mode != "normal":
            return
        sources = [c.ref for c in self.circuit.components if c.kind in ("V", "I")]

        def done(value: Optional[str]) -> None:
            if value is None:
                return
            self.snapshot()
            self.circuit.analysis = "" if value == ".op" else value
            self.live = True
            self.say(t("ckt.msg.analysis", directive=value))
            self.changed(edited=True)

        self.app.push_screen(AnalysisDialog(self.circuit.analysis, sources), done)

    # --- dosya ---
    def load(self, path: Path) -> None:
        from elektro.circuit.spice import is_spice
        self.circuit = Circuit.load(path)
        self.path, self.dirty, self.undo_stack, self.result, self.error = path, False, [], None, None
        if is_spice(path):                       # içe aktarıldı: JSON olarak kaydedilsin, netlist bozulmasın
            self.path, self.dirty = path.with_suffix(".json"), True
            self.say("\n".join([t("ckt.msg.imported", path=path.name)] + self.circuit.notes))

    def action_save(self) -> None:
        def done(value: Optional[str]) -> None:
            if not value:
                return
            path = Path(value).expanduser()
            if not path.suffix:
                path = path.with_suffix(".json")
            try:
                self.circuit.save(path)
            except OSError as e:
                self.say(f"{t('ui.error')}: {e}")
            else:
                self.path, self.dirty = path, False
                self.say(t("ckt.msg.saved", path=path))
            self.changed()

        self.app.push_screen(PromptDialog(t("ckt.prompt.save"), str(self.path or "devre.json")), done)

    def action_open(self) -> None:
        def validate(value: str) -> Optional[str]:
            try:
                Circuit.load(Path(value).expanduser())
            except CircuitError as e:
                return str(e)
            return None

        def done(value: Optional[str]) -> None:
            if value:
                self.snapshot()
                self.load(Path(value).expanduser())
                self.live = False
                self.say(t("ckt.msg.opened", path=value))
                self.changed()

        self.app.push_screen(PromptDialog(t("ckt.prompt.open"), str(self.path or ""), validate), done)

    def action_examples(self) -> None:
        if self.mode != "normal":
            return

        def done(name: Optional[str]) -> None:
            if not name:
                return
            from elektro.circuit import examples
            self.snapshot()
            self.circuit = examples.build(name)
            self.path, self.dirty, self.result, self.error = Path(f"{name}.json"), True, None, None
            self.cursor, self.ox, self.oy = (2, 2), 0, 0
            self.say(t("ckt.msg.example", title=t(f"ex.{name}")))
            self.action_simulate()                        # örnek açılınca hemen çöz

        self.app.push_screen(ExampleDialog(), done)

    def action_new(self) -> None:
        if self.mode != "normal":
            return
        self.snapshot()
        self.circuit, self.path, self.result, self.error, self.live = Circuit(), None, None, None, False
        self.dirty = False
        self.say(t("ckt.msg.new"))
        self.changed()

    # --- yan panel ---
    def info(self) -> Group:
        parts: List = []
        name = self.path.name if self.path else t("ckt.untitled")
        head = Text.assemble((name + (" •" if self.dirty else ""), "bold"), ("  ·  ", "dim"),
                             (t("ckt.mode." + self.mode), "yellow" if self.mode != "normal" else "dim"))
        parts.append(head)
        nets = self.circuit.nets()
        point = self._at_cursor()
        values = point if point is not None else (self.result if not self.error else None)
        here = Text(addr(self.cursor), style="bold yellow")
        net_here = self.circuit.net_at(self.cursor, nets)
        if net_here is not None:
            here.append(f"   {t('ckt.node')} {'GND' if net_here == '0' else net_here}", style="magenta")
            if values is not None and net_here in values.voltages:
                here.append(f"  {_fmt(values.voltages[net_here], 'V')}", style="bold magenta")
        parts.append(here)
        comp = self.circuit.component_at(self.cursor)
        if comp is not None:
            parts.append(Text())
            parts.append(Text(f"{comp.ref}  ({t('ckt.kind.' + comp.kind)})", style="bold cyan"))
            if comp.is_part:
                parts.append(Text(comp.value))
            if comp.is_part:
                pins = " – ".join(_net_name(nets.get(p, "?")) for p in comp.pins())
                parts.append(Text(f"{t('ckt.nodes')}: {pins}", style="dim"))
            if values is not None and comp.ref in values.elements:
                e = dict(values.elements[comp.ref])
                if point is not None:                    # imleçteki değer: sayısal artığı sıfırla
                    series = self.sweep.elements[comp.ref]
                    for key in ("v", "i", "p"):
                        peak = max((abs(x) for x in series[key]), default=0.0)
                        if abs(e[key]) < peak * 1e-9 or abs(e[key]) < 1e-18:
                            e[key] = 0.0
                line = f"V = {_fmt(e['v'], 'V')}   I = {_fmt(e['i'], 'A')}"
                if not isinstance(e["p"], complex):
                    line += f"   P = {format_si(e['p'], 'W')}"
                parts.append(Text(line))
        readings = prb.read_all(self.circuit, self.result if not self.error else None)
        if readings:
            parts.append(Text())
            if point is not None:
                parts.append(_sweep_probe_table(readings, self.traces, self.sweep, self.plot_cursor))
            else:
                parts.append(_probe_table(readings))
        if self.circuit.analysis:
            line = Text(f"{t('ckt.analysis')}: ", style="dim")
            line.append(self.circuit.analysis, style="bold")
            if self.busy:
                line.append(f"  {t('ckt.running')}", style="yellow")
            parts.append(line)
        if self.sweep_error:
            parts.append(Text(self.sweep_error, style="bold red"))
        if self.message:
            parts += [Text(), Text(self.message, style="green")]
        if self.error:
            parts += [Text(), Text(self.error, style="bold red")]
        if self.result and not self.error:
            parts.append(Text())
            parts.append(_result_table(self.result))
            for w in self.result.warnings:
                parts.append(Text(f"⚠ {w}", style="yellow"))
        return Group(*parts)


def _net_name(net: str) -> str:
    return "GND" if net == "0" else net


def _fmt(value, unit: str) -> str:
    """Gerçel değer ya da AC fazörü: '1.2 V' / '707 mV ∠ −45°'."""
    if isinstance(value, complex):
        return f"{format_si(abs(value), unit)} ∠ {math.degrees(math.atan2(value.imag, value.real)):.1f}°"
    return format_si(value, unit)


def _sweep_probe_table(readings, traces, sweep, k: int) -> Table:
    """Analiz varken probe değerleri: grafik imlecindeki an; transient'te RMS ve tepe de.

    Analizde çizilmeyen probe'lar (ör. R(A,B)) DC değeriyle gösterilir.
    """
    by_expr = {tr.expr: tr for tr in traces if tr.values is not None}
    tran = sweep.kind == "tran"
    title = t("ckt.probes_at", x=format_si(sweep.x[k], sweep.x_unit))
    tbl = Table(box=None, header_style="bold", padding=(0, 1), title=title, title_justify="left")
    tbl.add_column("#", style="dim", justify="right")
    tbl.add_column("", style="bold magenta")
    tbl.add_column("", justify="right")
    if tran:
        tbl.add_column("RMS", justify="right", style="cyan")
        tbl.add_column(t("ckt.col.peak"), justify="right", style="cyan")
    for i, r in enumerate(readings, 1):
        tr = by_expr.get(r.expr)
        extra = ["", ""] if tran else []
        if tr is not None:
            peak = max(abs(v) for v in tr.values)
            v = tr.values[k]
            if abs(v) < peak * 1e-9:                     # sayısal artık (sin(3π) ≈ 1e-16)
                v = 0.0
            value = Text(_fmt(v, tr.unit), style="bold")
            if tran:
                rms = math.sqrt(sum(x * x for x in tr.values) / len(tr.values))
                extra = [format_si(rms, tr.unit), format_si(peak, tr.unit)]
        elif r.error:
            value = Text(r.error, style="red")
        elif r.value is None:
            value = Text("F5", style="dim")
        else:
            value = Text(format_si(r.value, r.unit), style="bold")
        tbl.add_row(str(i), r.expr, value, *extra)
    return tbl


def _probe_table(readings) -> Table:
    tbl = Table(box=None, header_style="bold", padding=(0, 1), title=t("ckt.probes"), title_justify="left")
    tbl.add_column("#", style="dim", justify="right")
    tbl.add_column("", style="bold magenta")
    tbl.add_column("", justify="right")
    for i, r in enumerate(readings, 1):
        if r.error:
            value = Text(r.error, style="red")
        elif r.value is None:
            value = Text("F5", style="dim")
        else:
            value = Text(format_si(r.value, r.unit), style="bold")
        tbl.add_row(str(i), r.expr, value)
    return tbl


def _result_table(result: OpResult) -> Table:
    tbl = Table(box=None, header_style="bold", padding=(0, 1), title=t("ckt.op_title"), title_justify="left")
    tbl.add_column("", style="cyan")
    tbl.add_column("V", justify="right")
    tbl.add_column("I", justify="right")
    tbl.add_column("P", justify="right")
    for name, v in sorted(result.voltages.items(), key=lambda kv: (kv[0] != "0", len(kv[0]), kv[0])):
        if name != "0":
            tbl.add_row(_net_name(name), format_si(v, "V"), "", "", style="magenta")
    for ref, e in result.elements.items():
        tbl.add_row(ref, format_si(e["v"], "V"), format_si(e["i"], "A"), format_si(e["p"], "W"))
    return tbl

