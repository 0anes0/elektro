"""Elektrik makineleri: transformatör (oran, akımlar, küçük trafo sarımı) ve asenkron motor."""

from __future__ import annotations

import math
from typing import Optional

import typer

from elektro.i18n import pct, t
from elektro.modules.wiring import area_to_awg
from elektro.ui import eng, fail, result_panel, theory, warn
from elektro.units import format_si


# --- Transformatör -----------------------------------------------------------------------------

def wire_diameter(current: float, density: float) -> float:
    """Akım yoğunluğuna göre iletken çapı (mm)."""
    return math.sqrt(4 * current / (math.pi * density))


def transformer_design(va: float, v1: float, v2: float, freq: float, b: float, density: float,
                       eff: float, area_cm2: Optional[float], regulation: float) -> dict:
    """Tek fazlı küçük şebeke trafosu (EI nüve): nüve kesiti, sarım sayıları, tel çapları."""
    p1 = va / eff
    area = area_cm2 if area_cm2 else math.sqrt(p1)        # A [cm²] ≈ √P1
    turns_per_volt = 1e4 / (4.44 * freq * b * area)
    i1, i2 = p1 / v1, va / v2
    d1, d2 = wire_diameter(i1, density), wire_diameter(i2, density)
    return {
        "p1_va": p1, "area_cm2": area, "turns_per_volt": turns_per_volt,
        "n1": turns_per_volt * v1, "n2": turns_per_volt * v2 * (1 + regulation / 100),
        "i1_a": i1, "i2_a": i2, "d1_mm": d1, "d2_mm": d2,
        "awg1": area_to_awg(math.pi * (d1 / 2) ** 2 * 1e-6), "awg2": area_to_awg(math.pi * (d2 / 2) ** 2 * 1e-6),
    }


def transformer(
    v1: float = typer.Option(..., "--v1", **eng(t("tr.opt.v1"))),
    v2: float = typer.Option(..., "--v2", **eng(t("tr.opt.v2"))),
    va: Optional[float] = typer.Option(None, "--va", **eng(t("tr.opt.va"))),
    phases: int = typer.Option(1, "--phases", help=t("ac.opt.phases")),
    freq: float = typer.Option(50, "--freq", "-f", **eng(t("rect.opt.freq"))),
    b: float = typer.Option(1.2, "--b", help=t("tr.opt.b")),
    density: float = typer.Option(2.5, "--j", help=t("tr.opt.j")),
    eff: float = typer.Option(0.9, "--eff", help=t("tr.opt.eff")),
    area: Optional[float] = typer.Option(None, "--area", help=t("tr.opt.area")),
    regulation: float = typer.Option(5, "--reg", help=t("tr.opt.reg")),
):
    if phases not in (1, 3):
        fail(t("ac.bad_phases"))
    if min(v1, v2, freq, b, density) <= 0 or not 0 < eff <= 1 or (va is not None and va <= 0) \
            or (area is not None and area <= 0):
        fail(t("common.positive_all"))
    ratio = v1 / v2
    rows = {
        t("tr.ratio"): f"{ratio:.4g} : 1" if ratio >= 1 else f"1 : {1 / ratio:.4g}",
        t("tr.kind"): t("tr.step_down") if ratio > 1 else t("tr.step_up") if ratio < 1 else "1 : 1",
    }
    data = {"v1": v1, "v2": v2, "ratio": ratio, "phases": phases}
    if va is None:
        result_panel(t("tr.title"), rows, data=data)
        theory(t("tr.hint"))
        return

    k = math.sqrt(3) if phases == 3 else 1
    i1, i2 = va / eff / (k * v1), va / (k * v2)
    rows[t("tr.power")] = format_si(va, "VA")
    rows["I1 / I2"] = f"{format_si(i1, 'A')} / {format_si(i2, 'A')}"
    data.update(va=va, eff=eff, i1_a=i1, i2_a=i2)
    if phases == 3:
        result_panel(t("tr.title"), rows, data=data)
        theory(t("tr.three_note"))
        return

    d = transformer_design(va, v1, v2, freq, b, density, eff, area, regulation)
    rows[t("tr.area")] = f"{d['area_cm2']:.1f} cm²" + ("" if area else f"  (≈ √{d['p1_va']:.0f} VA)")
    rows[t("tr.tpv")] = f"{d['turns_per_volt']:.3g}"
    rows["N1"] = f"{math.ceil(d['n1'])}"
    rows["N2"] = f"{math.ceil(d['n2'])}  (+{pct(f'{regulation:g}')})"
    rows[t("tr.wire1")] = f"{d['d1_mm']:.2f} mm  (AWG {d['awg1']:.0f})"
    rows[t("tr.wire2")] = f"{d['d2_mm']:.2f} mm  (AWG {d['awg2']:.0f})"
    data.update({k_: v_ for k_, v_ in d.items() if k_ not in ("i1_a", "i2_a")})
    result_panel(t("tr.title"), rows, data=data)
    if va > 2000:
        warn(t("tr.big"))
    theory(t("tr.note1", b=f"{b:g}", j=f"{density:g}"), t("tr.note2"))


