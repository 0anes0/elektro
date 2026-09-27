"""Ohm kanunu ve güç hesapları."""

from __future__ import annotations

import math
from typing import Optional

import typer
from rich.prompt import Prompt

from elektro.i18n import t
from elektro.ui import console, eng, fail, result_panel, warn
from elektro.units import format_si, parse_value


def solve(v=None, i=None, r=None, p=None) -> dict:
    """V, I, R, P'den herhangi ikisi verilince diğer ikisini hesaplar."""
    given = {k: x for k, x in dict(v=v, i=i, r=r, p=p).items() if x is not None}
    if len(given) < 2:
        raise ValueError(t("ohm.need_two"))
    if r is not None and r < 0 or p is not None and p < 0:
        raise ValueError(t("ohm.negative"))

    try:
        if v is not None and i is not None:
            r_, p_ = v / i, v * i
            v_, i_ = v, i
        elif v is not None and r is not None:
            v_, r_ = v, r
            i_, p_ = v / r, v * v / r
        elif i is not None and r is not None:
            i_, r_ = i, r
            v_, p_ = i * r, i * i * r
        elif v is not None and p is not None:
            v_, p_ = v, p
            i_, r_ = p / v, v * v / p
        elif i is not None and p is not None:
            i_, p_ = i, p
            v_, r_ = p / i, p / (i * i)
        else:
            r_, p_ = r, p
            v_, i_ = math.sqrt(p * r), math.sqrt(p / r)
    except ZeroDivisionError:
        raise ValueError(t("ohm.div_zero"))

    result = {"v": v_, "i": i_, "r": r_, "p": p_}
    # Fazladan verilen değerler hesapla tutarlı mı?
    for key, val in given.items():
        calc = result[key]
        if not math.isclose(val, calc, rel_tol=0.01, abs_tol=1e-12):
            result.setdefault("_conflicts", []).append(key)
    return result


def ohm(
    v: Optional[float] = typer.Option(None, "--voltage", "-v", **eng(t("ohm.opt.v"))),
    i: Optional[float] = typer.Option(None, "--current", "-i", **eng(t("ohm.opt.i"))),
    r: Optional[float] = typer.Option(None, "--resistance", "-r", **eng(t("ohm.opt.r"))),
    p: Optional[float] = typer.Option(None, "--power", "-p", **eng(t("ohm.opt.p"))),
):
    if all(x is None for x in (v, i, r, p)):
        v, i, r, p = _ask()

    try:
        res = solve(v, i, r, p)
    except ValueError as e:
        fail(str(e))

    if res.get("_conflicts"):
        warn(t("ohm.conflict"))

    result_panel(t("ohm.title"), {
        t("ohm.voltage"): format_si(res["v"], "V"),
        t("ohm.current"): format_si(res["i"], "A"),
        t("ohm.resistance"): format_si(res["r"], "Ω"),
        t("ohm.power"): format_si(res["p"], "W"),
    })


def _ask():
    console.print(f"[bold]{t('ohm.wizard')}[/]\n")
    vals = []
    for key in ("ohm.ask.v", "ohm.ask.i", "ohm.ask.r", "ohm.ask.p"):
        while True:
            raw = Prompt.ask(f"  {t(key)}", default="", show_default=False).strip()
            if not raw:
                vals.append(None)
                break
            try:
                vals.append(parse_value(raw))
                break
            except ValueError as e:
                console.print(f"  [red]{e}[/]")
        if sum(x is not None for x in vals) == 2:
            vals += [None] * (4 - len(vals))
            break
    return vals
