"""Devre modeli: bileşenler, kablolar, düğüm (net) çıkarma, JSON dosyası ve SPICE netlist'i.

Koordinatlar ızgara birimidir. Yatay bir iki uçlu bileşen 3 birim, dikey olan 2 birim yer kaplar;
uçları (pin) her zaman ızgara noktalarına oturur. Kablolar yatay ya da dikey parçalardır.

Üç uçlu elemanların konumu (x, y) gövdenin ortasıdır:
    BJT / MOSFET (rot 0):  C/D (x, y−1) · B/G (x−1, y) · E/S (x, y+1); her 90° saat yönünde döner
    Op-amp (rot 0):        + (x−1, y−1) · − (x−1, y+1) · çıkış (x+2, y)
                           rot 90: girişler yer değiştirir, 180: aynalanır, 270: ikisi birden
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from elektro.i18n import t
from elektro.units import parse_value

Point = Tuple[int, int]
Segment = Tuple[int, int, int, int]

H_SPAN, V_SPAN = 3, 2
FORMAT_VERSION = 1


@dataclass(frozen=True)
class Kind:
    letter: str          # R, C, L, V, I, GND
    unit: str
    default: str
    pins: int = 2


KINDS: Dict[str, Kind] = {
    "R": Kind("R", "Ω", "1k"),
    "C": Kind("C", "F", "100n"),
    "L": Kind("L", "H", "10m"),
    "V": Kind("V", "V", "5"),
    "I": Kind("I", "A", "1m"),
    "GND": Kind("GND", "", "", pins=1),
    "N": Kind("N", "", "OUT", pins=1),                 # düğüm etiketi: aynı adlı noktalar bağlıdır
    "D": Kind("D", "", "1N4148"),
    "Q": Kind("Q", "", "2N2222", pins=3),
    "M": Kind("M", "", "2N7000", pins=3),
    "U": Kind("U", "", "ideal", pins=3),
}
THREE_PIN = ("Q", "M", "U")
SYMBOLS = ("GND", "N")                                  # elektriksel eleman değil, yalnızca bağlantı
LABEL_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,15}$")
GROUND_NAMES = ("GND", "0")
DIODE_ARROW = {0: "▶", 90: "▼", 180: "◀", 270: "▲"}        # anottan katoda iletim yönü


def _rotate(dx: int, dy: int, rot: int) -> Point:
    for _ in range(rot // 90):
        dx, dy = -dy, dx
    return dx, dy


@dataclass
class Component:
    ref: str
    kind: str
    value: str
    x: int
    y: int
    rot: int = 0         # 0: yatay (1. uç solda), 90: dikey (1. uç üstte), 180, 270

    @property
    def is_part(self) -> bool:
        """Devre elemanı mı (toprak ve düğüm etiketi değil)?"""
        return self.kind not in SYMBOLS

    @property
    def horizontal(self) -> bool:
        return self.rot in (0, 180)

    def pins(self) -> List[Point]:
        """Uç noktaları. V/I kaynağında 1. uç + ucudur; diyotta anot–katot; BJT'de C, B, E;
        MOSFET'te D, G, S; op-amp'ta çıkış, +, −."""
        if self.kind in SYMBOLS:
            return [(self.x, self.y)]
        if self.kind == "U":
            flip = -1 if self.rot in (90, 270) else 1
            mirror = -1 if self.rot in (180, 270) else 1
            return [(self.x + 2 * mirror, self.y), (self.x - mirror, self.y - flip), (self.x - mirror, self.y + flip)]
        if self.kind in THREE_PIN:
            return [(self.x + dx, self.y + dy) for dx, dy in
                    (_rotate(0, -1, self.rot), _rotate(-1, 0, self.rot), _rotate(0, 1, self.rot))]
        if self.horizontal:
            a, b = (self.x, self.y), (self.x + H_SPAN, self.y)
        else:
            a, b = (self.x, self.y), (self.x, self.y + V_SPAN)
        return [a, b] if self.rot in (0, 90) else [b, a]

    def cells(self) -> List[Point]:
        """Kapladığı tüm ızgara noktaları (seçim için)."""
        if self.kind in SYMBOLS:
            return [(self.x, self.y)]
        if self.kind in THREE_PIN:
            pts = self.pins() + [(self.x, self.y)]
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            return [(x, y) for x in range(min(xs), max(xs) + 1) for y in range(min(ys), max(ys) + 1)]
        if self.horizontal:
            return [(self.x + i, self.y) for i in range(H_SPAN + 1)]
        return [(self.x, self.y + i) for i in range(V_SPAN + 1)]

    def label(self) -> str:
        if self.kind == "GND":
            return "GND"
        if self.kind == "N":
            return self.value
        value = self.value
        unit = KINDS[self.kind].unit
        if self.kind in ("V", "I") and value:
            value = short_source(value, unit)
        if self.kind in ("D", "Q", "M", "U"):
            value = short_model(self.kind, value)
        if self.kind == "D":                             # iletim yönü: anottan katoda
            return f"{DIODE_ARROW[self.rot]}{self.ref} {value}"
        return f"{self.ref} {value}"

    def number(self) -> float:
        return parse_value(self.value)


def short_model(kind: str, text: str) -> str:
    """Şemada kısa model etiketi: 'NPN IS=14f BF=255' → 'NPN*' (* özel parametre); op-amp'ta ray kalır."""
    tokens = text.split()
    if len(tokens) <= 1:
        return text
    head = tokens[0] if "=" not in tokens[0] else {"D": "D", "Q": "BJT", "M": "MOS", "U": "ideal"}[kind]
    rails = [tok for tok in tokens if ".." in tok or tok.startswith(("±", "+-"))]
    custom = any("=" in tok for tok in tokens)
    return " ".join([head + ("*" if custom else "")] + rails)


