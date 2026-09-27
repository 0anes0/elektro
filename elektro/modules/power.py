"""Güç ve besleme: regülatör, batarya ömrü, ısıl hesap."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import List, Optional

import typer

from elektro.i18n import pct, t
from elektro.ui import cli_parser, eng, fail, result_panel, theory, warn
from elektro.units import format_si, nearest_standard, parse_value


# --- Regülatör --------------------------------------------------------------------

@dataclass(frozen=True)
class Regulator:
    name: str
    vref: Optional[float]      # ayarlıysa referans gerilimi
    vout: Optional[float]      # sabitse çıkış gerilimi
    r1: Optional[float]        # önerilen R1 (çıkış–ADJ arası)
    dropout: float             # tipik düşüm gerilimi (V)
    switching: bool = False
    iadj: float = 0.0          # ADJ bacağı akımı (A)


ADJUSTABLE = {
    "lm317": Regulator("LM317", 1.25, None, 240, 2.5, iadj=50e-6),
    "lm1117": Regulator("LM1117-ADJ", 1.25, None, 120, 1.2),
    "ams1117": Regulator("AMS1117-ADJ", 1.25, None, 120, 1.3),
    "lm2596": Regulator("LM2596-ADJ", 1.23, None, 1e3, 1.5, switching=True),
    "xl4015": Regulator("XL4015", 1.25, None, 1e3, 1.5, switching=True),
    "mp1584": Regulator("MP1584", 0.8, None, 10e3, 1.0, switching=True),
}


def find_regulator(name: str) -> Regulator:
    key = name.strip().lower().replace("_", "-")
    if key in ADJUSTABLE:
        return ADJUSTABLE[key]
    m = re.fullmatch(r"(?:l|lm|mc|ua)?78(?:l|m|s)?(\d{2})\w*", key)
    if m:
        return Regulator(name.upper(), None, float(m.group(1)), None, 2.0)
    m = re.fullmatch(r"(ams1117|lm1117|ld1117|az1117)-?(\d+(?:\.\d+)?)", key)
    if m:
        return Regulator(name.upper(), None, float(m.group(2)), None, 1.2)
    raise ValueError(t("reg.unknown", name=name, options="lm317, lm1117, ams1117, lm2596, xl4015, mp1584, 78xx, ams1117-3.3"))


def adjustable_r2(reg: Regulator, vout: float, r1: float) -> float:
    """Vout = Vref·(1 + R2/R1) + Iadj·R2  →  R2"""
    if vout <= reg.vref:
        raise ValueError(t("reg.vout_low", vref=reg.vref))
    return (vout - reg.vref) / (reg.vref / r1 + reg.iadj)


def adjustable_vout(reg: Regulator, r1: float, r2: float) -> float:
    return reg.vref * (1 + r2 / r1) + reg.iadj * r2


def regulator(
    part: str = typer.Argument(..., help=t("reg.arg")),
    vout: Optional[float] = typer.Option(None, "--vout", **eng(t("reg.opt.vout"))),
    vin: Optional[float] = typer.Option(None, "--vin", **eng(t("reg.opt.vin"))),
    iout: Optional[float] = typer.Option(None, "--iout", "-i", **eng(t("reg.opt.iout"))),
    r1: Optional[float] = typer.Option(None, "--r1", **eng(t("reg.opt.r1"))),
    r2: Optional[float] = typer.Option(None, "--r2", **eng(t("reg.opt.r2"))),
):
    try:
        reg = find_regulator(part)
    except ValueError as e:
        fail(str(e))

    rows, data = {}, {"part": reg.name, "switching": reg.switching}
    if reg.vref is not None:
        r1 = r1 or reg.r1
        if r2 is not None:
            vout = adjustable_vout(reg, r1, r2)
            rows[t("reg.vout")] = format_si(vout, "V")
        else:
            if vout is None:
                fail(t("reg.need_vout"))
            try:
                r2_calc = adjustable_r2(reg, vout, r1)
            except ValueError as e:
                fail(str(e))
            r2 = nearest_standard(r2_calc, "E24")
            r2_96 = nearest_standard(r2_calc, "E96")
            rows[t("reg.r2_calc")] = format_si(r2_calc, "Ω")
            rows["R2 (E24)"] = f"{format_si(r2, 'Ω')} → {format_si(adjustable_vout(reg, r1, r2), 'V')}"
            rows["R2 (E96)"] = f"{format_si(r2_96, 'Ω')} → {format_si(adjustable_vout(reg, r1, r2_96), 'V')}"
            data.update(r2_calc_ohm=r2_calc, r2_e24_ohm=r2, r2_e96_ohm=r2_96,
                        vout_e24_v=adjustable_vout(reg, r1, r2))
        rows = {"R1": format_si(r1, "Ω"), **rows}
        data.update(vref_v=reg.vref, r1_ohm=r1, r2_ohm=r2, vout_v=vout)
    else:
        vout = reg.vout
        rows[t("reg.vout")] = format_si(vout, "V")
        data["vout_v"] = vout

    rows[t("reg.dropout")] = format_si(reg.dropout, "V")
    if vin is not None:
        headroom = vin - vout
        rows[t("reg.headroom")] = format_si(headroom, "V")
        data.update(vin_v=vin, headroom_v=headroom)
        if headroom < reg.dropout:
            warn(t("reg.dropout_warn", headroom=f"{headroom:.2f}", dropout=reg.dropout))
        if iout is not None and not reg.switching:
            p = headroom * iout
            rows[t("reg.power")] = format_si(p, "W")
            rows[t("reg.efficiency")] = pct(f"{vout / vin * 100:.0f}")
            data.update(iout_a=iout, dissipation_w=p, efficiency=vout / vin)
    result_panel(reg.name, rows, data=data)
    if reg.switching:
        theory(t("reg.switching_note"))
    elif vin is not None and iout is not None and (vin - vout) * iout > 1:
        theory(t("reg.heat_note"))


# --- Batarya -----------------------------------------------------------------------

def average_current(active: float, active_time: float, sleep: float, sleep_time: float) -> float:
    return (active * active_time + sleep * sleep_time) / (active_time + sleep_time)


def battery(
    capacity: float = typer.Argument(..., help=t("bat.arg")),
    current: Optional[float] = typer.Option(None, "--current", "-i", **eng(t("bat.opt.current"))),
    active: Optional[float] = typer.Option(None, "--active", **eng(t("bat.opt.active"))),
    active_time: Optional[float] = typer.Option(None, "--active-time", **eng(t("bat.opt.active_time"))),
    sleep: Optional[float] = typer.Option(None, "--sleep", **eng(t("bat.opt.sleep"))),
    sleep_time: Optional[float] = typer.Option(None, "--sleep-time", **eng(t("bat.opt.sleep_time"))),
    derate: float = typer.Option(0.8, "--derate", help=t("bat.opt.derate")),
):
    if capacity <= 0 or not 0 < derate <= 1:
        fail(t("common.positive_all"))
    if current is None:
        parts = (active, active_time, sleep, sleep_time)
        if any(x is None for x in parts):
            fail(t("bat.need"))
        if active_time + sleep_time <= 0:
            fail(t("common.positive_all"))
        current = average_current(*parts)
    if current <= 0:
        fail(t("common.positive"))
    usable_mah = capacity * derate
    hours = usable_mah / (current * 1e3)
    result_panel(t("bat.title"), {
        t("bat.capacity"): f"{capacity:g} mAh",
        t("bat.usable"): f"{usable_mah:g} mAh",
        t("bat.avg_current"): format_si(current, "A"),
        t("bat.life"): _duration(hours),
    }, data={"capacity_mah": capacity, "usable_mah": usable_mah, "average_current_a": current,
             "life_hours": hours, "life_days": hours / 24})
    theory(t("bat.note"))


def _duration(hours: float) -> str:
    if hours < 1:
        return f"{hours * 60:.1f} {t('time.min')}"
    if hours < 48:
        return f"{hours:.1f} {t('time.hours')}"
    days = hours / 24
    if days < 60:
        return f"{days:.1f} {t('time.days')} ({hours:.0f} {t('time.hours')})"
    return f"{days / 30.44:.1f} {t('time.months')} ({days:.0f} {t('time.days')})"


# --- Isıl hesap ----------------------------------------------------------------------

def thermal(
    power: float = typer.Option(..., "--power", "-p", **eng(t("th.opt.power"))),
    ta: float = typer.Option(25, "--ta", help=t("th.opt.ta")),
    tj_max: float = typer.Option(150, "--tj-max", help=t("th.opt.tjmax")),
    rth_ja: Optional[float] = typer.Option(None, "--rth-ja", help=t("th.opt.rja")),
    rth_jc: Optional[float] = typer.Option(None, "--rth-jc", help=t("th.opt.rjc")),
    rth_cs: float = typer.Option(0.5, "--rth-cs", help=t("th.opt.rcs")),
    rth_sa: Optional[float] = typer.Option(None, "--rth-sa", help=t("th.opt.rsa")),
):
    if power <= 0:
        fail(t("common.positive"))
    rows, data = {t("th.power"): format_si(power, "W"), "Ta": f"{ta:g} °C"}, {"power_w": power, "ta_c": ta}
    if rth_ja is not None:
        tj = ta + power * rth_ja
        rows["Rθja"] = f"{rth_ja:g} °C/W"
        data["rth_ja"] = rth_ja
    elif rth_jc is not None and rth_sa is not None:
        total = rth_jc + rth_cs + rth_sa
        tj = ta + power * total
        rows[t("th.total")] = f"{total:g} °C/W"
        data["rth_total"] = total
    elif rth_jc is not None:
        need = (tj_max - ta) / power - rth_jc - rth_cs
        rows[t("th.need_sa")] = f"{need:.2f} °C/W" if need > 0 else t("th.impossible")
        data["required_rth_sa"] = need if need > 0 else None
        result_panel(t("th.title"), rows, data=data)
        theory(t("th.margin_note"))
        return
    else:
        fail(t("th.need"))
    margin = tj_max - tj
    color = "green" if margin > 25 else "yellow" if margin >= 0 else "red"
    rows["Tj"] = f"[{color}]{tj:.1f} °C[/]"
    rows[t("th.margin")] = f"{margin:.1f} °C"
    data.update(tj_c=tj, margin_c=margin)
    result_panel(t("th.title"), rows, data=data)
    if margin < 0:
        warn(t("th.over"))


# --- Doğrultucu + filtre kondansatörü -------------------------------------------------------

CAP_VOLTAGES = [6.3, 10, 16, 25, 35, 50, 63, 80, 100, 160, 200, 250, 350, 400, 450]
RECTIFIERS = {"bridge": (2, 2), "center": (1, 2), "half": (1, 1)}   # (seri diyot, dalgalanma çarpanı)


def rectifier_calc(vac: float, kind: str, freq: float, vdiode: float, iload: Optional[float],
                   ripple: Optional[float], c: Optional[float]) -> dict:
    diodes, k = RECTIFIERS[kind]
    vpeak = vac * math.sqrt(2) - diodes * vdiode
    if vpeak <= 0:
        raise ValueError(t("rect.too_low"))
    out = {"vpeak": vpeak, "piv": vac * math.sqrt(2) * (2 if kind == "center" else 1), "ripple_freq": k * freq}
    if iload is not None:
        if c is None and ripple is not None:
            c = iload / (k * freq * ripple)
        if c is not None:
            ripple = iload / (k * freq * c)
            out.update(c=c, ripple=ripple, vdc=vpeak - ripple / 2, vmin=vpeak - ripple)
    out["cap_voltage"] = next((v for v in CAP_VOLTAGES if v >= vpeak * 1.25), None)
    return out


def rectifier(
    vac: float = typer.Option(..., "--vac", **eng(t("rect.opt.vac"))),
    kind: str = typer.Option("bridge", "--type", help=t("rect.opt.type")),
    freq: float = typer.Option(50, "--freq", "-f", **eng(t("rect.opt.freq"))),
    iload: Optional[float] = typer.Option(None, "--iload", "-i", **eng(t("rect.opt.iload"))),
    ripple: Optional[float] = typer.Option(None, "--ripple", **eng(t("rect.opt.ripple"))),
    c: Optional[float] = typer.Option(None, "--c", **eng(t("rect.opt.c"))),
    vdiode: float = typer.Option(0.7, "--vdiode", help=t("rect.opt.vdiode")),
    vmains: Optional[float] = typer.Option(None, "--vmains", **eng(t("rect.opt.vmains"))),
):
    kind = kind.lower()
    if kind not in RECTIFIERS:
        fail(t("rect.bad_type", options=", ".join(RECTIFIERS)))
    try:
        r = rectifier_calc(vac, kind, freq, vdiode, iload, ripple, c)
    except ValueError as e:
        fail(str(e))
    rows = {
        t("rect.type"): t(f"rect.kind.{kind}"),
        t("rect.vpeak"): format_si(r["vpeak"], "V"),
        t("rect.piv"): format_si(r["piv"], "V"),
        t("rect.ripple_freq"): format_si(r["ripple_freq"], "Hz"),
    }
    if "c" in r:
        c_std = next((x for x in (1e-6 * v for v in (100, 220, 330, 470, 680, 1000, 1500, 2200, 3300,
                                                          4700, 6800, 10000, 15000, 22000)) if x >= r["c"]), None)
        rows[t("rect.c")] = format_si(r["c"], "F") + (f"  → {format_si(c_std, 'F')}" if c_std else "")
        rows[t("rect.ripple")] = format_si(r["ripple"], "V")
        rows["Vdc (avg)"] = format_si(r["vdc"], "V")
        rows["Vmin"] = format_si(r["vmin"], "V")
    if r["cap_voltage"]:
        rows[t("rect.cap_voltage")] = f"≥ {r['cap_voltage']:g} V"
    if vmains:
        rows[t("rect.ratio")] = f"{vmains / vac:.2f} : 1"
    if iload is not None:
        rows[t("rect.diode_i")] = format_si(iload * (1 if kind == "half" else 0.5), "A") + " (avg)"
    result_panel(t("rect.title"), rows, data={"type": kind, **{k: v for k, v in r.items()}})
    if "c" not in r:
        theory(t("rect.hint"))
    else:
        theory(t("rect.note"))


# --- AC güç ------------------------------------------------------------------------------------

def ac_power(v: float, i: float, pf: float, phases: int) -> dict:
    s = (math.sqrt(3) if phases == 3 else 1) * v * i
    p = s * pf
    q = math.sqrt(max(s * s - p * p, 0))
    return {"s": s, "p": p, "q": q, "phi": math.degrees(math.acos(pf))}


def correction_capacitor(p: float, pf_from: float, pf_to: float, v: float, freq: float, phases: int) -> dict:
    qc = p * (math.tan(math.acos(pf_from)) - math.tan(math.acos(pf_to)))
    w = 2 * math.pi * freq
    # 3 fazda üçgen bağlı kondansatör başına: V hat gerilimi
    c = qc / (3 * w * v * v) if phases == 3 else qc / (w * v * v)
    return {"qc": qc, "c": c}


def acpower(
    v: float = typer.Option(230, "--v", **eng(t("ac.opt.v"))),
    i: Optional[float] = typer.Option(None, "--i", **eng(t("ac.opt.i"))),
    p: Optional[float] = typer.Option(None, "--p", **eng(t("ac.opt.p"))),
    pf: float = typer.Option(1.0, "--pf", help=t("ac.opt.pf")),
    phases: int = typer.Option(1, "--phases", help=t("ac.opt.phases")),
    target_pf: Optional[float] = typer.Option(None, "--target-pf", help=t("ac.opt.target")),
    freq: float = typer.Option(50, "--freq", "-f", **eng(t("rect.opt.freq"))),
):
    if phases not in (1, 3):
        fail(t("ac.bad_phases"))
    if not 0 < pf <= 1 or v <= 0:
        fail(t("ac.bad_pf"))
    k = math.sqrt(3) if phases == 3 else 1
    if i is None:
        if p is None:
            fail(t("ac.need"))
        i = p / (k * v * pf)
    r = ac_power(v, i, pf, phases)
    rows = {
        t("ac.system"): t("ac.three") if phases == 3 else t("ac.single"),
        t("ac.current"): format_si(i, "A"),
        t("ac.p"): format_si(r["p"], "W"),
        t("ac.q"): format_si(r["q"], "var"),
        t("ac.s"): format_si(r["s"], "VA"),
        "cos φ / φ": f"{pf:g} / {r['phi']:.1f}°",
    }
    data = {"phases": phases, "v": v, "i_a": i, "p_w": r["p"], "q_var": r["q"], "s_va": r["s"],
            "pf": pf, "phi_deg": r["phi"]}
    if target_pf is not None:
        if not pf < target_pf <= 1:
            fail(t("ac.bad_target"))
        cc = correction_capacitor(r["p"], pf, target_pf, v, freq, phases)
        new_i = r["p"] / (k * v * target_pf)
        rows[t("ac.qc")] = format_si(cc["qc"], "var")
        rows[t("ac.cap_delta") if phases == 3 else t("ac.cap")] = format_si(cc["c"], "F")
        rows[t("ac.new_current")] = format_si(new_i, "A")
        data.update(qc_var=cc["qc"], c_f=cc["c"], new_current_a=new_i)
    result_panel(t("ac.title"), rows, data=data)
    if phases == 3:
        theory(t("ac.three_note"))


def star_delta(mode: str, a: float, b: float, c: float) -> tuple:
    if mode == "delta":            # Δ (Rab, Rbc, Rca) → Y (Ra, Rb, Rc)
        total = a + b + c
        return (a * c / total, a * b / total, b * c / total)
    s = a * b + b * c + c * a      # Y (Ra, Rb, Rc) → Δ (Rab, Rbc, Rca)
    return (s / c, s / a, s / b)


def stardelta(
    mode: str = typer.Argument(..., help=t("sd.arg.mode")),
    values: List[float] = typer.Argument(..., parser=cli_parser(parse_value), metavar="R1 R2 R3", help=t("sd.arg.values")),
):
    mode = mode.lower()
    if mode not in ("delta", "star") or len(values) != 3:
        fail(t("sd.bad"))
    if min(values) <= 0:
        fail(t("common.positive_all"))
    out = star_delta(mode, *values)
    if mode == "delta":
        rows = {"Ra (A)": format_si(out[0], "Ω"), "Rb (B)": format_si(out[1], "Ω"), "Rc (C)": format_si(out[2], "Ω")}
        data = {"ra": out[0], "rb": out[1], "rc": out[2]}
        title = "Δ → Y"
    else:
        rows = {"Rab": format_si(out[0], "Ω"), "Rbc": format_si(out[1], "Ω"), "Rca": format_si(out[2], "Ω")}
        data = {"rab": out[0], "rbc": out[1], "rca": out[2]}
        title = "Y → Δ"
    result_panel(title, rows, data=data)
    theory(t("sd.note"))
