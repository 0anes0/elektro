"""Gömülü sistem hesapları: UART, PWM/timer, ADC, I²C pull-up, CRC."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import List, Optional

import typer
from rich.table import Table

from elektro.i18n import pct, t
from elektro.ui import cli_parser, emit, eng, fail, result_panel, theory, warn
from elektro.units import format_si, parse_value, series_values

MCUS = ("avr", "stm32", "generic")


def _mcu_opt():
    return typer.Option("avr", "--mcu", "-m", help=t("mcu.opt.mcu"))


def _check_mcu(mcu: str) -> str:
    mcu = mcu.lower()
    if mcu not in MCUS:
        fail(t("mcu.unknown", mcu=mcu, options=", ".join(MCUS)))
    return mcu


# --- UART -------------------------------------------------------------------------------

COMMON_BAUDS = [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600, 1000000]


def uart_settings(clock: float, baud: float, mcu: str, oversample: int = 16) -> List[dict]:
    """Olası bölücü ayarları: [{mode, divider, actual, error}]."""
    out = []
    if mcu == "avr":
        for mode, div in (("U2X=0", 16), ("U2X=1", 8)):
            ubrr = round(clock / (div * baud)) - 1
            if 0 <= ubrr <= 4095:
                actual = clock / (div * (ubrr + 1))
                out.append({"mode": mode, "register": "UBRR", "value": ubrr, "actual": actual,
                            "error": (actual - baud) / baud})
    elif mcu == "stm32":
        # OVER8=0: BRR = fck/baud.  OVER8=1: USARTDIV = 2·fck/baud, BRR[3] = 0, BRR[2:0] = DIV[3:0] >> 1
        brr = round(clock / baud)
        if brr >= 16:
            actual = clock / brr
            out.append({"mode": "OVER8=0", "register": "BRR", "value": f"0x{brr:X}", "actual": actual,
                        "error": (actual - baud) / baud})
        div8 = round(2 * clock / baud)
        if div8 >= 16:
            actual = 2 * clock / div8
            brr8 = (div8 & 0xFFF0) | ((div8 & 0xF) >> 1)
            out.append({"mode": "OVER8=1", "register": "BRR", "value": f"0x{brr8:X}", "actual": actual,
                        "error": (actual - baud) / baud})
    else:
        div = round(clock / (oversample * baud))
        if div >= 1:
            actual = clock / (oversample * div)
            out.append({"mode": f"÷{oversample}", "register": "DIV", "value": div, "actual": actual,
                        "error": (actual - baud) / baud})
    return out


def uart(
    clock: float = typer.Option(..., "--clock", "-c", **eng(t("mcu.opt.clock"))),
    baud: Optional[float] = typer.Option(None, "--baud", "-b", **eng(t("uart.opt.baud"))),
    mcu: str = _mcu_opt(),
    oversample: int = typer.Option(16, "--oversample", help=t("uart.opt.oversample")),
):
    mcu = _check_mcu(mcu)
    if clock <= 0:
        fail(t("common.positive"))
    bauds = [baud] if baud else COMMON_BAUDS
    tbl = Table(title=f"UART — {mcu.upper()} @ {format_si(clock, 'Hz')}")
    for key in ("uart.col.baud", "uart.col.mode", "uart.col.register", "uart.col.actual", "uart.col.error"):
        tbl.add_column(t(key), justify="right")
    records = []
    for b in bauds:
        settings = uart_settings(clock, b, mcu, oversample)
        if not settings:
            tbl.add_row(f"{b:g}", "-", "-", "-", f"[red]{t('uart.impossible')}[/]")
            continue
        for s in settings:
            err = s["error"] * 100
            color = "green" if abs(err) <= 1 else "yellow" if abs(err) <= 2 else "red"
            tbl.add_row(f"{b:g}", s["mode"], f"{s['register']}={s['value']}", f"{s['actual']:.0f}",
                        f"[{color}]{pct(f'{err:+.2f}')}[/]")
            records.append({"baud": b, **s})
    emit(tbl, records)
    theory(t("uart.note"))


# --- PWM / timer ---------------------------------------------------------------------------

AVR_PRESCALERS = (1, 8, 64, 256, 1024)


def pwm_settings(clock: float, freq: float, mcu: str, bits: int) -> Optional[dict]:
    top_max = 2 ** bits - 1
    if mcu == "avr":
        for n in AVR_PRESCALERS:
            top = round(clock / (n * freq)) - 1
            if 1 <= top <= top_max:
                return {"prescaler": n, "register": "TOP (ICR1/OCR1A)", "top": top,
                        "actual": clock / (n * (top + 1))}
        return None
    # STM32 / genel: PSC 0..65535, ARR 0..top_max
    psc = max(0, math.ceil(clock / (freq * (top_max + 1))) - 1)
    if psc > 65535:
        return None
    arr = round(clock / ((psc + 1) * freq)) - 1
    if arr < 1:
        return None
    return {"prescaler": psc + 1, "psc_register": psc, "register": "ARR", "top": arr,
            "actual": clock / ((psc + 1) * (arr + 1))}


def pwm(
    clock: float = typer.Option(..., "--clock", "-c", **eng(t("mcu.opt.clock"))),
    freq: float = typer.Option(..., "--freq", "-f", **eng(t("pwm.opt.freq"))),
    mcu: str = _mcu_opt(),
    bits: int = typer.Option(16, "--bits", help=t("pwm.opt.bits")),
    duty: Optional[float] = typer.Option(None, "--duty", "-d", help=t("pwm.opt.duty")),
):
    mcu = _check_mcu(mcu)
    if clock <= 0 or freq <= 0 or bits not in (8, 10, 16, 32):
        fail(t("pwm.bad"))
    s = pwm_settings(clock, freq, mcu, bits)
    if s is None:
        fail(t("pwm.impossible"))
    resolution = math.log2(s["top"] + 1)
    rows = {
        t("pwm.prescaler"): f"{s['prescaler']}" + (f"  (PSC={s['psc_register']})" if "psc_register" in s else ""),
        s["register"]: str(s["top"]),
        t("pwm.actual"): format_si(s["actual"], "Hz"),
        t("pwm.error"): pct(f"{(s['actual'] - freq) / freq * 100:+.3f}"),
        t("pwm.resolution"): f"{resolution:.1f} bit ({s['top'] + 1} {t('pwm.steps')})",
    }
    data = {"mcu": mcu, **s, "error": (s["actual"] - freq) / freq, "resolution_bits": resolution}
    if duty is not None:
        compare = round((s["top"] + 1) * duty / 100)
        rows[t("pwm.compare", duty=pct(f"{duty:g}"))] = str(compare)
        data["compare"] = compare
    result_panel(f"PWM — {mcu.upper()}", rows, data=data)
    if resolution < 8:
        warn(t("pwm.low_res"))


# --- ADC -------------------------------------------------------------------------------------

def adc(
    bits: int = typer.Option(..., "--bits", "-b", min=1, max=32, help=t("adc.opt.bits")),
    vref: float = typer.Option(..., "--vref", **eng(t("adc.opt.vref"))),
    code: Optional[int] = typer.Option(None, "--code", help=t("adc.opt.code")),
    volt: Optional[float] = typer.Option(None, "--volt", **eng(t("adc.opt.volt"))),
):
    if vref <= 0:
        fail(t("common.positive"))
    steps = 2 ** bits
    lsb = vref / steps
    rows = {
        "LSB": format_si(lsb, "V"),
        t("adc.steps"): f"{steps} (0 … {steps - 1})",
        t("adc.snr"): f"{6.02 * bits + 1.76:.1f} dB",
    }
    data = {"bits": bits, "vref_v": vref, "lsb_v": lsb, "steps": steps, "ideal_snr_db": 6.02 * bits + 1.76}
    if code is not None:
        if not 0 <= code < steps:
            fail(t("adc.code_range", max=steps - 1))
        rows[t("adc.voltage_of", code=code)] = format_si(code * lsb, "V")
        data["voltage_v"] = code * lsb
    if volt is not None:
        c = min(steps - 1, max(0, math.floor(volt / lsb)))
        rows[t("adc.code_of", volt=format_si(volt, "V"))] = f"{c} (0x{c:X})"
        data["code"] = c
        if not 0 <= volt <= vref:
            warn(t("adc.clipped"))
    result_panel(f"ADC {bits} bit", rows, data=data)
    theory(t("adc.note"))


# --- I²C pull-up -------------------------------------------------------------------------------

I2C_MODES = {100e3: (1000e-9, 3e-3), 400e3: (300e-9, 3e-3), 1e6: (120e-9, 20e-3)}


def i2c_pullup_range(vdd: float, cb: float, speed: float) -> tuple:
    rise, iol = I2C_MODES[speed]
    r_min = (vdd - 0.4) / iol
    r_max = rise / (0.8473 * cb)
    return r_min, r_max


def _i2c_speed(text: str) -> float:
    v = parse_value(text)
    if v not in I2C_MODES:
        raise ValueError(t("i2c.bad_speed"))
    return v


def i2c(
    vdd: float = typer.Option(3.3, "--vdd", **eng(t("i2c.opt.vdd"))),
    cb: float = typer.Option(..., "--cb", **eng(t("i2c.opt.cb"))),
    speed: float = typer.Option(400e3, "--speed", "-s", parser=cli_parser(_i2c_speed),
                                metavar="100k|400k|1M", help=t("i2c.opt.speed")),
):
    if vdd <= 0.4 or cb <= 0:
        fail(t("common.positive_all"))
    if cb > 400e-12:
        warn(t("i2c.cb_limit"))
    r_min, r_max = i2c_pullup_range(vdd, cb, speed)
    rows = {"Rmin": format_si(r_min, "Ω"), "Rmax": format_si(r_max, "Ω")}
    data = {"vdd_v": vdd, "cb_f": cb, "speed_hz": speed, "r_min_ohm": r_min, "r_max_ohm": r_max}
    if r_min > r_max:
        result_panel(f"I²C {format_si(speed, 'Hz')}", rows, data=data)
        fail(t("i2c.impossible"))
    candidates = series_values("E12", r_min, r_max)
    if candidates:
        best = min(candidates, key=lambda r: abs(math.log(r / math.sqrt(r_min * r_max))))
        rows[t("i2c.suggested")] = format_si(best, "Ω")
        data["suggested_ohm"] = best
    result_panel(f"I²C {format_si(speed, 'Hz')}", rows, data=data)
    theory(t("i2c.note"))


# --- CRC -----------------------------------------------------------------------------------------

@dataclass(frozen=True)
class CrcAlgo:
    name: str
    width: int
    poly: int
    init: int
    refin: bool
    refout: bool
    xorout: int


CRC_ALGOS = [
    CrcAlgo("CRC-8", 8, 0x07, 0x00, False, False, 0x00),
    CrcAlgo("CRC-8/MAXIM", 8, 0x31, 0x00, True, True, 0x00),
    CrcAlgo("CRC-16/MODBUS", 16, 0x8005, 0xFFFF, True, True, 0x0000),
    CrcAlgo("CRC-16/CCITT-FALSE", 16, 0x1021, 0xFFFF, False, False, 0x0000),
    CrcAlgo("CRC-16/XMODEM", 16, 0x1021, 0x0000, False, False, 0x0000),
    CrcAlgo("CRC-32", 32, 0x04C11DB7, 0xFFFFFFFF, True, True, 0xFFFFFFFF),
]


def _reflect(value: int, width: int) -> int:
    out = 0
    for _ in range(width):
        out = (out << 1) | (value & 1)
        value >>= 1
    return out


def crc_compute(algo: CrcAlgo, data: bytes) -> int:
    top = 1 << (algo.width - 1)
    mask = (1 << algo.width) - 1
    crc = algo.init
    for byte in data:
        if algo.refin:
            byte = _reflect(byte, 8)
        crc ^= byte << (algo.width - 8)
        for _ in range(8):
            crc = ((crc << 1) ^ algo.poly) if crc & top else (crc << 1)
            crc &= mask
    if algo.refout:
        crc = _reflect(crc, algo.width)
    return crc ^ algo.xorout


def parse_hex_bytes(text: str) -> bytes:
    s = re.sub(r"0x", "", text, flags=re.I)
    s = re.sub(r"[\s,:;-]", "", s)
    if not s or len(s) % 2 or not re.fullmatch(r"[0-9A-Fa-f]+", s):
        raise ValueError(t("crc.bad_hex"))
    return bytes.fromhex(s)


def crc(
    data: str = typer.Argument(..., help=t("crc.arg")),
    text: bool = typer.Option(False, "--text", help=t("crc.opt.text")),
    algo: Optional[str] = typer.Option(None, "--algo", "-a", help=t("crc.opt.algo")),
):
    try:
        raw = data.encode("utf-8") if text else parse_hex_bytes(data)
    except ValueError as e:
        fail(str(e))
    algos = CRC_ALGOS
    if algo:
        algos = [a for a in CRC_ALGOS if a.name.lower() == algo.lower() or a.name.lower().endswith(algo.lower())]
        if not algos:
            fail(t("crc.unknown", algo=algo, options=", ".join(a.name for a in CRC_ALGOS)))
    tbl = Table(title=t("crc.title", n=len(raw)))
    tbl.add_column(t("crc.col.algo"))
    tbl.add_column("Hex", justify="right", style="bold green")
    tbl.add_column(t("crc.col.bytes"), justify="right")
    records = []
    for a in algos:
        value = crc_compute(a, raw)
        digits = a.width // 4
        nbytes = a.width // 8
        order = "little" if a.refout else "big"     # yansımalı CRC'ler genelde LSB önce gönderilir
        wire_bytes = value.to_bytes(nbytes, order).hex(" ").upper()
        tbl.add_row(a.name, f"0x{value:0{digits}X}", wire_bytes)
        records.append({"algorithm": a.name, "value": value, "hex": f"0x{value:0{digits}X}",
                        "bytes": wire_bytes})
    checksum = sum(raw) & 0xFF
    xor = 0
    for b in raw:
        xor ^= b
    tbl.add_row("SUM8", f"0x{checksum:02X}", f"{checksum:02X}")
    tbl.add_row("XOR8", f"0x{xor:02X}", f"{xor:02X}")
    records += [{"algorithm": "SUM8", "value": checksum}, {"algorithm": "XOR8", "value": xor}]
    emit(tbl, records)
