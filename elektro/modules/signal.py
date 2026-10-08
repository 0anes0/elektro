"""Sinyal analizi: dalga şekli RMS/ortalama/tepe faktörü ve CSV verisinden FFT."""

from __future__ import annotations

import cmath
import importlib.util
import math
from pathlib import Path
from typing import Callable, List, Optional

import typer
from rich.table import Table

from elektro.i18n import pct, t
from elektro.plot import PlotError, curve, plot_path, spectrum
from elektro.ui import cli_parser, console, eng, fail, json_mode, plot_saved, result_panel, theory, warn
from elektro.units import format_si

TWO_PI = 2 * math.pi

# --- Dalga şekilleri ------------------------------------------------------------------------

# x: periyot içindeki konum [0, 1), a: tepe genliği, d: doluluk oranı (0…1)
SHAPES = {
    "sine": lambda x, a, d: a * math.sin(TWO_PI * x),
    "square": lambda x, a, d: a if x < d else -a,
    "triangle": lambda x, a, d: a * (1 - 4 * abs(x - 0.5)),
    "sawtooth": lambda x, a, d: a * (2 * x - 1),
    "pwm": lambda x, a, d: a if x < d else 0.0,
    "halfwave": lambda x, a, d: max(0.0, a * math.sin(TWO_PI * x)),
    "fullwave": lambda x, a, d: abs(a * math.sin(TWO_PI * x)),
}
UNIPOLAR = {"pwm", "halfwave", "fullwave"}


def stats(samples: List[float]) -> dict:
    """Örneklerden DC, RMS, AC RMS, doğrultulmuş ortalama, tepe faktörü, biçim faktörü."""
    n = len(samples)
    mean = sum(samples) / n
    rms = math.sqrt(sum(v * v for v in samples) / n)
    rect = sum(abs(v) for v in samples) / n
    hi, lo = max(samples), min(samples)
    ac_rms = math.sqrt(max(rms * rms - mean * mean, 0.0))
    peak = max(abs(hi), abs(lo))
    return {"max": hi, "min": lo, "vpp": hi - lo, "dc": mean, "rms": rms, "ac_rms": ac_rms, "rect_avg": rect,
            "crest": peak / rms if rms else math.inf, "form": rms / rect if rect else math.inf}


def sample_wave(shape: str, amplitude: float, duty: float, offset: float, n: int = 100_000) -> List[float]:
    fn = SHAPES[shape]
    return [fn((i + 0.5) / n, amplitude, duty) + offset for i in range(n)]


def wave_stats(shape: str, amplitude: float, duty: float = 0.5, offset: float = 0.0) -> dict:
    out = stats(sample_wave(shape, amplitude, duty, offset))
    # Tepe değerleri orta noktalarda tam yakalanmaz: köşe noktalarını da yokla
    fn = SHAPES[shape]
    edges = [i / 1000 for i in range(1000)] + [1 - 1e-12, duty - 1e-12]
    extra = [fn(x, amplitude, duty) + offset for x in edges]
    out["max"], out["min"] = max(out["max"], *extra), min(out["min"], *extra)
    out["vpp"] = out["max"] - out["min"]
    peak = max(abs(out["max"]), abs(out["min"]))
    out["crest"] = peak / out["rms"] if out["rms"] else math.inf
    # örneklemenin sayısal artıklarını temizle (ör. sinüsün DC'si 1e-17)
    scale = max(peak, 1e-30)
    return {k: (0.0 if abs(v) < scale * 1e-9 else float(f"{v:.9g}")) if math.isfinite(v) else v
            for k, v in out.items()}


