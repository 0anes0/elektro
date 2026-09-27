"""RF hesapları: FSPL, link bütçesi, dalga boyu, birim dönüşümleri."""

from __future__ import annotations

import math
from typing import Optional

import typer
from rich.table import Table

from elektro.i18n import pct, t
from elektro.ui import console, fail, result_panel, theory
from elektro.units import format_si, parse_value

app = typer.Typer(help=t("rf.help"), no_args_is_help=True)

C0 = 299_792_458.0


def parse_freq(text: str) -> float:
    """Frekans → Hz. Yalın sayı MHz kabul edilir: '868' = 868 MHz, '2.4G' = 2.4 GHz."""
    try:
        return float(text) * 1e6
    except ValueError:
        return parse_value(text)


def parse_distance(text: str) -> float:
    """Mesafe → metre. Yalın sayı km kabul edilir: '5' = 5 km, '500m' = 500 m."""
    s = text.strip().lower().replace(",", ".")
    try:
        if s.endswith("km"):
            return float(s[:-2]) * 1e3
        if s.endswith("m"):
            return float(s[:-1])
        return float(s) * 1e3
    except ValueError:
        raise ValueError(t("rf.bad_distance", text=text))


def format_distance(m: float) -> str:
    return f"{m / 1e3:.4g} km" if m >= 1e3 else format_si(m, "m")


def fspl_db(freq_hz: float, dist_m: float) -> float:
    return 20 * math.log10(dist_m) + 20 * math.log10(freq_hz) + 20 * math.log10(4 * math.pi / C0)


def max_distance(freq_hz: float, loss_db: float) -> float:
    return 10 ** ((loss_db - 20 * math.log10(freq_hz) - 20 * math.log10(4 * math.pi / C0)) / 20)


def _freq_opt():
    return typer.Option(..., "--freq", "-f", parser=parse_freq, metavar=t("rf.metavar.freq"),
                        help=t("rf.opt.freq"))


def _dist_opt():
    return typer.Option(..., "--dist", "-d", parser=parse_distance, metavar=t("rf.metavar.dist"),
                        help=t("rf.opt.dist"))


@app.command(help=t("rf.fspl.help"))
def fspl(freq: float = _freq_opt(), dist: float = _dist_opt()):
    if freq <= 0 or dist <= 0:
        fail(t("rf.positive"))
    result_panel(t("rf.fspl.title"), {
        t("rf.freq"): format_si(freq, "Hz"),
        t("rf.dist"): format_distance(dist),
        t("rf.wavelength"): format_si(C0 / freq, "m"),
        "FSPL": f"{fspl_db(freq, dist):.2f} dB",
    })
    theory(t("rf.fspl.note"))


@app.command(help=t("rf.link.help"))
def link(
    freq: float = _freq_opt(),
    dist: float = _dist_opt(),
    tx: float = typer.Option(14, "--tx", help=t("rf.link.opt.tx")),
    gtx: float = typer.Option(2.15, "--gtx", help=t("rf.link.opt.gtx")),
    grx: float = typer.Option(2.15, "--grx", help=t("rf.link.opt.grx")),
    sens: float = typer.Option(-120, "--sens", "-s", help=t("rf.link.opt.sens")),
    loss: float = typer.Option(0, "--loss", help=t("rf.link.opt.loss")),
):
    if freq <= 0 or dist <= 0:
        fail(t("rf.positive"))
    path = fspl_db(freq, dist)
    eirp = tx + gtx
    prx = eirp + grx - path - loss
    margin = prx - sens
    budget = tx + gtx + grx - loss - sens
    if margin >= 10:
        color, verdict = "green", t("rf.link.solid")
    elif margin >= 0:
        color, verdict = "yellow", t("rf.link.marginal")
    else:
        color, verdict = "red", t("rf.link.no_link")
    result_panel(t("rf.link.title"), {
        "EIRP": f"{eirp:.1f} dBm ({format_si(10 ** (eirp / 10) / 1000, 'W')})",
        "FSPL": f"{path:.1f} dB",
        t("rf.link.prx"): f"{prx:.1f} dBm",
        t("rf.link.sens"): f"{sens:.1f} dBm",
        t("rf.link.margin"): f"[{color}]{margin:.1f} dB ({verdict})[/]",
        t("rf.link.range0"): format_distance(max_distance(freq, budget)),
        t("rf.link.range10"): format_distance(max_distance(freq, budget - 10)),
    })
    theory(t("rf.link.note1"), t("rf.link.note2"))


