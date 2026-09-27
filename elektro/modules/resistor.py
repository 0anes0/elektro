"""Direnç renk kodu, SMD kodu ve ters (değerden renge) hesap."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import List, Optional

import typer
from rich.table import Table
from rich.text import Text

from elektro.i18n import get_language, pct, t, upper
from elektro.ui import console, default_group, fail, json_mode, print_json, result_panel
from elektro.units import E_SERIES_BASE, format_si, nearest_standard, parse_value

app = typer.Typer(
    cls=default_group("decode"),
    help=t("res.help"),
    invoke_without_command=True,
)


@dataclass(frozen=True)
class Color:
    code_tr: str      # Türkçe kısa kod (k s r a ...)
    code_iec: str     # IEC 60757 kısa kodu (bn bk rd gd ...)
    names: dict       # dil -> ad
    digit: Optional[int]
    multiplier: Optional[float]
    tolerance: Optional[float]   # %
    tempco: Optional[int]        # ppm/K
    style: str
    aliases: tuple = ()

    @property
    def name(self) -> str:
        return self.names.get(get_language(), self.names["en"])

    @property
    def code(self) -> str:
        return self.code_tr if get_language() == "tr" else self.code_iec


def _n(en, tr, de, ru):
    return {"en": en, "tr": tr, "de": de, "ru": ru}


COLORS = [
    Color("s", "bk", _n("black", "siyah", "schwarz", "чёрный"), 0, 1, None, 250,
          "white on black", ("черный",)),
    Color("k", "bn", _n("brown", "kahverengi", "braun", "коричневый"), 1, 10, 1, 100,
          "white on rgb(139,69,19)", ("kah",)),
    Color("r", "rd", _n("red", "kırmızı", "rot", "красный"), 2, 100, 2, 50,
          "white on red", ("kirmizi", "kir")),
    Color("t", "og", _n("orange", "turuncu", "orange", "оранжевый"), 3, 1e3, None, 15,
          "black on rgb(255,140,0)"),
    Color("sa", "ye", _n("yellow", "sarı", "gelb", "жёлтый"), 4, 1e4, None, 25,
          "black on yellow", ("sari", "желтый")),
    Color("y", "gn", _n("green", "yeşil", "grün", "зелёный"), 5, 1e5, 0.5, 20,
          "white on green", ("yesil", "gruen", "зеленый")),
    Color("m", "bu", _n("blue", "mavi", "blau", "синий"), 6, 1e6, 0.25, 10,
          "white on blue", ("голубой",)),
    Color("mo", "vt", _n("violet", "mor", "violett", "фиолетовый"), 7, 1e7, 0.1, 5,
          "white on purple", ("purple", "lila")),
    Color("g", "gy", _n("grey", "gri", "grau", "серый"), 8, 1e8, 0.05, 1,
          "black on grey62", ("gray",)),
    Color("b", "wh", _n("white", "beyaz", "weiß", "белый"), 9, 1e9, None, None,
          "black on white", ("weiss",)),
    Color("a", "gd", _n("gold", "altın", "gold", "золотой"), None, 0.1, 5, None,
          "black on gold1", ("altin",)),
    Color("gu", "sr", _n("silver", "gümüş", "silber", "серебряный"), None, 0.01, 10, None,
          "black on grey82", ("gumus",)),
    Color("x", "none", _n("none", "yok", "keine", "нет"), None, None, 20, None,
          "dim", ("-", "ohne", "без")),
]

_LOOKUP = {}
for _c in COLORS:
    for _k in (_c.code_tr, _c.code_iec, *_c.names.values(), *_c.aliases):
        _LOOKUP[_k.lower()] = _c
NONE = COLORS[-1]
BY_DIGIT = {c.digit: c for c in COLORS if c.digit is not None}
BY_MULT_EXP = {round(math.log10(c.multiplier)): c for c in COLORS if c.multiplier}
BY_TOL = {c.tolerance: c for c in COLORS if c.tolerance is not None}


def lookup(code: str) -> Color:
    c = _LOOKUP.get(code.strip().lower())
    if c is None:
        raise ValueError(t("res.unknown_color", code=code))
    return c


def decode_bands(codes: List[str]) -> dict:
    """3-6 bantlı renk kodunu çözer."""
    bands = [lookup(c) for c in codes]
    n = len(bands)
    if n not in (3, 4, 5, 6):
        raise ValueError(t("res.band_count"))

    ndigits = 2 if n <= 4 else 3
    digits, mult = bands[:ndigits], bands[ndigits]
    tol = bands[ndigits + 1] if n > ndigits + 1 else NONE
    tempco = bands[5] if n == 6 else None

    for pos, b in enumerate(digits, 1):
        if b.digit is None:
            raise ValueError(t("res.bad_digit", pos=pos, color=b.name))
    if mult.multiplier is None:
        raise ValueError(t("res.bad_mult", color=mult.name))
    if tol.tolerance is None:
        raise ValueError(t("res.bad_tol", color=tol.name))
    if tempco is not None and tempco.tempco is None:
        raise ValueError(t("res.bad_tempco", color=tempco.name))

    base = int("".join(str(b.digit) for b in digits))
    value = base * mult.multiplier
    return {
        "value": value,
        "tolerance": tol.tolerance,
        "tempco": tempco.tempco if tempco else None,
        "bands": bands,
    }


def encode_value(value: float, bands: int = 4, tolerance: float = 5) -> List[Color]:
    """Direnç değerinden renk bantları üretir."""
    if value <= 0:
        raise ValueError(t("common.positive"))
    ndigits = 2 if bands == 4 else 3
    exp = math.floor(math.log10(value)) - (ndigits - 1)
    sig = round(value / 10 ** exp)
    if sig >= 10 ** ndigits:           # 99.6 -> 100 gibi taşma
        sig //= 10
        exp += 1
    min_exp = min(BY_MULT_EXP)
    if exp < min_exp:                  # 0.47 Ω 5 bantta: 0-4-7 × 0.01
        sig = round(value / 10 ** min_exp)
        exp = min_exp
    if exp not in BY_MULT_EXP:
        raise ValueError(t("res.cannot_encode", value=format_si(value, "Ω")))
    if tolerance not in BY_TOL:
        raise ValueError(t("res.bad_tol_value", tol=f"{tolerance:g}",
                           options=", ".join(f"{x:g}" for x in sorted(BY_TOL))))
    digits = [BY_DIGIT[int(d)] for d in str(sig).zfill(ndigits)]
    return digits + [BY_MULT_EXP[exp], BY_TOL[tolerance]]


# --- SMD ------------------------------------------------------------------

EIA96_MULT = {"Z": 0.001, "Y": 0.01, "R": 0.01, "X": 0.1, "S": 0.1, "A": 1,
              "B": 10, "H": 10, "C": 100, "D": 1e3, "E": 1e4, "F": 1e5}


def decode_smd(code: str) -> float:
    """SMD direnç kodu: 103, 4R7, R47, 1002, 01C (EIA-96)."""
    c = code.strip().upper()
    m = re.fullmatch(r"(\d{2})([A-Z])", c)
    if m and m.group(2) in EIA96_MULT:
        idx = int(m.group(1))
        if not 1 <= idx <= 96:
            raise ValueError(t("res.eia96_range"))
        return round(E_SERIES_BASE["E96"][idx - 1] * 100 * EIA96_MULT[m.group(2)], 6)
    if "R" in c and re.fullmatch(r"\d*R\d*", c) and c != "R":
        return float(c.replace("R", "."))
    if re.fullmatch(r"\d{3,4}", c):
        return int(c[:-1]) * 10 ** int(c[-1])
    raise ValueError(t("res.smd_invalid", code=code))


# --- Komutlar ---------------------------------------------------------------

def _band_strip(bands: List[Color]) -> Text:
    text = Text()
    for b in bands:
        text.append(f" {upper(b.name)} ", style=b.style)
        text.append(" ")
    return text


@app.callback(help=t("res.help_long"))
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        show_table()


@app.command(help=t("res.decode.help"))
def decode(bands: List[str] = typer.Argument(..., help=t("res.decode.arg"))):
    try:
        res = decode_bands(bands)
    except ValueError as e:
        fail(f"{e}\n[dim]{t('res.see_table')}[/]")

    v, tol = res["value"], res["tolerance"]
    rows = {
        t("res.value"): format_si(v, "Ω"),
        t("res.tolerance"): "±" + pct(f"{tol:g}"),
        t("res.range"): f"{format_si(v * (1 - tol / 100), 'Ω')} … {format_si(v * (1 + tol / 100), 'Ω')}",
    }
    if res["tempco"]:
        rows[t("res.tempco")] = f"{res['tempco']} ppm/K"
    rows[t("res.bands")] = _band_strip(res["bands"])
    result_panel(t("res.title"), rows, data={
        "resistance_ohm": v, "tolerance_pct": tol, "min_ohm": v * (1 - tol / 100),
        "max_ohm": v * (1 + tol / 100), "tempco_ppm": res["tempco"],
        "bands": [b.names["en"] for b in res["bands"]]})


@app.command(help=t("res.encode.help"))
def encode(
    value: float = typer.Argument(..., parser=parse_value, metavar=t("ui.metavar.value"),
                                  help=t("res.encode.arg")),
    bands: int = typer.Option(4, "--bands", "-b", help=t("res.encode.opt.bands")),
    tolerance: Optional[float] = typer.Option(None, "--tol", "-t", help=t("res.encode.opt.tol")),
):
    if bands not in (4, 5):
        fail(t("res.encode.bad_bands"))
    if tolerance is None:
        tolerance = 5 if bands == 4 else 1
    try:
        colors = encode_value(value, bands, tolerance)
    except ValueError as e:
        fail(str(e))

    actual = decode_bands([c.code_iec for c in colors])["value"]
    rows = {t("res.value"): format_si(actual, "Ω"), t("res.bands"): _band_strip(colors),
            t("res.codes"): " ".join(c.code for c in colors)}
    if not math.isclose(actual, value, rel_tol=1e-6):
        rows[t("res.note")] = t("res.rounded", value=format_si(value, "Ω"), bands=bands)
    series = "E24" if bands == 4 else "E96"
    std = nearest_standard(value, series)
    if not math.isclose(std, value, rel_tol=1e-6):
        rows[t("res.nearest_std")] = f"{format_si(std, 'Ω')} ({series})"
    result_panel(t("res.encode.title"), rows, data={
        "resistance_ohm": actual, "requested_ohm": value, "tolerance_pct": tolerance,
        "bands": [c.names["en"] for c in colors], "codes": [c.code_iec for c in colors],
        "nearest_standard_ohm": std, "series": series})


@app.command(help=t("res.smd.help"))
def smd(code: str = typer.Argument(..., help=t("res.smd.arg"))):
    try:
        value = decode_smd(code)
    except ValueError as e:
        fail(str(e))
    result_panel(t("res.smd.title"), {t("res.code"): code.upper(), t("res.value"): format_si(value, "Ω")},
                 data={"code": code.upper(), "resistance_ohm": value})


@app.command(help=t("res.table.help"))
def table():
    show_table()


def show_table():
    if json_mode():
        print_json([{"color": c.names["en"], "code": c.code_iec, "code_tr": c.code_tr,
                     "digit": c.digit, "multiplier": c.multiplier, "tolerance_pct": c.tolerance,
                     "tempco_ppm": c.tempco} for c in COLORS if c is not NONE])
        return
    tbl = Table(title=t("res.table.title"), header_style="bold")
    for key in ("res.col.code", "res.col.color", "res.col.digit", "res.col.mult", "res.col.tol"):
        tbl.add_column(t(key), justify="left" if key == "res.col.color" else "center")
    tbl.add_column("ppm/K", justify="center")
    for c in COLORS:
        if c is NONE:
            continue
        tbl.add_row(
            c.code,
            Text(f" {c.name[0].upper() + c.name[1:]} ", style=c.style),
            "-" if c.digit is None else str(c.digit),
            "-" if c.multiplier is None else "×" + format_si(c.multiplier, "", 3),
            "-" if c.tolerance is None else "±" + pct(f"{c.tolerance:g}"),
            "-" if c.tempco is None else str(c.tempco),
        )
    console.print(tbl)
    console.print(f"[dim]{t('res.table.footer')}[/]")