def _ascii_wave(fn: Callable[[float], float], lo: float, hi: float, width: int = 48, height: int = 7) -> str:
    """İki periyotluk küçük metin grafiği (kutu çizgileriyle; raporda kod bloğu olur)."""
    span = (hi - lo) or 1.0
    grid = [[" "] * width for _ in range(height)]
    for col in range(width):
        v = fn(2 * (col + 0.5) / width % 1.0)
        row = height - 1 - round((v - lo) / span * (height - 1))
        grid[row][col] = "•"
    zero = height - 1 - round((0 - lo) / span * (height - 1)) if lo <= 0 <= hi else None
    lines = []
    for r, cells in enumerate(grid):
        label = f"{hi:>8.3g} ┤" if r == 0 else f"{lo:>8.3g} ┤" if r == height - 1 else \
            f"{0:>8g} ┤" if r == zero else " " * 8 + " │"
        if r == zero:
            cells = [c if c != " " else "─" for c in cells]
        lines.append(label + "".join(cells))
    return "\n".join(lines)


def wave(
    shape: str = typer.Argument(..., metavar="|".join(SHAPES), help=t("wave.arg")),
    vp: Optional[float] = typer.Option(None, "--vp", **eng(t("wave.opt.vp"))),
    vpp: Optional[float] = typer.Option(None, "--vpp", **eng(t("wave.opt.vpp"))),
    rms: Optional[float] = typer.Option(None, "--rms", **eng(t("wave.opt.rms"))),
    offset: float = typer.Option(0, "--offset", **eng(t("wave.opt.offset"))),
    duty: float = typer.Option(50, "--duty", "-d", help=t("wave.opt.duty")),
    freq: Optional[float] = typer.Option(None, "--freq", "-f", **eng(t("wave.opt.freq"))),
    load: Optional[float] = typer.Option(None, "--load", "-r", **eng(t("wave.opt.load"))),
    unit: str = typer.Option("V", "--unit", "-u", help=t("wave.opt.unit")),
    plot: Optional[Path] = typer.Option(None, "--plot", parser=cli_parser(plot_path), metavar=t("plot.metavar"),
                                        help=t("plot.opt")),
):
    shape = shape.lower()
    if shape not in SHAPES:
        fail(t("wave.bad_shape", options=", ".join(SHAPES)))
    if sum(x is not None for x in (vp, vpp, rms)) != 1:
        fail(t("wave.need"))
    if not 0 < duty < 100 or (freq is not None and freq <= 0) or (load is not None and load <= 0):
        fail(t("wave.bad"))
    d = duty / 100
    if vp is not None:
        amplitude = vp
    elif vpp is not None:
        amplitude = vpp if shape in UNIPOLAR else vpp / 2
    else:
        amplitude = rms / wave_stats(shape, 1.0, d)["rms"]
    if amplitude <= 0:
        fail(t("common.positive"))
    s = wave_stats(shape, amplitude, d, offset)
    rows = {
        t("wave.shape"): t(f"wave.kind.{shape}") + (f", D = {pct(f'{duty:g}')}" if shape in ("pwm", "square") else ""),
        t("wave.peak"): f"{format_si(s['max'], unit)} / {format_si(s['min'], unit)}",
        t("wave.vpp"): format_si(s["vpp"], unit),
        t("wave.dc"): format_si(s["dc"], unit),
        t("wave.rms"): format_si(s["rms"], unit),
        t("wave.ac_rms"): format_si(s["ac_rms"], unit),
        t("wave.rect"): format_si(s["rect_avg"], unit),
        t("wave.crest"): f"{s['crest']:.4g}",
        t("wave.form"): f"{s['form']:.4g}" if math.isfinite(s["form"]) else "-",
    }
    data = {"shape": shape, "amplitude": amplitude, "offset": offset, "duty": d, **s}
    if freq is not None:
        rows[t("wave.period")] = format_si(1 / freq, "s")
        data["period_s"] = 1 / freq
        if shape in ("pwm", "square"):
            rows[t("wave.t_high")] = format_si(d / freq, "s")
            data["t_high_s"] = d / freq
    if load is not None:
        p = s["rms"] ** 2 / load
        rows[t("wave.power", r=format_si(load, "Ω"))] = format_si(p, "W")
        data["power_w"] = p
    result_panel(t("wave.title"), rows, data=data)

    fn = SHAPES[shape]
    if plot is not None:
        period = 1 / freq if freq else 1.0
        xs = [2 * period * i / 800 for i in range(801)]
        try:
            out = curve(plot, t(f"wave.kind.{shape}"), xs, [fn(x / period % 1.0, amplitude, d) + offset for x in xs],
                        t("plot.time"), "s" if freq else "T", unit)
        except (PlotError, OSError) as e:
            fail(str(e))
        plot_saved(out)
    if not json_mode():
        console.print(_ascii_wave(lambda x: fn(x, amplitude, d) + offset, min(s["min"], 0), max(s["max"], 0)))
    theory(t("wave.note1"), t("wave.note2"))


