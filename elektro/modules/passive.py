"""Pasif eleman hesapları: seri/paralel, gerilim bölücü, LED direnci, E serisi, kondansatör kodu."""

from __future__ import annotations

import math
import re
from typing import List, Optional

import typer
from rich.table import Table

from elektro.ui import console, eng, fail, result_panel, warn
from elektro.units import (SERIES_NAMES, format_si, nearest_standard, normalize_series,
                           parse_value, series_neighbors, series_values)

POWER_RATINGS = [0.063, 0.1, 0.125, 0.25, 0.5, 1, 2, 3, 5, 10]


def _values_arg(help_text: str):
    return typer.Argument(..., parser=parse_value, metavar="DEĞERLER...", help=help_text)


def series_sum(values: List[float]) -> float:
    return sum(values)


def parallel_sum(values: List[float]) -> float:
    if any(v == 0 for v in values):
        return 0.0
    return 1 / sum(1 / v for v in values)


def _combine(values, capacitor, inductor, parallel):
    unit = "F" if capacitor else "H" if inductor else "Ω"
    # Kondansatörde formüller yer değiştirir.
    use_reciprocal = parallel != capacitor
    total = parallel_sum(values) if use_reciprocal else series_sum(values)
    title = ("Paralel" if parallel else "Seri") + " Bağlantı"
    rows = {f"{k + 1}. eleman": format_si(v, unit) for k, v in enumerate(values)}
    rows["Toplam"] = format_si(total, unit)
    result_panel(title, rows)


def series(
    values: List[float] = _values_arg("Eleman değerleri, örn: 1k 2k2 470"),
    capacitor: bool = typer.Option(False, "--cap", "-c", help="Kondansatör olarak hesapla"),
    inductor: bool = typer.Option(False, "--ind", "-l", help="Bobin olarak hesapla"),
):
    """Seri bağlı elemanların toplamı (varsayılan: direnç).

    Örnekler:
      elektro series 1k 2k2 470
      elektro series 100n 100n --cap
    """
    _combine(values, capacitor, inductor, parallel=False)


def parallel(
    values: List[float] = _values_arg("Eleman değerleri, örn: 1k 1k"),
    capacitor: bool = typer.Option(False, "--cap", "-c", help="Kondansatör olarak hesapla"),
    inductor: bool = typer.Option(False, "--ind", "-l", help="Bobin olarak hesapla"),
):
    """Paralel bağlı elemanların eşdeğeri (varsayılan: direnç).

    Örnekler:
      elektro parallel 1k 1k
      elektro parallel 10u 22u --cap
    """
    _combine(values, capacitor, inductor, parallel=True)


# --- Gerilim bölücü -----------------------------------------------------------

def best_divider(vin: float, vout: float, series: str = "E24",
                 r_min: float = 1e3, r_max: float = 1e6, limit: int = 5):
    """Hedef çıkış gerilimi için en iyi R1/R2 çiftlerini arar (R2 toprağa bağlı)."""
    if not 0 < vout < vin:
        raise ValueError("0 < Vout < Vin olmalı")
    ratio = vout / vin
    results = []
    for r2 in series_values(series, r_min, r_max):
        ideal_r1 = r2 * (1 / ratio - 1)
        if not r_min <= ideal_r1 <= r_max:
            continue
        for r1 in set(series_neighbors(ideal_r1, series)):
            out = vin * r2 / (r1 + r2)
            results.append((abs(out - vout) / vout, r1 + r2, r1, r2, out))
    # Önce hata; eşitlikte toplamı ~30 kΩ'a yakın olan (ne çok akım çeken ne gürültüye açık)
    results.sort(key=lambda x: (round(x[0], 6), abs(math.log10(x[1] / 3e4))))
    seen, best = set(), []
    for err, _, r1, r2, out in results:
        ratio = round(r1 / r2, 9)       # 4k7/9k1 ile 47k/91k aynı oran
        if ratio in seen:
            continue
        seen.add(ratio)
        best.append({"r1": r1, "r2": r2, "vout": out, "error": err})
        if len(best) == limit:
            break
    return best


