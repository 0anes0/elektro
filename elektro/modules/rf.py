"""RF hesapları: FSPL, link bütçesi, dalga boyu, birim dönüşümleri."""

from __future__ import annotations

import math
from typing import Optional

import typer
from rich.table import Table

from elektro.ui import console, fail, result_panel, theory
from elektro.units import format_si, parse_value

app = typer.Typer(help="RF: FSPL, link bütçesi, dalga boyu ve birim dönüşümleri.", no_args_is_help=True)

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
        raise ValueError(f"'{text}' mesafe olarak anlaşılamadı (örn: 5, 2.5km, 800m)")


def format_distance(m: float) -> str:
    return f"{m / 1e3:.4g} km" if m >= 1e3 else format_si(m, "m")


def fspl_db(freq_hz: float, dist_m: float) -> float:
    return 20 * math.log10(dist_m) + 20 * math.log10(freq_hz) + 20 * math.log10(4 * math.pi / C0)


def max_distance(freq_hz: float, loss_db: float) -> float:
    return 10 ** ((loss_db - 20 * math.log10(freq_hz) - 20 * math.log10(4 * math.pi / C0)) / 20)


FREQ = typer.Option(..., "--freq", "-f", parser=parse_freq, metavar="FREKANS",
                    help="Frekans. Yalın sayı MHz: 868, 2.4G, 433.92M")
DIST = typer.Option(..., "--dist", "-d", parser=parse_distance, metavar="MESAFE",
                    help="Mesafe. Yalın sayı km: 5, 800m, 12km")


@app.command()
def fspl(freq: float = FREQ, dist: float = DIST):
    """Serbest uzay yol kaybı (ITU-R P.525).

    FSPL(dB) = 20·log₁₀(d) + 20·log₁₀(f) + 20·log₁₀(4π/c)

    Örnekler:
      elektro rf fspl -f 868 -d 5
      elektro rf fspl -f 2.4G -d 300m
    """
    if freq <= 0 or dist <= 0:
        fail("frekans ve mesafe pozitif olmalı")
    result_panel("Serbest Uzay Yol Kaybı", {
        "Frekans": format_si(freq, "Hz"),
        "Mesafe": format_distance(dist),
        "Dalga boyu": format_si(C0 / freq, "m"),
        "FSPL": f"{fspl_db(freq, dist):.2f} dB",
    })
    theory("Link marjını görmek için: elektro rf link --help")


@app.command()
def link(
    freq: float = FREQ,
    dist: float = DIST,
    tx: float = typer.Option(14, "--tx", help="Verici gücü (dBm)"),
    gtx: float = typer.Option(2.15, "--gtx", help="Verici anten kazancı (dBi)"),
    grx: float = typer.Option(2.15, "--grx", help="Alıcı anten kazancı (dBi)"),
    sens: float = typer.Option(-120, "--sens", "-s", help="Alıcı hassasiyeti (dBm)"),
    loss: float = typer.Option(0, "--loss", help="Kablo/konnektör/ortam kayıpları toplamı (dB)"),
):
    """Link bütçesi: alınan güç, link marjı ve teorik maksimum menzil.

    Prx = Ptx + Gtx + Grx − FSPL − kayıplar

    Örnekler:
      elektro rf link -f 868 -d 10 --tx 14 --sens -137
      elektro rf link -f 2.4G -d 500m --tx 20 --gtx 5 --grx 5 --sens -90 --loss 3
    """
    path = fspl_db(freq, dist)
    eirp = tx + gtx
    prx = eirp + grx - path - loss
    margin = prx - sens
    budget = tx + gtx + grx - loss - sens
    color = "green" if margin >= 10 else "yellow" if margin >= 0 else "red"
    verdict = "sağlam" if margin >= 10 else "sınırda" if margin >= 0 else "BAĞLANTI YOK"
    result_panel("Link Bütçesi", {
        "EIRP": f"{eirp:.1f} dBm ({format_si(10 ** (eirp / 10) / 1000, 'W')})",
        "FSPL": f"{path:.1f} dB",
        "Alınan güç": f"{prx:.1f} dBm",
        "Hassasiyet": f"{sens:.1f} dBm",
        "Link marjı": f"[{color}]{margin:.1f} dB ({verdict})[/]",
        "Maks. menzil (0 dB marj)": format_distance(max_distance(freq, budget)),
        "Maks. menzil (10 dB marj)": format_distance(max_distance(freq, budget - 10)),
    })
    theory("Serbest uzay varsayımıdır; engeller, Fresnel bölgesi ve sönümleme menzili ciddi azaltır.",
           "Pratikte 10-20 dB marj bırakılması önerilir.")


