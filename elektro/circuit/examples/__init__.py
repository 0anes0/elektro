"""Hazır örnek devre kütüphanesi: Falstad'daki gibi klasörlere ayrılmış eğitim devreleri.

Devre sekmesinde Ctrl+E, terminalde `elektro examples`. Her örneğin başlığı ve öğrenciye
yönelik kısa bir açıklaması dört dilde vardır; probe'ları ve analizi hazırdır.

Örnekler klasör modüllerinde `@example(...)` ile kaydedilir (basics.py, diodes.py …).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

from elektro.circuit.model import Circuit
from elektro.i18n import get_language

Text4 = Dict[str, str]


@dataclass
class Example:
    key: str
    folder: Tuple[str, ...]                 # ("opamp", "amps")
    title: Text4
    desc: Text4
    builder: Callable[[], Circuit]
    check: Optional[Callable] = None        # testlerde fiziksel kontrol: check(circuit, op, sweep, traces)


REGISTRY: Dict[str, Example] = {}
FOLDERS: Dict[str, Text4] = {}              # "opamp/amps" → adlar
FOLDER_ORDER: List[str] = []


def T(en: str, tr: str, de: str, ru: str) -> Text4:
    return {"en": en, "tr": tr, "de": de, "ru": ru}


def folder(path: str, names: Text4) -> None:
    FOLDERS[path] = names
    FOLDER_ORDER.append(path)


def example(key: str, path: str, title: Text4, desc: Text4, check: Optional[Callable] = None):
    """Örnek kaydı (dekoratör). path: "basics/ohm" gibi klasör yolu."""
    def wrap(builder: Callable[[], Circuit]):
        if key in REGISTRY:
            raise ValueError(f"duplicate example {key}")
        REGISTRY[key] = Example(key, tuple(path.split("/")), title, desc, builder, check)
        return builder
    return wrap


def text(value: Text4) -> str:
    return value.get(get_language()) or value["en"]


def title(key: str) -> str:
    return text(REGISTRY[key].title)


def description(key: str) -> str:
    return text(REGISTRY[key].desc)


def folder_name(path: str) -> str:
    return text(FOLDERS[path])


def names() -> List[str]:
    return list(REGISTRY)


def tree() -> List[Tuple[str, List[str]]]:
    """[(klasör yolu, [örnek adları]), …] klasör sırasıyla; boş klasörler (yalnızca alt klasörü
    olanlar) da listede yer alır."""
    out = []
    for path in FOLDER_ORDER:
        items = [k for k, ex in REGISTRY.items() if "/".join(ex.folder) == path]
        out.append((path, items))
    return out


def build(key: str) -> Circuit:
    """Örneği kurar; sola yaslı etiketler satır numaralarına taşmasın diye C sütunundan başlatır."""
    circuit = REGISTRY[key].builder()
    xs = [c.x for c in circuit.components] + [v for w in circuit.wires for v in (w[0], w[2])]
    ys = [c.y for c in circuit.components] + [v for w in circuit.wires for v in (w[1], w[3])]
    shift(circuit, 2 - min(xs), 1 - min(ys))
    return circuit


def shift(circuit: Circuit, dx: int, dy: int = 0) -> None:
    from elektro.circuit.model import addr, parse_addr
    from elektro.circuit.probes import PROBE_RE
    for c in circuit.components:
        c.x, c.y = c.x + dx, c.y + dy
    circuit.wires = [(x1 + dx, y1 + dy, x2 + dx, y2 + dy) for x1, y1, x2, y2 in circuit.wires]
    labels = {c.value.upper() for c in circuit.components if c.kind == "N"}

    def move(arg: str) -> str:
        p = parse_addr(arg) if arg else None
        if p is None or arg.upper() in labels:
            return arg
        return addr((p[0] + dx, p[1] + dy))

    probes = []
    for expr in circuit.probes:                  # adres içeren probe'lar da kaysın
        m = PROBE_RE.match(expr)
        if m and (m.group(1).upper() in "VR" or m.group(3)):
            a, b = move(m.group(2)), move(m.group(3) or "")
            expr = f"{m.group(1).upper()}({a}{',' + b if b else ''})"
        probes.append(expr)
    circuit.probes = probes


# klasör modülleri yüklenince örnekler kaydolur; içe aktarma sırası = menü sırası
from elektro.circuit.examples import basics  # noqa: E402,F401
from elektro.circuit.examples import ac  # noqa: E402,F401
from elektro.circuit.examples import filters  # noqa: E402,F401
from elektro.circuit.examples import diodes  # noqa: E402,F401
from elektro.circuit.examples import bjt  # noqa: E402,F401
from elektro.circuit.examples import mosfet  # noqa: E402,F401
from elektro.circuit.examples import opamp  # noqa: E402,F401
from elektro.circuit.examples import oscillators  # noqa: E402,F401
from elektro.circuit.examples import power  # noqa: E402,F401
