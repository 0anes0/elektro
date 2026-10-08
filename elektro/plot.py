"""Grafik çıktısı: bağımlılıksız SVG, matplotlib varsa PNG/PDF.

Üç tür grafik var:
  bode(...)     — logaritmik frekans ekseni, üstte genlik (dB), altta faz (°)
  curve(...)    — doğrusal x ekseni, tek eğri (ör. RC dolma)
  spectrum(...) — logaritmik frekans ekseni, tek eğri (FFT)
"""

from __future__ import annotations

import math
import sys
from html import escape
from pathlib import Path
from typing import List, Optional, Sequence

from elektro.i18n import t
from elektro.units import format_si

W, H = 760, 520
MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B = 70, 20, 40, 45
STYLE = """
  text { font-family: sans-serif; font-size: 12px; fill: #333; }
  .title { font-size: 15px; font-weight: bold; }
  .grid { stroke: #ddd; stroke-width: 1; }
  .axis { stroke: #555; stroke-width: 1; }
  .line { fill: none; stroke: #1f6feb; stroke-width: 2; }
  .phase { fill: none; stroke: #d9480f; stroke-width: 2; }
  .mark { stroke: #999; stroke-dasharray: 4 3; }
"""


def logspace(start: float, stop: float, n: int) -> List[float]:
    a, b = math.log10(start), math.log10(stop)
    return [10 ** (a + (b - a) * i / (n - 1)) for i in range(n)]


def _nice_step(span: float, target: int = 6) -> float:
    raw = span / target
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            return m * mag
    return 10 * mag


def _ticks(lo: float, hi: float) -> List[float]:
    step = _nice_step(hi - lo)
    start = math.ceil(lo / step) * step
    out, v = [], start
    while v <= hi + step * 1e-9:
        out.append(round(v, 10))
        v += step
    return out


class _Panel:
    """Bir çizim alanı: x (log veya doğrusal) ve y eksenleri."""

    def __init__(self, x0, y0, w, h, xs, ys, log_x, y_label, x_label, x_unit, css, series=None):
        """series verilirse [(ys, renk), …] eğrilerin hepsi aynı eksene çizilir."""
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        self.log_x = log_x
        finite = [y for y in ([v for s, _ in series for v in s] if series else ys) if math.isfinite(y)]
        lo, hi = (min(finite), max(finite)) if finite else (0, 1)
        if hi - lo < 1e-9:
            lo, hi = lo - 1, hi + 1
        pad = (hi - lo) * 0.05
        self.ylo, self.yhi = lo - pad, hi + pad
        self.xlo, self.xhi = min(xs), max(xs)
        self.parts = []
        self._axes(y_label, x_label, x_unit)
        for s_ys, color in series or [(ys, None)]:
            pts = " ".join(f"{self.px(x):.1f},{self.py(max(y, self.ylo)):.1f}"
                           for x, y in zip(xs, s_ys) if math.isfinite(y))
            attr = f'style="fill:none;stroke:{color};stroke-width:2"' if color else f'class="{css}"'
            self.parts.append(f'<polyline {attr} points="{pts}"/>')

    def px(self, x):
        if self.log_x:
            a, b = math.log10(self.xlo), math.log10(self.xhi)
            return self.x0 + (math.log10(x) - a) / (b - a) * self.w
        return self.x0 + (x - self.xlo) / (self.xhi - self.xlo) * self.w

    def py(self, y):
        return self.y0 + self.h - (y - self.ylo) / (self.yhi - self.ylo) * self.h

    def _axes(self, y_label, x_label, x_unit):
        p = self.parts
        for y in _ticks(self.ylo, self.yhi):
            yy = self.py(y)
            p.append(f'<line class="grid" x1="{self.x0}" x2="{self.x0 + self.w}" y1="{yy:.1f}" y2="{yy:.1f}"/>')
            p.append(f'<text x="{self.x0 - 6}" y="{yy + 4:.1f}" text-anchor="end">{y:g}</text>')
        if self.log_x:
            d = math.floor(math.log10(self.xlo))
            while 10 ** d <= self.xhi * 1.0001:
                for m in range(1, 10):
                    x = m * 10 ** d
                    if self.xlo <= x <= self.xhi:
                        xx = self.px(x)
                        p.append(f'<line class="grid" x1="{xx:.1f}" x2="{xx:.1f}" y1="{self.y0}" '
                                 f'y2="{self.y0 + self.h}" style="opacity:{1 if m == 1 else 0.45}"/>')
                        if m == 1:
                            p.append(f'<text x="{xx:.1f}" y="{self.y0 + self.h + 15}" text-anchor="middle">'
                                     f'{escape(format_si(x, x_unit, 3))}</text>')
                d += 1
        else:
            for x in _ticks(self.xlo, self.xhi):
                xx = self.px(x)
                p.append(f'<line class="grid" x1="{xx:.1f}" x2="{xx:.1f}" y1="{self.y0}" y2="{self.y0 + self.h}"/>')
                p.append(f'<text x="{xx:.1f}" y="{self.y0 + self.h + 15}" text-anchor="middle">'
                         f'{escape(format_si(x, x_unit, 3))}</text>')
        p.append(f'<rect class="axis" fill="none" x="{self.x0}" y="{self.y0}" width="{self.w}" height="{self.h}"/>')
        p.append(f'<text x="{self.x0 - 50}" y="{self.y0 + self.h / 2}" text-anchor="middle" '
                 f'transform="rotate(-90 {self.x0 - 50} {self.y0 + self.h / 2})">{escape(y_label)}</text>')
        if x_label:
            p.append(f'<text x="{self.x0 + self.w / 2}" y="{self.y0 + self.h + 32}" text-anchor="middle">'
                     f'{escape(x_label)}</text>')

    def vmark(self, x):
        xx = self.px(x)
        self.parts.append(f'<line class="mark" x1="{xx:.1f}" x2="{xx:.1f}" y1="{self.y0}" y2="{self.y0 + self.h}"/>')


