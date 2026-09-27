"""RC / RL / LC / RLC filtre analizi."""

from __future__ import annotations

import cmath
import math
from typing import Callable, Optional

import typer
from rich.panel import Panel
from rich.table import Table

from elektro.ui import console, eng, fail, result_panel, theory
from elektro.units import format_si

app = typer.Typer(help="RC/RL/LC/RLC filtre analizi ve tasarımı.", no_args_is_help=True)

TWO_PI = 2 * math.pi


def db(x: float) -> float:
    return 20 * math.log10(x) if x > 0 else -math.inf


def response_table(h: Callable[[float], complex], f0: float, title: str,
                   points=(0.1, 0.25, 0.5, 0.8, 1, 1.25, 2, 4, 10)) -> None:
    """Frekans yanıtını (genlik/faz) metin tabanlı grafikle yazdırır."""
    t = Table(title=title, box=None, header_style="bold")
    t.add_column("f", justify="right")
    t.add_column("Kazanç", justify="right")
    t.add_column("Faz", justify="right")
    t.add_column("", no_wrap=True)
    for mult in points:
        f = f0 * mult
        val = h(f)
        g = db(abs(val)) if abs(val) > 1e-6 else -math.inf
        # 0 dB'de 30 karakter, -60 dB'de 0 karakter
        width = max(0, min(30, round((g + 60) / 2))) if g != -math.inf else 0
        style = "bold yellow" if mult == 1 else "green"
        t.add_row(
            format_si(f, "Hz"), f"{g:6.1f} dB" if g != -math.inf else "  -∞ dB",
            f"{math.degrees(cmath.phase(val)):6.1f}°",
            f"[{style}]{'█' * width}[/]",
        )
    console.print(t)


def _solve_first_order(r, x, fc, x_name, x_to_fc, fc_to_x, fc_to_r):
    """R, X (C veya L), fc'den ikisi verilince üçüncüsünü bulur."""
    given = sum(v is not None for v in (r, x, fc))
    if given != 2:
        fail(f"--r, --{x_name} ve --fc'den tam olarak ikisini ver")
    if any(v is not None and v <= 0 for v in (r, x, fc)):
        fail("değerler pozitif olmalı")
    if fc is None:
        fc = x_to_fc(r, x)
    elif x is None:
        x = fc_to_x(r, fc)
    else:
        r = fc_to_r(x, fc)
    return r, x, fc


@app.command()
def rc(
    r: Optional[float] = typer.Option(None, "--r", **eng("Direnç (Ω), örn: 1k")),
    c: Optional[float] = typer.Option(None, "--c", **eng("Kapasitans (F), örn: 100n")),
    fc: Optional[float] = typer.Option(None, "--fc", **eng("Kesim frekansı (Hz), örn: 1k")),
    high: bool = typer.Option(False, "--high", "-H", help="Yüksek geçiren (C seri, R toprağa)"),
):
    """RC filtre (varsayılan alçak geçiren). R, C, fc'den ikisini ver.

    fc = 1 / (2πRC)    τ = RC

    Örnekler:
      elektro filter rc --r 1k --c 100n
      elektro filter rc --fc 1k --c 10n          (R'yi bulur)
      elektro filter rc --r 10k --fc 50 --high   (C'yi bulur)
    """
    r, c, fc = _solve_first_order(
        r, c, fc, "c",
        x_to_fc=lambda r, c: 1 / (TWO_PI * r * c),
        fc_to_x=lambda r, fc: 1 / (TWO_PI * r * fc),
        fc_to_r=lambda c, fc: 1 / (TWO_PI * c * fc),
    )
    kind = "Yüksek Geçiren" if high else "Alçak Geçiren"
    result_panel(f"RC {kind} Filtre", {
        "Kesim frekansı (fc)": format_si(fc, "Hz"),
        "Açısal frekans (ωc)": format_si(TWO_PI * fc, "rad/s"),
        "Zaman sabiti (τ)": format_si(r * c, "s"),
        "Direnç (R)": format_si(r, "Ω"),
        "Kapasitans (C)": format_si(c, "F"),
    })
    if high:
        h = lambda f: 1j * f / fc / (1 + 1j * f / fc)
    else:
        h = lambda f: 1 / (1 + 1j * f / fc)
    console.print()
    response_table(h, fc, "Frekans yanıtı")
    theory("fc'de kazanç -3 dB, faz " + ("+45°" if high else "-45°") + "; eğim 20 dB/dekad.",
           "τ süresinde kondansatör son değerinin %63'üne ulaşır, ~5τ'da tamamen dolar.")


