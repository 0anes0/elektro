"""SPICE netlist'ini (.cir, .sp, .net) elektro devresine çevirir.

Netlist'te konum bilgisi yoktur: elemanlar ızgaraya satır satır dizilir ve kablo yerine her ucuna
düğüm adıyla bir etiket konur (toprak düğümüne GND sembolü). Böylece devre hemen çözülebilir ve
şema editörde elle düzenlenebilir.

Desteklenen satırlar:
    R/C/L  ad n1 n2 değer
    V/I    ad n+ n− [DC x] [AC m [φ]] [SIN(…)|SINE(…)|PULSE(…)]
    D      ad anot katot model
    Q      ad c b e [s] model
    M      ad d g s b model [W=… L=…]
    E      ad out+ out− in+ in− kazanç          (out− toprak ise op-amp olarak)
    .model ad TÜR(parametreler)    .tran  .ac  .dc  .op  .end
Diğer satırlar (.include, .param, X alt devreleri …) atlanır ve uyarı verilir.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

from elektro.circuit.model import LABEL_RE, Circuit, CircuitError
from elektro.i18n import t

SUFFIXES = (".cir", ".sp", ".spi", ".spice", ".net", ".ckt")
_MODEL_RE = re.compile(r"(?i)^\.model\s+(\S+)\s+(\w+)\s*\(?(.*?)\)?\s*$")
_PARAM_RE = re.compile(r"([A-Za-z]+)\s*=\s*([^\s,()]+)")
SUPPORTED = {"D": ("IS", "N", "RS", "BV", "IBV"), "NPN": ("IS", "BF", "BR", "VAF"), "PNP": ("IS", "BF", "BR", "VAF"),
             "NMOS": ("VTO", "KP", "LAMBDA"), "PMOS": ("VTO", "KP", "LAMBDA")}

COLUMNS = 6          # bir satırdaki eleman sayısı
STEP_X, STEP_Y = 6, 5


def is_spice(path: Path) -> bool:
    return Path(path).suffix.lower() in SUFFIXES


def _lines(text: str) -> List[str]:
    """Yorumları atar, '+' ile devam eden satırları birleştirir. İlk satır başlıktır (SPICE kuralı)."""
    out: List[str] = []
    for i, raw in enumerate(text.splitlines()):
        line = raw.split(";", 1)[0].rstrip()
        if i == 0 or not line.strip() or line.lstrip().startswith("*"):
            continue
        if line.lstrip().startswith("+") and out:
            out[-1] += " " + line.lstrip()[1:].strip()
        else:
            out.append(line.strip())
    return out


def _label(node: str) -> str:
    """SPICE düğüm adı → geçerli etiket adı ("1" → "N1", "out-" → "OUT_")."""
    name = re.sub(r"[^A-Za-z0-9_]", "_", node)
    if not name or not name[0].isalpha():
        name = "N" + name
    return name[:16] if LABEL_RE.match(name[:16]) else "N_" + name[:14]


def _model_value(kind: str, name: str, models: Dict[str, Tuple[str, Dict[str, str]]], warnings: List[str]) -> str:
    """Eleman satırındaki model adı → elektro değer yazımı."""
    from elektro.circuit.devices import LIBRARY
    key = name.upper()
    if key in models:
        typ, params = models[key]
        allowed = SUPPORTED.get(typ, ())
        dropped = [p for p in params if p not in allowed]
        if dropped:
            warnings.append(t("spice.dropped", model=name, params=" ".join(dropped)))
        body = " ".join(f"{k}={v}" for k, v in params.items() if k in allowed)
        prefix = "" if typ == "D" else typ
        return f"{prefix} {body}".strip() or ("D" if typ == "D" else typ)
    if key in LIBRARY:
        return key
    for lib in LIBRARY:                                   # D1N4148 → 1N4148, Q2N2222 → 2N2222
        if key.endswith(lib):
            return lib
    warnings.append(t("spice.unknown_model", model=name))
    return {"D": "D", "Q": "NPN", "M": "NMOS"}[kind]


def parse_spice(text: str) -> Tuple[Circuit, List[str]]:
    from elektro.circuit.sources import parse_directive, parse_source
    warnings: List[str] = []
    lines = _lines(text)
    models: Dict[str, Tuple[str, Dict[str, str]]] = {}
    for line in lines:
        m = _MODEL_RE.match(line)
        if m:
            typ = m.group(2).upper()
            params = {k.upper(): v for k, v in _PARAM_RE.findall(m.group(3))}
            models[m.group(1).upper()] = (typ, params)

    elements: List[Tuple[str, str, str, List[str]]] = []      # (tür, ad, değer, düğümler)
    analysis = ""
    for line in lines:
        tok = line.split()
        head = tok[0].upper()
        if head.startswith("."):
            if head in (".TRAN", ".AC", ".DC", ".OP"):
                try:
                    analysis = parse_directive(line).directive()
                    if analysis == ".op":
                        analysis = ""
                except CircuitError:
                    warnings.append(t("spice.skipped", line=line))
            elif head not in (".MODEL", ".END", ".ENDS"):
                warnings.append(t("spice.skipped", line=line))
            continue
        kind = head[0]
        try:
            if kind in "RCL" and len(tok) >= 4:
                elements.append((kind, tok[0], tok[3], tok[1:3]))
            elif kind in "VI" and len(tok) >= 3:
                value = " ".join(tok[3:]) or "0"
                parse_source(value)                               # geçerli mi?
                elements.append((kind, tok[0], value, tok[1:3]))
            elif kind == "D" and len(tok) >= 4:
                elements.append(("D", tok[0], _model_value("D", tok[3], models, warnings), tok[1:3]))
            elif kind == "Q" and len(tok) >= 5:
                model = tok[5] if len(tok) >= 6 and tok[5].upper() in models else tok[4]
                elements.append(("Q", tok[0], _model_value("Q", model, models, warnings), tok[1:4]))
            elif kind == "M" and len(tok) >= 6:
                elements.append(("M", tok[0], _model_value("M", tok[5], models, warnings), tok[1:4]))
            elif kind == "E" and len(tok) >= 6 and tok[2] in ("0", "gnd", "GND"):
                elements.append(("U", tok[0], f"ideal A={tok[5]}", [tok[1], tok[3], tok[4]]))
            else:
                warnings.append(t("spice.skipped", line=line))
        except CircuitError as e:
            warnings.append(f"{tok[0]}: {e}")
    if not elements:
        raise CircuitError(t("spice.empty"))
    return layout(elements, analysis), warnings


def layout(elements, analysis: str) -> Circuit:
    """Elemanları ızgaraya diz; her uca düğüm etiketi (toprakta GND sembolü) koy."""
    circuit = Circuit(analysis=analysis)
    used = set()
    for k, (kind, name, value, nodes) in enumerate(elements):
        col, row = k % COLUMNS, k // COLUMNS
        x, y = 2 + col * STEP_X, 1 + row * STEP_Y
        if kind in ("Q", "M"):
            comp = circuit.add(kind, x + 1, y + 1, value=value)
        elif kind == "U":
            comp = circuit.add(kind, x + 1, y + 1, value=value)
        else:
            comp = circuit.add(kind, x, y, rot=90, value=value)
        ref = name.upper()
        if ref[0] != kind and kind != "U":
            ref = kind + ref
        if kind == "U":
            ref = "U" + ref[1:] if len(ref) > 1 else "U1"
        if ref not in used:                                       # SPICE adını koru (R1, Q2 …)
            comp.ref = ref
        used.add(comp.ref)
        for pin, node in zip(comp.pins(), nodes):
            if node.upper() in ("0", "GND"):
                circuit.add("GND", *pin)
            else:
                label = circuit.add("N", *pin, value=_label(node))
                label.rot = 0 if pin[0] >= comp.x else 180
    return circuit


def load_spice(path: Path) -> Tuple[Circuit, List[str]]:
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        raise CircuitError(str(e))
    return parse_spice(text)