def divider(
    vin: float = typer.Option(..., "--vin", **eng("Giriş gerilimi (V)")),
    r1: Optional[float] = typer.Option(None, "--r1", **eng("Üst direnç (Vin ile çıkış arası)")),
    r2: Optional[float] = typer.Option(None, "--r2", **eng("Alt direnç (çıkış ile toprak arası)")),
    vout: Optional[float] = typer.Option(None, "--vout", **eng("Hedef çıkış (R1/R2 önerisi için)")),
    series: str = typer.Option("E24", "--series", "-s", help="Öneri için E serisi"),
    load: Optional[float] = typer.Option(None, "--load", **eng("Çıkışa bağlı yük direnci")),
):
    """Gerilim bölücü: Vout = Vin · R2 / (R1 + R2)

    R1 ve R2 verilirse çıkışı hesaplar; --vout verilirse standart değerlerden
    en iyi R1/R2 çiftlerini önerir.

    Örnekler:
      elektro divider --vin 12 --r1 10k --r2 4k7
      elektro divider --vin 5 --vout 3.3
      elektro divider --vin 12 --vout 3.3 --series E12
    """
    if r1 is not None and r2 is not None:
        r2_eff = parallel_sum([r2, load]) if load else r2
        out = vin * r2_eff / (r1 + r2_eff)
        i = vin / (r1 + r2_eff)
        rows = {
            "Vout": format_si(out, "V"),
            "Oran": f"{out / vin:.4f}",
            "Akım": format_si(i, "A"),
            "P(R1)": format_si(i * i * r1, "W"),
            "P(R2)": format_si((out ** 2) / r2, "W"),
        }
        if load:
            rows["Yüksüz Vout"] = format_si(vin * r2 / (r1 + r2), "V")
        result_panel("Gerilim Bölücü", rows)
        return

    if vout is None:
        fail("--r1 ve --r2 ya da --vout verilmeli")
    try:
        best = best_divider(vin, vout, normalize_series(series))
    except ValueError as e:
        fail(str(e))
    if not best:
        fail("uygun çift bulunamadı")

    t = Table(title=f"{format_si(vin, 'V')} → {format_si(vout, 'V')} ({normalize_series(series)})")
    for col in ("R1", "R2", "Vout", "Hata", "Akım"):
        t.add_column(col, justify="right")
    for b in best:
        t.add_row(format_si(b["r1"], "Ω"), format_si(b["r2"], "Ω"), format_si(b["vout"], "V"),
                  f"%{b['error'] * 100:.2f}", format_si(vin / (b["r1"] + b["r2"]), "A"))
    console.print(t)


# --- LED ------------------------------------------------------------------------

def led_resistor(vs: float, vf: float, current: float, count: int = 1) -> float:
    drop = vf * count
    if vs <= drop:
        raise ValueError(f"besleme ({vs} V) LED gerilim düşümünden ({drop:g} V) büyük olmalı")
    if current <= 0:
        raise ValueError("akım pozitif olmalı")
    return (vs - drop) / current


def led(
    vs: float = typer.Option(..., "--vs", **eng("Besleme gerilimi (V)")),
    vf: float = typer.Option(2.0, "--vf", **eng("LED ileri gerilimi (V). Kırmızı ~2, mavi/beyaz ~3")),
    current: float = typer.Option(0.02, "--if", "-i", **eng("LED akımı (A), örn: 20m")),
    count: int = typer.Option(1, "--count", "-n", help="Seri bağlı LED sayısı"),
    series: str = typer.Option("E12", "--series", "-s", help="Önerilecek E serisi"),
):
    """LED ön direnci hesabı.

    Örnekler:
      elektro led --vs 5
      elektro led --vs 12 --vf 3.1 -i 15m -n 3
    """
    try:
        r = led_resistor(vs, vf, current, count)
        _, std = series_neighbors(r, series)      # güvenli taraf: bir üst değer
    except ValueError as e:
        fail(str(e))
    i_real = (vs - vf * count) / std
    p = i_real ** 2 * std
    rating = next((x for x in POWER_RATINGS if x >= 2 * p), None)
    result_panel("LED Direnci", {
        "Hesaplanan R": format_si(r, "Ω"),
        f"Önerilen ({normalize_series(series)})": format_si(std, "Ω"),
        "Gerçek akım": format_si(i_real, "A"),
        "Direnç gücü": format_si(p, "W"),
        "Önerilen güç sınıfı": f"{rating:g} W" if rating else "> 10 W (farklı çözüm düşün)",
        "Verim": f"%{vf * count / vs * 100:.0f}",
    })