@app.command()
def rl(
    r: Optional[float] = typer.Option(None, "--r", **eng("Direnç (Ω)")),
    l: Optional[float] = typer.Option(None, "--l", **eng("Endüktans (H), örn: 10m")),
    fc: Optional[float] = typer.Option(None, "--fc", **eng("Kesim frekansı (Hz)")),
    low: bool = typer.Option(False, "--low", "-L", help="Alçak geçiren (L seri, R toprağa)"),
):
    """RL filtre (varsayılan yüksek geçiren). R, L, fc'den ikisini ver.

    fc = R / (2πL)    τ = L / R

    Örnekler:
      elektro filter rl --r 1k --l 10m
      elektro filter rl --r 100 --fc 10k --low
    """
    r, l, fc = _solve_first_order(
        r, l, fc, "l",
        x_to_fc=lambda r, l: r / (TWO_PI * l),
        fc_to_x=lambda r, fc: r / (TWO_PI * fc),
        fc_to_r=lambda l, fc: TWO_PI * fc * l,
    )
    kind = "Alçak Geçiren" if low else "Yüksek Geçiren"
    result_panel(f"RL {kind} Filtre", {
        "Kesim frekansı (fc)": format_si(fc, "Hz"),
        "Zaman sabiti (τ)": format_si(l / r, "s"),
        "Direnç (R)": format_si(r, "Ω"),
        "Endüktans (L)": format_si(l, "H"),
    })
    if low:
        h = lambda f: 1 / (1 + 1j * f / fc)
    else:
        h = lambda f: 1j * f / fc / (1 + 1j * f / fc)
    console.print()
    response_table(h, fc, "Frekans yanıtı")


@app.command()
def lc(
    l: Optional[float] = typer.Option(None, "--l", **eng("Endüktans (H)")),
    c: Optional[float] = typer.Option(None, "--c", **eng("Kapasitans (F)")),
    f: Optional[float] = typer.Option(None, "--f", **eng("Rezonans frekansı (Hz)")),
):
    """LC rezonans. L, C, f'den ikisini ver.

    f₀ = 1 / (2π√(LC))    Z₀ = √(L/C)

    Örnekler:
      elektro filter lc --l 10u --c 100n
      elektro filter lc --f 433.92M --c 10p     (L'yi bulur)
    """
    if sum(v is not None for v in (l, c, f)) != 2:
        fail("--l, --c ve --f'den tam olarak ikisini ver")
    if any(v is not None and v <= 0 for v in (l, c, f)):
        fail("değerler pozitif olmalı")
    if f is None:
        f = 1 / (TWO_PI * math.sqrt(l * c))
    elif l is None:
        l = 1 / ((TWO_PI * f) ** 2 * c)
    else:
        c = 1 / ((TWO_PI * f) ** 2 * l)
    x = TWO_PI * f * l
    result_panel("LC Rezonans", {
        "Rezonans frekansı (f₀)": format_si(f, "Hz"),
        "Reaktans (XL = XC)": format_si(x, "Ω"),
        "Karakteristik empedans": format_si(math.sqrt(l / c), "Ω"),
        "Endüktans (L)": format_si(l, "H"),
        "Kapasitans (C)": format_si(c, "F"),
    })
    theory("Seri LC rezonansta empedans minimum, paralel LC (tank) rezonansta maksimumdur.")


