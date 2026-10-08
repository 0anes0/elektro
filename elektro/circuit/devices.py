"""Doğrusal olmayan elemanlar: diyot, BJT, MOSFET, op-amp. Model kütüphanesi ve Newton-Raphson için
doğrusallaştırma (her elemanın uç akımları ve bunların uç gerilimlerine göre türevleri).

Değer yazımı:
    D:  1N4148 · 1N4007 · 1N5819 · LED · LED-GREEN · LED-BLUE · BZX5V1 · IS=1e-14 N=1.8 RS=1 BV=5.1
    Q:  2N2222 · BC547 · 2N3904 (NPN) · 2N3906 · BC557 (PNP) · NPN BF=200 · PNP IS=1e-14
    M:  2N7000 · IRFZ44N (N kanal) · BS250 · IRF9540 (P kanal) · NMOS VTO=2 KP=0.5
    U:  ideal · LM358 · TL072 · LM741, isteğe bağlı çıkış sınırı: ±15, 0..5   (ör. "TL072 ±15")
Model adından sonra parametre yazılarak değiştirilebilir: "2N2222 BF=150".

Modeller: diyot Shockley (+ seri direnç, ters kırılma); BJT Ebers-Moll taşıma modeli (+ Early
etkisi); MOSFET seviye-1 kare yasası (+ kanal boyu modülasyonu); op-amp tek kutuplu kazanç
(GBW) ve yumuşak çıkış sınırı. Gövde diyotu ve jonksiyon kapasiteleri yoktur.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from elektro.i18n import t

VT = 0.025852          # termal gerilim, 300 K
GMIN = 1e-12
EXP_MAX = 80.0

# Model adı → (tür, parametreler). Değerler üretici SPICE modellerinden sadeleştirilmiştir.
LIBRARY: Dict[str, Tuple[str, Dict[str, float]]] = {
    # diyotlar
    "1N4148": ("D", {"IS": 2.52e-9, "N": 1.752, "RS": 0.568, "BV": 100, "IBV": 100e-6}),
    "1N4007": ("D", {"IS": 7.02e-9, "N": 1.808, "RS": 0.034, "BV": 1000, "IBV": 5e-6}),
    "1N5819": ("D", {"IS": 3.0e-6, "N": 1.05, "RS": 0.05, "BV": 40, "IBV": 1e-3}),
    "LED": ("D", {"IS": 1e-18, "N": 2.0, "RS": 5, "BV": 5, "IBV": 10e-6}),
    "LED-RED": ("D", {"IS": 1e-18, "N": 2.0, "RS": 5, "BV": 5, "IBV": 10e-6}),
    "LED-GREEN": ("D", {"IS": 3.5e-21, "N": 2.0, "RS": 5, "BV": 5, "IBV": 10e-6}),
    "LED-BLUE": ("D", {"IS": 7.6e-23, "N": 2.5, "RS": 5, "BV": 5, "IBV": 10e-6}),
    "LED-WHITE": ("D", {"IS": 7.6e-23, "N": 2.5, "RS": 5, "BV": 5, "IBV": 10e-6}),
    "BZX5V1": ("D", {"IS": 1e-14, "N": 1.0, "RS": 1, "BV": 5.1, "IBV": 1e-3}),
    "BZX3V3": ("D", {"IS": 1e-14, "N": 1.0, "RS": 1, "BV": 3.3, "IBV": 1e-3}),
    "BZX12": ("D", {"IS": 1e-14, "N": 1.0, "RS": 1, "BV": 12, "IBV": 1e-3}),
    # BJT
    "2N2222": ("NPN", {"IS": 14.34e-15, "BF": 255.9, "BR": 6.092, "VAF": 74.03}),
    "2N3904": ("NPN", {"IS": 6.734e-15, "BF": 416.4, "BR": 0.7371, "VAF": 74.03}),
    "BC547": ("NPN", {"IS": 7.05e-15, "BF": 290, "BR": 7.5, "VAF": 62.8}),
    "2N3906": ("PNP", {"IS": 1.41e-15, "BF": 180.7, "BR": 4.977, "VAF": 18.7}),
    "BC557": ("PNP", {"IS": 1.0e-14, "BF": 250, "BR": 3.0, "VAF": 40}),
    # MOSFET (KP: A/V², W/L dahil)
    "2N7000": ("NMOS", {"VTO": 2.0, "KP": 0.32, "LAMBDA": 0.01}),
    "IRFZ44N": ("NMOS", {"VTO": 3.0, "KP": 10.0, "LAMBDA": 0.005}),
    "BS250": ("PMOS", {"VTO": -2.5, "KP": 0.2, "LAMBDA": 0.01}),
    "IRF9540": ("PMOS", {"VTO": -3.0, "KP": 5.0, "LAMBDA": 0.005}),
    # op-amp (A: açık çevrim kazancı, GBW: kazanç-bant genişliği)
    "IDEAL": ("OPAMP", {"A": 1e6, "GBW": 0.0}),
    "LM358": ("OPAMP", {"A": 1e5, "GBW": 1e6}),
    "LM741": ("OPAMP", {"A": 2e5, "GBW": 1e6}),
    "TL072": ("OPAMP", {"A": 2e5, "GBW": 3e6}),
}
GENERIC = {"D": ("D", {"IS": 1e-14, "N": 1.0, "RS": 0.0, "BV": 0.0, "IBV": 1e-3}),
           "NPN": ("NPN", {"IS": 1e-14, "BF": 100, "BR": 1, "VAF": 0.0}),
           "PNP": ("PNP", {"IS": 1e-14, "BF": 100, "BR": 1, "VAF": 0.0}),
           "NMOS": ("NMOS", {"VTO": 1.0, "KP": 0.1, "LAMBDA": 0.0}),
           "PMOS": ("PMOS", {"VTO": -1.0, "KP": 0.1, "LAMBDA": 0.0})}
DEFAULT = {"D": "D", "Q": "NPN", "M": "NMOS", "U": "IDEAL"}
FAMILY = {"D": ("D",), "Q": ("NPN", "PNP"), "M": ("NMOS", "PMOS"), "U": ("OPAMP",)}
PIN_NAMES = {"D": ("A", "K"), "Q": ("C", "B", "E"), "M": ("D", "G", "S"), "U": ("O", "P", "N")}

_RAIL_RE = re.compile(r"^(?:±|\+-|\+/-)(\S+)$|^(\S+?)\.\.(\S+)$")


@dataclass
class Model:
    name: str
    type: str                       # D | NPN | PNP | NMOS | PMOS | OPAMP
    params: Dict[str, float] = field(default_factory=dict)
    vmin: Optional[float] = None    # op-amp çıkış sınırları
    vmax: Optional[float] = None


def models_for(kind: str) -> List[str]:
    return [name for name, (typ, _) in LIBRARY.items() if typ in FAMILY[kind] and name != "LED-RED"]


def parse_model(kind: str, text: str) -> Model:
    """'2N2222 BF=150' → Model. Hatalıysa CircuitError."""
    from elektro.circuit.model import CircuitError
    from elektro.circuit.sources import _num
    tokens = text.replace(",", " ").split()
    if not tokens:
        tokens = [DEFAULT[kind]]
    first = tokens[0].upper()
    if first in LIBRARY and LIBRARY[first][0] in FAMILY[kind]:
        typ, params = LIBRARY[first]
        name, rest = first, tokens[1:]
    elif first in GENERIC and first in FAMILY[kind]:
        typ, params = GENERIC[first]
        name, rest = first, tokens[1:]
    elif "=" in tokens[0] or _RAIL_RE.match(tokens[0]):
        typ, params = GENERIC.get(DEFAULT[kind]) or LIBRARY[DEFAULT[kind]]
        name, rest = DEFAULT[kind], tokens
    else:
        raise CircuitError(t("dev.unknown", name=tokens[0], options=", ".join(models_for(kind))))
    model = Model(name, typ, dict(params))
    for tok in rest:
        m = _RAIL_RE.match(tok)
        if m and typ == "OPAMP":
            if m.group(1):
                v = abs(_num(m.group(1)))
                model.vmin, model.vmax = -v, v
            else:
                model.vmin, model.vmax = _num(m.group(2)), _num(m.group(3))
            if model.vmax <= model.vmin:
                raise CircuitError(t("dev.bad_rail", text=tok))
            continue
        if "=" not in tok:
            raise CircuitError(t("dev.bad_param", text=tok))
        key, val = tok.split("=", 1)
        key = key.upper()
        if key not in model.params:
            raise CircuitError(t("dev.bad_param", text=tok))
        model.params[key] = _num(val)
    p = model.params
    if typ == "D" and (p["IS"] <= 0 or p["N"] <= 0 or p["RS"] < 0 or p["BV"] < 0):
        raise CircuitError(t("dev.bad_param", text=text))
    if typ in ("NPN", "PNP") and (p["IS"] <= 0 or p["BF"] <= 0 or p["BR"] <= 0 or p["VAF"] < 0):
        raise CircuitError(t("dev.bad_param", text=text))
    if typ in ("NMOS", "PMOS") and (p["KP"] <= 0 or p["LAMBDA"] < 0):
        raise CircuitError(t("dev.bad_param", text=text))
    if typ == "OPAMP" and (p["A"] <= 0 or p["GBW"] < 0):
        raise CircuitError(t("dev.bad_param", text=text))
    return model


# --- yardımcılar --------------------------------------------------------------------------------

def _exp(x: float) -> Tuple[float, float]:
    """exp(x) ve türevi; büyük x'te taşmasın diye doğrusal devam eder."""
    if x > EXP_MAX:
        e = math.exp(EXP_MAX)
        return e * (1 + x - EXP_MAX), e
    e = math.exp(x)
    return e, e