def _svg(title: str, panels) -> str:
    body = "".join(part for panel in panels for part in panel.parts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<style>{STYLE}</style><rect width="100%" height="100%" fill="white"/>'
            f'<text class="title" x="{W / 2}" y="24" text-anchor="middle">{escape(title)}</text>{body}</svg>\n')


class PlotError(Exception):
    pass


def _matplotlib():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        raise PlotError(t("plot.need_mpl", pip=f"{sys.executable} -m pip install matplotlib"))


def plot_path(text) -> Path:
    """--plot seçeneği için ayrıştırıcı: uzantıyı ve (PNG/PDF için) matplotlib'i baştan kontrol eder."""
    path = Path(str(text)).expanduser()
    try:
        if _check_suffix(path) != ".svg":
            _matplotlib()
    except PlotError as e:
        raise ValueError(str(e))
    return path


def _check_suffix(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix not in (".svg", ".png", ".pdf"):
        raise PlotError(t("plot.bad_suffix"))
    return suffix


def bode(path: Path, title: str, freqs: Sequence[float], gains: Sequence[float],
         phases: Sequence[float], mark: Optional[float] = None) -> Path:
    suffix = _check_suffix(path)
    gains = [max(g, -120.0) if math.isfinite(g) else -120.0 for g in gains]
    if suffix != ".svg":
        plt = _matplotlib()
        fig, (a1, a2) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
        a1.semilogx(freqs, gains)
        a1.set_ylabel(f"{t('flt.gain')} (dB)")
        a2.semilogx(freqs, phases, color="tab:orange")
        a2.set_ylabel(f"{t('flt.phase')} (°)")
        a2.set_xlabel(f"{t('plot.freq')} (Hz)")
        for ax in (a1, a2):
            ax.grid(True, which="both", alpha=0.4)
            if mark:
                ax.axvline(mark, color="grey", linestyle="--")
        fig.suptitle(title)
        fig.tight_layout()
        fig.savefig(path)
        plt.close(fig)
        return path
    w = W - MARGIN_L - MARGIN_R
    h = (H - MARGIN_T - MARGIN_B - 30) / 2
    top = _Panel(MARGIN_L, MARGIN_T, w, h, freqs, gains, True, f"{t('flt.gain')} (dB)", "", "Hz", "line")
    bottom = _Panel(MARGIN_L, MARGIN_T + h + 30, w, h, freqs, phases, True, f"{t('flt.phase')} (°)",
                    f"{t('plot.freq')}", "Hz", "phase")
    if mark:
        top.vmark(mark)
        bottom.vmark(mark)
    path.write_text(_svg(title, [top, bottom]), encoding="utf-8")
    return path


def curve(path: Path, title: str, xs: Sequence[float], ys: Sequence[float],
          x_label: str, x_unit: str, y_label: str) -> Path:
    suffix = _check_suffix(path)
    if suffix != ".svg":
        plt = _matplotlib()
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(xs, ys)
        ax.set_xlabel(f"{x_label} ({x_unit})")
        ax.set_ylabel(y_label)
        ax.grid(True, alpha=0.4)
        ax.set_title(title)
        fig.tight_layout()
        fig.savefig(path)
        plt.close(fig)
        return path
    panel = _Panel(MARGIN_L, MARGIN_T, W - MARGIN_L - MARGIN_R, H - MARGIN_T - MARGIN_B, xs, ys, False,
                   y_label, x_label, x_unit, "line")
    path.write_text(_svg(title, [panel]), encoding="utf-8")
    return path


def spectrum(path: Path, title: str, freqs: Sequence[float], levels: Sequence[float], y_label: str) -> Path:
    """Genlik spektrumu: logaritmik frekans ekseni, dB cinsinden seviye."""
    suffix = _check_suffix(path)
    if suffix != ".svg":
        plt = _matplotlib()
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.semilogx(freqs, levels)
        ax.set_xlabel(f"{t('plot.freq')} (Hz)")
        ax.set_ylabel(y_label)
        ax.grid(True, which="both", alpha=0.4)
        ax.set_title(title)
        fig.tight_layout()
        fig.savefig(path)
        plt.close(fig)
        return path
    panel = _Panel(MARGIN_L, MARGIN_T, W - MARGIN_L - MARGIN_R, H - MARGIN_T - MARGIN_B, freqs, levels, True,
                   y_label, t("plot.freq"), "Hz", "line")
    path.write_text(_svg(title, [panel]), encoding="utf-8")
    return path


PALETTE = ["#1f6feb", "#d9480f", "#2f9e44", "#ae3ec9", "#f08c00", "#0c8599", "#e03131", "#495057"]


def multi(path: Path, title: str, xs: Sequence[float], series: Sequence[tuple], x_label: str, x_unit: str,
          y_label: str, log_x: bool = False) -> Path:
    """Aynı eksende birden çok eğri: series = [(ad, ys), …]."""
    suffix = _check_suffix(path)
    if suffix != ".svg":
        plt = _matplotlib()
        fig, ax = plt.subplots(figsize=(8, 5))
        for name, ys in series:
            (ax.semilogx if log_x else ax.plot)(xs, ys, label=name)
        ax.set_xlabel(f"{x_label} ({x_unit})")
        ax.set_ylabel(y_label)
        ax.grid(True, which="both", alpha=0.4)
        ax.legend()
        ax.set_title(title)
        fig.tight_layout()
        fig.savefig(path)
        plt.close(fig)
        return path
    colored = [(list(ys), PALETTE[i % len(PALETTE)]) for i, (_, ys) in enumerate(series)]
    panel = _Panel(MARGIN_L, MARGIN_T, W - MARGIN_L - MARGIN_R, H - MARGIN_T - MARGIN_B, xs,
                   colored[0][0] if colored else [0.0] * len(xs), log_x, y_label, x_label, x_unit, "line",
                   series=colored)
    x = MARGIN_L + 8
    for (name, _), (_, color) in zip(series, colored):
        panel.parts.append(f'<rect x="{x}" y="{MARGIN_T + 6}" width="10" height="10" fill="{color}"/>'
                           f'<text x="{x + 14}" y="{MARGIN_T + 15}">{escape(name)}</text>')
        x += 24 + 7 * len(name)
    path.write_text(_svg(title, [panel]), encoding="utf-8")
    return path
