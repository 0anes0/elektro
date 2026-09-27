"""Ohm kanunu ve güç hesapları."""

from __future__ import annotations

import math
from typing import Optional

import typer
from rich.prompt import Prompt

from elektro.ui import console, eng, fail, result_panel, warn
from elektro.units import format_si, parse_value


def solve(v=None, i=None, r=None, p=None) -> dict:
    """V, I, R, P'den herhangi ikisi verilince diğer ikisini hesaplar."""
    given = {k: x for k, x in dict(v=v, i=i, r=r, p=p).items() if x is not None}
    if len(given) < 2:
        raise ValueError("en az 2 değer gerekli")
    if r is not None and r < 0 or p is not None and p < 0:
        raise ValueError("direnç ve güç negatif olamaz")

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
        raise ValueError("sıfıra bölme — girilen değerlerle devre tanımsız")

    result = {"v": v_, "i": i_, "r": r_, "p": p_}
    # Fazladan verilen değerler hesapla tutarlı mı?
    for key, val in given.items():
        calc = result[key]
        if not math.isclose(val, calc, rel_tol=0.01, abs_tol=1e-12):
            result.setdefault("_conflicts", []).append(key)
    return result


def ohm(
    v: Optional[float] = typer.Option(None, "--voltage", "-v", **eng("Gerilim (V)")),
    i: Optional[float] = typer.Option(None, "--current", "-i", **eng("Akım (A), örn: 20m")),
    r: Optional[float] = typer.Option(None, "--resistance", "-r", **eng("Direnç (Ω), örn: 4k7")),
    p: Optional[float] = typer.Option(None, "--power", "-p", **eng("Güç (W)")),
):
    """Ohm kanunu: V, I, R, P'den herhangi ikisini ver, diğerlerini hesaplasın.

    V = I·R    P = V·I = I²·R = V²/R

    Parametresiz çalıştırılırsa soru sorarak ilerler.

    Örnekler:
      elektro ohm -v 12 -r 1k
      elektro ohm -i 20m -p 0.5
      elektro ohm
    """
    if all(x is None for x in (v, i, r, p)):
        v, i, r, p = _ask()

    try:
        res = solve(v, i, r, p)
    except ValueError as e:
        fail(str(e))

    if res.get("_conflicts"):
        warn("Verilen değerler birbiriyle tutarsız; ilk iki değer esas alındı.")

    result_panel("Ohm Kanunu", {
        "Gerilim (V)": format_si(res["v"], "V"),
        "Akım (I)": format_si(res["i"], "A"),
        "Direnç (R)": format_si(res["r"], "Ω"),
        "Güç (P)": format_si(res["p"], "W"),
    })


def _ask():
    console.print("[bold]Ohm Kanunu Sihirbazı[/] — bilmediğin değeri boş bırak (Enter)\n")
    vals = []
    for label in ("Gerilim V", "Akım I", "Direnç R", "Güç P"):
        while True:
            raw = Prompt.ask(f"  {label}", default="", show_default=False).strip()
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