def pnjlim(vnew: float, vold: float, nvt: float, vcrit: float) -> float:
    """SPICE jonksiyon gerilimi sınırlaması: Newton adımları üstel bölgede patlamasın."""
    if vnew > vcrit and abs(vnew - vold) > 2 * nvt:
        if vold > 0:
            arg = 1 + (vnew - vold) / nvt
            vnew = vold + nvt * math.log(arg) if arg > 0 else vcrit
        else:
            vnew = nvt * math.log(vnew / nvt)
    return vnew


def _softplus(z: float) -> Tuple[float, float]:
    """log(1 + eᶻ) ve türevi (lojistik fonksiyon), taşmasız."""
    if z > 40:
        return z, 1.0
    if z < -40:
        return 0.0, 0.0
    e = math.exp(z)
    return math.log1p(e), e / (1 + e)


def _vcrit(nvt: float, isat: float) -> float:
    return nvt * math.log(nvt / (math.sqrt(2) * isat))


# --- elemanlar ----------------------------------------------------------------------------------

class Device:
    """Uçları düğüm adlarıdır. linearize(v) → (uçlardan elemana giren akımlar, dI/dV matrisi)."""

    ref: str
    nodes: Tuple[str, ...]
    limited = False

    def linearize(self, v: List[float]) -> Tuple[List[float], List[List[float]]]:
        raise NotImplementedError

    def currents(self, v: List[float]) -> List[float]:
        """Sınırlama uygulamadan, verilen gerilimlerdeki uç akımları."""
        raise NotImplementedError


