"""Şemayı karakter hücrelerine çizer (kompakt etiket stili).

    ●──[R1 10k]──●
    │            │
 [V1 5V]     [R2 4k7]
    │            │
    ●────────────●
              [GND]

Bir ızgara noktası 4 sütun × 2 satırdır. Kesişen kablolar ┼ ile, bağlantı noktaları ● ile,
probe konan noktalar ◉ ile gösterilir. Üstte sütun harfleri, solda satır numaraları vardır (Excel
gibi: C3 = C sütunu, 3. satır). Bu modül Textual'a bağlı değildir; çıktısı rich.Text satırlarıdır.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from rich.text import Text

from elektro.circuit.model import THREE_PIN, Circuit, Component, Point, Segment, col_name, segment_points
from elektro.units import format_si

STEP_X, STEP_Y = 4, 2
MARGIN_X, MARGIN_Y = 5, 2          # solda satır numaraları, üstte sütun harfleri

U, D, L, R = "U", "D", "L", "R"
BOX = {
    frozenset({U, D}): "│", frozenset({L, R}): "─", frozenset({D, R}): "┌", frozenset({D, L}): "┐",
    frozenset({U, R}): "└", frozenset({U, L}): "┘", frozenset({U, D, R}): "├", frozenset({U, D, L}): "┤",
    frozenset({D, L, R}): "┬", frozenset({U, L, R}): "┴", frozenset({U, D, L, R}): "┼",
    frozenset({U}): "│", frozenset({D}): "│", frozenset({L}): "─", frozenset({R}): "─",
}

STYLE_WIRE = "bright_white"
STYLE_PART = "bold cyan"
STYLE_SOURCE = "bold yellow"
STYLE_DEVICE = "bold bright_green"
STYLE_LABEL = "bold bright_magenta"
STYLE_GND = "bold green"
STYLE_DOT = "grey35"
STYLE_VOLT = "magenta"
STYLE_SELECTED = "bold reverse cyan"
STYLE_CURSOR = "bold reverse yellow"
STYLE_PREVIEW = "yellow"
STYLE_PROBE = "bold magenta"
STYLE_HEADER = "grey50"
STYLE_HEADER_ON = "bold black on yellow"


@dataclass
class View:
    ox: int = 0                     # görünen alanın sol üst ızgara noktası
    oy: int = 0
    width: int = 80                 # karakter
    height: int = 24
    cursor: Optional[Point] = None
    selected: Optional[str] = None  # vurgulanan bileşen
    preview: List[Segment] = field(default_factory=list)     # çizilmekte olan kablo
    voltages: Dict[str, float] = field(default_factory=dict) # düğüm → V (simülasyondan sonra)
    probe_points: Set[Point] = field(default_factory=set)    # V probe noktaları
    probe_parts: Set[str] = field(default_factory=set)       # akım probe'lu bileşenler
    marks: Set[Point] = field(default_factory=set)           # seçilmiş başlangıç noktası (ör. akım probe'u)

    def cols(self) -> int:
        return max((self.width - MARGIN_X) // STEP_X, 1)

    def rows(self) -> int:
        return max((self.height - MARGIN_Y) // STEP_Y, 1)


class _Canvas:
    def __init__(self, view: View):
        self.v = view
        self.cells: Dict[Tuple[int, int], Tuple[str, str]] = {}
        self.locked: Set[Tuple[int, int]] = set()
        self.mos_centers: Dict[Point, bool] = {}           # transistör gövde noktaları

    def pos(self, p: Point) -> Tuple[int, int]:
        return ((p[0] - self.v.ox) * STEP_X + MARGIN_X, (p[1] - self.v.oy) * STEP_Y + MARGIN_Y)

    def put(self, col: int, row: int, ch: str, style: str = "", overwrite: bool = True) -> None:
        if 0 <= col < self.v.width and 0 <= row < self.v.height:
            if overwrite or (col, row) not in self.cells:
                self.cells[(col, row)] = (ch, style)

    def text(self, col: int, row: int, s: str, style: str = "", overwrite: bool = True) -> None:
        for i, ch in enumerate(s):
            self.put(col + i, row, ch, style, overwrite)

    def label(self, col: int, row: int, s: str, style: str) -> None:
        """Bileşen etiketi: sonradan çizilen düğüm karakterleri üstüne yazamaz."""
        self.text(col, row, s, style)
        self.locked.update((col + i, row) for i in range(len(s)))

    def free(self, col: int, row: int, length: int) -> bool:
        return all((c, row) not in self.cells for c in range(col, col + length)) and 0 <= row < self.v.height

    def lines(self) -> List[Text]:
        out = []
        for row in range(self.v.height):
            line = Text()
            for col in range(self.v.width):
                ch, style = self.cells.get((col, row), (" ", ""))
                line.append(ch, style)
            out.append(line)
        return out


def _label_style(c: Component) -> str:
    if c.kind == "GND":
        return STYLE_GND
    if c.kind == "N":
        return STYLE_LABEL
    if c.kind in ("V", "I"):
        return STYLE_SOURCE
    return STYLE_DEVICE if c.kind in ("D", "Q", "M", "U") else STYLE_PART


MOS_BOX = {frozenset({U, D, L}): "╢", frozenset({U, D, R}): "╟", frozenset({L, R, D}): "╤",
           frozenset({L, R, U}): "╧"}
ARROWS = {(1, 0): "→", (-1, 0): "←", (0, 1): "↓", (0, -1): "↑"}


def _three_pin(cv: "_Canvas", comp: Component, style: str, link) -> None:
    """Transistör ve op-amp çizimi.

    BJT (rot 0):       C            MOSFET:   D          Op-amp:  +●─┐
                       │                      ║                      ├▷──────●
                   B ●─┤ [Q1 …]           G ●─╢ [M1 …]           −●─┘
                       ↓                      ║                      U1 TL072
                       E                      S
    """
    pins = comp.pins()
    center = (comp.x, comp.y)
    ccol, crow = cv.pos(center)
    label = f"[{comp.label()}]"
    if comp.kind == "U":
        out, inp, inn = pins
        back = (comp.x, comp.y)
        top, bottom = (back[0], inp[1]), (back[0], inn[1])
        link(inp, top)
        link(inn, bottom)
        link(top, (back[0], back[1]))
        link((back[0], back[1]), bottom)
        link(back, out)
        for a, b in ((inp, top), (inn, bottom), (back, out)):
            (c1, r1), (c2, _) = cv.pos(a), cv.pos(b)
            for c in range(min(c1, c2) + 1, max(c1, c2)):
                cv.put(c, r1, "─", STYLE_WIRE)
        for r in range(cv.pos(top)[1] + 1, cv.pos(bottom)[1]):
            cv.put(ccol, r, "│", STYLE_WIRE)
        step = 1 if out[0] > back[0] else -1
        cv.put(ccol + step, crow, "▷" if step > 0 else "◁", STYLE_DEVICE)
        for pin, sign in ((inp, "+"), (inn, "−")):
            col, row = cv.pos(pin)
            cv.put(col + step, row - 1 if row > 0 else row, sign, STYLE_DEVICE)
        text = label[1:-1]
        col = ccol + 2 if step > 0 else ccol - 1 - len(text)
        below = cv.pos(bottom)[1] + 1 if inn[1] > inp[1] else cv.pos(top)[1] + 1
        cv.label(col, below, text, style)
        return
    for pin in pins:
        link(pin, center)
        (c1, r1), (c2, r2) = cv.pos(pin), cv.pos(center)
        if r1 == r2:
            for c in range(min(c1, c2) + 1, max(c1, c2)):
                cv.put(c, r1, "─", STYLE_WIRE)
        else:
            for r in range(min(r1, r2) + 1, max(r1, r2)):
                cv.put(c1, r, "║" if comp.kind == "M" else "│", STYLE_WIRE)
    cv.mos_centers[center] = comp.kind == "M"
    # emetör oku: NPN dışarı, PNP içeri
    if comp.kind == "Q":
        from elektro.circuit.devices import parse_model
        try:
            npn = parse_model("Q", comp.value).type == "NPN"
        except ValueError:
            npn = True
        e = pins[2]
        d = (e[0] - comp.x, e[1] - comp.y)
        (ec, er) = cv.pos(e)
        mid = ((ccol + ec) // 2, (crow + er) // 2)
        cv.put(*mid, ARROWS[d if npn else (-d[0], -d[1])], STYLE_DEVICE)
    base = pins[1]
    bx, by = base[0] - comp.x, base[1] - comp.y
    if bx < 0:
        cv.label(ccol + 2, crow, label, style)
    elif bx > 0:
        cv.label(ccol - 1 - len(label), crow, label, style)
    elif by < 0:
        cv.label(ccol + 2, crow + 1, label, style)
    else:
        cv.label(ccol + 2, crow - 1, label, style)


def render(circuit: Circuit, view: View) -> List[Text]:
    cv = _Canvas(view)
    dirs: Dict[Point, Set[str]] = {}
    pins: Set[Point] = set()

    def link(a: Point, b: Point) -> None:
        if a[1] == b[1]:
            left, right = (a, b) if a[0] < b[0] else (b, a)
            dirs.setdefault(left, set()).add(R)
            dirs.setdefault(right, set()).add(L)
        else:
            top, bottom = (a, b) if a[1] < b[1] else (b, a)
            dirs.setdefault(top, set()).add(D)
            dirs.setdefault(bottom, set()).add(U)

    def draw_segment(seg: Segment, style: str) -> None:
        pts = segment_points(seg)
        for a, b in zip(pts, pts[1:]):
            link(a, b)
            (c1, r1), (c2, r2) = cv.pos(a), cv.pos(b)
            if r1 == r2:
                for c in range(min(c1, c2) + 1, max(c1, c2)):
                    cv.put(c, r1, "─", style)
            else:
                for r in range(min(r1, r2) + 1, max(r1, r2)):
                    cv.put(c1, r, "│", style)

    # 1) arka plan ızgarası
    for gy in range(view.oy, view.oy + view.rows() + 1):
        for gx in range(view.ox, view.ox + view.cols() + 1):
            cv.put(*cv.pos((gx, gy)), "·", STYLE_DOT)

    # 2) kablolar
    for seg in circuit.wires:
        draw_segment(seg, STYLE_WIRE)

    # 3) bileşenler
    for comp in circuit.components:
        sel = comp.ref == view.selected
        style = STYLE_SELECTED if sel else _label_style(comp)
        if comp.ref in view.probe_parts:
            style += " underline"
        label = f"[{comp.label()}]"
        p = comp.pins()
        pins.update(p)
        if comp.kind in THREE_PIN:
            _three_pin(cv, comp, style, link)
            continue
        if comp.kind == "GND":
            col, row = cv.pos(p[0])
            dirs.setdefault(p[0], set()).add(D)
            cv.label(col - len(label) // 2, row + 1, label, style)
            continue
        if comp.kind == "N":                              # düğüm etiketi: noktanın yanında ◂AD▸
            col, row = cv.pos(p[0])
            dirs.setdefault(p[0], set())
            text = f"◂{comp.value}" if comp.rot in (0, 90, 270) else f"{comp.value}▸"
            if comp.rot == 0:
                cv.label(col + 1, row, text, style)
            elif comp.rot == 180:
                cv.label(col - len(text), row, text, style)
            else:
                cv.label(col - len(text) // 2, row + (1 if comp.rot == 90 else -1), text, style)
            continue
        a, b = comp.cells()[0], comp.cells()[-1]
        link(a, b)
        (c1, r1), (c2, r2) = cv.pos(a), cv.pos(b)
        if comp.horizontal:
            for c in range(c1 + 1, c2):
                cv.put(c, r1, "─", STYLE_WIRE)
            mid = (c1 + c2) // 2
            cv.label(mid - len(label) // 2, r1, label, style)
            if comp.kind in ("V", "I"):
                plus_col = c1 + 1 if comp.rot == 0 else c2 - 1
                cv.put(plus_col, r1, "+" if comp.kind == "V" else ("→" if comp.rot == 0 else "←"), STYLE_SOURCE)
        else:
            for r in range(r1 + 1, r2):
                cv.put(c1, r, "│", STYLE_WIRE)
            mid = (r1 + r2) // 2
            cv.label(c1 - len(label) // 2, mid, label, style)
            if comp.kind in ("V", "I"):
                plus_row = r1 + 1 if comp.rot == 90 else r2 - 1
                cv.put(c1, plus_row, "+" if comp.kind == "V" else ("↓" if comp.rot == 90 else "↑"), STYLE_SOURCE)

    # 4) çizilmekte olan kablo
    for seg in view.preview:
        draw_segment(seg, STYLE_PREVIEW)

    # 5) düğüm noktaları: uç ve 3+ bağlantı ●, köşe/kesişim kutu karakteri.
    #    Kablo ortasında uç olmadan kesişen kablolar bağlı değildir (┼).
    terminals = set(pins)
    for s in circuit.wires:
        terminals |= {(s[0], s[1]), (s[2], s[3])}
    for point, ds in dirs.items():
        col, row = cv.pos(point)
        if (col, row) in cv.locked:
            continue
        if point in cv.mos_centers:                      # transistör gövdesi: ● değil, gövde çizgisi
            ch = (MOS_BOX if cv.mos_centers[point] else BOX).get(frozenset(ds), "┼")
        elif point in pins or (len(ds) >= 3 and point in terminals):
            ch = "●"
        else:
            ch = BOX.get(frozenset(ds), "·")
        cv.put(col, row, ch, STYLE_WIRE)

    # 6) düğüm gerilimleri
    if view.voltages:
        for name, pts in circuit.net_points().items():
            if name not in view.voltages or name == "0":
                continue
            txt = format_si(view.voltages[name], "V", 4).replace(" ", "")
            for p in sorted(pts, key=lambda q: (q[1], q[0])):
                col, row = cv.pos(p)
                for c, r in ((col + 1, row - 1), (col - len(txt), row - 1), (col + 1, row + 1)):
                    if cv.free(c, r, len(txt)) and c >= 0:
                        cv.text(c, r, txt, STYLE_VOLT)
                        break
                else:
                    continue
                break

    # 7) probe noktaları ve işaretler
    for point in view.probe_points:
        cv.put(*cv.pos(point), "◉", STYLE_PROBE)
    for point in view.marks:
        cv.put(*cv.pos(point), "◎", STYLE_CURSOR)

    # 8) imleç
    if view.cursor is not None:
        col, row = cv.pos(view.cursor)
        ch = cv.cells.get((col, row), ("┼", ""))[0]
        cv.put(col, row, "┼" if ch in ("·", " ") else ch, STYLE_CURSOR)

    # 9) Excel gibi başlıklar: üstte sütun harfleri, solda satır numaraları
    cx, cy = view.cursor if view.cursor is not None else (None, None)
    for r in range(MARGIN_Y):
        for c in range(view.width):
            cv.put(c, r, " ")
    for row in range(MARGIN_Y, view.height):
        for c in range(MARGIN_X - 1):
            cv.put(c, row, " ")
    for gx in range(view.ox, view.ox + view.cols() + 1):
        name = col_name(gx)
        col = cv.pos((gx, 0))[0]
        cv.text(col - (len(name) - 1) // 2, 0, name, STYLE_HEADER_ON if gx == cx else STYLE_HEADER)
    for gy in range(view.oy, view.oy + view.rows() + 1):
        num = str(gy + 1).rjust(MARGIN_X - 2)
        cv.text(0, cv.pos((0, gy))[1], num, STYLE_HEADER_ON if gy == cy else STYLE_HEADER)
    return cv.lines()

