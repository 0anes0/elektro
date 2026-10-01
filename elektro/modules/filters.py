"""RC / RL / LC / RLC filtre analizi."""

from __future__ import annotations

import cmath
import math
from pathlib import Path
from typing import Callable, Optional

import typer
from rich.panel import Panel
from rich.table import Table

from elektro.i18n import t
from elektro.plot import PlotError, bode, logspace, plot_path
from elektro.ui import cli_parser, console, eng, fail, json_mode, plot_saved, result_panel, theory
from elektro.units import format_si

app = typer.Typer(help=t("flt.help"), no_args_is_help=True)

TWO_PI = 2 * math.pi


def db(x: float) -> float:
    return 20 * math.log10(x) if x > 0 else -math.inf


def response(h: Callable[[float], complex], f0: float,
             points=(0.1, 0.25, 0.5, 0.8, 1, 1.25, 2, 4, 10)) -> list:
    """Seçili frekanslarda genlik (dB) ve faz (°)."""
    out = []
    for mult in points:
        f = f0 * mult
        val = h(f)
        g = db(abs(val)) if abs(val) > 1e-6 else -math.inf
        out.append({"f_hz": f, "gain_db": g, "phase_deg": math.degrees(cmath.phase(val)), "_mult": mult})
    return out


def print_response(points: list) -> None:
    """Frekans yanıtını metin tabanlı grafikle yazdırır."""
    if json_mode():
        return
    tbl = Table(title=t("flt.response"), box=None, header_style="bold")
    tbl.add_column("f", justify="right")
    tbl.add_column(t("flt.gain"), justify="right")
    tbl.add_column(t("flt.phase"), justify="right")
    tbl.add_column("", no_wrap=True)
    for p in points:
        g = p["gain_db"]
        # 0 dB'de 30 karakter, -60 dB'de 0 karakter
        width = max(0, min(30, round((g + 60) / 2))) if g != -math.inf else 0
        style = "bold yellow" if p["_mult"] == 1 else "green"
        tbl.add_row(
            format_si(p["f_hz"], "Hz"), f"{g:6.1f} dB" if g != -math.inf else "  -∞ dB",
            f"{p['phase_deg']:6.1f}°", f"[{style}]{'█' * width}[/]",
        )
    console.print()
    console.print(tbl)


def _public(points: list) -> list:
    return [{k: v for k, v in p.items() if not k.startswith("_")} for p in points]


def _plot_opt():
    return typer.Option(None, "--plot", parser=cli_parser(plot_path), metavar=t("plot.metavar"), help=t("plot.opt"))


def save_plot(path: Optional[Path], h: Callable[[float], complex], f0: float, title: str) -> None:
    """--plot verildiyse f0/100 … f0·100 aralığında Bode grafiği kaydeder."""
    if path is None:
        return
    freqs = logspace(f0 / 100, f0 * 100, 401)
    vals = [h(f) for f in freqs]
    gains = [db(abs(v)) if abs(v) > 1e-6 else -math.inf for v in vals]
    phases = [math.degrees(cmath.phase(v)) for v in vals]
    try:
        out = bode(path, title, freqs, gains, phases, mark=f0)
    except (PlotError, OSError) as e:
        fail(str(e))
    plot_saved(out)


def _solve_first_order(r, x, fc, x_name, x_to_fc, fc_to_x, fc_to_r):
    """R, X (C veya L), fc'den ikisi verilince üçüncüsünü bulur."""
    if sum(v is not None for v in (r, x, fc)) != 2:
        fail(t("flt.need_two", opts=f"--r, --{x_name}, --fc"))
    if any(v is not None and v <= 0 for v in (r, x, fc)):
        fail(t("common.positive_all"))
    if fc is None:
        fc = x_to_fc(r, x)
    elif x is None:
        x = fc_to_x(r, fc)
    else:
        r = fc_to_r(x, fc)
    return r, x, fc