class Diode(Device):
    def __init__(self, ref: str, anode: str, cathode: str, model: Model):
        p = model.params
        self.ref, self.nodes = ref, (anode, cathode)
        self.isat, self.nvt, self.bv, self.ibv = p["IS"], p["N"] * VT, p["BV"], p["IBV"]
        self.vcrit = _vcrit(self.nvt, self.isat)
        self.vd = 0.0

    def _iv(self, vd: float) -> Tuple[float, float]:
        e, de = _exp(vd / self.nvt)
        i = self.isat * (e - 1) + GMIN * vd
        g = self.isat * de / self.nvt + GMIN
        if self.bv:                                      # ters kırılma (zener)
            eb, deb = _exp(-(vd + self.bv) / VT)
            i -= self.ibv * eb
            g += self.ibv * deb / VT
        return i, g

    def linearize(self, v):
        vd = v[0] - v[1]
        new = pnjlim(vd, self.vd, self.nvt, self.vcrit)
        if self.bv and vd < -self.bv * 0.5:              # kırılma yönünde de sınırla
            new = -self.bv - pnjlim(-vd - self.bv, -self.vd - self.bv, VT, _vcrit(VT, self.ibv))
        self.limited = abs(new - vd) > 1e-9
        self.vd = new
        i, g = self._iv(new)
        ieq = i - g * new                                # i(v) ≈ ieq + g·v (v = va − vk)
        # akım anottan girer, katottan çıkar
        return [ieq + g * (v[0] - v[1]), -(ieq + g * (v[0] - v[1]))], [[g, -g], [-g, g]]

    def currents(self, v):
        i, _ = self._iv(v[0] - v[1])
        return [i, -i]


