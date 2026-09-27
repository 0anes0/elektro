"""Transistör anahtarlama ve RC/RL geçici hal."""

from __future__ import annotations

import math
from typing import Optional

import typer
from rich.table import Table

from elektro.i18n import pct, t
from elektro.ui import console, eng, fail, json_mode, result_panel, theory, warn
from elektro.units import format_si, series_neighbors

switch_app = typer.Typer(help=t("sw.help"), no_args_is_help=True)


@switch_app.command(help=t("sw.bjt.help"))
def bjt(
    ic: Optional[float] = typer.Option(None, "--ic", **eng(t("sw.bjt.opt.ic"))),
    vdrive: float = typer.Option(..., "--vdrive", "-v", **eng(t("sw.opt.vdrive"))),
    hfe: float = typer.Option(100, "--hfe", help=t("sw.bjt.opt.hfe")),
    overdrive: float = typer.Option(3, "--overdrive", help=t("sw.bjt.opt.overdrive")),
    vbe: float = typer.Option(0.7, "--vbe", help=t("sw.bjt.opt.vbe")),
    vcesat: float = typer.Option(0.2, "--vcesat", help=t("sw.bjt.opt.vcesat")),
    vcc: Optional[float] = typer.Option(None, "--vcc", **eng(t("sw.bjt.opt.vcc"))),
    rload: Optional[float] = typer.Option(None, "--rload", **eng(t("sw.bjt.opt.rload"))),
):
    if ic is None:
        if vcc is None or rload is None:
            fail(t("sw.bjt.need"))
        ic = (vcc - vcesat) / rload
    if ic <= 0 or hfe <= 0 or overdrive <= 0:
        fail(t("common.positive_all"))
    if vdrive <= vbe:
        fail(t("sw.bjt.vdrive_low", vbe=vbe))
    ib = ic / hfe * overdrive
    rb = (vdrive - vbe) / ib
    rb_std, _ = series_neighbors(rb, "E12")      # bir alt değer: taban akımı azalmasın
    ib_real = (vdrive - vbe) / rb_std
    result_panel(t("sw.bjt.title"), {
        "Ic": format_si(ic, "A"),
        t("sw.bjt.ib"): format_si(ib, "A"),
        t("sw.bjt.rb_calc"): format_si(rb, "Ω"),
        t("sw.bjt.rb_std"): f"{format_si(rb_std, 'Ω')} (Ib = {format_si(ib_real, 'A')})",
        t("sw.bjt.forced_beta"): f"{ic / ib_real:.1f}",
        t("sw.bjt.p_transistor"): format_si(vcesat * ic, "W"),
        t("sw.bjt.p_rb"): format_si(ib_real ** 2 * rb_std, "W"),
    }, data={"ic_a": ic, "ib_a": ib, "rb_calc_ohm": rb, "rb_ohm": rb_std, "ib_real_a": ib_real,
             "forced_beta": ic / ib_real, "p_transistor_w": vcesat * ic})
    if ib_real > 20e-3:
        warn(t("sw.bjt.gpio_warn", ib=format_si(ib_real, "A")))
    theory(t("sw.bjt.note"))


