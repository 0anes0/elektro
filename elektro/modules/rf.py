"""RF hesapları: FSPL, link bütçesi, dalga boyu, birim dönüşümleri."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

import typer
from rich.table import Table

from elektro.i18n import pct, t
from elektro.ui import emit, fail, result_panel, theory
from elektro.modules.wiring import parse_length
from elektro.units import format_si, parse_value

app = typer.Typer(help=t("rf.help"), no_args_is_help=True)

C0 = 299_792_458.0


def parse_freq(text: str) -> float:
    """Frekans → Hz. Yalın sayı MHz kabul edilir: '868' = 868 MHz, '2.4G' = 2.4 GHz."""
    try:
        return float(text) * 1e6
    except ValueError:
        return parse_value(text)


def parse_distance(text: str) -> float:
    """Mesafe → metre. Yalın sayı km kabul edilir: '5' = 5 km, '500m' = 500 m."""
    s = text.strip().lower().replace(",", ".")
    try:
        if s.endswith("km"):
            return float(s[:-2]) * 1e3
        if s.endswith("m"):
            return float(s[:-1])
        return float(s) * 1e3
    except ValueError:
        raise ValueError(t("rf.bad_distance", text=text))


def format_distance(m: float) -> str:
    return f"{m / 1e3:.4g} km" if m >= 1e3 else format_si(m, "m")


def fspl_db(freq_hz: float, dist_m: float) -> float:
    return 20 * math.log10(dist_m) + 20 * math.log10(freq_hz) + 20 * math.log10(4 * math.pi / C0)


def max_distance(freq_hz: float, loss_db: float) -> float:
    return 10 ** ((loss_db - 20 * math.log10(freq_hz) - 20 * math.log10(4 * math.pi / C0)) / 20)


def _freq_opt():
    return typer.Option(..., "--freq", "-f", parser=parse_freq, metavar=t("rf.metavar.freq"),
                        help=t("rf.opt.freq"))


def _dist_opt():
    return typer.Option(..., "--dist", "-d", parser=parse_distance, metavar=t("rf.metavar.dist"),
                        help=t("rf.opt.dist"))


@app.command(help=t("rf.fspl.help"))
def fspl(freq: float = _freq_opt(), dist: float = _dist_opt()):
    if freq <= 0 or dist <= 0:
        fail(t("rf.positive"))
    result_panel(t("rf.fspl.title"), {
        t("rf.freq"): format_si(freq, "Hz"),
        t("rf.dist"): format_distance(dist),
        t("rf.wavelength"): format_si(C0 / freq, "m"),
        "FSPL": f"{fspl_db(freq, dist):.2f} dB",
    }, data={"freq_hz": freq, "dist_m": dist, "wavelength_m": C0 / freq, "fspl_db": fspl_db(freq, dist)})
    theory(t("rf.fspl.note"))


@app.command(help=t("rf.link.help"))
def link(
    freq: float = _freq_opt(),
    dist: float = _dist_opt(),
    tx: float = typer.Option(14, "--tx", help=t("rf.link.opt.tx")),
    gtx: float = typer.Option(2.15, "--gtx", help=t("rf.link.opt.gtx")),
    grx: float = typer.Option(2.15, "--grx", help=t("rf.link.opt.grx")),
    sens: float = typer.Option(-120, "--sens", "-s", help=t("rf.link.opt.sens")),
    loss: float = typer.Option(0, "--loss", help=t("rf.link.opt.loss")),
):
    if freq <= 0 or dist <= 0:
        fail(t("rf.positive"))
    path = fspl_db(freq, dist)
    eirp = tx + gtx
    prx = eirp + grx - path - loss
    margin = prx - sens
    budget = tx + gtx + grx - loss - sens
    if margin >= 10:
        color, verdict = "green", t("rf.link.solid")
    elif margin >= 0:
        color, verdict = "yellow", t("rf.link.marginal")
    else:
        color, verdict = "red", t("rf.link.no_link")
    result_panel(t("rf.link.title"), {
        "EIRP": f"{eirp:.1f} dBm ({format_si(10 ** (eirp / 10) / 1000, 'W')})",
        "FSPL": f"{path:.1f} dB",
        t("rf.link.prx"): f"{prx:.1f} dBm",
        t("rf.link.sens"): f"{sens:.1f} dBm",
        t("rf.link.margin"): f"[{color}]{margin:.1f} dB ({verdict})[/]",
        t("rf.link.range0"): format_distance(max_distance(freq, budget)),
        t("rf.link.range10"): format_distance(max_distance(freq, budget - 10)),
    }, data={"freq_hz": freq, "dist_m": dist, "eirp_dbm": eirp, "fspl_db": path, "prx_dbm": prx,
             "sensitivity_dbm": sens, "margin_db": margin,
             "max_range_m": max_distance(freq, budget), "max_range_10db_m": max_distance(freq, budget - 10)})
    theory(t("rf.link.note1"), t("rf.link.note2"))


@app.command(help=t("rf.wave.help"))
def wave(
    freq: float = typer.Option(..., "--freq", "-f", parser=parse_freq, metavar=t("rf.metavar.freq"),
                               help=t("rf.opt.freq")),
    vf: float = typer.Option(1.0, "--vf", help=t("rf.wave.opt.vf")),
):
    if freq <= 0 or not 0 < vf <= 1:
        fail(t("rf.wave.bad"))
    lam = C0 / freq * vf
    result_panel(t("rf.wave.title"), {
        t("rf.freq"): format_si(freq, "Hz"),
        "λ": format_si(lam, "m"),
        t("rf.wave.dipole"): format_si(lam / 2, "m"),
        t("rf.wave.monopole"): format_si(lam / 4, "m"),
        "5λ/8": format_si(lam * 5 / 8, "m"),
    }, data={"freq_hz": freq, "velocity_factor": vf, "wavelength_m": lam, "half_wave_m": lam / 2,
             "quarter_wave_m": lam / 4, "five_eighths_m": lam * 5 / 8})


# --- Dönüşümler ------------------------------------------------------------------

POWER_TO_DBM = {
    "dbm": lambda x: x,
    "dbw": lambda x: x + 30,
    "w": lambda x: 10 * math.log10(x * 1e3),
    "mw": lambda x: 10 * math.log10(x),
    "uw": lambda x: 10 * math.log10(x * 1e-3),
}
DBM_TO_POWER = {
    "dbm": lambda d: d,
    "dbw": lambda d: d - 30,
    "w": lambda d: 10 ** (d / 10) / 1e3,
    "mw": lambda d: 10 ** (d / 10),
    "uw": lambda d: 10 ** (d / 10) * 1e3,
}


def gamma_from(unit: str, x: float) -> float:
    if unit == "vswr":
        if x < 1:
            raise ValueError(t("rf.conv.vswr"))
        return (x - 1) / (x + 1)
    if unit == "rl":
        if x < 0:
            raise ValueError(t("rf.conv.rl"))
        return 10 ** (-x / 20)
    if not 0 <= x <= 1:
        raise ValueError(t("rf.conv.gamma"))
    return x


_ALIASES = {"watt": "w", "mwatt": "mw", "µw": "uw", "s11": "rl", "g": "gamma", "Γ": "gamma"}
POWER_UNITS = set(POWER_TO_DBM)
MATCH_UNITS = {"vswr", "rl", "gamma"}


def convert_units(value: float, src: str, dst: Optional[str]):
    src = _ALIASES.get(src.lower(), src.lower())
    dst = _ALIASES.get(dst.lower(), dst.lower()) if dst else None
    if src in POWER_UNITS:
        if src not in ("dbm", "dbw") and value <= 0:
            raise ValueError(t("rf.conv.power_pos"))
        if dst and dst not in POWER_UNITS:
            raise ValueError(t("rf.conv.no_path", src=src, dst=dst))
        dbm = POWER_TO_DBM[src](value)
        targets = [dst] if dst else ["dbm", "dbw", "w", "mw"]
        return {k: DBM_TO_POWER[k](dbm) for k in targets}
    if src in MATCH_UNITS:
        if dst and dst not in MATCH_UNITS:
            raise ValueError(t("rf.conv.no_path", src=src, dst=dst))
        g = gamma_from(src, value)
        vals = {
            "gamma": g,
            "vswr": math.inf if g >= 1 else (1 + g) / (1 - g),
            "rl": math.inf if g == 0 else -20 * math.log10(g),
            "mismatch": math.inf if g >= 1 else -10 * math.log10(1 - g * g),
            "reflected": g * g * 100,
        }
        return {dst: vals[dst]} if dst else vals
    raise ValueError(t("rf.conv.unknown", unit=src))


def _label(key: str) -> tuple:
    return {
        "dbm": ("dBm", None), "dbw": ("dBW", None), "w": ("W", "W"), "mw": ("mW", None),
        "uw": ("µW", None), "gamma": ("|Γ|", None), "vswr": ("VSWR", None),
        "rl": (t("rf.conv.l.rl"), "dB"), "mismatch": (t("rf.conv.l.mismatch"), "dB"),
        "reflected": (t("rf.conv.l.reflected"), "%"),
    }[key]


@app.command(help=t("rf.conv.help"))
def convert(
    value: float = typer.Argument(..., help=t("rf.conv.arg.value")),
    src: str = typer.Argument(..., help=t("rf.conv.arg.src")),
    dst: Optional[str] = typer.Argument(None, help=t("rf.conv.arg.dst")),
):
    try:
        res = convert_units(value, src, dst)
    except ValueError as e:
        fail(str(e))
    tbl = Table(show_header=False, box=None)
    tbl.add_column(style="cyan", justify="right")
    tbl.add_column(style="bold green")
    for key, v in res.items():
        label, unit = _label(key)
        if unit == "W":
            text = format_si(v, "W")
        elif math.isinf(v):
            text = "∞"
        elif unit == "%":
            text = pct(f"{v:.3g}")
        else:
            text = f"{v:.4g}" + (f" {unit}" if unit else "")
        tbl.add_row(label, text)
    emit(tbl, res)


# --- Mikroşerit hat ------------------------------------------------------------------

def microstrip_z0(w_h: float, er: float) -> tuple:
    """Hammerstad: W/h oranından (Z0, εeff)."""
    if w_h <= 1:
        eeff = (er + 1) / 2 + (er - 1) / 2 * ((1 + 12 / w_h) ** -0.5 + 0.04 * (1 - w_h) ** 2)
        z0 = 60 / math.sqrt(eeff) * math.log(8 / w_h + w_h / 4)
    else:
        eeff = (er + 1) / 2 + (er - 1) / 2 * (1 + 12 / w_h) ** -0.5
        z0 = 120 * math.pi / (math.sqrt(eeff) * (w_h + 1.393 + 0.667 * math.log(w_h + 1.444)))
    return z0, eeff


def microstrip_width(z0: float, er: float) -> float:
    """Hedef Z0 için W/h (analiz formülünün sayısal tersi)."""
    lo, hi = 1e-3, 100.0
    if not microstrip_z0(hi, er)[0] < z0 < microstrip_z0(lo, er)[0]:
        raise ValueError(t("ms.range"))
    for _ in range(100):
        mid = math.sqrt(lo * hi)
        if microstrip_z0(mid, er)[0] > z0:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


@app.command(help=t("ms.help"))
def microstrip(
    z0: Optional[float] = typer.Option(None, "--z0", help=t("ms.opt.z0")),
    width: Optional[float] = typer.Option(None, "--width", "-w", help=t("ms.opt.width")),
    h: float = typer.Option(1.6, "--h", help=t("ms.opt.h")),
    er: float = typer.Option(4.4, "--er", help=t("ms.opt.er")),
    freq: Optional[float] = typer.Option(None, "--freq", "-f", parser=parse_freq,
                                         metavar=t("rf.metavar.freq"), help=t("rf.opt.freq")),
):
    if (z0 is None) == (width is None):
        fail(t("ms.need"))
    if h <= 0 or er < 1:
        fail(t("common.positive_all"))
    try:
        w_h = microstrip_width(z0, er) if z0 is not None else width / h
    except ValueError as e:
        fail(str(e))
    z, eeff = microstrip_z0(w_h, er)
    rows = {
        "Z0": f"{z:.2f} Ω",
        t("ms.width"): f"{w_h * h:.3f} mm ({w_h * h / 0.0254:.1f} mil)",
        "W/h": f"{w_h:.3f}",
        "εeff": f"{eeff:.3f}",
    }
    data = {"z0_ohm": z, "width_mm": w_h * h, "w_h": w_h, "eeff": eeff, "h_mm": h, "er": er}
    if freq is not None:
        lam = C0 / freq / math.sqrt(eeff)
        rows[t("ms.lambda")] = format_si(lam, "m")
        rows["λ/4"] = format_si(lam / 4, "m")
        data.update(freq_hz=freq, guided_wavelength_m=lam)
    result_panel(t("ms.title"), rows, data=data)
    theory(t("ms.note"))


# --- LoRa ---------------------------------------------------------------------------

LORA_SNR_LIMIT = {7: -7.5, 8: -10.0, 9: -12.5, 10: -15.0, 11: -17.5, 12: -20.0}


def parse_cr(text: str) -> int:
    s = str(text).strip()
    if "/" in s:
        s = s.split("/")[1]
        value = int(s) - 4
    else:
        value = int(s)
        if value >= 5:
            value -= 4
    if not 1 <= value <= 4:
        raise ValueError(t("lora.bad_cr"))
    return value


def lora_airtime(sf: int, bw: float, cr: int, payload: int, preamble: int = 8,
                 explicit_header: bool = True, crc: bool = True, ldro: Optional[bool] = None) -> dict:
    """Semtech AN1200.13 formülü. cr: 1..4 (4/5..4/8)."""
    t_sym = 2 ** sf / bw
    if ldro is None:
        ldro = t_sym > 16e-3
    de = 1 if ldro else 0
    ih = 0 if explicit_header else 1
    num = 8 * payload - 4 * sf + 28 + 16 * (1 if crc else 0) - 20 * ih
    n_payload = 8 + max(math.ceil(num / (4 * (sf - 2 * de))) * (cr + 4), 0)
    t_preamble = (preamble + 4.25) * t_sym
    t_payload = n_payload * t_sym
    return {"t_sym": t_sym, "t_preamble": t_preamble, "t_payload": t_payload,
            "airtime": t_preamble + t_payload, "symbols": n_payload, "ldro": ldro,
            "bitrate": sf * bw / 2 ** sf * 4 / (4 + cr)}


@app.command(help=t("lora.help"))
def lora(
    sf: int = typer.Option(9, "--sf", min=7, max=12, help=t("lora.opt.sf")),
    bw: float = typer.Option(125e3, "--bw", parser=parse_value, metavar="Hz", help=t("lora.opt.bw")),
    cr: int = typer.Option(1, "--cr", parser=parse_cr, metavar="4/5..4/8", help=t("lora.opt.cr")),
    payload: int = typer.Option(20, "--payload", "-p", min=0, max=255, help=t("lora.opt.payload")),
    preamble: int = typer.Option(8, "--preamble", min=6, help=t("lora.opt.preamble")),
    no_crc: bool = typer.Option(False, "--no-crc", help=t("lora.opt.no_crc")),
    implicit: bool = typer.Option(False, "--implicit", help=t("lora.opt.implicit")),
    duty: float = typer.Option(1.0, "--duty", help=t("lora.opt.duty")),
    nf: float = typer.Option(6.0, "--nf", help=t("lora.opt.nf")),
):
    r = lora_airtime(sf, bw, cr, payload, preamble, not implicit, not no_crc)
    sens = -174 + 10 * math.log10(bw) + nf + LORA_SNR_LIMIT[sf]
    per_hour = 3600 * duty / 100 / r["airtime"]
    result_panel("LoRa", {
        t("lora.airtime"): format_si(r["airtime"], "s"),
        t("lora.symbol"): format_si(r["t_sym"], "s"),
        t("lora.bitrate"): format_si(r["bitrate"], "bps"),
        t("lora.sensitivity"): f"{sens:.1f} dBm",
        t("lora.per_hour", duty=pct(f"{duty:g}")): f"{per_hour:.0f} ({t('lora.interval')} {format_si(3600 / per_hour, 's')})",
        "LDRO": t("lora.on") if r["ldro"] else t("lora.off"),
    }, data={"sf": sf, "bw_hz": bw, "cr": f"4/{cr + 4}", "payload_bytes": payload,
             "airtime_s": r["airtime"], "symbol_s": r["t_sym"], "bitrate_bps": r["bitrate"],
             "sensitivity_dbm": sens, "max_packets_per_hour": per_hour, "ldro": r["ldro"]})
    theory(t("lora.note"))


# --- Fresnel bölgesi ----------------------------------------------------------------------

EARTH_RADIUS = 6_371_000.0


@app.command(help=t("fresnel.help"))
def fresnel(
    freq: float = _freq_opt(),
    dist: float = _dist_opt(),
    at: Optional[float] = typer.Option(None, "--at", parser=parse_distance, metavar=t("rf.metavar.dist"),
                                       help=t("fresnel.opt.at")),
    k: float = typer.Option(4 / 3, "--k", help=t("fresnel.opt.k")),
):
    if freq <= 0 or dist <= 0:
        fail(t("rf.positive"))
    d1 = dist / 2 if at is None else at
    if not 0 < d1 < dist:
        fail(t("fresnel.bad_at"))
    d2 = dist - d1
    lam = C0 / freq
    r1 = math.sqrt(lam * d1 * d2 / dist)
    bulge = d1 * d2 / (2 * k * EARTH_RADIUS)
    need = 0.6 * r1 + bulge
    result_panel(t("fresnel.title"), {
        t("fresnel.point"): f"{format_distance(d1)} / {format_distance(d2)}",
        t("fresnel.r1"): format_si(r1, "m"),
        t("fresnel.r60"): format_si(0.6 * r1, "m"),
        t("fresnel.bulge"): format_si(bulge, "m"),
        t("fresnel.need"): format_si(need, "m"),
    }, data={"freq_hz": freq, "dist_m": dist, "d1_m": d1, "r1_m": r1, "clearance_60_m": 0.6 * r1,
             "earth_bulge_m": bulge, "required_height_m": need})
    theory(t("fresnel.note"))


# --- Koaksiyel kablo kaybı ------------------------------------------------------------------

@dataclass(frozen=True)
class Coax:
    name: str
    z0: float
    vf: float
    a100: float     # dB/100 m @ 100 MHz (tipik)
    a1000: float    # dB/100 m @ 1 GHz (tipik)

    def attenuation(self, f_mhz: float) -> float:
        """dB/100 m. α = k1·√f + k2·f modeli, iki noktadan uydurulur."""
        # 10·k1 + 100·k2 = a100 ;  31.623·k1 + 1000·k2 = a1000
        k1 = (10 * self.a100 - self.a1000) / (100 - 31.623)
        k2 = (self.a100 - 10 * k1) / 100
        return k1 * math.sqrt(f_mhz) + k2 * f_mhz


_FT = 100 / 30.48   # dB/100ft → dB/100m


def _lmr(name, z0, vf, k1, k2):
    """Times Microwave katsayıları (dB/100ft, f MHz) → dB/100m noktaları."""
    return Coax(name, z0, vf, (k1 * 10 + k2 * 100) * _FT, (k1 * math.sqrt(1000) + k2 * 1000) * _FT)


COAX = {c.name.lower().replace("-", ""): c for c in [
    Coax("RG-58", 50, 0.66, 16.0, 62.0),
    Coax("RG-174", 50, 0.66, 29.0, 100.0),
    Coax("RG-316", 50, 0.69, 26.0, 85.0),
    Coax("RG-213", 50, 0.66, 7.0, 26.0),
    Coax("RG-6", 75, 0.82, 6.6, 21.0),
    _lmr("LMR-195", 50, 0.80, 0.34466, 0.00083),
    _lmr("LMR-240", 50, 0.84, 0.24208, 0.00033),
    _lmr("LMR-400", 50, 0.85, 0.12229, 0.00026),
    _lmr("LMR-600", 50, 0.87, 0.07581, 0.00024),
]}


def find_coax(name: str) -> Coax:
    key = name.lower().replace("-", "").replace("_", "").replace(" ", "")
    if key not in COAX:
        raise ValueError(t("coax.unknown", name=name, options=", ".join(c.name for c in COAX.values())))
    return COAX[key]


@app.command(help=t("coax.help"))
def coax(
    cable: str = typer.Argument(..., help=t("coax.arg")),
    freq: float = _freq_opt(),
    length: float = typer.Option(..., "--length", "-l", parser=parse_length,
                                 metavar=t("coax.metavar.length"), help=t("coax.opt.length")),
):
    try:
        c = find_coax(cable)
    except ValueError as e:
        fail(str(e))
    if freq <= 0 or length <= 0:
        fail(t("common.positive_all"))
    per100 = c.attenuation(freq / 1e6)
    loss = per100 * length / 100
    delivered = 10 ** (-loss / 10)
    lam = C0 / freq * c.vf
    result_panel(c.name, {
        "Z0 / VF": f"{c.z0:g} Ω / {c.vf:g}",
        t("coax.per100"): f"{per100:.2f} dB",
        t("coax.loss"): f"{loss:.2f} dB",
        t("coax.delivered"): pct(f"{delivered * 100:.1f}"),
        t("coax.delay"): format_si(length / (C0 * c.vf), "s"),
        t("coax.electrical"): f"{length / lam:.2f} λ",
    }, data={"cable": c.name, "freq_hz": freq, "length_m": length, "db_per_100m": per100,
             "loss_db": loss, "power_delivered": delivered, "velocity_factor": c.vf,
             "delay_s": length / (C0 * c.vf)})
    theory(t("coax.note"))
