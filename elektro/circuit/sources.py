"""Kaynak değerleri (SPICE yazımı) ve analiz komutları.

Kaynak değeri — parçalar herhangi bir sırayla yazılabilir:
    5                       DC 5
    DC 5 AC 1               DC çalışma noktasında 5, AC analizde 1∠0°
    AC 1 90                 AC genlik 1, faz 90°
    SINE(0 1 1k)            SINE(Voff Vamp f [Td [θ [faz°]]])   (SIN da olur)
    PULSE(0 5 0 1u 1u 0.5m 1m)   PULSE(V1 V2 [Td [Tr [Tf [Ton [Per]]]]])

Analiz komutu (LTspice gibi):
    .op
    .tran 10m               bitiş süresi (adım otomatik)
    .tran 1u 10m            adım ve bitiş süresi
    .ac dec 100 10 100k     dec|oct|lin, nokta sayısı, başlangıç ve bitiş frekansı
    .dc V1 0 5 0.1          kaynak, başlangıç, bitiş, adım
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import List, Optional

from elektro.circuit.model import CircuitError
from elektro.i18n import t
from elektro.units import parse_value


def _num(text: str) -> float:
    """SPICE sayısı: 1k, 4k7, 1meg/1Meg (mega), 10m (mili), 1u."""
    s = re.sub(r"(?i)meg", "meg", text.strip())
    try:
        return parse_value(s)
    except ValueError:
        raise CircuitError(t("src.bad_number", text=text))


@dataclass
class Source:
    dc: Optional[float] = None
    ac_mag: float = 0.0
    ac_phase: float = 0.0                        # derece
    wave: Optional[str] = None                   # SINE | PULSE
    params: List[float] = field(default_factory=list)

    def at(self, time: float) -> float:
        """Transient analizde t anındaki değer."""
        if self.wave == "SINE":
            p = self.params + [0.0] * (6 - len(self.params))
            vo, va, freq, td, theta, phase = p[:6]
            if time < td:
                return vo + va * math.sin(math.radians(phase))
            tt = time - td
            return vo + va * math.exp(-tt * theta) * math.sin(2 * math.pi * freq * tt + math.radians(phase))
        if self.wave == "PULSE":
            p = self.params + [None] * (7 - len(self.params))
            v1, v2, td, tr, tf, ton, per = p[:7]
            td, tr, tf = td or 0.0, tr or 0.0, tf or 0.0
            if time < td:
                return v1
            tt = time - td
            if per:
                tt = math.fmod(tt, per)
            if tr and tt < tr:
                return v1 + (v2 - v1) * tt / tr
            if ton is None or tt < tr + ton:
                return v2
            if tf and tt < tr + ton + tf:
                return v2 + (v1 - v2) * (tt - tr - ton) / tf
            return v1
        return self.dc or 0.0

    def dc_value(self) -> float:
        """DC çalışma noktasında kullanılan değer: DC yazılmışsa o, yoksa dalganın t = 0 değeri."""
        if self.dc is not None:
            return self.dc
        return self.at(0.0) if self.wave else 0.0

    def ac_phasor(self) -> complex:
        return complex(self.ac_mag * math.cos(math.radians(self.ac_phase)),
                       self.ac_mag * math.sin(math.radians(self.ac_phase)))

    def is_plain(self) -> bool:
        return self.wave is None and not self.ac_mag


_WAVE_RE = re.compile(r"(?i)\b(SINE?|PULSE)\s*\(([^)]*)\)")


def parse_source(text: str) -> Source:
    s = text.strip()
    if not s:
        raise CircuitError(t("src.bad", text=text))
    src = Source()
    m = _WAVE_RE.search(s)
    if m:
        name = m.group(1).upper()
        src.wave = "SINE" if name.startswith("SIN") else "PULSE"
        src.params = [_num(x) for x in re.split(r"[\s,]+", m.group(2).strip()) if x]
        need = 3 if src.wave == "SINE" else 2
        if len(src.params) < need or len(src.params) > (6 if src.wave == "SINE" else 7):
            raise CircuitError(t("src.bad_wave", name=src.wave))
        s = (s[:m.start()] + " " + s[m.end():]).strip()
    tokens = s.split()
    i = 0
    while i < len(tokens):
        tok = tokens[i].upper()
        if tok == "DC" and i + 1 < len(tokens):
            src.dc = _num(tokens[i + 1])
            i += 2
        elif tok == "AC" and i + 1 < len(tokens):
            src.ac_mag = _num(tokens[i + 1])
            i += 2
            if i < len(tokens) and tokens[i].upper() not in ("DC", "AC"):
                try:
                    src.ac_phase = _num(tokens[i])
                    i += 1
                except CircuitError:
                    pass
        elif src.dc is None and i == 0:
            src.dc = _num(tokens[i])
            i += 1
        else:
            raise CircuitError(t("src.bad", text=text))
    return src


def spice_source(text: str) -> str:
    """Kaynak değerini SPICE satırına çevirir: '12' → 'DC 12', '4k7' → 'DC 4.7k'."""
    from elektro.circuit.model import spice_number
    src = parse_source(text)
    parts = []
    if src.dc is not None or src.is_plain():
        parts.append(f"DC {spice_number(src.dc or 0.0)}")
    if src.ac_mag:
        parts.append(f"AC {spice_number(src.ac_mag)}" + (f" {src.ac_phase:g}" if src.ac_phase else ""))
    if src.wave:
        parts.append(f"{'SIN' if src.wave == 'SINE' else 'PULSE'}({' '.join(spice_number(v) for v in src.params)})")
    return " ".join(parts)


# --- Analiz komutları ---------------------------------------------------------------------------

@dataclass
class Analysis:
    kind: str = "op"                 # op | tran | ac | dc
    tstop: float = 0.0
    tstep: float = 0.0               # 0: otomatik
    sweep: str = "dec"               # dec | oct | lin
    points: int = 100
    fstart: float = 0.0
    fstop: float = 0.0
    source: str = ""
    start: float = 0.0
    stop: float = 0.0
    step: float = 0.0

    def directive(self) -> str:
        from elektro.circuit.model import spice_number as n
        if self.kind == "tran":
            return f".tran {n(self.tstep)} {n(self.tstop)}" if self.tstep else f".tran {n(self.tstop)}"
        if self.kind == "ac":
            return f".ac {self.sweep} {self.points} {n(self.fstart)} {n(self.fstop)}"
        if self.kind == "dc":
            return f".dc {self.source} {n(self.start)} {n(self.stop)} {n(self.step)}"
        return ".op"


def parse_directive(text: str) -> Analysis:
    parts = text.strip().split()
    if not parts:
        return Analysis()
    head = parts[0].lower().lstrip(".")
    args = parts[1:]
    try:
        if head == "op" and not args:
            return Analysis()
        if head == "tran" and 1 <= len(args) <= 2:
            values = [_num(a) for a in args]
            tstep, tstop = (0.0, values[0]) if len(values) == 1 else values
            if tstop <= 0 or tstep < 0 or tstep > tstop:
                raise CircuitError(t("an.bad_tran"))
            return Analysis("tran", tstop=tstop, tstep=tstep)
        if head == "ac" and len(args) == 4 and args[0].lower() in ("dec", "oct", "lin"):
            points = int(_num(args[1]))
            fstart, fstop = _num(args[2]), _num(args[3])
            if points < 1 or fstart <= 0 or fstop <= fstart:
                raise CircuitError(t("an.bad_ac"))
            return Analysis("ac", sweep=args[0].lower(), points=points, fstart=fstart, fstop=fstop)
        if head == "dc" and len(args) == 4:
            start, stop, step = (_num(a) for a in args[1:])
            if step == 0 or (stop - start) / step < 0:
                raise CircuitError(t("an.bad_dc"))
            return Analysis("dc", source=args[0].upper(), start=start, stop=stop, step=step)
    except CircuitError:
        raise
    except ValueError:
        pass
    raise CircuitError(t("an.bad", text=text))


def ac_frequencies(an: Analysis, limit: int = 2000) -> List[float]:
    if an.sweep == "lin":
        n = max(min(an.points, limit), 2)
        return [an.fstart + (an.fstop - an.fstart) * i / (n - 1) for i in range(n)]
    base = 10 if an.sweep == "dec" else 2
    per = an.points
    count = max(int(math.ceil(math.log(an.fstop / an.fstart, base) * per)) + 1, 2)
    count = min(count, limit)
    a, b = math.log10(an.fstart), math.log10(an.fstop)
    return [10 ** (a + (b - a) * i / (count - 1)) for i in range(count)]


def dc_values(an: Analysis, limit: int = 5000) -> List[float]:
    count = int(math.floor((an.stop - an.start) / an.step + 1e-9)) + 1
    count = min(count, limit)
    return [an.start + an.step * i for i in range(count)]