class BJT(Device):
    """Ebers-Moll taşıma modeli; uçlar: C, B, E."""

    def __init__(self, ref: str, c: str, b: str, e: str, model: Model):
        p = model.params
        self.ref, self.nodes = ref, (c, b, e)
        self.sign = 1.0 if model.type == "NPN" else -1.0
        self.isat, self.bf, self.br, self.vaf = p["IS"], p["BF"], p["BR"], p["VAF"]
        self.vcrit = _vcrit(VT, self.isat)
        self.vbe = self.vbc = 0.0

    def _eval(self, vbe: float, vbc: float):
        ef, def_ = _exp(vbe / VT)
        er, der = _exp(vbc / VT)
        i_f, i_r = self.isat * (ef - 1), self.isat * (er - 1)
        gf, gr = self.isat * def_ / VT, self.isat * der / VT
        kq, dkq = 1.0, 0.0                               # Early etkisi: (1 − Vbc/VAF)
        if self.vaf and 1 - vbc / self.vaf > 0.05:
            kq, dkq = 1 - vbc / self.vaf, -1 / self.vaf
        elif self.vaf:
            kq = 0.05
        ic = (i_f - i_r) * kq - i_r / self.br
        ib = i_f / self.bf + i_r / self.br + GMIN * vbe + GMIN * vbc
        dic_be = gf * kq
        dic_bc = -gr * kq + (i_f - i_r) * dkq - gr / self.br
        dib_be = gf / self.bf + GMIN
        dib_bc = gr / self.br + GMIN
        return ic, ib, dic_be, dic_bc, dib_be, dib_bc

    def _terminal(self, vbe, vbc):
        ic, ib, dic_be, dic_bc, dib_be, dib_bc = self._eval(vbe, vbc)
        ie = -(ic + ib)
        # dX/dvc = −dX/dvbc, dX/dvb = dX/dvbe + dX/dvbc, dX/dve = −dX/dvbe
        jc = [-dic_bc, dic_be + dic_bc, -dic_be]
        jb = [-dib_bc, dib_be + dib_bc, -dib_be]
        je = [-(jc[k] + jb[k]) for k in range(3)]
        return [ic, ib, ie], [jc, jb, je]

    def linearize(self, v):
        s = self.sign
        vbe, vbc = s * (v[1] - v[2]), s * (v[1] - v[0])
        nbe = pnjlim(vbe, self.vbe, VT, self.vcrit)
        nbc = pnjlim(vbc, self.vbc, VT, self.vcrit)
        self.limited = abs(nbe - vbe) > 1e-9 or abs(nbc - vbc) > 1e-9
        self.vbe, self.vbc = nbe, nbc
        cur, jac = self._terminal(nbe, nbc)
        # Sınırlanmış noktada doğrusallaştır, gerçek uç gerilimlerine taşı (E'ye göre; akımlar
        # yalnızca gerilim farklarına bağlı olduğundan referans seçimi sonucu değiştirmez).
        vlim = [nbe - nbc, nbe, 0.0]
        vreal = [s * (v[k] - v[2]) for k in range(3)]
        out = []
        for k in range(3):
            i = cur[k] + sum(jac[k][j] * (vreal[j] - vlim[j]) for j in range(3))
            out.append(s * i)
        return out, jac                                   # PNP: iki işaret değişimi türevde birbirini götürür

    def currents(self, v):
        s = self.sign
        cur, _ = self._terminal(s * (v[1] - v[2]), s * (v[1] - v[0]))
        return [s * c for c in cur]