# --- CSV okuma ------------------------------------------------------------------------------

def _num(text: str) -> Optional[float]:
    try:
        v = float(text)
    except ValueError:
        return None
    return v if math.isfinite(v) else None


def _split(line: str, sep: Optional[str]) -> List[str]:
    if sep is None:
        return line.split()
    return [f.strip().strip('"') for f in line.split(sep)]


def _detect_sep(lines: List[str]) -> Optional[str]:
    sample = "\n".join(lines[:200])
    for sep in (";", "\t", ","):
        if sep in sample:
            return sep
    return None


def read_csv(path: Path) -> dict:
    """Osiloskop/veri kaydedici CSV'si: sayısal sütunlar, varsa zaman adımı ('Increment').

    Satırın sonundaki sayısal alanlar alınır (Tektronix gibi baştaki meta veri sütunları atlanır).
    """
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as e:
        raise ValueError(str(e))
    sep = _detect_sep(lines)
    rows: List[List[float]] = []
    names: List[str] = []
    dt = None
    prev_header: List[str] = []
    for line in lines:
        if not line.strip():
            continue
        fields = _split(line, sep)
        if sep == ";":
            fields = [f.replace(",", ".") for f in fields]
        numeric = []
        for f in reversed(fields):
            if f == "":
                continue
            v = _num(f)
            if v is None:
                break
            numeric.append(v)
        numeric.reverse()
        fully_numeric = all(f == "" or _num(f) is not None for f in fields)
        if not fully_numeric:
            lowered = [f.lower() for f in prev_header]
            if "increment" in lowered:              # Rigol: "X,CH1,Start,Increment" + değer satırı
                i = lowered.index("increment")
                if i < len(fields) and _num(fields[i]) is not None:
                    dt = _num(fields[i])
                    prev_header = []
                    continue
            prev_header = fields
            if not numeric and not names:
                names = [f for f in fields if f]
            if not numeric:
                continue
        if numeric:
            rows.append(numeric)
    if not rows:
        raise ValueError(t("fft.no_data"))
    widths = {}
    for r in rows:
        widths[len(r)] = widths.get(len(r), 0) + 1
    width = max(widths, key=widths.get)
    data = [r for r in rows if len(r) == width]
    columns = [list(c) for c in zip(*data)]
    return {"columns": columns, "names": names[:width] if len(names) >= width else [], "dt": dt}


