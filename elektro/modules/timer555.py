"""NE555 zamanlayıcı hesapları."""

from __future__ import annotations

import math
from typing import Optional

import typer

from elektro.ui import eng, fail, result_panel, theory
from elektro.units import format_si, nearest_standard

app = typer.Typer(help="NE555 zamanlayıcı: astable ve monostable.", no_args_is_help=True)

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
        raise ValueError("klasik 555 astable'da görev oranı %50'den büyük olmalı "
                         "(daha düşük oran için R2'ye paralel diyot kullanılır)")
    period = 1 / freq
    t_high, t_low = duty * period, (1 - duty) * period
    r2 = t_low / (LN2 * c)
    r1 = t_high / (LN2 * c) - r2
    return r1, r2


@app.command()
def astable(
    r1: Optional[float] = typer.Option(None, "--r1", **eng("R1 (VCC–DIS arası)")),
    r2: Optional[float] = typer.Option(None, "--r2", **eng("R2 (DIS–THR/TRIG arası)")),
    c: float = typer.Option(..., "--c", **eng("Zamanlama kondansatörü")),
    freq: Optional[float] = typer.Option(None, "--freq", "-f", **eng("Hedef frekans (tasarım modu)")),
    duty: float = typer.Option(60, "--duty", "-d", help="Hedef görev oranı % (tasarım modu)"),
):
    """Astable (osilatör) mod.

    f = 1.44 / ((R1 + 2R2)·C)    D = (R1 + R2) / (R1 + 2R2)

    Örnekler:
      elektro 555 astable --r1 1k --r2 10k --c 10u
      elektro 555 astable -f 1k -d 60 --c 10n     (R1, R2'yi bulur)
    """
    if freq is not None:
        try:
            r1, r2 = astable_design(freq, duty / 100, c)
        except ValueError as e:
            fail(str(e))
        r1s, r2s = nearest_standard(r1, "E24"), nearest_standard(r2, "E24")
        real = astable_timing(r1s, r2s, c)
        result_panel("555 Astable Tasarım", {
            "R1 (hesap)": format_si(r1, "Ω"),
            "R2 (hesap)": format_si(r2, "Ω"),
            "R1 / R2 (E24)": f"{format_si(r1s, 'Ω')} / {format_si(r2s, 'Ω')}",
            "Gerçek frekans": format_si(real["freq"], "Hz"),
            "Gerçek görev oranı": f"%{real['duty'] * 100:.1f}",
        })
        if r1 < 1e3 or r2 > 1e6:
            theory("Uyarı: R1 ≥ 1 kΩ ve R2 ≤ 1 MΩ aralığı önerilir; kondansatör değerini değiştir.")
        return

    if r1 is None or r2 is None:
        fail("--r1 ve --r2 ya da --freq verilmeli")
    if min(r1, r2, c) <= 0:
        fail("değerler pozitif olmalı")
    t = astable_timing(r1, r2, c)
    result_panel("555 Astable", {
        "Frekans": format_si(t["freq"], "Hz"),
        "Periyot": format_si(t["period"], "s"),
        "Yüksek süre": format_si(t["t_high"], "s"),
        "Düşük süre": format_si(t["t_low"], "s"),
        "Görev oranı": f"%{t['duty'] * 100:.1f}",
    })


@app.command()
def mono(
    r: Optional[float] = typer.Option(None, "--r", **eng("Zamanlama direnci")),
    c: Optional[float] = typer.Option(None, "--c", **eng("Zamanlama kondansatörü")),
    t: Optional[float] = typer.Option(None, "--t", **eng("Darbe süresi (s)")),
):
    """Monostable (tek darbe) mod. R, C, t'den ikisini ver.

    t = 1.1 · R · C

    Örnekler:
      elektro 555 mono --r 100k --c 10u
      elektro 555 mono --t 5 --c 100u     (R'yi bulur)
    """
    if sum(x is not None for x in (r, c, t)) != 2:
        fail("--r, --c ve --t'den tam olarak ikisini ver")
    if any(x is not None and x <= 0 for x in (r, c, t)):
        fail("değerler pozitif olmalı")
    k = math.log(3)
    if t is None:
        t = k * r * c
    elif r is None:
        r = t / (k * c)
    else:
        c = t / (k * r)
    result_panel("555 Monostable", {
        "Darbe süresi": format_si(t, "s"),
        "R": format_si(r, "Ω") + f"  (E24: {format_si(nearest_standard(r, 'E24'), 'Ω')})",
        "C": format_si(c, "F"),
    })