# --- E serisi --------------------------------------------------------------------

def eseries(
    value: float = typer.Argument(..., parser=parse_value, metavar="DEĞER", help="Aranan değer, örn: 4k8"),
    series: Optional[str] = typer.Option(None, "--series", "-s", help="Sadece bu seri (örn: E24)"),
):
    """Bir değere en yakın standart (E3…E192) değerleri gösterir.

    Örnekler:
      elektro eseries 4k8
      elektro eseries 3.3u -s E12
    """
    if value <= 0:
        fail("değer pozitif olmalı")
    names = [normalize_series(series)] if series else SERIES_NAMES
    t = Table(title=f"{format_si(value)} için standart değerler")
    for col in ("Seri", "Alt", "Üst", "En yakın", "Hata"):
        t.add_column(col, justify="right")
    for name in names:
        lo, hi = series_neighbors(value, name)
        near = nearest_standard(value, name)
        t.add_row(name, format_si(lo), format_si(hi), f"[bold]{format_si(near)}[/]",
                  f"%{(near - value) / value * 100:+.2f}")
    console.print(t)


# --- Kondansatör kodu --------------------------------------------------------------

CAP_TOLERANCE = {"B": "±0.1 pF", "C": "±0.25 pF", "D": "±0.5 pF", "F": "±%1", "G": "±%2",
                 "J": "±%5", "K": "±%10", "M": "±%20", "Z": "+%80 / -%20"}


def decode_cap(code: str):
    c = code.strip().upper()
    m = re.fullmatch(r"(\d{2})(\d)([A-Z]?)", c)
    if not m:
        raise ValueError("3 haneli kod bekleniyor (örn: 104, 472K)")
    exp = int(m.group(2))
    mult = {8: 0.01, 9: 0.1}.get(exp, 10 ** exp)
    return int(m.group(1)) * mult * 1e-12, CAP_TOLERANCE.get(m.group(3))


def encode_cap(value: float) -> str:
    pf = value / 1e-12
    if pf < 10:
        return f"{pf:g}".replace(".", "R") if pf != int(pf) else f"{int(pf)}"
    exp = math.floor(math.log10(pf)) - 1
    sig = round(pf / 10 ** exp)
    if sig >= 100:
        sig, exp = sig // 10, exp + 1
    return f"{sig}{exp}"


def cap(code: str = typer.Argument(..., help="Kod (104, 472K) veya değer (100n)")):
    """Seramik kondansatör kodunu çözer ya da değerden kod üretir.

    Örnekler:
      elektro cap 104       → 100 nF
      elektro cap 472K      → 4.7 nF ±%10
      elektro cap 22n       → 223
    """
    if re.fullmatch(r"\d{3}[A-Za-z]?", code.strip()):
        try:
            value, tol = decode_cap(code)
        except ValueError as e:
            fail(str(e))
        rows = {"Kod": code.upper(), "Değer": format_si(value, "F"),
                "pF": f"{value / 1e-12:g} pF"}
        if tol:
            rows["Tolerans"] = tol
        result_panel("Kondansatör", rows)
        return
    try:
        value = parse_value(code)
    except ValueError as e:
        fail(str(e))
    if value >= 1e-3:
        warn("bu değer muhtemelen seramik kondansatör değil")
    result_panel("Kondansatör", {"Değer": format_si(value, "F"), "Kod": encode_cap(value)})
