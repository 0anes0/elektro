"""Direnç renk kodu, SMD kodu ve ters (değerden renge) hesap."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import List, Optional

import typer
from rich.table import Table
from rich.text import Text

from elektro.ui import console, default_group, fail, result_panel
from elektro.units import E_SERIES_BASE, format_si, nearest_standard, parse_value

app = typer.Typer(
    cls=default_group("decode"),
    help="Direnç renk kodu, SMD kodu ve standart değerler.",
    invoke_without_command=True,
)


@dataclass(frozen=True)
class Color:
    key: str          # kısa kod
    name: str         # Türkçe ad
    digit: Optional[int]
    multiplier: Optional[float]
    tolerance: Optional[float]   # %
    tempco: Optional[int]        # ppm/K
    style: str
    aliases: tuple = ()


COLORS = [
    Color("s", "siyah", 0, 1, None, 250, "white on black", ("black",)),
    Color("k", "kahverengi", 1, 10, 1, 100, "white on rgb(139,69,19)", ("brown", "kah")),
    Color("r", "kırmızı", 2, 100, 2, 50, "white on red", ("kirmizi", "red", "kir")),
    Color("t", "turuncu", 3, 1e3, None, 15, "black on rgb(255,140,0)", ("orange",)),
    Color("sa", "sarı", 4, 1e4, None, 25, "black on yellow", ("sari", "yellow")),
    Color("y", "yeşil", 5, 1e5, 0.5, 20, "white on green", ("yesil", "green")),
    Color("m", "mavi", 6, 1e6, 0.25, 10, "white on blue", ("blue",)),
    Color("mo", "mor", 7, 1e7, 0.1, 5, "white on purple", ("violet", "purple")),
    Color("g", "gri", 8, 1e8, 0.05, 1, "black on grey62", ("grey", "gray")),
    Color("b", "beyaz", 9, 1e9, None, None, "black on white", ("white",)),
    Color("a", "altın", None, 0.1, 5, None, "black on gold1", ("altin", "gold")),
    Color("gu", "gümüş", None, 0.01, 10, None, "black on grey82", ("gumus", "silver")),
    Color("x", "yok", None, None, 20, None, "dim", ("none", "-")),
]

_LOOKUP = {}
for _c in COLORS:
    for _k in (_c.key, _c.name, *_c.aliases):
        _LOOKUP[_k] = _c
BY_DIGIT = {c.digit: c for c in COLORS if c.digit is not None}
BY_MULT_EXP = {round(math.log10(c.multiplier)): c for c in COLORS if c.multiplier}
BY_TOL = {c.tolerance: c for c in COLORS if c.tolerance is not None}


def lookup(code: str) -> Color:
    c = _LOOKUP.get(code.strip().lower())
    if c is None:
        raise ValueError(f"bilinmeyen renk '{code}'")
    return c


def decode_bands(codes: List[str]) -> dict:
    """3-6 bantlı renk kodunu çözer."""
    bands = [lookup(c) for c in codes]
    n = len(bands)
    if n not in (3, 4, 5, 6):
        raise ValueError("3, 4, 5 veya 6 bant girilmeli")

    ndigits = 2 if n <= 4 else 3
    digits, mult = bands[:ndigits], bands[ndigits]
    tol = bands[ndigits + 1] if n > ndigits + 1 else lookup("x")
    tempco = bands[5] if n == 6 else None

    for pos, b in enumerate(digits, 1):
        if b.digit is None:
            raise ValueError(f"{pos}. bant ({b.name}) rakam bandı olamaz")
    if mult.multiplier is None:
        raise ValueError(f"çarpan bandı {mult.name} olamaz")
    if tol.tolerance is None:
        raise ValueError(f"tolerans bandı {tol.name} olamaz")
    if tempco is not None and tempco.tempco is None:
        raise ValueError(f"sıcaklık katsayısı bandı {tempco.name} olamaz")

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
        raise ValueError("değer pozitif olmalı")
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
        raise ValueError(f"{format_si(value, 'Ω')} renk koduyla yazılamaz")
    if tolerance not in BY_TOL:
        raise ValueError(f"geçersiz tolerans %{tolerance} (seçenekler: {sorted(BY_TOL)})")
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
            raise ValueError("EIA-96 kodu 01-96 arasında olmalı")
        return round(E_SERIES_BASE["E96"][idx - 1] * 100 * EIA96_MULT[m.group(2)], 6)
    if "R" in c and re.fullmatch(r"\d*R\d*", c) and c != "R":
        return float(c.replace("R", "."))
    if re.fullmatch(r"\d{3,4}", c):
        return int(c[:-1]) * 10 ** int(c[-1])
    raise ValueError(f"'{code}' SMD kodu anlaşılamadı (örnek: 103, 4R7, 1002, 01C)")


# --- Komutlar ---------------------------------------------------------------

def _band_strip(bands: List[Color]) -> Text:
    t = Text()
    for b in bands:
        t.append(f" {b.name.replace('i', 'İ').upper()} ", style=b.style)
        t.append(" ")
    return t


@app.callback()
def main(ctx: typer.Context):
    """Direnç renk kodu çözücü.

    Bant sırası: rakamlar → çarpan → tolerans → (sıcaklık katsayısı).
    Renkler kısa kod, Türkçe veya İngilizce ad olarak yazılabilir.

    Örnekler:
      elektro resistor k s r a          (1 kΩ ±%5)
      elektro resistor sa mo s k k      (4.7 kΩ ±%1, 5 bant)
      elektro resistor encode 4k7
      elektro resistor smd 103
    """
    if ctx.invoked_subcommand is None:
        show_table()


@app.command()
def decode(bands: List[str] = typer.Argument(..., help="Renk bantları (3-6 adet)")):
    """Renk bantlarından direnç değerini bulur."""
    try:
        res = decode_bands(bands)
    except ValueError as e:
        fail(f"{e}\n[dim]Renkler için: elektro resistor table[/]")

    v, tol = res["value"], res["tolerance"]
    rows = {
        "Değer": format_si(v, "Ω"),
        "Tolerans": f"±%{tol:g}",
        "Aralık": f"{format_si(v * (1 - tol / 100), 'Ω')} … {format_si(v * (1 + tol / 100), 'Ω')}",
    }
    if res["tempco"]:
        rows["Sıcaklık kats."] = f"{res['tempco']} ppm/K"
    rows["Bantlar"] = _band_strip(res["bands"])
    result_panel("Direnç", rows)


@app.command()
def encode(
    value: float = typer.Argument(..., parser=parse_value, metavar="DEĞER", help="Direnç, örn: 4k7, 220, 1M"),
    bands: int = typer.Option(4, "--bands", "-b", help="Bant sayısı (4 veya 5)"),
    tolerance: Optional[float] = typer.Option(None, "--tol", "-t", help="Tolerans % (varsayılan: 4 bantta 5, 5 bantta 1)"),
):
    """Direnç değerinden renk kodunu üretir."""
    if bands not in (4, 5):
        fail("bant sayısı 4 veya 5 olmalı")
    if tolerance is None:
        tolerance = 5 if bands == 4 else 1
    try:
        colors = encode_value(value, bands, tolerance)
    except ValueError as e:
        fail(str(e))

    actual = decode_bands([c.key for c in colors])["value"]
    rows = {"Değer": format_si(actual, "Ω"), "Bantlar": _band_strip(colors),
            "Kodlar": " ".join(c.key for c in colors)}
    if not math.isclose(actual, value, rel_tol=1e-6):
        rows["Not"] = f"{format_si(value, 'Ω')} {bands} bantla tam yazılamıyor, yuvarlandı"
    std = nearest_standard(value, "E24" if bands == 4 else "E96")
    if not math.isclose(std, value, rel_tol=1e-6):
        rows["En yakın standart"] = format_si(std, "Ω") + (" (E24)" if bands == 4 else " (E96)")
    result_panel("Renk Kodu", rows)


@app.command()
def smd(code: str = typer.Argument(..., help="SMD kodu: 103, 4R7, 1002, 01C")):
    """SMD direnç üzerindeki kodu çözer (3/4 hane ve EIA-96)."""
    try:
        value = decode_smd(code)
    except ValueError as e:
        fail(str(e))
    result_panel("SMD Direnç", {"Kod": code.upper(), "Değer": format_si(value, "Ω")})


@app.command()
def table():
    """Renk kodu referans tablosu."""
    show_table()


def show_table():
    t = Table(title="Direnç Renk Kodları", header_style="bold")
    for col in ("Kod", "Renk", "Rakam", "Çarpan", "Tolerans", "ppm/K"):
        t.add_column(col, justify="center" if col != "Renk" else "left")
    for c in COLORS:
        if c.key == "x":
            continue
        t.add_row(
            c.key,
            Text(f" {c.name.title()} ", style=c.style),
            "-" if c.digit is None else str(c.digit),
            "-" if c.multiplier is None else "×" + format_si(c.multiplier, "", 3),
            "-" if c.tolerance is None else f"±%{c.tolerance:g}",
            "-" if c.tempco is None else str(c.tempco),
        )
    console.print(t)
    console.print("[dim]Tolerans bandı yoksa ±%20. Örnek: elektro resistor k s r a[/]")