class MOSFET(Device):
    """Seviye-1 (kare yasası) MOSFET; uçlar: D, G, S (gövde kaynağa bağlı)."""

    def __init__(self, ref: str, d: str, g: str, s: str, model: Model):
        p = model.params
        self.ref, self.nodes = ref, (d, g, s)
        self.sign = 1.0 if model.type == "NMOS" else -1.0
        self.vto, self.kp, self.lam = self.sign * p["VTO"], p["KP"], p["LAMBDA"]
        self.vgs = self.vds = 0.0

    def _ids(self, vgs: float, vds: float):
        """vds ≥ 0 için savak akımı ve türevleri (gm, gds)."""
        vov = vgs - self.vto
        if vov <= 0:
            return 0.0, 0.0, 0.0
        clm = 1 + self.lam * vds
        if vds < vov:
            core = vov * vds - vds * vds / 2
            return self.kp * core * clm, self.kp * vds * clm, self.kp * (vov - vds) * clm + self.kp * core * self.lam
        return self.kp / 2 * vov * vov * clm, self.kp * vov * clm, self.kp / 2 * vov * vov * self.lam

    def _terminal(self, vd, vg, vs):
        if vd >= vs:
            i, gm, gds = self._ids(vg - vs, vd - vs)
            cur = [i, 0.0, -i]
            jd = [gds, gm, -(gm + gds)]
        else:                                             # savak ve kaynak yer değiştirir
            i, gm, gds = self._ids(vg - vd, vs - vd)
            cur = [-i, 0.0, i]
            jd = [gm + gds, -gm, -gds]
        cur[0] += GMIN * (vd - vs)
        cur[2] -= GMIN * (vd - vs)
        jd = [jd[0] + GMIN, jd[1], jd[2] - GMIN]
        return cur, [jd, [0.0, 0.0, 0.0], [-x for x in jd]]

    def linearize(self, v):
        s = self.sign
        vd, vg, vs = (s * x for x in v)
        vgs, vds = vg - vs, vd - vs
        # basit sınırlama: bir adımda kapı-kaynak gerilimi en fazla 0.5 V değişsin
        if abs(vgs - self.vgs) > 0.5 and vgs > self.vto:
            vgs = self.vgs + math.copysign(0.5, vgs - self.vgs)
        if abs(vds - self.vds) > 2.0:
            vds = self.vds + math.copysign(2.0, vds - self.vds)
        self.limited = abs(vgs - (vg - vs)) > 1e-9 or abs(vds - (vd - vs)) > 1e-9
        self.vgs, self.vds = vgs, vds
        lim = [vs + vds, vs + vgs, vs]
        cur, jac = self._terminal(*lim)
        real = [vd, vg, vs]
        out = [s * (cur[k] + sum(jac[k][j] * (real[j] - lim[j]) for j in range(3))) for k in range(3)]
        return out, jac

    def currents(self, v):
        s = self.sign
        cur, _ = self._terminal(*(s * x for x in v))
        return [s * c for c in cur]


