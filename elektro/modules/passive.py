"""Pasif eleman hesapları: seri/paralel, gerilim bölücü, LED direnci, E serisi, kondansatör kodu."""

from __future__ import annotations

import math
import re
from typing import List, Optional

import typer
from rich.table import Table

from elektro.i18n import pct, t
from elektro.ui import emit, eng, fail, result_panel, warn
from elektro.units import (SERIES_NAMES, format_si, nearest_standard, normalize_series,
                           parse_value, series_neighbors, series_values)

POWER_RATINGS = [0.063, 0.1, 0.125, 0.25, 0.5, 1, 2, 3, 5, 10]


def _values_arg(help_text: str):
    return typer.Argument(..., parser=parse_value, metavar=t("ui.metavar.values"), help=help_text)


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
    rows = {t("combine.item", n=k + 1): format_si(v, unit) for k, v in enumerate(values)}
    rows[t("combine.total")] = format_si(total, unit)
    kind = "capacitor" if capacitor else "inductor" if inductor else "resistor"
    result_panel(t("combine.parallel_title" if parallel else "combine.series_title"), rows,
                 data={"connection": "parallel" if parallel else "series", "component": kind,
                       "values": values, "total": total})


def _cap_opt():
    return typer.Option(False, "--cap", "-c", help=t("combine.opt.cap"))


def _ind_opt():
    return typer.Option(False, "--ind", "-l", help=t("combine.opt.ind"))


def series(
    values: List[float] = _values_arg(t("combine.arg.series")),
    capacitor: bool = _cap_opt(),
    inductor: bool = _ind_opt(),
):
    _combine(values, capacitor, inductor, parallel=False)


def parallel(
    values: List[float] = _values_arg(t("combine.arg.parallel")),
    capacitor: bool = _cap_opt(),
    inductor: bool = _ind_opt(),
):
    _combine(values, capacitor, inductor, parallel=True)


# --- Gerilim bölücü -----------------------------------------------------------

def best_divider(vin: float, vout: float, series: str = "E24",
                 r_min: float = 1e3, r_max: float = 1e6, limit: int = 5):
    """Hedef çıkış gerilimi için en iyi R1/R2 çiftlerini arar (R2 toprağa bağlı)."""
    if not 0 < vout < vin:
        raise ValueError(t("div.range"))
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
    vin: float = typer.Option(..., "--vin", **eng(t("div.opt.vin"))),
    r1: Optional[float] = typer.Option(None, "--r1", **eng(t("div.opt.r1"))),
    r2: Optional[float] = typer.Option(None, "--r2", **eng(t("div.opt.r2"))),
    vout: Optional[float] = typer.Option(None, "--vout", **eng(t("div.opt.vout"))),
    series: str = typer.Option("E24", "--series", "-s", help=t("div.opt.series")),
    load: Optional[float] = typer.Option(None, "--load", **eng(t("div.opt.load"))),
):
    if r1 is not None and r2 is not None:
        r2_eff = parallel_sum([r2, load]) if load else r2
        out = vin * r2_eff / (r1 + r2_eff)
        i = vin / (r1 + r2_eff)
        rows = {
            "Vout": format_si(out, "V"),
            t("div.ratio"): f"{out / vin:.4f}",
            t("div.current"): format_si(i, "A"),
            "P(R1)": format_si(i * i * r1, "W"),
            "P(R2)": format_si((out ** 2) / r2, "W"),
        }
        if load:
            rows[t("div.unloaded")] = format_si(vin * r2 / (r1 + r2), "V")
        result_panel(t("div.title"), rows, data={
            "vin_v": vin, "r1_ohm": r1, "r2_ohm": r2, "load_ohm": load, "vout_v": out,
            "ratio": out / vin, "current_a": i, "p_r1_w": i * i * r1, "p_r2_w": out ** 2 / r2})
        return

    if vout is None:
        fail(t("div.need"))
    try:
        best = best_divider(vin, vout, normalize_series(series))
    except ValueError as e:
        fail(str(e))
    if not best:
        fail(t("div.none"))

    tbl = Table(title=f"{format_si(vin, 'V')} → {format_si(vout, 'V')} ({normalize_series(series)})")
    for col in ("R1", "R2", "Vout", t("div.col.error"), t("div.col.current")):
        tbl.add_column(col, justify="right")
    for b in best:
        tbl.add_row(format_si(b["r1"], "Ω"), format_si(b["r2"], "Ω"), format_si(b["vout"], "V"),
                    pct(f"{b['error'] * 100:.2f}"), format_si(vin / (b["r1"] + b["r2"]), "A"))
    emit(tbl, [{**b, "current_a": vin / (b["r1"] + b["r2"])} for b in best])


# --- LED ------------------------------------------------------------------------

def led_resistor(vs: float, vf: float, current: float, count: int = 1) -> float:
    drop = vf * count
    if vs <= drop:
        raise ValueError(t("led.supply_low", vs=f"{vs:g}", drop=f"{drop:g}"))
    if current <= 0:
        raise ValueError(t("led.current_pos"))
    return (vs - drop) / current


