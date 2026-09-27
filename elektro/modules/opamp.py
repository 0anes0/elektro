"""Op-amp devreleri: evirmeyen, eviren, fark ve toplayıcı yükselteç."""

from __future__ import annotations

import math
from typing import List, Optional

import typer
from rich.table import Table

from elektro.i18n import pct, t
from elektro.ui import (
    cli_parser, console, eng, fail, json_mode, print_json, result_panel, theory, warn,
)
from elektro.units import format_si, normalize_series, parse_value, series_neighbors, series_values

app = typer.Typer(help=t("op.help"), no_args_is_help=True)


def best_ratio_pairs(ratio: float, series: str = "E24", r_min: float = 1e3, r_max: float = 1e6,
                     limit: int = 5) -> List[dict]:
    """Ra/Rb ≈ ratio olan standart direnç çiftleri (hataya göre sıralı)."""
    if ratio <= 0:
        raise ValueError(t("common.positive"))
    found = []
    for rb in series_values(series, r_min, r_max):
        ideal = rb * ratio
        if not r_min <= ideal <= r_max:
            continue
        for ra in set(series_neighbors(ideal, series)):
            found.append((abs(ra / rb - ratio) / ratio, abs(math.log10((ra + rb) / 2e4)), ra, rb))
    found.sort(key=lambda x: (round(x[0], 6), x[1]))
    seen, out = set(), []
    for err, _, ra, rb in found:
        key = round(ra / rb, 9)
        if key in seen:
            continue
        seen.add(key)
        out.append({"ra": ra, "rb": rb, "ratio": ra / rb, "error": err})
        if len(out) == limit:
            break
    return out


def _common_rows(gain: float, noise_gain: float, vin, vcc, gbw) -> tuple:
    rows, data = {}, {}
    if vin is not None:
        vout = gain * vin
        rows["Vout"] = format_si(vout, "V")
        data["vout_v"] = vout
        if vcc is not None and abs(vout) > vcc:
            warn(t("op.clip", vout=format_si(vout, "V"), vcc=format_si(vcc, "V")))
    if gbw is not None:
        bw = gbw / noise_gain
        rows[t("op.bandwidth")] = format_si(bw, "Hz")
        data["bandwidth_hz"] = bw
    return rows, data


def _pairs_table(pairs, label_a, label_b, gain_of) -> Table:
    tbl = Table(title=t("op.pairs"))
    for col in (label_a, label_b, t("op.gain"), t("op.col.error")):
        tbl.add_column(col, justify="right")
    for p in pairs:
        tbl.add_row(format_si(p["ra"], "Ω"), format_si(p["rb"], "Ω"), f"{gain_of(p):.4g}",
                    pct(f"{p['error'] * 100:.2f}"))
    return tbl


def _vin_opt():
    return typer.Option(None, "--vin", **eng(t("op.opt.vin")))


def _vcc_opt():
    return typer.Option(None, "--vcc", **eng(t("op.opt.vcc")))


def _gbw_opt():
    return typer.Option(None, "--gbw", **eng(t("op.opt.gbw")))


def _series_opt():
    return typer.Option("E24", "--series", "-s", help=t("div.opt.series"))


@app.command(help=t("op.noninv.help"))
def noninv(
    gain: Optional[float] = typer.Option(None, "--gain", "-g", help=t("op.opt.gain")),
    rf: Optional[float] = typer.Option(None, "--rf", **eng(t("op.opt.rf"))),
    rg: Optional[float] = typer.Option(None, "--rg", **eng(t("op.opt.rg"))),
    vin: Optional[float] = _vin_opt(),
    vcc: Optional[float] = _vcc_opt(),
    gbw: Optional[float] = _gbw_opt(),
    series: str = _series_opt(),
):
    if rf is not None and rg is not None:
        g = 1 + rf / rg
        rows, data = _common_rows(g, g, vin, vcc, gbw)
        result_panel(t("op.noninv.title"), {
            "Rf / Rg": f"{format_si(rf, 'Ω')} / {format_si(rg, 'Ω')}",
            t("op.gain"): f"{g:.4g} ({20 * math.log10(g):.2f} dB)", **rows},
            data={"gain": g, "rf_ohm": rf, "rg_ohm": rg, **data})
        return
    if gain is None:
        fail(t("op.need"))
    if gain < 1:
        fail(t("op.noninv.min"))
    if gain == 1:
        result_panel(t("op.noninv.title"), {t("op.gain"): "1", t("op.note"): t("op.follower")},
                     data={"gain": 1.0})
        return
    try:
        pairs = best_ratio_pairs(gain - 1, normalize_series(series))
    except ValueError as e:
        fail(str(e))
    rows, data = _common_rows(gain, gain, vin, vcc, gbw)
    if json_mode():
        print_json({"gain": gain, "pairs": [{"rf_ohm": p["ra"], "rg_ohm": p["rb"], "gain": 1 + p["ratio"],
                                              "error": p["error"]} for p in pairs], **data})
        return
    console.print(_pairs_table(pairs, "Rf", "Rg", lambda p: 1 + p["ratio"]))
    if rows:
        result_panel(t("op.noninv.title"), rows)
    theory("G = 1 + Rf / Rg", t("op.noninv.note"))