def short_source(text: str, unit: str) -> str:
    """Şemada kısa kaynak etiketi: '12' → '12V', 'SINE(0 1 1k) AC 1' → 'SIN 1kHz', PULSE(…) → 'PULSE'."""
    from elektro.circuit.sources import parse_source
    from elektro.units import format_si
    try:
        src = parse_source(text)
    except CircuitError:
        return text
    if src.wave == "SINE":
        return "SIN " + format_si(src.params[2], "Hz", 3).replace(" ", "")
    if src.wave == "PULSE":
        return "PULSE"
    if src.ac_mag and src.dc is None:
        return f"AC {format_si(src.ac_mag, unit, 3).replace(' ', '')}"
    return format_si(src.dc or 0.0, unit, 4).replace(" ", "")


def _on_segment(p: Point, s: Segment) -> bool:
    x1, y1, x2, y2 = s
    if x1 == x2 == p[0]:
        return min(y1, y2) <= p[1] <= max(y1, y2)
    if y1 == y2 == p[1]:
        return min(x1, x2) <= p[0] <= max(x1, x2)
    return False


def segment_points(s: Segment) -> List[Point]:
    x1, y1, x2, y2 = s
    if y1 == y2:
        step = 1 if x2 >= x1 else -1
        return [(x, y1) for x in range(x1, x2 + step, step)]
    step = 1 if y2 >= y1 else -1
    return [(x1, y) for y in range(y1, y2 + step, step)]


class CircuitError(ValueError):
    pass


# --- Excel tarzı adresler: sütun harf (A, B, … Z, AA), satır numara (1'den başlar) -----------

ADDR_RE = re.compile(r"^([A-Za-z]{1,3})(\d{1,4})$")


def col_name(x: int) -> str:
    name = ""
    x += 1
    while x:
        x, rem = divmod(x - 1, 26)
        name = chr(65 + rem) + name
    return name


def addr(p: Point) -> str:
    """(2, 0) → 'C1'"""
    return f"{col_name(p[0])}{p[1] + 1}"


def parse_addr(text: str) -> Optional[Point]:
    m = ADDR_RE.match(text.strip())
    if not m or int(m.group(2)) < 1:
        return None
    x = 0
    for ch in m.group(1).upper():
        x = x * 26 + ord(ch) - 64
    return (x - 1, int(m.group(2)) - 1)