def led(
    vs: float = typer.Option(..., "--vs", **eng(t("led.opt.vs"))),
    vf: float = typer.Option(2.0, "--vf", **eng(t("led.opt.vf"))),
    current: float = typer.Option(0.02, "--if", "-i", **eng(t("led.opt.if"))),
    count: int = typer.Option(1, "--count", "-n", help=t("led.opt.count")),
    series: str = typer.Option("E12", "--series", "-s", help=t("led.opt.series")),
):
    try:
        r = led_resistor(vs, vf, current, count)
        _, std = series_neighbors(r, series)      # güvenli taraf: bir üst değer
    except ValueError as e:
        fail(str(e))
    i_real = (vs - vf * count) / std
    p = i_real ** 2 * std
    rating = next((x for x in POWER_RATINGS if x >= 2 * p), None)
    result_panel(t("led.title"), {
        t("led.calc_r"): format_si(r, "Ω"),
        t("led.suggested", series=normalize_series(series)): format_si(std, "Ω"),
        t("led.real_i"): format_si(i_real, "A"),
        t("led.power"): format_si(p, "W"),
        t("led.rating"): f"{rating:g} W" if rating else t("led.rating_high"),
        t("led.efficiency"): pct(f"{vf * count / vs * 100:.0f}"),
    }, data={"calculated_ohm": r, "suggested_ohm": std, "series": normalize_series(series),
             "current_a": i_real, "resistor_power_w": p, "recommended_rating_w": rating,
             "efficiency": vf * count / vs})


# --- E serisi --------------------------------------------------------------------

def eseries(
    value: float = typer.Argument(..., parser=parse_value, metavar=t("ui.metavar.value"),
                                  help=t("eseries.arg")),
    series: Optional[str] = typer.Option(None, "--series", "-s", help=t("eseries.opt.series")),
):
    if value <= 0:
        fail(t("common.positive"))
    try:
        names = [normalize_series(series)] if series else SERIES_NAMES
    except ValueError as e:
        fail(str(e))
    tbl = Table(title=t("eseries.title", value=format_si(value)))
    for key in ("eseries.col.series", "eseries.col.lower", "eseries.col.upper",
                "eseries.col.nearest", "eseries.col.error"):
        tbl.add_column(t(key), justify="right")
    records = []
    for name in names:
        lo, hi = series_neighbors(value, name)
        near = nearest_standard(value, name)
        tbl.add_row(name, format_si(lo), format_si(hi), f"[bold]{format_si(near)}[/]",
                    pct(f"{(near - value) / value * 100:+.2f}"))
        records.append({"series": name, "lower": lo, "upper": hi, "nearest": near,
                        "error": (near - value) / value})
    emit(tbl, records)


# --- Kondansatör kodu --------------------------------------------------------------

CAP_TOLERANCE = {"B": "±0.1 pF", "C": "±0.25 pF", "D": "±0.5 pF", "F": "1", "G": "2",
                 "J": "5", "K": "10", "M": "20", "Z": None}


def decode_cap(code: str):
    c = code.strip().upper()
    m = re.fullmatch(r"(\d{2})(\d)([A-Z]?)", c)
    if not m:
        raise ValueError(t("cap.bad_code"))
    exp = int(m.group(2))
    mult = {8: 0.01, 9: 0.1}.get(exp, 10 ** exp)
    letter = m.group(3)
    if not letter or letter not in CAP_TOLERANCE:
        tol = None
    elif letter == "Z":
        tol = f"+{pct('80')} / -{pct('20')}"
    elif "pF" in CAP_TOLERANCE[letter]:
        tol = CAP_TOLERANCE[letter]
    else:
        tol = "±" + pct(CAP_TOLERANCE[letter])
    return int(m.group(1)) * mult * 1e-12, tol


def encode_cap(value: float) -> str:
    pf = value / 1e-12
    if pf < 10:
        return f"{pf:g}".replace(".", "R") if pf != int(pf) else f"{int(pf)}"
    exp = math.floor(math.log10(pf)) - 1
    sig = round(pf / 10 ** exp)
    if sig >= 100:
        sig, exp = sig // 10, exp + 1
    return f"{sig}{exp}"


def cap(code: str = typer.Argument(..., help=t("cap.arg"))):
    if re.fullmatch(r"\d{3}[A-Za-z]?", code.strip()):
        try:
            value, tol = decode_cap(code)
        except ValueError as e:
            fail(str(e))
        rows = {t("cap.code"): code.upper(), t("cap.value"): format_si(value, "F"),
                "pF": f"{value / 1e-12:g} pF"}
        if tol:
            rows[t("cap.tolerance")] = tol
        result_panel(t("cap.title"), rows, data={"code": code.upper(), "capacitance_f": value,
                                                 "tolerance": tol})
        return
    try:
        value = parse_value(code)
    except ValueError as e:
        fail(str(e))
    if value >= 1e-3:
        warn(t("cap.not_ceramic"))
    result_panel(t("cap.title"), {t("cap.value"): format_si(value, "F"), t("cap.code"): encode_cap(value)},
                 data={"capacitance_f": value, "code": encode_cap(value)})