@switch_app.command(help=t("sw.fet.help"))
def mosfet(
    vdrive: float = typer.Option(..., "--vdrive", "-v", **eng(t("sw.opt.vdrive"))),
    qg: float = typer.Option(..., "--qg", **eng(t("sw.fet.opt.qg"))),
    rg: float = typer.Option(10, "--rg", **eng(t("sw.fet.opt.rg"))),
    fsw: Optional[float] = typer.Option(None, "--fsw", "-f", **eng(t("sw.fet.opt.fsw"))),
    id_: Optional[float] = typer.Option(None, "--id", **eng(t("sw.fet.opt.id"))),
    rds: Optional[float] = typer.Option(None, "--rds", **eng(t("sw.fet.opt.rds"))),
    vds: Optional[float] = typer.Option(None, "--vds", **eng(t("sw.fet.opt.vds"))),
):
    if min(vdrive, qg, rg) <= 0:
        fail(t("common.positive_all"))
    i_peak = vdrive / rg
    t_sw = qg / i_peak
    rows = {
        t("sw.fet.ipeak"): format_si(i_peak, "A"),
        t("sw.fet.tsw"): format_si(t_sw, "s"),
    }
    data = {"gate_peak_a": i_peak, "switch_time_s": t_sw}
    total = 0.0
    if fsw is not None:
        p_gate = qg * vdrive * fsw
        rows[t("sw.fet.pgate")] = format_si(p_gate, "W")
        data["gate_drive_w"] = p_gate
        if t_sw * 2 > 0.1 / fsw:
            warn(t("sw.fet.slow"))
    if id_ is not None and rds is not None:
        p_cond = id_ ** 2 * rds
        rows[t("sw.fet.pcond")] = format_si(p_cond, "W")
        data["conduction_w"] = p_cond
        total += p_cond
    if id_ is not None and vds is not None and fsw is not None:
        p_sw = 0.5 * vds * id_ * (2 * t_sw) * fsw
        rows[t("sw.fet.psw")] = format_si(p_sw, "W")
        data["switching_w"] = p_sw
        total += p_sw
    if total:
        rows[t("sw.fet.ptotal")] = format_si(total, "W")
        data["total_w"] = total
    result_panel(t("sw.fet.title"), rows, data=data)
    if vdrive < 5:
        warn(t("sw.fet.logic_level"))
    theory(t("sw.fet.note"))


# --- Geçici hal -----------------------------------------------------------------------

def charge(
    r: float = typer.Option(..., "--r", **eng(t("chg.opt.r"))),
    c: Optional[float] = typer.Option(None, "--c", **eng(t("chg.opt.c"))),
    l: Optional[float] = typer.Option(None, "--l", **eng(t("chg.opt.l"))),
    v: float = typer.Option(..., "--v", **eng(t("chg.opt.v"))),
    v0: float = typer.Option(0, "--v0", **eng(t("chg.opt.v0"))),
    to: Optional[float] = typer.Option(None, "--to", **eng(t("chg.opt.to"))),
    at: Optional[float] = typer.Option(None, "--t", **eng(t("chg.opt.t"))),
):
    if (c is None) == (l is None):
        fail(t("chg.need"))
    if r <= 0 or (c or l) <= 0:
        fail(t("common.positive_all"))
    inductive = l is not None
    tau = l / r if inductive else r * c
    # RC: kondansatör gerilimi v0 → v;  RL: bobin akımı v0/r → v/r
    final = v / r if inductive else v
    start = v0 / r if inductive else v0
    unit = "A" if inductive else "V"

    def value_at(time):
        return final + (start - final) * math.exp(-time / tau)

    rows = {"τ": format_si(tau, "s"), t("chg.final"): format_si(final, unit)}
    data = {"tau_s": tau, "final": final, "start": start, "unit": unit}
    for n in (1, 3, 5):
        rows[f"{n}τ"] = f"{format_si(n * tau, 's')} → {format_si(value_at(n * tau), unit)}"
    if at is not None:
        rows[t("chg.value_at", time=format_si(at, "s"))] = format_si(value_at(at), unit)
        data["value_at_t"] = value_at(at)
    if to is not None:
        target = to / r if inductive else to
        ratio = (target - final) / (start - final) if start != final else -1
        if not 0 < ratio < 1:
            fail(t("chg.unreachable"))
        time = -tau * math.log(ratio)
        rows[t("chg.time_to", target=format_si(target, unit))] = format_si(time, "s")
        data["time_to_target_s"] = time
    result_panel(t("chg.title_rl" if inductive else "chg.title_rc"), rows, data=data)

    if json_mode():
        return
    # ASCII eğri: 0 … 5τ
    tbl = Table(box=None, show_header=False)
    tbl.add_column(justify="right", style="dim")
    tbl.add_column(justify="right")
    tbl.add_column(no_wrap=True)
    span = max(abs(final), abs(start)) or 1
    for step in range(11):
        time = step * tau / 2
        val = value_at(time)
        bar = "█" * round(30 * abs(val) / span)
        tbl.add_row(f"{step / 2:.1f}τ", format_si(val, unit), f"[green]{bar}[/]")
    console.print()
    console.print(tbl)
    if not inductive:
        theory(t("chg.note", pct=pct("63")))