@app.command(help=t("flt.rc.help"))
def rc(
    r: Optional[float] = typer.Option(None, "--r", **eng(t("flt.opt.r"))),
    c: Optional[float] = typer.Option(None, "--c", **eng(t("flt.opt.c"))),
    fc: Optional[float] = typer.Option(None, "--fc", **eng(t("flt.opt.fc"))),
    high: bool = typer.Option(False, "--high", "-H", help=t("flt.rc.opt.high")),
    plot: Optional[Path] = _plot_opt(),
):
    r, c, fc = _solve_first_order(
        r, c, fc, "c",
        x_to_fc=lambda r, c: 1 / (TWO_PI * r * c),
        fc_to_x=lambda r, fc: 1 / (TWO_PI * r * fc),
        fc_to_r=lambda c, fc: 1 / (TWO_PI * c * fc),
    )
    if high:
        h = lambda f: 1j * f / fc / (1 + 1j * f / fc)
    else:
        h = lambda f: 1 / (1 + 1j * f / fc)
    resp = response(h, fc)
    result_panel(t("flt.rc.title_high" if high else "flt.rc.title_low"), {
        t("flt.fc"): format_si(fc, "Hz"),
        t("flt.omega"): format_si(TWO_PI * fc, "rad/s"),
        t("flt.tau"): format_si(r * c, "s"),
        t("flt.r"): format_si(r, "Ω"),
        t("flt.c"): format_si(c, "F"),
    }, data={"type": "highpass" if high else "lowpass", "fc_hz": fc, "tau_s": r * c,
             "r_ohm": r, "c_f": c, "response": _public(resp)})
    print_response(resp)
    save_plot(plot, h, fc, t("flt.rc.title_high" if high else "flt.rc.title_low"))
    theory(t("flt.rc.note1", phase="+45°" if high else "-45°"), t("flt.rc.note2"))


@app.command(help=t("flt.rl.help"))
def rl(
    r: Optional[float] = typer.Option(None, "--r", **eng(t("flt.opt.r"))),
    l: Optional[float] = typer.Option(None, "--l", **eng(t("flt.opt.l"))),
    fc: Optional[float] = typer.Option(None, "--fc", **eng(t("flt.opt.fc"))),
    low: bool = typer.Option(False, "--low", "-L", help=t("flt.rl.opt.low")),
    plot: Optional[Path] = _plot_opt(),
):
    r, l, fc = _solve_first_order(
        r, l, fc, "l",
        x_to_fc=lambda r, l: r / (TWO_PI * l),
        fc_to_x=lambda r, fc: r / (TWO_PI * fc),
        fc_to_r=lambda l, fc: TWO_PI * fc * l,
    )
    if low:
        h = lambda f: 1 / (1 + 1j * f / fc)
    else:
        h = lambda f: 1j * f / fc / (1 + 1j * f / fc)
    resp = response(h, fc)
    result_panel(t("flt.rl.title_low" if low else "flt.rl.title_high"), {
        t("flt.fc"): format_si(fc, "Hz"),
        t("flt.tau"): format_si(l / r, "s"),
        t("flt.r"): format_si(r, "Ω"),
        t("flt.l"): format_si(l, "H"),
    }, data={"type": "lowpass" if low else "highpass", "fc_hz": fc, "tau_s": l / r,
             "r_ohm": r, "l_h": l, "response": _public(resp)})
    print_response(resp)
    save_plot(plot, h, fc, t("flt.rl.title_low" if low else "flt.rl.title_high"))