def _uniform_step(times: List[float]) -> Optional[float]:
    if len(times) < 3:
        return None
    steps = [b - a for a, b in zip(times, times[1:])]
    if min(steps) <= 0:
        return None
    steps.sort()
    return steps[len(steps) // 2]


# --- FFT --------------------------------------------------------------------------------------

def fft(values: List[complex]) -> List[complex]:
    """Yinelemeli radix-2 FFT (uzunluk 2'nin kuvveti olmalı)."""
    n = len(values)
    a = list(values)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    size = 2
    while size <= n:
        half = size // 2
        tw = [cmath.exp(-2j * math.pi * k / size) for k in range(half)]
        for start in range(0, n, size):
            for k in range(half):
                u = a[start + k]
                v = a[start + k + half] * tw[k]
                a[start + k] = u + v
                a[start + k + half] = u - v
        size *= 2
    return a


def _rfft_mag2(x: List[float]) -> List[float]:
    """Tek taraflı |X_k|² (k = 0 … n/2). numpy varsa onu kullanır."""
    try:
        import numpy as np
        return list(np.abs(np.fft.rfft(np.asarray(x))) ** 2)
    except ImportError:
        spec = fft([complex(v) for v in x])
        return [abs(c) ** 2 for c in spec[: len(x) // 2 + 1]]


WINDOWS = {
    "rect": (lambda i, n: 1.0, 1),
    "hann": (lambda i, n: 0.5 - 0.5 * math.cos(TWO_PI * i / n), 3),
    "hamming": (lambda i, n: 0.54 - 0.46 * math.cos(TWO_PI * i / n), 3),
    "blackman": (lambda i, n: 0.42 - 0.5 * math.cos(TWO_PI * i / n) + 0.08 * math.cos(2 * TWO_PI * i / n), 4),
    "flattop": (lambda i, n: (0.21557895 - 0.41663158 * math.cos(TWO_PI * i / n)
                              + 0.277263158 * math.cos(2 * TWO_PI * i / n)
                              - 0.083578947 * math.cos(3 * TWO_PI * i / n)
                              + 0.006947368 * math.cos(4 * TWO_PI * i / n)), 5),
}
MAX_POINTS = 1 << 18


def spectrum_of(x: List[float], fs: float, window: str = "hann") -> dict:
    """Pencereli genlik spektrumu. Genlikler tepe değeridir (sinüs için A)."""
    n = len(x)
    if importlib.util.find_spec("numpy") is not None:       # numpy varsa her uzunluk olur
        use = min(n, MAX_POINTS * 4)
    else:
        use = 1 << (min(n, MAX_POINTS).bit_length() - 1)      # 2'nin kuvveti
    x = x[:use]
    mean = sum(x) / use
    wfn, lobe = WINDOWS[window]
    w = [wfn(i, use) for i in range(use)]
    sw2 = sum(v * v for v in w)
    mag2 = _rfft_mag2([(v - mean) * wi for v, wi in zip(x, w)])
    return {"mag2": mag2, "n": use, "fs": fs, "df": fs / use, "dc": mean, "sw2": sw2, "lobe": lobe,
            "window": window}


def tone(spec: dict, k: int) -> dict:
    """k. kutu çevresindeki ana lobun enerjisinden genlik ve (parabolik) frekans."""
    mag2, lobe, n = spec["mag2"], spec["lobe"], spec["n"]
    lo, hi = max(1, k - lobe), min(len(mag2) - 1, k + lobe)
    energy = sum(mag2[lo:hi + 1])
    amplitude = 2 * math.sqrt(energy / (n * spec["sw2"]))
    # Parabolik ara değerleme (log genlik)
    f = k
    if 0 < k < len(mag2) - 1 and min(mag2[k - 1:k + 2]) > 0:
        a, b, c = (math.log(mag2[k - 1]), math.log(mag2[k]), math.log(mag2[k + 1]))
        den = a - 2 * b + c
        if den < 0:
            f = k + 0.5 * (a - c) / den
    return {"f_hz": f * spec["df"], "amplitude": amplitude, "rms": amplitude / math.sqrt(2), "bin": k}


def find_peaks(spec: dict, count: int) -> List[dict]:
    mag2, lobe = spec["mag2"], spec["lobe"]
    start = lobe + 1                         # DC lobunu atla
    candidates = [k for k in range(start, len(mag2) - 1) if mag2[k] >= mag2[k - 1] and mag2[k] > mag2[k + 1]]
    candidates.sort(key=lambda k: mag2[k], reverse=True)
    top = mag2[candidates[0]] if candidates else 0
    picked: List[int] = []
    for k in candidates:
        if top and mag2[k] < top * 1e-10:     # -100 dB altını gürültü say
            break
        if all(abs(k - p) > 2 * lobe for p in picked):
            picked.append(k)
        if len(picked) == count:
            break
    return [tone(spec, k) for k in picked]


def harmonics(spec: dict, f0: float, count: int = 10) -> List[dict]:
    out = []
    nyq = spec["fs"] / 2
    for h in range(2, count + 1):
        f = h * f0
        if f >= nyq - spec["df"] * spec["lobe"]:
            break
        k0 = round(f / spec["df"])
        lo, hi = max(1, k0 - 2), min(len(spec["mag2"]) - 2, k0 + 2)
        k = max(range(lo, hi + 1), key=lambda i: spec["mag2"][i])
        out.append({"n": h, **tone(spec, k)})
    return out


def analyze(x: List[float], fs: float, window: str = "hann", peaks: int = 5) -> dict:
    if len(x) < 16:
        raise ValueError(t("fft.too_short"))
    spec = spectrum_of(x, fs, window)
    found = find_peaks(spec, peaks)
    result = {"fs_hz": fs, "samples": len(x), "used": spec["n"], "df_hz": spec["df"], "window": window,
              "time": stats(x[:spec["n"]]), "peaks": found, "spec": spec}
    if found:
        f0 = found[0]
        hs = harmonics(spec, f0["f_hz"])
        a1 = f0["amplitude"]
        thd = math.sqrt(sum(h["amplitude"] ** 2 for h in hs)) / a1 if a1 else None
        ac_rms = result["time"]["ac_rms"]
        thdn = math.sqrt(max(ac_rms ** 2 - (a1 / math.sqrt(2)) ** 2, 0)) / (a1 / math.sqrt(2)) if a1 else None
        result.update(fundamental=f0, harmonics=hs, thd=thd, thdn=thdn)
    return result


def _db(x: float) -> float:
    return 20 * math.log10(x) if x > 0 else -math.inf


def _decimate_log(spec: dict, buckets: int = 900) -> tuple:
    """SVG için: logaritmik aralıklarla kutuların en büyüğü."""
    df, mag2, n, sw2 = spec["df"], spec["mag2"], spec["n"], spec["sw2"]
    k_max = len(mag2) - 1
    edges = [10 ** (math.log10(1) + (math.log10(k_max)) * i / buckets) for i in range(buckets + 1)]
    xs, ys, last = [], [], 0
    for lo, hi in zip(edges, edges[1:]):
        a, b = max(int(lo), last + 1), int(hi)
        if b < a:
            continue
        k = max(range(a, b + 1), key=lambda i: mag2[i])
        last = b
        xs.append(k * df)
        ys.append(max(_db(2 * math.sqrt(mag2[k] / (n * sw2))), -200))
    return xs, ys


def fft_cmd(
    file: Path = typer.Argument(..., exists=True, dir_okay=False, help=t("fft.arg")),
    column: Optional[int] = typer.Option(None, "--column", "-c", help=t("fft.opt.column")),
    rate: Optional[float] = typer.Option(None, "--rate", **eng(t("fft.opt.rate"))),
    window: str = typer.Option("hann", "--window", "-w", help=t("fft.opt.window", options=", ".join(WINDOWS))),
    peaks: int = typer.Option(6, "--peaks", "-n", help=t("fft.opt.peaks")),
    unit: str = typer.Option("V", "--unit", "-u", help=t("wave.opt.unit")),
    plot: Optional[Path] = typer.Option(None, "--plot", parser=cli_parser(plot_path), metavar=t("plot.metavar"),
                                        help=t("plot.opt")),
):
    window = window.lower()
    if window not in WINDOWS:
        fail(t("fft.bad_window", options=", ".join(WINDOWS)))
    if peaks < 1 or (rate is not None and rate <= 0):
        fail(t("common.positive_all"))
    try:
        csv = read_csv(file)
    except ValueError as e:
        fail(str(e))
    cols = csv["columns"]
    width = len(cols)
    col = column if column is not None else (2 if width >= 2 else 1)
    if not 1 <= col <= width:
        fail(t("fft.bad_column", n=width))
    values = cols[col - 1]
    source = t("fft.src.rate")
    if rate is not None:
        fs = rate
    elif csv["dt"]:
        fs, source = 1 / csv["dt"], t("fft.src.header")
    else:
        step = _uniform_step(cols[0]) if width >= 2 and col != 1 else None
        if step is None:
            fail(t("fft.need_rate"))
        fs, source = 1 / step, t("fft.src.time")
        if step == 1 and all(float(v).is_integer() for v in cols[0][:50]):
            warn(t("fft.index_col"))
    try:
        r = analyze(values, fs, window, peaks)
    except ValueError as e:
        fail(str(e))

    name = csv["names"][col - 1] if len(csv["names"]) == width else f"#{col}"
    ts = r["time"]
    rows = {
        t("fft.file"): f"{file.name}  ({name})",
        t("fft.fs"): f"{format_si(fs, 'Hz')}  ({source})",
        t("fft.samples"): f"{r['samples']}" + (f"  → {r['used']}" if r["used"] != r["samples"] else ""),
        t("fft.resolution"): format_si(r["df_hz"], "Hz"),
        t("wave.dc"): format_si(ts["dc"], unit),
        t("wave.rms"): f"{format_si(ts['rms'], unit)}  (AC: {format_si(ts['ac_rms'], unit)})",
        t("wave.vpp"): format_si(ts["vpp"], unit),
        t("wave.crest"): f"{ts['crest']:.3g}",
    }
    if r.get("fundamental"):
        f0 = r["fundamental"]
        rows[t("fft.fundamental")] = f"{format_si(f0['f_hz'], 'Hz')}  {format_si(f0['amplitude'], unit)} " \
                                     f"({format_si(f0['rms'], unit)} RMS)"
        if r["thd"] is not None:
            thd_txt = pct(f"{r['thd'] * 100:.3g}")
            rows["THD"] = f"{thd_txt}  ({_db(r['thd']):.1f} dB)" if r["thd"] > 0 else "0"
            rows["THD+N"] = pct(f"{r['thdn'] * 100:.3g}")
    data = {k: v for k, v in r.items() if k != "spec"}
    data.update(file=str(file), column=col, unit=unit)
    result_panel(t("fft.title"), rows, data=data)

    if r["peaks"] and not json_mode():
        a1 = r["peaks"][0]["amplitude"]
        f1 = r["peaks"][0]["f_hz"]
        tbl = Table(title=t("fft.peaks"), box=None, header_style="bold")
        tbl.add_column("f", justify="right")
        tbl.add_column(t("fft.amp"), justify="right")
        tbl.add_column("dBc", justify="right")
        tbl.add_column("n", justify="right", style="dim")
        tbl.add_column("", no_wrap=True)
        for p in sorted(r["peaks"], key=lambda p: p["f_hz"]):
            rel = _db(p["amplitude"] / a1)
            ratio = p["f_hz"] / f1
            harm = f"{round(ratio)}×" if abs(ratio - round(ratio)) < 0.02 and ratio > 0.5 else ""
            bar = "█" * max(0, round((rel + 80) / 80 * 30))
            tbl.add_row(format_si(p["f_hz"], "Hz"), format_si(p["amplitude"], unit), f"{rel:.1f}", harm,
                        f"[{'bold yellow' if p is r['peaks'][0] else 'green'}]{bar}[/]")
        console.print()
        console.print(tbl)
    if plot is not None:
        xs, ys = _decimate_log(r["spec"])
        try:
            out = spectrum(plot, f"FFT — {file.name}", xs, ys, f"{t('fft.amp')} (dB{unit})")
        except (PlotError, OSError) as e:
            fail(str(e))
        plot_saved(out)
    theory(t("fft.note", window=window))