@app.command()
def wave(
    freq: float = typer.Option(..., "--freq", "-f", parser=parse_freq, metavar="FREKANS",
                               help="Frekans. Yalın sayı MHz"),
    vf: float = typer.Option(1.0, "--vf", help="Hız faktörü (koaksiyel için ~0.66-0.85, tel anten ~0.95)"),
):
    """Dalga boyu ve temel anten boyları.

    Örnekler:
      elektro rf wave -f 433.92
      elektro rf wave -f 2.4G --vf 0.95
    """
    if freq <= 0 or not 0 < vf <= 1:
        fail("frekans pozitif ve 0 < vf ≤ 1 olmalı")
    lam = C0 / freq * vf
    result_panel("Dalga Boyu", {
        "Frekans": format_si(freq, "Hz"),
        "λ": format_si(lam, "m"),
        "λ/2 dipol (toplam)": format_si(lam / 2, "m"),
        "λ/4 monopol / GP": format_si(lam / 4, "m"),
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
            raise ValueError("VSWR ≥ 1 olmalı")
        return (x - 1) / (x + 1)
    if unit == "rl":
        if x < 0:
            raise ValueError("return loss ≥ 0 dB olmalı")
        return 10 ** (-x / 20)
    if unit == "gamma":
        if not 0 <= x <= 1:
            raise ValueError("|Γ| 0 ile 1 arasında olmalı")
        return x
    raise KeyError(unit)


_ALIASES = {"watt": "w", "mwatt": "mw", "µw": "uw", "s11": "rl", "g": "gamma", "Γ": "gamma"}
POWER_UNITS = set(POWER_TO_DBM)
MATCH_UNITS = {"vswr", "rl", "gamma"}


def convert_units(value: float, src: str, dst: Optional[str]):
    src = _ALIASES.get(src.lower(), src.lower())
    dst = _ALIASES.get(dst.lower(), dst.lower()) if dst else None
    if src in POWER_UNITS:
        if src != "dbm" and src != "dbw" and value <= 0:
            raise ValueError("güç pozitif olmalı")
        dbm = POWER_TO_DBM[src](value)
        targets = [dst] if dst else ["dbm", "dbw", "w", "mw"]
        if dst and dst not in POWER_UNITS:
            raise ValueError(f"{src} → {dst} dönüşümü yok")
        return {t: DBM_TO_POWER[t](dbm) for t in targets}
    if src in MATCH_UNITS:
        g = gamma_from(src, value)
        vals = {
            "gamma": g,
            "vswr": math.inf if g >= 1 else (1 + g) / (1 - g),
            "rl": math.inf if g == 0 else -20 * math.log10(g),
            "mismatch": math.inf if g >= 1 else -10 * math.log10(1 - g * g),
            "reflected": g * g * 100,
        }
        if dst and dst not in MATCH_UNITS:
            raise ValueError(f"{src} → {dst} dönüşümü yok")
        return {dst: vals[dst]} if dst else vals
    raise ValueError(f"bilinmeyen birim '{src}'")


_LABEL = {"dbm": ("dBm", None), "dbw": ("dBW", None), "w": ("W", "W"), "mw": ("mW", None),
          "uw": ("µW", None), "gamma": ("|Γ|", None), "vswr": ("VSWR", None), "rl": ("Return loss", "dB"),
          "mismatch": ("Uyumsuzluk kaybı", "dB"), "reflected": ("Yansıyan güç", "%")}


@app.command()
def convert(
    value: float = typer.Argument(..., help="Değer"),
    src: str = typer.Argument(..., help="Kaynak birim: dbm dbw w mw uw vswr rl gamma"),
    dst: Optional[str] = typer.Argument(None, help="Hedef birim (boşsa hepsi)"),
):
    """RF birim dönüşümü (güç ve empedans uyumu).

    Örnekler:
      elektro rf convert 14 dbm w
      elektro rf convert 0.1 w
      elektro rf convert 1.5 vswr
    """
    try:
        res = convert_units(value, src, dst)
    except ValueError as e:
        fail(str(e))
    t = Table(show_header=False, box=None)
    t.add_column(style="cyan", justify="right")
    t.add_column(style="bold green")
    for key, v in res.items():
        label, unit = _LABEL[key]
        if unit == "W":
            text = format_si(v, "W")
        elif math.isinf(v):
            text = "∞"
        elif unit == "%":
            text = f"%{v:.3g}"
        else:
            text = f"{v:.4g}" + (f" {unit}" if unit else "")
        t.add_row(label, text)
    console.print(t)
