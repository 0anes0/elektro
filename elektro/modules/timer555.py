"""NE555 zamanlayıcı hesapları."""

from __future__ import annotations

import math
from typing import Optional

import typer

from elektro.i18n import pct, t
from elektro.ui import eng, fail, result_panel, theory
from elektro.units import format_si, nearest_standard

app = typer.Typer(help=t("555.help"), no_args_is_help=True)

LN2 = math.log(2)


def astable_timing(r1: float, r2: float, c: float) -> dict:
    t_high = LN2 * (r1 + r2) * c
    t_low = LN2 * r2 * c
    period = t_high + t_low
    return {"t_high": t_high, "t_low": t_low, "period": period,
            "freq": 1 / period, "duty": t_high / period}


def astable_design(freq: float, duty: float, c: float) -> tuple:
    """Frekans ve görev oranından R1, R2 (duty > 0.5 olmalı)."""
    if not 0.5 < duty < 1:
        raise ValueError(t("555.duty_range"))
    period = 1 / freq
    t_high, t_low = duty * period, (1 - duty) * period
    r2 = t_low / (LN2 * c)
    r1 = t_high / (LN2 * c) - r2
    return r1, r2


@app.command(help=t("555.astable.help"))
def astable(
    r1: Optional[float] = typer.Option(None, "--r1", **eng(t("555.opt.r1"))),
    r2: Optional[float] = typer.Option(None, "--r2", **eng(t("555.opt.r2"))),
    c: float = typer.Option(..., "--c", **eng(t("555.opt.c"))),
    freq: Optional[float] = typer.Option(None, "--freq", "-f", **eng(t("555.opt.freq"))),
    duty: float = typer.Option(60, "--duty", "-d", help=t("555.opt.duty")),
):
    if freq is not None:
        try:
            r1, r2 = astable_design(freq, duty / 100, c)
        except ValueError as e:
            fail(str(e))
        r1s, r2s = nearest_standard(r1, "E24"), nearest_standard(r2, "E24")
        real = astable_timing(r1s, r2s, c)
        result_panel(t("555.design.title"), {
            t("555.r1_calc"): format_si(r1, "Ω"),
            t("555.r2_calc"): format_si(r2, "Ω"),
            "R1 / R2 (E24)": f"{format_si(r1s, 'Ω')} / {format_si(r2s, 'Ω')}",
            t("555.real_freq"): format_si(real["freq"], "Hz"),
            t("555.real_duty"): pct(f"{real['duty'] * 100:.1f}"),
        })
        if r1 < 1e3 or r2 > 1e6:
            theory(t("555.range_warn"))
        return

    if r1 is None or r2 is None:
        fail(t("555.need"))
    if min(r1, r2, c) <= 0:
        fail(t("common.positive_all"))
    tm = astable_timing(r1, r2, c)
    result_panel(t("555.astable.title"), {
        t("555.freq"): format_si(tm["freq"], "Hz"),
        t("555.period"): format_si(tm["period"], "s"),
        t("555.t_high"): format_si(tm["t_high"], "s"),
        t("555.t_low"): format_si(tm["t_low"], "s"),
        t("555.duty"): pct(f"{tm['duty'] * 100:.1f}"),
    })


@app.command(help=t("555.mono.help"))
def mono(
    r: Optional[float] = typer.Option(None, "--r", **eng(t("555.opt.r"))),
    c: Optional[float] = typer.Option(None, "--c", **eng(t("555.opt.c"))),
    t_: Optional[float] = typer.Option(None, "--t", **eng(t("555.opt.t"))),
):
    if sum(x is not None for x in (r, c, t_)) != 2:
        fail(t("555.mono.need"))
    if any(x is not None and x <= 0 for x in (r, c, t_)):
        fail(t("common.positive_all"))
    k = math.log(3)
    if t_ is None:
        t_ = k * r * c
    elif r is None:
        r = t_ / (k * c)
    else:
        c = t_ / (k * r)
    result_panel(t("555.mono.title"), {
        t("555.pulse"): format_si(t_, "s"),
        "R": f"{format_si(r, 'Ω')}  (E24: {format_si(nearest_standard(r, 'E24'), 'Ω')})",
        "C": format_si(c, "F"),
    })