@app.command(help=t("op.inv.help"))
def inv(
    gain: Optional[float] = typer.Option(None, "--gain", "-g", help=t("op.opt.gain_inv")),
    rf: Optional[float] = typer.Option(None, "--rf", **eng(t("op.opt.rf"))),
    rin: Optional[float] = typer.Option(None, "--rin", **eng(t("op.opt.rin"))),
    vin: Optional[float] = _vin_opt(),
    vcc: Optional[float] = _vcc_opt(),
    gbw: Optional[float] = _gbw_opt(),
    series: str = _series_opt(),
):
    if rf is not None and rin is not None:
        g = -rf / rin
        rows, data = _common_rows(g, 1 + rf / rin, vin, vcc, gbw)
        result_panel(t("op.inv.title"), {
            "Rf / Rin": f"{format_si(rf, 'Ω')} / {format_si(rin, 'Ω')}",
            t("op.gain"): f"{g:.4g} ({20 * math.log10(abs(g)):.2f} dB)",
            t("op.zin"): format_si(rin, "Ω"), **rows},
            data={"gain": g, "rf_ohm": rf, "rin_ohm": rin, **data})
        return
    if gain is None:
        fail(t("op.need"))
    mag = abs(gain)
    if mag == 0:
        fail(t("common.positive"))
    try:
        pairs = best_ratio_pairs(mag, normalize_series(series))
    except ValueError as e:
        fail(str(e))
    rows, data = _common_rows(-mag, 1 + mag, vin, vcc, gbw)
    if json_mode():
        print_json({"gain": -mag, "pairs": [{"rf_ohm": p["ra"], "rin_ohm": p["rb"], "gain": -p["ratio"],
                                              "error": p["error"]} for p in pairs], **data})
        return
    console.print(_pairs_table(pairs, "Rf", "Rin", lambda p: -p["ratio"]))
    if rows:
        result_panel(t("op.inv.title"), rows)
    theory("G = −Rf / Rin", t("op.inv.note"))


@app.command(help=t("op.diff.help"))
def diff(
    gain: float = typer.Option(..., "--gain", "-g", help=t("op.opt.gain")),
    series: str = _series_opt(),
):
    if gain <= 0:
        fail(t("common.positive"))
    try:
        pairs = best_ratio_pairs(gain, normalize_series(series))
    except ValueError as e:
        fail(str(e))
    if json_mode():
        print_json({"gain": gain, "pairs": [{"r2_ohm": p["ra"], "r1_ohm": p["rb"], "gain": p["ratio"],
                                              "error": p["error"]} for p in pairs]})
        return
    console.print(_pairs_table(pairs, "R2 = R4", "R1 = R3", lambda p: p["ratio"]))
    theory("Vout = (R2 / R1) · (V+ − V−)", t("op.diff.note"))


@app.command(name="sum", help=t("op.sum.help"))
def summing(
    rf: float = typer.Option(..., "--rf", **eng(t("op.opt.rf"))),
    rin: List[float] = typer.Option(..., "--rin", parser=cli_parser(parse_value), metavar=t("ui.metavar.value"),
                                    help=t("op.sum.opt.rin")),
    vin: List[float] = typer.Option(..., "--vin", parser=cli_parser(parse_value), metavar=t("ui.metavar.value"),
                                    help=t("op.sum.opt.vin")),
):
    if len(rin) != len(vin):
        fail(t("op.sum.mismatch"))
    if min(rin) <= 0 or rf <= 0:
        fail(t("common.positive_all"))
    vout = -rf * sum(v / r for v, r in zip(vin, rin))
    rows = {f"V{i + 1} · (−Rf/R{i + 1})": f"{format_si(v, 'V')} · {-rf / r:.4g}"
            for i, (v, r) in enumerate(zip(vin, rin))}
    rows["Vout"] = format_si(vout, "V")
    result_panel(t("op.sum.title"), rows, data={"rf_ohm": rf, "rin_ohm": rin, "vin_v": vin, "vout_v": vout})
    theory("Vout = −Rf · Σ (Vi / Ri)")
