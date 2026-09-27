"""Güç ve besleme: regülatör, batarya ömrü, ısıl hesap."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

import typer
from rich.table import Table

from elektro.i18n import pct, t
from elektro.ui import emit, eng, fail, result_panel, theory, warn
from elektro.units import format_si, nearest_standard


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