@app.command()
def rlc(
    r: float = typer.Option(..., "--r", **eng("Direnç (Ω)")),
    l: float = typer.Option(..., "--l", **eng("Endüktans (H)")),
    c: float = typer.Option(..., "--c", **eng("Kapasitans (F)")),
):
    """Seri RLC bant geçiren filtre (çıkış R üzerinden).

    f₀ = 1 / (2π√(LC))   BW = R / (2πL)   Q = f₀ / BW

    Örnek:
      elektro filter rlc --r 10 --l 1m --c 100n
    """
    f0 = 1 / (TWO_PI * math.sqrt(l * c))
    bw = r / (TWO_PI * l)
    q = f0 / bw
    # -3 dB noktaları (asimetrik, kesin formül)
    half = bw / 2
    f_lo = -half + math.sqrt(half ** 2 + f0 ** 2)
    f_hi = half + math.sqrt(half ** 2 + f0 ** 2)
    result_panel("Seri RLC Bant Geçiren", {
        "Merkez frekans (f₀)": format_si(f0, "Hz"),
        "Bant genişliği (BW)": format_si(bw, "Hz"),
        "Kalite faktörü (Q)": f"{q:.3g}",
        "Alt kesim": format_si(f_lo, "Hz"),
        "Üst kesim": format_si(f_hi, "Hz"),
    })
    h = lambda f: r / (r + 1j * TWO_PI * f * l + 1 / (1j * TWO_PI * f * c))
    console.print()
    response_table(h, f0, "Frekans yanıtı")
    theory("Yüksek Q → dar bant, yüksek seçicilik. Düşük Q → geniş bant.")


@app.command()
def notch(
    r: float = typer.Option(..., "--r", **eng("Yük direnci (Ω)")),
    l: float = typer.Option(..., "--l", **eng("Endüktans (H)")),
    c: float = typer.Option(..., "--c", **eng("Kapasitans (F)")),
):
    """Bant durduran (notch): sinyal yolunda paralel LC tankı, çıkış R üzerinden.

    f₀ = 1 / (2π√(LC))   Q = R / (2πf₀L)

    Örnek (50 Hz şebeke gürültüsü):
      elektro filter notch --r 1k --l 1.013 --c 10u
    """
    f0 = 1 / (TWO_PI * math.sqrt(l * c))
    q = r / (TWO_PI * f0 * l)
    result_panel("Bant Durduran (Notch)", {
        "Söndürme frekansı (f₀)": format_si(f0, "Hz"),
        "Kalite faktörü (Q)": f"{q:.3g}",
        "Bant genişliği": format_si(f0 / q, "Hz"),
    })

    def h(f):
        w = TWO_PI * f
        denom = 1 - w * w * l * c
        if denom == 0:
            return 0j
        z_tank = 1j * w * l / denom
        return r / (r + z_tank)

    console.print()
    response_table(h, f0, "Frekans yanıtı", points=(0.25, 0.5, 0.8, 0.9, 0.95, 1, 1.05, 1.1, 1.25, 2, 4))
    theory("İdeal elemanlarla f₀'da zayıflama sonsuzdur; gerçekte bobin direnci sınırlar.")


@app.command(name="theory")
def theory_cmd():
    """Filtre türleri ve formüllerin özeti."""
    console.print(Panel(
        "[bold]Alçak geçiren[/]  RC: R seri, C toprağa   ·  RL: L seri, R toprağa\n"
        "[bold]Yüksek geçiren[/] RC: C seri, R toprağa   ·  RL: R seri, L toprağa\n"
        "[bold]Bant geçiren[/]   Seri RLC, çıkış R üzerinden (rezonansta Z minimum)\n"
        "[bold]Bant durduran[/]  Paralel LC tankı sinyal yolunda (rezonansta Z maksimum)\n\n"
        "fc(RC) = 1/(2πRC)     fc(RL) = R/(2πL)\n"
        "f₀(LC) = 1/(2π√(LC))  Q = f₀/BW\n"
        "1. derece filtre: fc'de -3 dB, 20 dB/dekad eğim",
        title="[bold]Filtre Teorisi[/]", border_style="bright_blue", expand=False,
    ))
