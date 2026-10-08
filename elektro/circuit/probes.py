"""Probe ifadeleri: devre çözüldükten sonra ölçülecek büyüklükler.

    V(C3)        C3 noktasının bulunduğu düğümün gerilimi (toprağa göre)
    V(C3,E7)     iki nokta arasındaki gerilim farkı: V(C3) − V(E7)
    I(C1,C10)    C1 düğümünden C10 düğümüne, ikisini doğrudan bağlayan elemanlar üzerinden akan akım
    I(R1)        R1'in akımı (1. uçtan 2. uca)
    I(Q1.B)      çok uçlu bir elemanın bir ucundan elemana giren akım (Q: C B E, M: D G S,
                 U: O P N, D: A K); I(Q1) = 1. uç (kollektör/savak/çıkış)
    P(R1)        R1'in gücü (pozitif: tüketir)
    R(A1,D1)     iki nokta arasındaki eşdeğer direnç (kaynaklar söndürülmüş: Thevenin direnci)

Adres yerine düğüm etiketinin adı da yazılabilir: V(OUT), I(VCC,OUT).
Tek argümanlı V bir adres alır, tek argümanlı I ve P bir eleman adı alır; iki argümanlılar adres alır.
R için simülasyon gerekmez: yalnızca dirençten oluşan, toprağı olmayan devrelerde de çalışır.
Yalnızca adres yazmak (C3) V(C3) demektir.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional

from elektro.circuit.model import ADDR_RE, GROUND_NAMES, LABEL_RE, Circuit, CircuitError, parse_addr
from elektro.circuit.solver import OpResult, Sweep, equivalent_resistance
from elektro.i18n import t

PROBE_RE = re.compile(r"^\s*([VIPRvipr])\s*\(\s*([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z])?)\s*"
                      r"(?:[,;]\s*([A-Za-z_][A-Za-z0-9_]*)\s*)?\)\s*$")
UNITS = {"V": "V", "I": "A", "P": "W", "R": "Ω"}


def normalize(text: str) -> str:
    """'c3' → 'V(C3)', 'i( c1 , c10 )' → 'I(C1,C10)'."""
    s = text.strip()
    if ADDR_RE.match(s) or LABEL_RE.match(s):
        return f"V({s.upper()})"
    m = PROBE_RE.match(s)
    if not m:
        raise CircuitError(t("ckt.probe.bad", expr=text))
    func, a, b = m.group(1).upper(), m.group(2).upper(), m.group(3)
    if (func == "P" and b) or (func == "R" and not b) or ("." in a and (func != "I" or b)):
        raise CircuitError(t("ckt.probe.bad", expr=text))
    return f"{func}({a},{b.upper()})" if b else f"{func}({a})"


@dataclass
class Reading:
    expr: str
    value: Optional[float] = None
    unit: str = ""
    error: Optional[str] = None


def _net(circuit: Circuit, nets: Dict, text: str) -> str:
    """Adres (C3) ya da düğüm etiketi adı (OUT) → düğüm. Etiket adı adresten önce gelir."""
    key = text.upper()
    if key in GROUND_NAMES:
        return "0"
    for c in circuit.components:                          # önce düğüm etiketleri (N2 gibi adlar da)
        if c.kind == "N" and c.value.upper() == key:
            return nets[c.pins()[0]]
    point = parse_addr(text)
    net = circuit.net_at(point, nets) if point is not None else None
    if net is None:
        raise CircuitError(t("ckt.probe.no_net", addr=text))
    return net


def _element(result: OpResult, ref: str) -> dict:
    for name, e in result.elements.items():
        if name.upper() == ref:
            return e
    raise CircuitError(t("ckt.probe.no_part", ref=ref))


def current_between(result: OpResult, a: str, b: str) -> Optional[float]:
    """a düğümünden b düğümüne, iki düğümü doğrudan bağlayan elemanlardan geçen toplam akım."""
    total, found = 0.0, False
    for e in result.elements.values():
        if len(e["nodes"]) != 2:                       # transistör/op-amp: uç akımı I(Q1.B) ile
            continue
        n1, n2 = e["nodes"]
        if (n1, n2) == (a, b):
            total, found = total + e["i"], True
        elif (n1, n2) == (b, a):
            total, found = total - e["i"], True
    return total if found else None


def _pin_current(e: dict, ref: str, pin: str) -> float:
    from elektro.circuit.devices import PIN_NAMES
    names = PIN_NAMES.get(e["kind"])
    if not names or pin not in names:
        raise CircuitError(t("ckt.probe.no_pin", ref=ref, pin=pin, pins=" ".join(names or ())))
    k = names.index(pin)
    if "pins" in e:
        return e["pins"][k]
    return e["i"] if k == 0 else -e["i"]                  # iki uçlu: giren = −çıkan


def needs_result(expr: str) -> bool:
    return not expr.strip().upper().startswith("R")


def evaluate(expr: str, circuit: Circuit, result: Optional[OpResult], nets: Optional[Dict] = None) -> float:
    m = PROBE_RE.match(expr)
    if not m:
        raise CircuitError(t("ckt.probe.bad", expr=expr))
    func, a, b = m.group(1).upper(), m.group(2).upper(), m.group(3)
    nets = circuit.nets() if nets is None else nets
    if func == "R":
        na, nb = _net(circuit, nets, a), _net(circuit, nets, b.upper())
        return equivalent_resistance(circuit, na, nb)
    if func == "V":
        va = result.voltages.get(_net(circuit, nets, a), 0.0)
        return va - result.voltages.get(_net(circuit, nets, b.upper()), 0.0) if b else va
    if not b:
        ref, _, pin = a.partition(".")
        e = _element(result, ref)
        if pin:
            return _pin_current(e, ref, pin)
        return e["i"] if func == "I" else e["p"]
    na, nb = _net(circuit, nets, a), _net(circuit, nets, b.upper())
    if na == nb:
        raise CircuitError(t("ckt.probe.same", a=a, b=b.upper()))
    value = current_between(result, na, nb)
    if value is None:
        raise CircuitError(t("ckt.probe.no_path", a=a, b=b.upper()))
    return value


def read_all(circuit: Circuit, result: Optional[OpResult], extra: Optional[List[str]] = None) -> List[Reading]:
    out = []
    for expr in list(circuit.probes) + list(extra or []):
        func = expr.strip()[:1].upper()
        reading = Reading(expr, unit=UNITS.get(func, ""))
        if result is not None or not needs_result(expr):
            try:
                reading.value = evaluate(expr, circuit, result)
            except CircuitError as e:
                reading.error = str(e)
        out.append(reading)
    return out


# --- Analiz eğrileri ---------------------------------------------------------------------------

@dataclass
class Trace:
    expr: str
    unit: str
    values: Optional[list] = None          # gerçel (tran, dc) ya da karmaşık (ac)
    error: Optional[str] = None


def trace_exprs(circuit: Circuit, sweep: Sweep) -> List[str]:
    """Çizilecek ifadeler: probe'lar (R hariç); hiç probe yoksa tüm düğüm gerilimleri."""
    exprs = [e for e in circuit.probes if needs_result(e)]
    if exprs:
        return exprs
    return [f"V({n})" for n in sorted(sweep.voltages) if n != "0"]


def traces(circuit: Circuit, sweep: Sweep, exprs: Optional[List[str]] = None) -> List[Trace]:
    nets = circuit.nets()
    out = []
    for expr in exprs if exprs is not None else trace_exprs(circuit, sweep):
        tr = Trace(expr, UNITS.get(expr[:1].upper(), ""))
        if sweep.kind == "ac" and expr[:1].upper() == "P":
            tr.error = t("ckt.probe.no_ac_power")
            out.append(tr)
            continue
        try:
            tr.values = [evaluate(expr, circuit, sweep.point(k), nets) for k in range(len(sweep.x))]
        except CircuitError as e:
            tr.error = str(e)
        out.append(tr)
    return out