# --- Asenkron motor --------------------------------------------------------------------------

def motor_calc(power: float, v: float, phases: int, pf: float, eff: float, freq: float, poles: int,
               rpm: Optional[float], start_ratio: float) -> dict:
    ns = 120 * freq / poles
    assumed = rpm is None
    n = rpm if rpm is not None else ns * 0.96
    slip = (ns - n) / ns
    pin = power / eff
    k = math.sqrt(3) if phases == 3 else 1
    current = pin / (k * v * pf)
    s = pin / pf
    torque = power / (2 * math.pi * n / 60)
    return {"ns_rpm": ns, "n_rpm": n, "slip": slip, "rotor_freq_hz": slip * freq, "speed_assumed": assumed,
            "pin_w": pin, "losses_w": pin - power, "current_a": current, "s_va": s,
            "q_var": math.sqrt(max(s * s - pin * pin, 0)), "torque_nm": torque, "hp": power / 745.7,
            "start_current_a": start_ratio * current, "star_delta_current_a": start_ratio * current / 3}


def motor(
    power: float = typer.Option(..., "--power", "-p", **eng(t("mot.opt.power"))),
    v: float = typer.Option(400, "--v", **eng(t("mot.opt.v"))),
    phases: int = typer.Option(3, "--phases", help=t("ac.opt.phases")),
    pf: float = typer.Option(0.85, "--pf", help=t("ac.opt.pf")),
    eff: float = typer.Option(0.9, "--eff", help=t("mot.opt.eff")),
    freq: float = typer.Option(50, "--freq", "-f", **eng(t("rect.opt.freq"))),
    poles: int = typer.Option(4, "--poles", help=t("mot.opt.poles")),
    rpm: Optional[float] = typer.Option(None, "--rpm", help=t("mot.opt.rpm")),
    start: float = typer.Option(7, "--start", help=t("mot.opt.start")),
):
    if phases not in (1, 3):
        fail(t("ac.bad_phases"))
    if poles < 2 or poles % 2:
        fail(t("mot.bad_poles"))
    if min(power, v, freq, start) <= 0 or not 0 < pf <= 1 or not 0 < eff <= 1:
        fail(t("common.positive_all"))
    ns = 120 * freq / poles
    if rpm is not None and not 0 < rpm <= ns:
        fail(t("mot.bad_rpm", ns=f"{ns:g}"))
    r = motor_calc(power, v, phases, pf, eff, freq, poles, rpm, start)
    slip = pct(f"{r['slip'] * 100:.2f}")
    speed = f"{r['n_rpm']:.0f} rpm" + (f"  ({t('mot.assumed')})" if r["speed_assumed"] else "")
    rows = {
        t("mot.power"): f"{format_si(power, 'W')} ({r['hp']:.2f} HP)",
        t("mot.ns"): f"{ns:g} rpm  ({poles} {t('mot.poles')})",
        t("mot.speed"): speed,
        t("mot.slip"): f"{slip}  (f2 = {r['rotor_freq_hz']:.2f} Hz)",
        t("mot.torque"): f"{r['torque_nm']:.2f} N·m",
        t("mot.pin"): format_si(r["pin_w"], "W"),
        t("mot.losses"): format_si(r["losses_w"], "W"),
        t("mot.current"): format_si(r["current_a"], "A"),
        "S / Q": f"{format_si(r['s_va'], 'VA')} / {format_si(r['q_var'], 'var')}",
        t("mot.start_dol"): f"≈ {format_si(r['start_current_a'], 'A')}  ({start:g} × In)",
    }
    if phases == 3:
        rows[t("mot.start_yd")] = f"≈ {format_si(r['star_delta_current_a'], 'A')}"
    data = {"power_w": power, "v": v, "phases": phases, "pf": pf, "eff": eff, "freq_hz": freq,
            "poles": poles, **r}
    result_panel(t("mot.title"), rows, data=data)
    theory(t("mot.note1"), t("mot.note2") if phases == 3 else t("mot.note_single"))