@app.command(help=t("rf.wave.help"))
def wave(
    freq: float = typer.Option(..., "--freq", "-f", parser=parse_freq, metavar=t("rf.metavar.freq"),
                               help=t("rf.opt.freq")),
    vf: float = typer.Option(1.0, "--vf", help=t("rf.wave.opt.vf")),
):
    if freq <= 0 or not 0 < vf <= 1:
        fail(t("rf.wave.bad"))
    lam = C0 / freq * vf
    result_panel(t("rf.wave.title"), {
        t("rf.freq"): format_si(freq, "Hz"),
        "λ": format_si(lam, "m"),
        t("rf.wave.dipole"): format_si(lam / 2, "m"),
        t("rf.wave.monopole"): format_si(lam / 4, "m"),
        "5λ/8": format_si(lam * 5 / 8, "m"),
    })


# --- Dönüşümler ------------------------------------------------------------------

POWER_TO_DBM = {
    "dbm": lambda x: x,
    "dbw": lambda x: x + 30,
    "w": lambda x: 10 * math.log10(x * 1e3),
    "mw": lambda x: 10 * math.log10(x),
    "uw": lambda x: 10 * math.log10(x * 1e-3),
}
DBM_TO_POWER = {
    "dbm": lambda d: d,
    "dbw": lambda d: d - 30,
    "w": lambda d: 10 ** (d / 10) / 1e3,
    "mw": lambda d: 10 ** (d / 10),
    "uw": lambda d: 10 ** (d / 10) * 1e3,
}


def gamma_from(unit: str, x: float) -> float:
    if unit == "vswr":
        if x < 1:
            raise ValueError(t("rf.conv.vswr"))
        return (x - 1) / (x + 1)
    if unit == "rl":
        if x < 0:
            raise ValueError(t("rf.conv.rl"))
        return 10 ** (-x / 20)
    if not 0 <= x <= 1:
        raise ValueError(t("rf.conv.gamma"))
    return x


_ALIASES = {"watt": "w", "mwatt": "mw", "µw": "uw", "s11": "rl", "g": "gamma", "Γ": "gamma"}
POWER_UNITS = set(POWER_TO_DBM)
MATCH_UNITS = {"vswr", "rl", "gamma"}


def convert_units(value: float, src: str, dst: Optional[str]):
    src = _ALIASES.get(src.lower(), src.lower())
    dst = _ALIASES.get(dst.lower(), dst.lower()) if dst else None
    if src in POWER_UNITS:
        if src not in ("dbm", "dbw") and value <= 0:
            raise ValueError(t("rf.conv.power_pos"))
        if dst and dst not in POWER_UNITS:
            raise ValueError(t("rf.conv.no_path", src=src, dst=dst))
        dbm = POWER_TO_DBM[src](value)
        targets = [dst] if dst else ["dbm", "dbw", "w", "mw"]
        return {k: DBM_TO_POWER[k](dbm) for k in targets}
    if src in MATCH_UNITS:
        if dst and dst not in MATCH_UNITS:
            raise ValueError(t("rf.conv.no_path", src=src, dst=dst))
        g = gamma_from(src, value)
        vals = {
            "gamma": g,
            "vswr": math.inf if g >= 1 else (1 + g) / (1 - g),
            "rl": math.inf if g == 0 else -20 * math.log10(g),
            "mismatch": math.inf if g >= 1 else -10 * math.log10(1 - g * g),
            "reflected": g * g * 100,
        }
        return {dst: vals[dst]} if dst else vals
    raise ValueError(t("rf.conv.unknown", unit=src))


def _label(key: str) -> tuple:
    return {
        "dbm": ("dBm", None), "dbw": ("dBW", None), "w": ("W", "W"), "mw": ("mW", None),
        "uw": ("µW", None), "gamma": ("|Γ|", None), "vswr": ("VSWR", None),
        "rl": (t("rf.conv.l.rl"), "dB"), "mismatch": (t("rf.conv.l.mismatch"), "dB"),
        "reflected": (t("rf.conv.l.reflected"), "%"),
    }[key]


@app.command(help=t("rf.conv.help"))
def convert(
    value: float = typer.Argument(..., help=t("rf.conv.arg.value")),
    src: str = typer.Argument(..., help=t("rf.conv.arg.src")),
    dst: Optional[str] = typer.Argument(None, help=t("rf.conv.arg.dst")),
):
    try:
        res = convert_units(value, src, dst)
    except ValueError as e:
        fail(str(e))
    tbl = Table(show_header=False, box=None)
    tbl.add_column(style="cyan", justify="right")
    tbl.add_column(style="bold green")
    for key, v in res.items():
        label, unit = _label(key)
        if unit == "W":
            text = format_si(v, "W")
        elif math.isinf(v):
            text = "∞"
        elif unit == "%":
            text = pct(f"{v:.3g}")
        else:
            text = f"{v:.4g}" + (f" {unit}" if unit else "")
        tbl.add_row(label, text)
    console.print(tbl)
