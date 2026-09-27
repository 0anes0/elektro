"""İletkenler: kablo (AWG/mm²) ve PCB yol genişliği (IPC-2221)."""

from __future__ import annotations

import math
from typing import Optional

import typer

from elektro.i18n import t
from elektro.ui import cli_parser, eng, fail, result_panel, theory, warn
from elektro.units import format_si

RHO_CU = 1.724e-8      # Ω·m, 20 °C
ALPHA_CU = 0.00393     # 1/°C
MIL = 25.4e-6          # m
OZ_THICKNESS = 34.8e-6  # 1 oz/ft² bakır kalınlığı (m)


def awg_diameter(awg: float) -> float:
    """AWG → çap (m). 0000 için -3 kullanılır."""
    return 0.127e-3 * 92 ** ((36 - awg) / 39)


def area_to_awg(area_m2: float) -> float:
    d = math.sqrt(4 * area_m2 / math.pi)
    return 36 - 39 * math.log(d / 0.127e-3, 92)


def copper_resistance(area_m2: float, length_m: float, temp_c: float = 20) -> float:
    return RHO_CU * (1 + ALPHA_CU * (temp_c - 20)) * length_m / area_m2


def parse_length(text: str) -> float:
    """Uzunluk → metre. Yalın sayı metre: '3', '50cm', '12mm', '10ft', '6in'."""
    s = text.strip().lower().replace(",", ".")
    for suffix, mult in (("km", 1e3), ("cm", 1e-2), ("mm", 1e-3), ("ft", 0.3048), ("in", 0.0254), ("m", 1.0)):
        if s.endswith(suffix):
            s, factor = s[: -len(suffix)], mult
            break
    else:
        factor = 1.0
    try:
        return float(s) * factor
    except ValueError:
        raise ValueError(t("wire.bad_length", text=text))


def _length_opt(help_key: str):
    return typer.Option(None, "--length", "-l", parser=cli_parser(parse_length), metavar=t("wire.metavar.length"),
                        help=t(help_key))


def wire(
    awg: Optional[float] = typer.Option(None, "--awg", help=t("wire.opt.awg")),
    mm2: Optional[float] = typer.Option(None, "--mm2", help=t("wire.opt.mm2")),
    length: Optional[float] = _length_opt("wire.opt.length"),
    current: Optional[float] = typer.Option(None, "--current", "-i", **eng(t("wire.opt.current"))),
    round_trip: bool = typer.Option(False, "--round-trip", "-2", help=t("wire.opt.round_trip")),
    temp: float = typer.Option(20, "--temp", help=t("wire.opt.temp")),
):
    if (awg is None) == (mm2 is None):
        fail(t("wire.need"))
    if awg is not None:
        d = awg_diameter(awg)
        area = math.pi * d * d / 4
    else:
        if mm2 <= 0:
            fail(t("common.positive"))
        area = mm2 * 1e-6
        d = math.sqrt(4 * area / math.pi)
        awg = area_to_awg(area)

    r_per_m = copper_resistance(area, 1, temp)
    rows = {
        "AWG": f"{awg:.1f}" if awg != int(awg) else str(int(awg)),
        t("wire.diameter"): f"{d * 1e3:.3f} mm",
        t("wire.area"): f"{area * 1e6:.4g} mm²",
        t("wire.r_per_m"): format_si(r_per_m, "Ω/m"),
    }
    data = {"awg": awg, "diameter_mm": d * 1e3, "area_mm2": area * 1e6, "ohm_per_m": r_per_m}
    if length is not None:
        total_len = length * (2 if round_trip else 1)
        r = r_per_m * total_len
        rows[t("wire.resistance")] = format_si(r, "Ω")
        data.update(length_m=total_len, resistance_ohm=r)
        if current is not None:
            rows[t("wire.drop")] = format_si(current * r, "V")
            rows[t("wire.loss")] = format_si(current ** 2 * r, "W")
            data.update(voltage_drop_v=current * r, power_loss_w=current ** 2 * r)
    if current is not None:
        density = current / (area * 1e6)
        rows[t("wire.density")] = f"{density:.2f} A/mm²"
        data["current_density_a_mm2"] = density
        if density > 6:
            warn(t("wire.hot"))
    result_panel(t("wire.title"), rows, data=data)
    theory(t("wire.note"))


# --- PCB yolu ---------------------------------------------------------------------------

def ipc2221_area_mil2(current: float, rise: float, internal: bool) -> float:
    k = 0.024 if internal else 0.048
    return (current / (k * rise ** 0.44)) ** (1 / 0.725)


def ipc2221_current(area_mil2: float, rise: float, internal: bool) -> float:
    k = 0.024 if internal else 0.048
    return k * rise ** 0.44 * area_mil2 ** 0.725


def trace(
    current: Optional[float] = typer.Option(None, "--current", "-i", **eng(t("trace.opt.current"))),
    width: Optional[float] = typer.Option(None, "--width", "-w", help=t("trace.opt.width")),
    rise: float = typer.Option(10, "--rise", help=t("trace.opt.rise")),
    oz: float = typer.Option(1, "--oz", help=t("trace.opt.oz")),
    internal: bool = typer.Option(False, "--internal", help=t("trace.opt.internal")),
    length: Optional[float] = _length_opt("trace.opt.length"),
):
    if (current is None) == (width is None):
        fail(t("trace.need"))
    if rise <= 0 or oz <= 0:
        fail(t("common.positive_all"))
    thickness = oz * OZ_THICKNESS
    thickness_mil = thickness / MIL
    if current is not None:
        area_mil2 = ipc2221_area_mil2(current, rise, internal)
        width_m = area_mil2 / thickness_mil * MIL
    else:
        width_m = width * 1e-3
        area_mil2 = (width_m / MIL) * thickness_mil
        current = ipc2221_current(area_mil2, rise, internal)
    area_m2 = width_m * thickness
    rows = {
        t("trace.width"): f"{width_m * 1e3:.3f} mm ({width_m / MIL:.1f} mil)",
        t("trace.current"): format_si(current, "A"),
        t("trace.thickness"): f"{oz:g} oz ({thickness * 1e6:.1f} µm)",
        t("trace.layer"): t("trace.internal" if internal else "trace.external"),
        t("trace.rise"): f"{rise:g} °C",
    }
    data = {"width_mm": width_m * 1e3, "width_mil": width_m / MIL, "current_a": current,
            "copper_oz": oz, "rise_c": rise, "internal": internal}
    if length is not None:
        r = copper_resistance(area_m2, length, 20 + rise)
        rows[t("wire.resistance")] = format_si(r, "Ω")
        rows[t("wire.drop")] = format_si(current * r, "V")
        rows[t("wire.loss")] = format_si(current ** 2 * r, "W")
        data.update(length_m=length, resistance_ohm=r, voltage_drop_v=current * r,
                    power_loss_w=current ** 2 * r)
    result_panel(t("trace.title"), rows, data=data)
    theory(t("trace.note"))