@app.command(help=t("flt.lc.help"))
def lc(
    l: Optional[float] = typer.Option(None, "--l", **eng(t("flt.opt.l"))),
    c: Optional[float] = typer.Option(None, "--c", **eng(t("flt.opt.c"))),
    f: Optional[float] = typer.Option(None, "--f", **eng(t("flt.opt.f0"))),
):
    if sum(v is not None for v in (l, c, f)) != 2:
        fail(t("flt.need_two", opts="--l, --c, --f"))
    if any(v is not None and v <= 0 for v in (l, c, f)):
        fail(t("common.positive_all"))
    if f is None:
        f = 1 / (TWO_PI * math.sqrt(l * c))
    elif l is None:
        l = 1 / ((TWO_PI * f) ** 2 * c)
    else:
        c = 1 / ((TWO_PI * f) ** 2 * l)
    result_panel(t("flt.lc.title"), {
        t("flt.f0"): format_si(f, "Hz"),
        t("flt.lc.reactance"): format_si(TWO_PI * f * l, "Ω"),
        t("flt.lc.z0"): format_si(math.sqrt(l / c), "Ω"),
        t("flt.l"): format_si(l, "H"),
        t("flt.c"): format_si(c, "F"),
    }, data={"f0_hz": f, "reactance_ohm": TWO_PI * f * l, "z0_ohm": math.sqrt(l / c),
             "l_h": l, "c_f": c})
    theory(t("flt.lc.note"))


@app.command(help=t("flt.rlc.help"))
def rlc(
    r: float = typer.Option(..., "--r", **eng(t("flt.opt.r"))),
    l: float = typer.Option(..., "--l", **eng(t("flt.opt.l"))),
    c: float = typer.Option(..., "--c", **eng(t("flt.opt.c"))),
    plot: Optional[Path] = _plot_opt(),
):
    f0 = 1 / (TWO_PI * math.sqrt(l * c))
    bw = r / (TWO_PI * l)
    q = f0 / bw
    # -3 dB noktaları (asimetrik, kesin formül)
    half = bw / 2
    f_lo = -half + math.sqrt(half ** 2 + f0 ** 2)
    f_hi = half + math.sqrt(half ** 2 + f0 ** 2)
    h = lambda f: r / (r + 1j * TWO_PI * f * l + 1 / (1j * TWO_PI * f * c))
    resp = response(h, f0)
    result_panel(t("flt.rlc.title"), {
        t("flt.center"): format_si(f0, "Hz"),
        t("flt.bw"): format_si(bw, "Hz"),
        t("flt.q"): f"{q:.3g}",
        t("flt.lower"): format_si(f_lo, "Hz"),
        t("flt.upper"): format_si(f_hi, "Hz"),
    }, data={"f0_hz": f0, "bandwidth_hz": bw, "q": q, "f_low_hz": f_lo, "f_high_hz": f_hi,
             "response": _public(resp)})
    print_response(resp)
    save_plot(plot, h, f0, t("flt.rlc.title"))
    theory(t("flt.rlc.note"))


@app.command(help=t("flt.notch.help"))
def notch(
    r: float = typer.Option(..., "--r", **eng(t("flt.notch.opt.r"))),
    l: float = typer.Option(..., "--l", **eng(t("flt.opt.l"))),
    c: float = typer.Option(..., "--c", **eng(t("flt.opt.c"))),
    plot: Optional[Path] = _plot_opt(),
):
    f0 = 1 / (TWO_PI * math.sqrt(l * c))
    q = r / (TWO_PI * f0 * l)
    def h(f):
        w = TWO_PI * f
        denom = 1 - w * w * l * c
        if denom == 0:
            return 0j
        return r / (r + 1j * w * l / denom)

    resp = response(h, f0, points=(0.25, 0.5, 0.8, 0.9, 0.95, 1, 1.05, 1.1, 1.25, 2, 4))
    result_panel(t("flt.notch.title"), {
        t("flt.notch.f0"): format_si(f0, "Hz"),
        t("flt.q"): f"{q:.3g}",
        t("flt.bw"): format_si(f0 / q, "Hz"),
    }, data={"f0_hz": f0, "q": q, "bandwidth_hz": f0 / q, "response": _public(resp)})
    print_response(resp)
    save_plot(plot, h, f0, t("flt.notch.title"))
    theory(t("flt.notch.note"))


@app.command(name="theory", help=t("flt.theory.help"))
def theory_cmd():
    if json_mode():
        return
    console.print(Panel(t("flt.theory.body"), title=f"[bold]{t('flt.theory.title')}[/]",
                        border_style="bright_blue", expand=False))