class OpAmp:
    """Op-amp: V(çıkış) = sınır(u), u = A·(V+ − V−) ya da kutup düğümünün gerilimi (GBW varsa).

    Çıkış, toprağa göre gerilim kaynağı gibi bir akım değişkeniyle yazılır. Sınırlar içinde çıkış
    tam doğrusaldır; yalnızca raylara ~50 mV kala köşeler yuvarlanır (softplus), böylece Newton
    türevi her yerde tanımlıdır.
    """

    def __init__(self, ref: str, out: str, inp: str, inn: str, model: Model):
        p = model.params
        self.ref = ref
        self.out, self.inp, self.inn = out, inp, inn
        self.gain, self.gbw = p["A"], p["GBW"]
        self.vmin, self.vmax = model.vmin, model.vmax
        self.pole = f"{ref}:p" if self.gbw else None     # iç düğüm
        self.u = 0.0
        self.k = 1.0
        self.limited = False

    def drive(self) -> List[Tuple[str, float]]:
        """u'yu oluşturan düğümler ve katsayıları."""
        if self.pole:
            return [(self.pole, 1.0)]
        return [(self.inp, self.gain), (self.inn, -self.gain)]

    def clamp(self, u: float) -> Tuple[float, float]:
        if self.vmin is None:
            return u, 1.0
        w = 0.05
        sp_hi, sg_hi = _softplus((u - self.vmax) / w)
        sp_lo, sg_lo = _softplus((self.vmin - u) / w)
        return u - w * sp_hi + w * sp_lo, max(1 - sg_hi - sg_lo, 0.0)

    def windup(self, vp: float) -> Tuple[float, float]:
        """Kutup düğümünün sınırların biraz dışında tutulması (doyumdan hızlı çıkış).

        Gerçek op-amp'ın iç katı da beslemeye dayanır; bu olmadan kutup düğümü doyumda
        A·Vd'ye kadar şişer ve çıkış milisaniyelerce takılı kalırdı. Yumuşak (softplus) bir
        akım düğümden çekilir: sınır içinde etkisiz, dışında büyük iletkenlik.
        """
        if self.vmin is None or not self.pole:
            return 0.0, 0.0
        hi, lo, w, g = self.vmax + 0.5, self.vmin - 0.5, 0.05, 10 * self.gain
        sp_hi, sg_hi = _softplus((vp - hi) / w)
        sp_lo, sg_lo = _softplus((lo - vp) / w)
        return g * w * (sp_hi - sp_lo), g * (sg_hi + sg_lo)

    def pole_values(self) -> Tuple[float, float]:
        """Kutup düğümü: g·(V+ − V−) akımı, 1 Ω'a ve C'ye akar → A = g·1 Ω, fp = GBW/A."""
        fp = self.gbw / self.gain
        return self.gain, 1 / (2 * math.pi * fp)


def make_device(comp, pins: Tuple[str, ...]):
    """Bileşenden eleman nesnesi."""
    model = parse_model(comp.kind, comp.value)
    if comp.kind == "D":
        return Diode(comp.ref, pins[0], pins[1], model), model
    if comp.kind == "Q":
        return BJT(comp.ref, *pins, model), model
    if comp.kind == "M":
        return MOSFET(comp.ref, *pins, model), model
    return OpAmp(comp.ref, *pins, model), model


def spice_model(comp) -> Tuple[str, Optional[str]]:
    """SPICE satırındaki model adı ve .model satırı."""
    from elektro.circuit.model import spice_number
    model = parse_model(comp.kind, comp.value)
    name = f"{comp.ref}_{model.name}".replace("-", "_")
    spice_type = {"D": "D", "NPN": "NPN", "PNP": "PNP", "NMOS": "NMOS", "PMOS": "PMOS"}.get(model.type)
    if spice_type is None:
        return name, None
    params = dict(model.params)
    if model.type == "D" and not params.get("BV"):
        params.pop("BV", None)
        params.pop("IBV", None)
    body = " ".join(f"{k}={spice_number(v)}" for k, v in params.items() if v or k in ("VTO",))
    return name, f".model {name} {spice_type}({body})"
