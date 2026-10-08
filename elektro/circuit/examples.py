"""Hazır örnek devreler (Devre sekmesinde Ctrl+E, terminalde `elektro examples`).

Her örnek kodla çizilir; probe'ları ve analizi hazırdır, açılınca F5 yeterlidir.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Tuple

from elektro.circuit.model import Circuit

CATEGORIES = ("basic", "filters", "power", "transistor", "opamp")


def _divider() -> Circuit:
    c = Circuit()
    c.add("V", 1, 1, rot=90, value="12")
    c.add("R", 1, 1, value="10k")
    c.add("R", 4, 1, rot=90, value="4k7")
    c.add_wire((1, 3), (4, 3))
    c.add("GND", 1, 3)
    c.add("N", 4, 1, value="OUT")
    c.probes = ["V(OUT)", "I(R1)", "R(OUT,GND)"]
    return c


def _bridge() -> Circuit:
    c = Circuit()
    c.add("R", 1, 1, value="1k")
    c.add("R", 4, 1, value="1k")
    c.add_wire((1, 1), (1, 3))
    c.add("R", 1, 3, value="2k")
    c.add("R", 4, 3, value="2k")
    c.add_wire((7, 1), (7, 3))
    c.add("R", 4, 1, rot=90, value="5k")
    c.add("N", 1, 2, value="A", rot=180)
    c.add("N", 7, 2, value="B")
    c.probes = ["R(A,B)"]
    return c


def _rc_charge() -> Circuit:
    c = Circuit()
    c.add("V", 1, 1, rot=90, value="PULSE(0 5 0.5m 1u 1u 10m 20m)")
    c.add("R", 1, 1, value="1k")
    c.add("C", 4, 1, rot=90, value="1u")
    c.add_wire((1, 3), (4, 3))
    c.add("GND", 1, 3)
    c.add("N", 4, 1, value="OUT")
    c.probes = ["V(OUT)", "I(C1)"]
    c.analysis = ".tran 6m"
    return c


def _rc_lowpass() -> Circuit:
    c = Circuit()
    c.add("V", 1, 1, rot=90, value="SINE(0 1 1k) AC 1")
    c.add("R", 1, 1, value="1k")
    c.add("C", 4, 1, rot=90, value="159n")
    c.add_wire((1, 3), (4, 3))
    c.add("GND", 1, 3)
    c.add("N", 1, 1, value="IN", rot=180)
    c.add("N", 4, 1, value="OUT")
    c.probes = ["V(IN)", "V(OUT)"]
    c.analysis = ".ac dec 50 10 100k"
    return c


def _rlc_bandpass() -> Circuit:
    c = Circuit()
    c.add("V", 1, 1, rot=90, value="AC 1")
    c.add("L", 1, 1, value="10m")
    c.add("C", 4, 1, value="1u")
    c.add("R", 7, 1, rot=90, value="100")
    c.add_wire((1, 3), (7, 3))
    c.add("GND", 1, 3)
    c.add("N", 7, 1, value="OUT")
    c.probes = ["V(OUT)"]
    c.analysis = ".ac dec 100 100 10k"
    return c


def _half_wave() -> Circuit:
    c = Circuit()
    c.add("V", 1, 1, rot=90, value="SINE(0 12 50)")
    c.add("D", 1, 1, rot=0, value="1N4007")
    c.add("C", 4, 1, rot=90, value="470u")
    c.add_wire((4, 1), (7, 1))
    c.add("R", 7, 1, rot=90, value="470")
    c.add_wire((1, 3), (7, 3))
    c.add("GND", 1, 3)
    c.add("N", 1, 1, value="IN", rot=180)
    c.add("N", 7, 1, value="OUT")
    c.probes = ["V(IN)", "V(OUT)", "I(D1)"]
    c.analysis = ".tran 100m"
    return c


def _bridge_rectifier() -> Circuit:
    c = Circuit()
    c.add("V", 1, 1, rot=90, value="SINE(0 12 50)")
    c.add("N", 1, 1, value="AC1", rot=180)
    c.add("N", 1, 3, value="AC2", rot=180)
    for k, (anode, cathode) in enumerate((("AC1", "OUT"), ("AC2", "OUT"), ("GND", "AC1"), ("GND", "AC2"))):
        y = 1 + 2 * k
        c.add("D", 5, y, rot=0, value="1N4007")
        if anode == "GND":
            c.add("GND", 5, y)
        else:
            c.add("N", 5, y, value=anode, rot=180)
        c.add("N", 8, y, value=cathode)
    c.add("C", 12, 1, rot=90, value="470u")
    c.add("R", 15, 1, rot=90, value="1k")
    c.add_wire((12, 1), (15, 1))
    c.add_wire((12, 3), (15, 3))
    c.add("N", 12, 1, value="OUT", rot=180)
    c.add("GND", 12, 3)
    c.probes = ["V(AC1,AC2)", "V(OUT)"]
    c.analysis = ".tran 60m"
    return c


def _zener() -> Circuit:
    c = Circuit()
    c.add("V", 1, 1, rot=90, value="12")
    c.add("R", 1, 1, value="470")
    c.add("D", 4, 1, rot=270, value="BZX5V1")
    c.add_wire((4, 1), (7, 1))
    c.add("R", 7, 1, rot=90, value="1k")
    c.add_wire((1, 3), (7, 3))
    c.add("GND", 1, 3)
    c.add("N", 7, 1, value="OUT")
    c.probes = ["V(OUT)", "I(D1.K)"]
    c.analysis = ".dc V1 0 15 0.1"
    return c


def _led_driver() -> Circuit:
    c = Circuit()
    c.add("V", 1, 1, rot=90, value="5")
    c.add_wire((1, 1), (8, 1))
    c.add("R", 8, 1, rot=90, value="220")
    c.add("D", 8, 3, rot=90, value="LED")
    c.add("Q", 8, 7)
    c.add_wire((8, 5), (8, 6))
    c.add("V", 4, 7, rot=90, value="PULSE(0 3.3 1m 1u 1u 2m 4m)")
    c.add("R", 4, 7, value="4k7")
    c.add_wire((1, 3), (1, 10))
    c.add_wire((1, 10), (8, 10))
    c.add_wire((8, 8), (8, 10))
    c.add_wire((4, 9), (4, 10))
    c.add("GND", 1, 10)
    c.probes = ["I(D1)", "I(Q1.B)"]
    c.analysis = ".tran 8m"
    return c


def _common_emitter() -> Circuit:
    c = Circuit()
    c.add("V", 12, 2, rot=90, value="12")
    c.add("N", 12, 2, value="VCC")
    c.add("GND", 12, 4)
    c.add("R", 5, 1, rot=90, value="100k")
    c.add("N", 5, 1, value="VCC")
    c.add("R", 9, 1, rot=90, value="4k7")
    c.add("N", 9, 1, value="VCC")
    c.add("Q", 9, 5)                                     # C (9,4) B (8,5) E (9,6)
    c.add_wire((9, 3), (9, 4))
    c.add_wire((5, 3), (5, 5))
    c.add_wire((5, 5), (8, 5))
    c.add("R", 5, 5, rot=90, value="22k")              # (5,5)–(5,7)
    c.add("R", 9, 6, rot=90, value="1k")               # emetör direnci (9,6)–(9,8)
    c.add("C", 2, 5, value="10u")
    c.add_wire((5, 7), (5, 8))
    c.add_wire((5, 8), (9, 8))
    c.add("GND", 5, 8)
    c.add("V", 2, 5, rot=90, value="SINE(0 10m 1k) AC 1")
    c.add("GND", 2, 7)
    c.add("N", 2, 5, value="IN", rot=180)
    c.add("N", 9, 3, value="OUT")
    c.probes = ["V(IN)", "V(OUT)"]
    c.analysis = ".tran 3m"
    return c


def _mosfet_switch() -> Circuit:
    c = Circuit()
    c.add("V", 11, 1, rot=90, value="12")
    c.add("N", 11, 1, value="VCC")
    c.add("GND", 11, 3)
    c.add("R", 6, 1, rot=90, value="100")
    c.add("N", 6, 1, value="VCC", rot=180)
    c.add("M", 6, 4)                                     # D (6,3) G (5,4) S (6,5)
    c.add("GND", 6, 5)
    c.add("R", 2, 4, value="100")
    c.add("V", 2, 4, rot=90, value="PULSE(0 10 0 1u 1u 0.5m 1m)")
    c.add("GND", 2, 6)
    c.add("N", 6, 3, value="OUT")
    c.add("N", 2, 4, value="GATE", rot=180)
    c.probes = ["V(GATE)", "V(OUT)", "I(M1)"]
    c.analysis = ".tran 3m"
    return c


def _inverting(feedback_c: bool = False) -> Circuit:
    """Eviren yükselteç (Rf) ya da entegratör (Rf ∥ C). Op-amp: − üstte (rot 90)."""
    c = Circuit()
    c.add("U", 6, 5, rot=90, value="TL072 ±15")          # çıkış (8,5), − (5,4), + (5,6)
    c.add("GND", 5, 6)
    c.add("R", 5, 2, value="47k" if feedback_c else "10k")
    c.add_wire((5, 2), (5, 4))
    c.add_wire((8, 2), (8, 5))
    if feedback_c:
        c.add("C", 5, 0, value="10n")
        c.add_wire((5, 0), (5, 2))
        c.add_wire((8, 0), (8, 2))
    c.add("R", 1, 4, value="10k" if feedback_c else "1k")
    c.add_wire((4, 4), (5, 4))
    c.add("V", 1, 4, rot=90, value="PULSE(-1 1 0 1u 1u 0.5m 1m)" if feedback_c else "SINE(0 0.5 1k) AC 1")
    c.add("GND", 1, 6)
    c.add("N", 1, 4, value="IN", rot=180)
    c.add("N", 8, 5, value="OUT")
    c.probes = ["V(IN)", "V(OUT)"]
    c.analysis = ".tran 6m" if feedback_c else ".tran 3m"
    return c


def _non_inverting() -> Circuit:
    c = Circuit()
    c.add("V", 1, 2, rot=90, value="SINE(0 0.5 1k) AC 1")
    c.add("U", 5, 3, value="TL072 ±15")                  # çıkış (7,3), + (4,2), − (4,4)
    c.add_wire((1, 2), (4, 2))
    c.add("R", 4, 4, rot=90, value="1k")
    c.add("R", 4, 4, value="10k")
    c.add_wire((7, 4), (7, 3))
    c.add_wire((1, 4), (1, 7))
    c.add_wire((1, 7), (4, 7))
    c.add_wire((4, 6), (4, 7))
    c.add("GND", 1, 7)
    c.add("N", 1, 2, value="IN", rot=180)
    c.add("N", 7, 3, value="OUT")
    c.probes = ["V(IN)", "V(OUT)"]
    c.analysis = ".tran 3m"
    return c


def _comparator() -> Circuit:
    c = Circuit()
    c.add("V", 1, 2, rot=90, value="SINE(2.5 2 1k)")
    c.add("GND", 1, 4)
    c.add("U", 6, 3, value="LM358 0..5")                 # çıkış (8,3), + (5,2), − (5,4)
    c.add_wire((1, 2), (5, 2))
    c.add("V", 5, 4, rot=90, value="2.5")
    c.add("GND", 5, 6)
    c.add("N", 1, 2, value="IN", rot=180)
    c.add("N", 5, 4, value="REF", rot=180)
    c.add("N", 8, 3, value="OUT")
    c.probes = ["V(IN)", "V(REF)", "V(OUT)"]
    c.analysis = ".tran 3m"
    return c


EXAMPLES: Dict[str, Tuple[str, Callable[[], Circuit]]] = {
    "divider": ("basic", _divider),
    "bridge": ("basic", _bridge),
    "rc_charge": ("basic", _rc_charge),
    "rc_lowpass": ("filters", _rc_lowpass),
    "rlc_bandpass": ("filters", _rlc_bandpass),
    "half_wave": ("power", _half_wave),
    "bridge_rectifier": ("power", _bridge_rectifier),
    "zener": ("power", _zener),
    "led_driver": ("transistor", _led_driver),
    "common_emitter": ("transistor", _common_emitter),
    "mosfet_switch": ("transistor", _mosfet_switch),
    "non_inverting": ("opamp", _non_inverting),
    "inverting": ("opamp", lambda: _inverting(False)),
    "integrator": ("opamp", lambda: _inverting(True)),
    "comparator": ("opamp", _comparator),
}


def names() -> List[str]:
    return list(EXAMPLES)


def build(name: str) -> Circuit:
    """Örneği kurar ve sola yaslı etiketler satır numaralarına taşmasın diye C sütunundan başlatır."""
    circuit = EXAMPLES[name][1]()
    xs = [c.x for c in circuit.components] + [v for w in circuit.wires for v in (w[0], w[2])]
    shift(circuit, 2 - min(xs))
    return circuit


def shift(circuit: Circuit, dx: int, dy: int = 0) -> None:
    for c in circuit.components:
        c.x, c.y = c.x + dx, c.y + dy
    circuit.wires = [(x1 + dx, y1 + dy, x2 + dx, y2 + dy) for x1, y1, x2, y2 in circuit.wires]
    # adres içeren probe'lar da kaysın (etiket adları değişmez)
    from elektro.circuit.model import addr, parse_addr
    from elektro.circuit.probes import PROBE_RE

    def move(arg: str) -> str:
        p = parse_addr(arg) if arg else None
        labels = {c.value.upper() for c in circuit.components if c.kind == "N"}
        if p is None or arg.upper() in labels:
            return arg
        return addr((p[0] + dx, p[1] + dy))

    probes = []
    for expr in circuit.probes:
        m = PROBE_RE.match(expr)
        if m and (m.group(1).upper() in "VR" or m.group(3)):
            a, b = move(m.group(2)), move(m.group(3) or "")
            expr = f"{m.group(1).upper()}({a}{',' + b if b else ''})"
        probes.append(expr)
    circuit.probes = probes
