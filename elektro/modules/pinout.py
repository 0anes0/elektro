"""Sık kullanılan entegre ve transistörlerin bacak bağlantıları (çevrimdışı)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import typer
from rich.table import Table
from rich.text import Text

from elektro.i18n import t
from elektro.ui import console, emit, fail, json_mode, print_json, theory


@dataclass(frozen=True)
class Part:
    key: str
    name: str
    package: str                  # DIP8, DIP14, DIP16, DIP28, TO-92, TO-220, SOT-223
    pins: Tuple[str, ...]         # 1. bacaktan başlayarak
    aliases: Tuple[str, ...] = field(default_factory=tuple)
    tab: Optional[str] = None     # soğutucu tablası neye bağlı


PARTS: List[Part] = [
    Part("ne555", "NE555", "DIP8", ("GND", "TRIG", "OUT", "RESET", "CTRL", "THR", "DIS", "VCC"),
         ("555", "lm555", "tlc555")),
    Part("lm358", "LM358", "DIP8", ("OUT A", "IN− A", "IN+ A", "GND / V−", "IN+ B", "IN− B", "OUT B", "VCC"),
         ("lm2904", "tl072", "tl082", "ne5532", "lm393", "mcp6002")),
    Part("ua741", "µA741", "DIP8", ("OFFSET N1", "IN−", "IN+", "V−", "OFFSET N2", "OUT", "V+", "NC"),
         ("741", "lm741", "tl071", "tl081")),
    Part("lm386", "LM386", "DIP8", ("GAIN", "IN−", "IN+", "GND", "VOUT", "VS", "BYPASS", "GAIN")),
    Part("attiny85", "ATtiny85", "DIP8",
         ("PB5 RESET ADC0", "PB3 ADC3 XTAL1", "PB4 ADC2 XTAL2", "GND",
          "PB0 MOSI SDA OC0A", "PB1 MISO OC0B", "PB2 SCK SCL ADC1", "VCC"), ("tiny85", "attiny45", "attiny25")),
    Part("pc817", "PC817", "DIP4", ("ANODE", "CATHODE", "EMITTER", "COLLECTOR"), ("el817", "ltv817")),
    Part("74hc00", "74HC00", "DIP14", ("1A", "1B", "1Y", "2A", "2B", "2Y", "GND",
                                       "3Y", "3A", "3B", "4Y", "4A", "4B", "VCC"),
         ("7400", "74ls00", "74hc08", "74hc32", "74hc86")),
    Part("74hc04", "74HC04", "DIP14", ("1A", "1Y", "2A", "2Y", "3A", "3Y", "GND",
                                       "4Y", "4A", "5Y", "5A", "6Y", "6A", "VCC"), ("7404", "74ls04", "74hc14")),
    Part("74hc595", "74HC595", "DIP16", ("QB", "QC", "QD", "QE", "QF", "QG", "QH", "GND",
                                         "QH'", "SRCLR (MR)", "SRCLK (SHCP)", "RCLK (STCP)", "OE", "SER (DS)",
                                         "QA", "VCC"), ("595",)),
    Part("cd4017", "CD4017", "DIP16", ("Q5", "Q1", "Q0", "Q2", "Q6", "Q7", "Q3", "VSS",
                                       "Q8", "Q4", "Q9", "CO", "CLK INH", "CLK", "RST", "VDD"), ("4017",)),
    Part("l293d", "L293D", "DIP16", ("EN 1,2", "1A", "1Y", "GND", "GND", "2Y", "2A", "VCC2 (motor)",
                                     "EN 3,4", "3A", "3Y", "GND", "GND", "4Y", "4A", "VCC1 (5V)"), ("l293",)),
    Part("atmega328p", "ATmega328P", "DIP28", (
        "PC6 RESET", "PD0 RXD (D0)", "PD1 TXD (D1)", "PD2 INT0 (D2)", "PD3 INT1 OC2B (D3)", "PD4 T0 (D4)",
        "VCC", "GND", "PB6 XTAL1", "PB7 XTAL2", "PD5 OC0B (D5)", "PD6 OC0A (D6)", "PD7 AIN1 (D7)",
        "PB0 ICP1 (D8)", "PB1 OC1A (D9)", "PB2 SS OC1B (D10)", "PB3 MOSI OC2A (D11)", "PB4 MISO (D12)",
        "PB5 SCK (D13)", "AVCC", "AREF", "GND", "PC0 ADC0 (A0)", "PC1 ADC1 (A1)", "PC2 ADC2 (A2)",
        "PC3 ADC3 (A3)", "PC4 ADC4 SDA (A4)", "PC5 ADC5 SCL (A5)"), ("atmega328", "mega328", "arduino")),
    Part("78xx", "78xx", "TO-220", ("IN", "GND", "OUT"), ("7805", "7809", "7812", "7815", "lm7805", "l7805"),
         tab="GND"),
    Part("79xx", "79xx", "TO-220", ("GND", "IN", "OUT"), ("7905", "7912", "lm7905", "l7905"), tab="IN"),
    Part("lm317", "LM317", "TO-220", ("ADJ", "OUT", "IN"), ("317",), tab="OUT"),
    Part("ams1117", "AMS1117", "SOT-223", ("GND / ADJ", "VOUT", "VIN"), ("lm1117", "ams1117-3.3", "ams1117-5.0"),
         tab="VOUT"),
    Part("irfz44n", "IRFZ44N", "TO-220", ("G", "D", "S"), ("irf540n", "irlz44n", "irf3205", "irf540"), tab="D"),
    Part("bc547", "BC547", "TO-92", ("C", "B", "E"), ("bc546", "bc548", "bc549", "bc557", "bc558")),
    Part("2n2222", "2N2222A", "TO-92", ("E", "B", "C"), ("2n2222a", "pn2222", "2n3904", "2n3906")),
    Part("lm35", "LM35", "TO-92", ("+VS", "VOUT", "GND"), ("lm35dz",)),
    Part("ds18b20", "DS18B20", "TO-92", ("GND", "DQ", "VDD"), ("18b20",)),
    Part("tl431", "TL431", "TO-92", ("REF", "ANODE", "CATHODE"), ("431",)),
]

_INDEX: Dict[str, Part] = {}
for _p in PARTS:
    for _k in (_p.key, *_p.aliases):
        _INDEX[_k] = _p


def find_part(name: str) -> Optional[Part]:
    key = name.strip().lower().replace(" ", "").replace("_", "")
    if key in _INDEX:
        return _INDEX[key]
    m = re.fullmatch(r"(?:l|lm|mc|ua)?(78|79)(?:l|m)?\d{2}\w{0,4}", key)
    if m:
        return _INDEX[m.group(1) + "xx"]
    # NE555P, LM358N, SN74HC595N gibi soneklere / öneklere izin ver
    for prefix in ("", "sn", "ne", "lm", "cd", "mc"):
        k = key[len(prefix):] if prefix and key.startswith(prefix) else key
        for cand in sorted(_INDEX, key=len, reverse=True):
            if k.startswith(cand) and len(k) - len(cand) <= 3 and not k[len(cand):].isdigit():
                return _INDEX[cand]
    return None


def shown_aliases(part: Part) -> List[str]:
    """Kısaltmalar (555, mega328) ve takma adlar (arduino) "aynı bacak düzeni" listesinde gösterilmez."""
    return [a for a in part.aliases if a not in part.key and a != "arduino"]


def _pin_style(label: str) -> str:
    up = label.upper()
    if up.startswith(("GND", "VSS", "V−")) or up == "E" or up == "S":
        return "bold blue"
    if up.startswith(("VCC", "VDD", "V+", "VS", "+VS", "AVCC", "VIN", "IN")) and "IN−" not in up and "IN+" not in up:
        return "bold red"
    if up in ("NC",):
        return "dim"
    return "cyan"


def draw_dip(part: Part) -> Text:
    n = len(part.pins)
    half = n // 2
    left = [(i + 1, part.pins[i]) for i in range(half)]
    right = [(n - i, part.pins[n - 1 - i]) for i in range(half)]
    lw = max(len(p) for _, p in left)
    inner = max(10, len(part.name) + 4)
    num_w = len(str(n))
    pad = " " * (lw + 1 + num_w + 1)
    notch = (inner - 2) // 2
    out = Text()
    out.append(f"{pad}┌{'─' * notch}╮╭{'─' * (inner - notch - 2)}┐\n")
    for row, ((ln, lp), (rn, rp)) in enumerate(zip(left, right)):
        mid = part.name.center(inner) if row == (half - 1) // 2 else " " * inner
        out.append(lp.rjust(lw), style=_pin_style(lp))
        out.append(f" {str(ln).rjust(num_w)} ┤")
        out.append(mid, style="bold yellow" if mid.strip() else "")
        out.append(f"├ {str(rn).ljust(num_w)} ")
        out.append(rp, style=_pin_style(rp))
        out.append("\n")
    out.append(f"{pad}└{'─' * inner}┘")
    return out


def draw_3pin(part: Part) -> Text:
    w = max(5, *(len(p) for p in part.pins)) + 2
    body = w * 3
    out = Text()
    if part.tab:
        out.append(f"  ┌{'─' * body}┐   {t('pin.tab')}: ")
        out.append(part.tab, style=_pin_style(part.tab))
        out.append("\n")
    else:
        out.append(f"  ╭{'─' * body}╮\n")
    out.append("  │")
    out.append(part.name.center(body), style="bold yellow")
    out.append("│\n")
    out.append(f"  └{'─' * body}┘\n")
    out.append("   " + "".join("│".center(w) for _ in part.pins) + "\n")
    out.append("   " + "".join(str(i + 1).center(w) for i in range(3)) + "\n")
    out.append("   ")
    for p in part.pins:
        out.append(p.center(w), style=_pin_style(p))
    return out


def pinout(
    name: Optional[str] = typer.Argument(None, help=t("pin.arg")),
):
    if name is None:
        if json_mode():
            print_json([{"name": p.name, "package": p.package, "aliases": list(p.aliases)} for p in PARTS])
            return
        tbl = Table(header_style="bold", box=None)
        tbl.add_column(t("pin.col.part"), style="cyan")
        tbl.add_column(t("pin.col.package"))
        tbl.add_column(t("pin.col.desc"))
        tbl.add_column(t("pin.col.aliases"), style="dim")
        for p in PARTS:
            tbl.add_row(p.name, p.package, t(f"pin.desc.{p.key}"), ", ".join(shown_aliases(p)))
        console.print(tbl)
        theory(t("pin.usage"))
        return
    part = find_part(name)
    if part is None:
        fail(t("pin.unknown", name=name))
    data = {"name": part.name, "package": part.package, "description": t(f"pin.desc.{part.key}"),
            "pins": {str(i + 1): p for i, p in enumerate(part.pins)}, "tab": part.tab,
            "aliases": list(part.aliases)}
    if json_mode():
        print_json(data)
        return
    console.print(f"[bold]{part.name}[/] — {t(f'pin.desc.{part.key}')}  [dim]({part.package})[/]")
    drawing = draw_dip(part) if part.package.startswith("DIP") else draw_3pin(part)
    emit(drawing, data)
    if part.package.startswith("DIP"):
        theory(t("pin.note.dip"))
    else:
        theory(t("pin.note.front"))
    if shown_aliases(part):
        theory(t("pin.same", parts=", ".join(a.upper() for a in shown_aliases(part))))
