"""Terminal grafiği: Braille karakterleriyle (her hücre 2×4 nokta) çok eğrili çizim.

    V(D1)  I(R1)                          x = 1.2 ms  V(D1) = 530 mV  I(R1) = 470 µA
     1 V ┤⠀⠀⠀⢀⡠⠔⠒⠉⠉⠒⠢⢄⡀⠀⠀⠀⠀
         ┤⠀⡠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⡀⠀⠀
    -1 V ┤⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⣀
          0        2.5 ms       5 ms

İlk birimin eğrileri sol eksene, ikinci birimin eğrileri sağ eksene göre çizilir. AC
sonuçları karmaşık sayıdır: genlik (dB) ya da faz (°) olarak gösterilir.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from rich.text import Text

from elektro.units import format_si

COLORS = ["bright_cyan", "bright_magenta", "bright_yellow", "bright_green", "bright_red", "bright_blue",
          "orange1", "white"]
_BITS = ((0x01, 0x08), (0x02, 0x10), (0x04, 0x20), (0x40, 0x80))     # [satır][sütun]
LEFT, RIGHT = 9, 9


@dataclass
class Series:
    label: str
    unit: str
    ys: List[float]
    color: str = "white"


def series_from(traces, mode: str = "mag") -> List[Series]:
    """probes.Trace listesi → çizilecek gerçel seriler. mode: AC için 'mag' (dB) ya da 'phase' (°)."""
    out = []
    for i, tr in enumerate(traces):
        if tr.values is None:
            continue
        color = COLORS[i % len(COLORS)]
        if any(isinstance(v, complex) for v in tr.values):
            if mode == "phase":
                ys = [math.degrees(math.atan2(v.imag, v.real)) for v in tr.values]
                out.append(Series(tr.expr, "°", ys, color))
            else:
                ys = [20 * math.log10(abs(v)) if abs(v) > 1e-30 else -600.0 for v in tr.values]
                out.append(Series(tr.expr, f"dB{tr.unit}", ys, color))
        else:
            out.append(Series(tr.expr, tr.unit, [float(v) for v in tr.values], color))
    return out


def _nice_ticks(lo: float, hi: float, count: int = 4) -> List[float]:
    if hi - lo <= 0:
        return [lo]
    raw = (hi - lo) / count
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if raw <= m * mag)
    start = math.ceil(lo / step - 1e-9) * step
    ticks, v = [], start
    while v <= hi + step * 1e-9:
        ticks.append(round(v / step) * step)
        v += step
    return ticks


def _range(values: Sequence[float]) -> Tuple[float, float]:
    finite = [v for v in values if math.isfinite(v)]
    if not finite:
        return -1.0, 1.0
    lo, hi = min(finite), max(finite)
    if hi - lo < max(abs(hi), abs(lo), 1e-30) * 1e-9:
        pad = abs(hi) * 0.1 or 1.0
        return lo - pad, hi + pad
    pad = (hi - lo) * 0.06
    return lo - pad, hi + pad


def _fmt(v: float, unit: str) -> str:
    if unit in ("°",) or unit.startswith("dB"):
        return f"{v:.3g}{unit[:2] if unit.startswith('dB') else unit}"
    return format_si(v, unit, 3).replace(" ", "")


def render(series: List[Series], xs: Sequence[float], width: int, height: int, *, log_x: bool = False,
           x_unit: str = "", cursor: Optional[int] = None, title: str = "", hint: str = "") -> List[Text]:
    """Grafiği width × height karakterlik satırlar olarak döndürür."""
    width, height = max(width, 30), max(height, 6)
    lines = [Text() for _ in range(height)]
    plot_w = width - LEFT - RIGHT
    plot_h = height - 3                         # üstte açıklama, altta 2 satır x ekseni
    if not series or not xs or plot_h < 2:
        lines[0].append(title, style="bold")
        if hint:
            lines[min(2, height - 1)].append("  " + hint, style="dim")
        return lines

    units: List[str] = []
    for s in series:
        if s.unit not in units:
            units.append(s.unit)
    axes: Dict[str, Tuple[float, float]] = {}
    for u in units[:2]:
        axes[u] = _range([v for s in series if s.unit == u for v in s.ys])
    drawn = [s for s in series if s.unit in axes]

    def fx(x: float) -> float:
        if log_x:
            a, b = math.log10(xs[0]), math.log10(xs[-1])
            return (math.log10(x) - a) / ((b - a) or 1) * (plot_w * 2 - 1)
        return (x - xs[0]) / ((xs[-1] - xs[0]) or 1) * (plot_w * 2 - 1)

    def fy(y: float, unit: str) -> float:
        lo, hi = axes[unit]
        return (hi - y) / (hi - lo) * (plot_h * 4 - 1)

    dots: Dict[Tuple[int, int], int] = {}
    color: Dict[Tuple[int, int], str] = {}

    def plot_px(px: int, py: int, col: str) -> None:
        if 0 <= px < plot_w * 2 and 0 <= py < plot_h * 4:
            cell = (px // 2, py // 4)
            dots[cell] = dots.get(cell, 0) | _BITS[py % 4][px % 2]
            color[cell] = col

    # sıfır çizgisi
    for u, (lo, hi) in axes.items():
        if lo < 0 < hi and u == units[0]:
            py = round(fy(0.0, u))
            for px in range(0, plot_w * 2, 4):
                plot_px(px, py, "grey35")
    # imleç çizgisi
    if cursor is not None and 0 <= cursor < len(xs):
        cx = round(fx(xs[cursor]))
        for py in range(0, plot_h * 4, 2):
            plot_px(cx, py, "grey50")

    for s in drawn:
        prev = None
        for x, y in zip(xs, s.ys):
            if not math.isfinite(y):
                prev = None
                continue
            px, py = round(fx(x)), round(fy(y, s.unit))
            if prev is None:
                plot_px(px, py, s.color)
            else:
                (x0, y0) = prev
                steps = max(abs(px - x0), abs(py - y0), 1)
                for i in range(1, steps + 1):
                    plot_px(round(x0 + (px - x0) * i / steps), round(y0 + (py - y0) * i / steps), s.color)
            prev = (px, py)

    # 1. satır: açıklama ve imleç değerleri
    head = lines[0]
    if title:
        head.append(title + "  ", style="bold")
    for s in series:
        head.append("■ ", style=s.color)
        head.append(s.label + ("" if s.unit in axes else " ✗") + "  ", style=s.color if s.unit in axes else "dim")
    if cursor is not None and 0 <= cursor < len(xs):
        head.append("│ ", style="dim")
        head.append(f"x = {format_si(xs[cursor], x_unit, 4)}  ", style="bold")
        for s in drawn:
            scale = max((abs(v) for v in s.ys if math.isfinite(v)), default=0.0)
            value = 0.0 if abs(s.ys[cursor]) < scale * 1e-9 else s.ys[cursor]     # sayısal artık
            head.append(f"{_fmt(value, s.unit)}  ", style=s.color)
    head.truncate(width)

    # eksen etiketleri
    left_unit, right_unit = units[0], units[1] if len(units) > 1 else None
    tick_rows: Dict[int, str] = {}
    for v in _nice_ticks(*axes[left_unit]):
        tick_rows.setdefault(min(max(round(fy(v, left_unit) / 4), 0), plot_h - 1), _fmt(v, left_unit))
    rtick_rows: Dict[int, str] = {}
    if right_unit:
        for v in _nice_ticks(*axes[right_unit]):
            rtick_rows.setdefault(min(max(round(fy(v, right_unit) / 4), 0), plot_h - 1), _fmt(v, right_unit))
    for r in range(plot_h):
        line = lines[1 + r]
        line.append(tick_rows.get(r, "").rjust(LEFT - 2)[: LEFT - 2], style="grey62")
        line.append(" ┤" if r in tick_rows else " │", style="grey50")
        for c in range(plot_w):
            bits = dots.get((c, r))
            if bits:
                line.append(chr(0x2800 + bits), style=color[(c, r)])
            else:
                line.append(" ")
        if right_unit:
            line.append(("├ " if r in rtick_rows else "  ") + rtick_rows.get(r, "")[: RIGHT - 2],
                        style="grey62")
    # x ekseni
    axis = lines[1 + plot_h]
    axis.append(" " * LEFT + "└" + "─" * (plot_w - 1), style="grey50")
    labels = lines[2 + plot_h]
    if log_x:
        ticks = [10 ** d for d in range(math.ceil(math.log10(xs[0]) - 1e-9), math.floor(math.log10(xs[-1]) + 1e-9) + 1)]
    else:
        ticks = _nice_ticks(xs[0], xs[-1], max(plot_w // 14, 2))
    row = [" "] * width
    for v in ticks:
        txt = format_si(v, x_unit, 3).replace(" ", "")
        col = LEFT + round(fx(v) / 2) - len(txt) // 2
        if 0 <= col and col + len(txt) <= width and all(ch == " " for ch in row[max(col - 1, 0):col + len(txt) + 1]):
            row[col:col + len(txt)] = list(txt)
    labels.append("".join(row), style="grey62")
    return lines