@dataclass
class Circuit:
    components: List[Component] = field(default_factory=list)
    wires: List[Segment] = field(default_factory=list)
    probes: List[str] = field(default_factory=list)      # "V(C3)", "I(B2,B6)", "I(R1)"
    analysis: str = ""                                    # ".tran 10m", ".ac dec 100 10 100k" …
    notes: List[str] = field(default_factory=list, compare=False, repr=False)   # içe aktarma uyarıları

    # --- düzenleme ---
    def next_ref(self, kind: str) -> str:
        if kind == "GND":
            return "GND"
        if kind == "N":
            kind = "LBL"
        used = {c.ref for c in self.components}
        n = 1
        while f"{kind}{n}" in used:
            n += 1
        return f"{kind}{n}"

    def add(self, kind: str, x: int, y: int, rot: int = 0, value: Optional[str] = None) -> Component:
        spec = KINDS[kind]
        comp = Component(self.next_ref(kind), kind, value if value is not None else spec.default, x, y, rot)
        self.components.append(comp)
        return comp

    def add_wire(self, a: Point, b: Point) -> None:
        """İki nokta arasına kablo: önce yatay, sonra dikey parça (L biçimi)."""
        (x1, y1), (x2, y2) = a, b
        parts = []
        if x1 != x2:
            parts.append((x1, y1, x2, y1))
        if y1 != y2:
            parts.append((x2, y1, x2, y2))
        for seg in parts:
            if seg not in self.wires and (seg[2], seg[3], seg[0], seg[1]) not in self.wires:
                self.wires.append(seg)

    def component_at(self, p: Point) -> Optional[Component]:
        for comp in reversed(self.components):
            if p in comp.cells():
                return comp
        return None

    def wire_at(self, p: Point) -> Optional[Segment]:
        for seg in reversed(self.wires):
            if _on_segment(p, seg):
                return seg
        return None

    def delete_at(self, p: Point) -> bool:
        comp = self.component_at(p)
        if comp is not None:
            self.components.remove(comp)
            return True
        seg = self.wire_at(p)
        if seg is not None:
            self.wires.remove(seg)
            return True
        return False

    # --- düğümler ---
    def nets(self) -> Dict[Point, str]:
        """Her bağlantı noktasının düğüm adı. GND'ye bağlı düğüm '0'; diğerleri Excel gibi,
        düğümün en üst-soldaki noktasının adresiyle adlandırılır (B3, C1…).

        Kablo uçları ve bileşen uçları "terminal"dir; bir terminal başka bir kablonun
        ortasına değiyorsa bağlanır (T bağlantısı). Uç olmadan kesişen kablolar bağlanmaz.
        """
        parent: Dict[Point, Point] = {}

        def find(p: Point) -> Point:
            parent.setdefault(p, p)
            while parent[p] != p:
                parent[p] = parent[parent[p]]
                p = parent[p]
            return p

        def union(a: Point, b: Point) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)

        terminals = {p for c in self.components for p in c.pins()}
        for x1, y1, x2, y2 in self.wires:
            terminals |= {(x1, y1), (x2, y2)}
        for p in terminals:
            find(p)
        for seg in self.wires:
            a, b = (seg[0], seg[1]), (seg[2], seg[3])
            union(a, b)
            for p in terminals:
                if _on_segment(p, seg):
                    union(p, a)
        # düğüm etiketleri: aynı adı (büyük/küçük harf farketmez) taşıyan noktalar bağlıdır
        labels = [c for c in self.components if c.kind == "N"]
        first: Dict[str, Point] = {}
        for c in labels:
            key = c.value.upper()
            if key in first:
                union(first[key], c.pins()[0])
            else:
                first[key] = c.pins()[0]
        groups: Dict[Point, List[Point]] = {}
        for p in terminals:
            groups.setdefault(find(p), []).append(p)
        grounds = {find(c.pins()[0]) for c in self.components if c.kind == "GND"}
        grounds |= {find(c.pins()[0]) for c in labels if c.value.upper() in GROUND_NAMES}
        label_name: Dict[Point, str] = {}
        for c in sorted(labels, key=lambda c: c.value.upper()):
            label_name.setdefault(find(c.pins()[0]), c.value)
        names: Dict[Point, str] = {}
        for root, pts in groups.items():
            if root in grounds:
                name = "0"
            else:
                name = label_name.get(root) or addr(min(pts, key=lambda q: (q[1], q[0])))
            for p in pts:
                names[p] = name
        return names

    def net_at(self, p: Point, nets: Optional[Dict[Point, str]] = None) -> Optional[str]:
        """Noktanın düğümü: bileşen ucu, kablo ucu ya da bir kablonun ortası."""
        nets = self.nets() if nets is None else nets
        if p in nets:
            return nets[p]
        seg = self.wire_at(p)
        return nets.get((seg[0], seg[1])) if seg else None

    def net_points(self) -> Dict[str, List[Point]]:
        out: Dict[str, List[Point]] = {}
        for p, name in self.nets().items():
            out.setdefault(name, []).append(p)
        return out

    # --- dosya ---
    def to_dict(self) -> dict:
        return {"elektro_circuit": FORMAT_VERSION,
                "components": [asdict(c) for c in self.components],
                "wires": [list(w) for w in self.wires],
                "probes": list(self.probes),
                "analysis": self.analysis}

    @classmethod
    def from_dict(cls, data: dict) -> "Circuit":
        if not isinstance(data, dict) or "components" not in data:
            raise CircuitError(t("ckt.bad_file"))
        try:
            comps = [Component(str(c["ref"]), str(c["kind"]), str(c.get("value", "")), int(c["x"]), int(c["y"]),
                               int(c.get("rot", 0)) % 360) for c in data["components"]]
            wires = [tuple(int(v) for v in w) for w in data.get("wires", [])]
            probes = [str(x) for x in data.get("probes", [])]
            analysis = str(data.get("analysis", "") or "")
        except (KeyError, TypeError, ValueError):
            raise CircuitError(t("ckt.bad_file"))
        for c in comps:
            if c.kind not in KINDS or c.rot not in (0, 90, 180, 270):
                raise CircuitError(t("ckt.bad_file"))
        if any(len(w) != 4 or (w[0] != w[2] and w[1] != w[3]) for w in wires):
            raise CircuitError(t("ckt.bad_file"))
        return cls(comps, [tuple(w) for w in wires], probes, analysis)

    def save(self, path: Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "Circuit":
        """JSON devre dosyası ya da SPICE netlist'i (.cir, .sp, .net …). İçe aktarma uyarıları
        `notes` özelliğinde döner."""
        from elektro.circuit.spice import is_spice, load_spice
        if is_spice(path):
            circuit, notes = load_spice(path)
            circuit.notes = notes
            return circuit
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except OSError as e:
            raise CircuitError(str(e))
        except ValueError:
            raise CircuitError(t("ckt.bad_file"))
        return cls.from_dict(data)

    # --- SPICE ---
    def to_spice(self, title: str = "elektro circuit") -> str:
        nets = self.nets()
        lines = [f"* {title}"]
        models = []
        for c in self.components:
            if not c.is_part:
                continue
            pins = [nets.get(p, "?") for p in c.pins()]
            if c.kind in ("D", "Q", "M", "U"):
                from elektro.circuit.devices import parse_model, spice_model
                name, line = spice_model(c)
                if c.kind == "U":                        # davranışsal kaynak: çıkış = A·(V+ − V−)
                    gain = parse_model("U", c.value).params["A"]
                    lines.append(f"E{c.ref} {pins[0]} 0 {pins[1]} {pins[2]} {spice_number(gain)}")
                    continue
                if c.kind == "M":
                    pins.append(pins[2])                 # gövde kaynağa bağlı
                lines.append(f"{c.ref} {' '.join(pins)} {name}")
                models.append(line)
                continue
            if c.kind in ("V", "I"):
                from elektro.circuit.sources import spice_source
                value = spice_source(c.value)
            else:
                value = spice_number(c.number())
            lines.append(f"{c.ref} {pins[0]} {pins[1]} {value}")
        lines += [m for m in models if m]
        lines += [self.analysis.strip() or ".op", ".end"]
        return "\n".join(lines) + "\n"


_SPICE_SUFFIX = [(1e12, "T"), (1e9, "G"), (1e6, "Meg"), (1e3, "k"), (1.0, ""), (1e-3, "m"), (1e-6, "u"),
                 (1e-9, "n"), (1e-12, "p"), (1e-15, "f")]


def spice_number(value: float) -> str:
    """SPICE değeri: 4700 → 4.7k, 1e6 → 1Meg (SPICE'ta M mili demektir)."""
    if value == 0:
        return "0"
    for factor, suffix in _SPICE_SUFFIX:
        if abs(value) >= factor * 0.99995:
            return f"{value / factor:.6g}{suffix}"
    return f"{value:.6g}"


def valid_value(kind: str, text: str) -> bool:
    if kind == "GND":
        return True
    if kind == "N":
        return bool(LABEL_RE.match(text))
    if kind in ("V", "I"):
        from elektro.circuit.sources import parse_source
        try:
            parse_source(text)
            return True
        except CircuitError:
            return False
    if kind in ("D", "Q", "M", "U"):
        from elektro.circuit.devices import parse_model
        try:
            parse_model(kind, text)
            return True
        except CircuitError:
            return False
    try:
        v = parse_value(text)
    except ValueError:
        return False
    return v > 0 if kind in ("R", "C", "L") else True

