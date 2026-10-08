"""Düğüm gerilimi analizi (Modified Nodal Analysis): DC çalışma noktası, transient, AC, DC tarama.

DC çalışma noktası: kondansatör açık devre, bobin kısa devre (0 V kaynak) sayılır.
Her düğümden toprağa çok küçük bir iletkenlik (GMIN) eklenir; böylece yalnızca kondansatörle
bağlı düğümler tekil matris yerine 0 V'ta kalır (SPICE de böyle yapar).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from elektro.circuit.model import Circuit, CircuitError
from elektro.i18n import t

GMIN = 1e-12


def _scales(a: List[list]):
    """Tekillik eşiği için satır ve sütun büyüklükleri.

    Eşik, pivotun kendi satırının ve sütununun küçüğüne göre alınır: op-amp kazancı (1e6) gibi
    büyük katsayılar, boşta kalan bir girişin GMIN'li (1e-12) satırını "tekil" göstermesin.
    Gerçek tekillik (gerilim kaynağı döngüsü) sıfıra çok yakın bir pivot verir ve yine yakalanır.
    """
    n = len(a)
    cols = [max((abs(a[r][c]) for r in range(n)), default=1.0) or 1.0 for c in range(n)]
    rows = [max((abs(v) for v in row), default=1.0) or 1.0 for row in a]
    return rows, cols


def solve(a: List[list], b: list) -> list:
    """Kısmi pivotlamalı Gauss eliminasyonu (gerçel veya karmaşık)."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    rows, cols = _scales(a)
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[pivot][col]) < min(rows[pivot], cols[col]) * 1e-13:
            raise CircuitError(t("ckt.singular"))
        m[col], m[pivot] = m[pivot], m[col]
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(col + 1, n):
            f = m[r][col] / m[col][col]
            if f:
                for c in range(col, n + 1):
                    m[r][c] -= f * m[col][c]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][c] * x[c] for c in range(r + 1, n))) / m[r][r]
    return x


@dataclass
class OpResult:
    voltages: Dict[str, float]                       # düğüm → V ("0" dahil)
    elements: Dict[str, dict] = field(default_factory=dict)   # ref → {v, i, p}
    warnings: List[str] = field(default_factory=list)


def check(circuit: Circuit) -> List[str]:
    """Simülasyondan önce yapı kontrolü; uyarı listesi döner, ciddi hatada CircuitError."""
    parts = [c for c in circuit.components if c.is_part]
    if not parts:
        raise CircuitError(t("ckt.empty"))
    nets = circuit.nets()
    if "0" not in nets.values():                          # GND sembolü ya da "GND" etiketi
        raise CircuitError(t("ckt.no_ground"))
    count: Dict[str, int] = {}
    for c in circuit.components:
        if c.is_part or c.kind == "N":                # etiketlenmiş çıkış bilerek açık bırakılmıştır
            for p in c.pins():
                count[nets[p]] = count.get(nets[p], 0) + 1
    warnings = []
    for c in parts:
        names = [nets[p] for p in c.pins()]
        if len(set(names)) == 1:
            warnings.append(t("ckt.shorted", ref=c.ref))
        for n in names:
            if count[n] == 1 and n != "0":
                warnings.append(t("ckt.open_pin", ref=c.ref))
                break
    return warnings


MAX_NEWTON = 150


class System:
    """Devrenin MNA yapısı.

    Değişkenler: düğüm gerilimleri (dış düğümler + elemanların iç düğümleri, ör. "D1:a") ve
    akımı bilinmeyen dallar (gerilim kaynağı, bobin, op-amp çıkışı). Doğrusal kısım bir kez
    yazılır; diyot/transistör gibi elemanlar her Newton adımında yeniden doğrusallaştırılır.
    """

    def __init__(self, circuit: Circuit):
        from elektro.circuit.devices import OpAmp, make_device
        from elektro.circuit.sources import parse_source
        self.warnings = check(circuit)
        nets = circuit.nets()
        self.parts = [c for c in circuit.components if c.is_part]
        self.pins = {c.ref: tuple(nets[p] for p in c.pins()) for c in self.parts}
        external = {n for c in self.parts for n in self.pins[c.ref]} - {"0"}
        self.values: Dict[str, float] = {}
        self.sources = {}
        self.devices = []                     # diyot, BJT, MOSFET
        self.opamps = {}
        self.res: List[tuple] = []            # (n1, n2, iletkenlik)
        self.caps: List[tuple] = []           # (anahtar, n1, n2, C)
        self.vccs: List[tuple] = []           # (çıkış düğümü, n+, n−, g): g·(V+ − V−) çıkış düğümüne akar
        internal = []
        for c in self.parts:
            n = self.pins[c.ref]
            try:
                if c.kind in ("V", "I"):
                    self.sources[c.ref] = parse_source(c.value)
                elif c.kind in ("D", "Q", "M", "U"):
                    dev, model = make_device(c, n)
                    if isinstance(dev, OpAmp):
                        self.opamps[c.ref] = dev
                        if dev.pole:
                            gain, cap = dev.pole_values()
                            internal.append(dev.pole)
                            self.vccs.append((dev.pole, dev.inp, dev.inn, gain))
                            self.res.append((dev.pole, "0", 1.0))
                            self.caps.append((dev.pole, dev.pole, "0", cap))
                    else:
                        rs = model.params.get("RS", 0.0) if c.kind == "D" else 0.0
                        if rs > 0:                # seri direnç: iç düğüm üzerinden
                            inner = f"{c.ref}:a"
                            internal.append(inner)
                            self.res.append((n[0], inner, 1 / rs))
                            dev.nodes = (inner, n[1])
                        self.devices.append(dev)
                else:
                    self.values[c.ref] = c.number()
            except ValueError as e:
                raise CircuitError(f"{c.ref}: {e}")
            if c.kind in ("R", "C", "L") and self.values[c.ref] <= 0:
                raise CircuitError(t("ckt.bad_value", ref=c.ref))
            if c.kind == "R":
                self.res.append((n[0], n[1], 1 / self.values[c.ref]))
            elif c.kind == "C":
                self.caps.append((c.ref, n[0], n[1], self.values[c.ref]))
        self.nodes = sorted(external) + internal
        self.index = {name: i for i, name in enumerate(self.nodes)}
        self.branches = [c for c in self.parts if c.kind in ("V", "L", "U")]   # akımı bilinmeyenler
        self.row = {c.ref: len(self.nodes) + k for k, c in enumerate(self.branches)}
        self.size = len(self.nodes) + len(self.branches)
        self.nonlinear = bool(self.devices) or any(op.vmin is not None for op in self.opamps.values())

    # --- yazım yardımcıları ---
    def matrix(self, zero=0.0) -> List[list]:
        a = [[zero] * self.size for _ in range(self.size)]
        for n in self.nodes:
            a[self.index[n]][self.index[n]] += GMIN
        return a

    def stamp_g(self, a, n1: str, n2: str, g) -> None:
        i, j = self.index.get(n1), self.index.get(n2)
        if i is not None:
            a[i][i] += g
        if j is not None:
            a[j][j] += g
        if i is not None and j is not None:
            a[i][j] -= g
            a[j][i] -= g

    def stamp_branch(self, a, ref: str) -> None:
        """V/L/op-amp akım değişkeni: akım 1. uçtan elemanın içinden 2. uca (op-amp: çıkıştan toprağa)."""
        n1, n2 = (self.pins[ref][0], "0") if ref in self.opamps else self.pins[ref]
        row = self.row[ref]
        if n1 in self.index:
            a[self.index[n1]][row] += 1
            if ref not in self.opamps:
                a[row][self.index[n1]] += 1
        if n2 in self.index:
            a[self.index[n2]][row] -= 1
            a[row][self.index[n2]] -= 1

    def inject(self, b, n1: str, n2: str, current) -> None:
        """Akım n1'den kaynağın içinden n2'ye (n1'den çekilir, n2'ye verilir)."""
        if n1 in self.index:
            b[self.index[n1]] -= current
        if n2 in self.index:
            b[self.index[n2]] += current

    def stamp_linear(self, a) -> None:
        """Dirençler, bağımlı kaynaklar ve dal değişkenlerinin KCL sütunları."""
        for n1, n2, g in self.res:
            self.stamp_g(a, n1, n2, g)
        for out, np_, nn, g in self.vccs:
            i = self.index[out]
            if np_ in self.index:
                a[i][self.index[np_]] -= g
            if nn in self.index:
                a[i][self.index[nn]] += g
        for c in self.branches:
            self.stamp_branch(a, c.ref)

    def stamp_devices(self, a, b, x) -> bool:
        """Doğrusal olmayan elemanları x noktasında doğrusallaştırıp yazar; sınırlama oldu mu?"""
        limited = False
        for dev in self.devices:
            v = [x[self.index[n]] if n in self.index else 0.0 for n in dev.nodes]
            cur, jac = dev.linearize(v)
            limited |= dev.limited
            for k, nk in enumerate(dev.nodes):
                ik = self.index.get(nk)
                if ik is None:
                    continue
                rhs = cur[k]
                for j, nj in enumerate(dev.nodes):
                    ij = self.index.get(nj)
                    if ij is not None:
                        a[ik][ij] += jac[k][j]
                    rhs -= jac[k][j] * v[j]
                b[ik] -= rhs
        for ref, op in self.opamps.items():
            if op.pole and op.vmin is not None:
                ip = self.index[op.pole]
                i, g = op.windup(x[ip])
                a[ip][ip] += g
                b[ip] -= i - g * x[ip]
            row = self.row[ref]
            terms = op.drive()
            u = sum(w * (x[self.index[n]] if n in self.index else 0.0) for n, w in terms)
            y, k = op.clamp(u)
            op.u, op.k = u, k
            a[row][self.index[op.out]] += 1 if op.out in self.index else 0
            for n, w in terms:
                if n in self.index:
                    a[row][self.index[n]] -= k * w
            b[row] += y - k * u
        return limited

    def voltages(self, x) -> Dict[str, float]:
        zero = 0.0 * (x[0] if x else 0.0)
        return {"0": zero, **{n: x[self.index[n]] for n in self.nodes if ":" not in n}}

    # --- Newton-Raphson ---
    def newton(self, base_a, base_b, x0) -> List[float]:
        if not self.nonlinear:
            a = [row[:] for row in base_a]
            b = list(base_b)
            self.stamp_devices(a, b, x0)               # op-amp çıkış denklemi (doğrusal)
            return solve(a, b)
        x = list(x0)
        loose_since = None
        for it in range(MAX_NEWTON):
            a = [row[:] for row in base_a]
            b = list(base_b)
            limited = self.stamp_devices(a, b, x)
            x_new = solve(a, b)
            pairs = list(zip(x_new, x))
            x = x_new
            if limited:
                continue
            # Sıkı ölçüt: normalde Newton karesel yakınsar ve buna hızla ulaşır.
            if all(abs(n - o) <= 1e-9 + 1e-7 * max(abs(n), abs(o)) for n, o in pairs):
                return x
            # Gevşek ölçüt (SPICE varsayılanı: RELTOL 1e-3, VNTOL 1 µV): yalnızca sızıntı akımıyla
            # tutulan düğümler (köprü doğrultucuda ters kutuplu diyotlar) küçük salınımda takılırsa
            # birkaç ek denemeden sonra kabul edilir.
            if all(abs(n - o) <= 1e-6 + 1e-3 * max(abs(n), abs(o)) for n, o in pairs):
                loose_since = it if loose_since is None else loose_since
                if it - loose_since >= 4:
                    return x
            else:
                loose_since = None
        raise CircuitError(t("ckt.no_converge"))

    # --- DC ---
    def dc_matrix(self, values: Dict[str, float], scale: float = 1.0):
        a, b = self.matrix(), [0.0] * self.size
        self.stamp_linear(a)
        for c in self.parts:
            if c.kind == "I":
                self.inject(b, *self.pins[c.ref], values[c.ref] * scale)
            elif c.kind == "V":
                b[self.row[c.ref]] = values[c.ref] * scale
            # bobin: dal denklemi V(n1) − V(n2) = 0 (kısa devre); kondansatör açık devre
        return a, b

    def dc(self, overrides: Optional[Dict[str, float]] = None, x0: Optional[list] = None) -> List[float]:
        values = {ref: src.dc_value() for ref, src in self.sources.items()}
        values.update(overrides or {})
        if not self.size:
            return []
        a, b = self.dc_matrix(values)
        try:
            return self.newton(a, b, x0 or [0.0] * self.size)
        except CircuitError:
            if not self.nonlinear:
                raise
        # kaynak adımlama: kaynakları sıfırdan yavaşça açarak çözüme yürü
        x = [0.0] * self.size
        for step in range(1, 21):
            a, b = self.dc_matrix(values, step / 20)
            x = self.newton(a, b, x)
        return x

    def element_values(self, x, volts_all, source_values, cap_currents=None, ac: bool = False) -> Dict[str, dict]:
        """Her elemanın gerilimi, akımı (1. uca giren) ve gücü; çok uçlularda uç akımları da."""
        out = {}
        get = lambda n: volts_all.get(n, 0.0)          # noqa: E731
        devs = {d.ref: d for d in self.devices}
        for c in self.parts:
            nodes = list(self.pins[c.ref])
            if c.kind in ("Q", "M", "U", "D"):
                if c.ref in self.opamps:
                    i_out = x[self.row[c.ref]]           # çıkıştan elemana giren akım
                    pin_i = [i_out, 0.0, 0.0]
                elif ac:                                 # AC'de küçük işaret akımları sonra yazılır
                    pin_i = [0j] * len(nodes)
                else:
                    dev = devs[c.ref]
                    pin_i = dev.currents([get(n) for n in dev.nodes])
                v = get(nodes[0]) - get(nodes[-1]) if c.kind != "U" else get(nodes[0])
                p = sum(get(n) * i for n, i in zip(nodes, pin_i)) if c.kind != "U" else -get(nodes[0]) * pin_i[0]
                out[c.ref] = {"kind": c.kind, "nodes": nodes, "v": v, "i": pin_i[0], "p": p, "pins": pin_i}
                continue
            n1, n2 = nodes
            vd = get(n1) - get(n2)
            if c.kind == "R":
                i = vd / self.values[c.ref]
            elif c.kind == "C":
                i = (cap_currents or {}).get(c.ref, 0.0 * vd)
            elif c.kind == "I":
                i = source_values[c.ref]
            else:
                i = x[self.row[c.ref]]
            # Güç: pozitif = eleman tüketir; kaynaklarda negatif = devreye güç verir
            out[c.ref] = {"kind": c.kind, "nodes": nodes, "v": vd, "i": i, "p": vd * i}
        return out

    def all_voltages(self, x) -> Dict[str, float]:
        zero = 0.0 * (x[0] if x else 0.0)
        return {"0": zero, **{n: x[self.index[n]] for n in self.nodes}}


def dc_operating_point(circuit: Circuit, overrides: Optional[Dict[str, float]] = None) -> OpResult:
    sys_ = System(circuit)
    x = sys_.dc(overrides)
    values = {ref: src.dc_value() for ref, src in sys_.sources.items()}
    values.update(overrides or {})
    volts = sys_.voltages(x) if x else {"0": 0.0}
    elements = sys_.element_values(x, sys_.all_voltages(x) if x else {"0": 0.0}, values)
    return OpResult(volts, elements, sys_.warnings)


# --- LU ayrıştırma: aynı matrisle çok sayıda çözüm (doğrusal transient) ------------------------------

def lu_factor(a: List[list]):
    n = len(a)
    m = [row[:] for row in a]
    piv = list(range(n))
    rows, cols = _scales(a)
    for col in range(n):
        p = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[p][col]) < min(rows[p], cols[col]) * 1e-13:
            raise CircuitError(t("ckt.singular"))
        m[col], m[p] = m[p], m[col]
        rows[col], rows[p] = rows[p], rows[col]
        piv[col], piv[p] = piv[p], piv[col]
        for r in range(col + 1, n):
            f = m[r][col] / m[col][col]
            m[r][col] = f
            if f:
                row_r, row_c = m[r], m[col]
                for c in range(col + 1, n):
                    row_r[c] -= f * row_c[c]
    return m, piv


def lu_solve(lu, b: list) -> list:
    m, piv = lu
    n = len(b)
    y = [b[piv[i]] for i in range(n)]
    for i in range(n):
        row = m[i]
        s = y[i]
        for j in range(i):
            s -= row[j] * y[j]
        y[i] = s
    for i in range(n - 1, -1, -1):
        row = m[i]
        s = y[i]
        for j in range(i + 1, n):
            s -= row[j] * y[j]
        y[i] = s / row[i]
    return y


# --- Zaman, frekans ve DC tarama sonuçları --------------------------------------------------------

@dataclass
class Sweep:
    kind: str                                   # tran | ac | dc
    x: List[float]                              # zaman (s), frekans (Hz) ya da kaynak değeri
    x_unit: str
    voltages: Dict[str, list]                   # düğüm → değerler ("0" dahil)
    elements: Dict[str, dict]                   # ref → {kind, nodes, v: [...], i: [...], p: [...], pins}
    warnings: List[str] = field(default_factory=list)
    label: str = ""                             # ör. ".tran 10m"

    def point(self, k: int) -> OpResult:
        """k. noktadaki değerler (probe hesaplamak için)."""
        volts = {n: vals[k] for n, vals in self.voltages.items()}
        elems = {}
        for ref, e in self.elements.items():
            item = {"kind": e["kind"], "nodes": e["nodes"], "v": e["v"][k], "i": e["i"][k], "p": e["p"][k]}
            if "pins" in e:
                item["pins"] = [pin[k] for pin in e["pins"]]
            elems[ref] = item
        return OpResult(volts, elems)


def _collect(sys_: System, rows: List[tuple], kind: str, xs: List[float], unit: str, label: str) -> Sweep:
    """rows: (x vektörü, kaynak değerleri, kondansatör akımları) listesi → Sweep."""
    volts = {"0": [0.0] * len(rows), **{n: [] for n in sys_.nodes if ":" not in n}}
    elems: Dict[str, dict] = {}
    for x, src_vals, caps in rows:
        allv = sys_.all_voltages(x)
        for n in volts:
            if n != "0":
                volts[n].append(allv[n])
        for ref, e in sys_.element_values(x, allv, src_vals, caps, ac=kind == "ac").items():
            item = elems.setdefault(ref, {"kind": e["kind"], "nodes": e["nodes"], "v": [], "i": [], "p": []})
            item["v"].append(e["v"])
            item["i"].append(e["i"])
            item["p"].append(e["p"])
            if "pins" in e:
                pins = item.setdefault("pins", [[] for _ in e["pins"]])
                for lst, val in zip(pins, e["pins"]):
                    lst.append(val)
    return Sweep(kind, xs, unit, volts, elems, sys_.warnings, label)


MAX_TRAN_POINTS = 20000


def transient(circuit: Circuit, tstop: float, tstep: float = 0.0, label: str = "") -> Sweep:
    """Zaman analizi: başlangıç DC çalışma noktası, sonra sabit adımla trapez yöntemi.

    Kondansatör ve bobinler eşdeğer iletkenlik + akım kaynağı (companion model) olarak yazılır.
    Doğrusal devrede matris yalnızca iki kez (ilk adım geri Euler, sonrası trapez) ayrıştırılır;
    diyot/transistör varsa her adımda Newton yinelemesi yapılır.
    """
    sys_ = System(circuit)
    h = tstep if tstep else tstop / 1000
    steps = int(math.ceil(tstop / h - 1e-9))
    if steps > MAX_TRAN_POINTS:
        steps = MAX_TRAN_POINTS
        h = tstop / steps
    inds = [c for c in sys_.parts if c.kind == "L"]

    def base(method: str):
        a = sys_.matrix()
        k = 2.0 if method == "trap" else 1.0
        sys_.stamp_linear(a)
        for _, n1, n2, cap in sys_.caps:
            sys_.stamp_g(a, n1, n2, k * cap / h)
        for c in inds:
            a[sys_.row[c.ref]][sys_.row[c.ref]] -= k * sys_.values[c.ref] / h
        return a

    # t = 0: DC çalışma noktası (kondansatör açık, bobin kısa)
    x = sys_.dc()
    src0 = {ref: src.dc_value() for ref, src in sys_.sources.items()}
    allv = sys_.all_voltages(x)
    vc = {key: allv[n1] - allv[n2] for key, n1, n2, _ in sys_.caps}
    ic = {key: 0.0 for key, *_ in sys_.caps}
    il = {c.ref: x[sys_.row[c.ref]] for c in inds}
    vl = {c.ref: 0.0 for c in inds}
    rows = [(x, src0, dict(ic))]
    times = [0.0]
    mats, lus = {}, {}
    linear = not sys_.nonlinear and not sys_.opamps
    for step in range(1, steps + 1):
        time = min(step * h, tstop)
        method = "be" if step == 1 else "trap"
        if method not in mats:
            mats[method] = base(method)
            if linear:
                lus[method] = lu_factor(mats[method])
        k = 2.0 if method == "trap" else 1.0
        b = [0.0] * sys_.size
        values = {ref: src.at(time) for ref, src in sys_.sources.items()}
        for c in sys_.parts:
            if c.kind == "I":
                sys_.inject(b, *sys_.pins[c.ref], values[c.ref])
            elif c.kind == "V":
                b[sys_.row[c.ref]] = values[c.ref]
        for key, n1, n2, cap in sys_.caps:
            g = k * cap / h
            ieq = g * vc[key] + (ic[key] if method == "trap" else 0.0)
            sys_.inject(b, n1, n2, -ieq)              # eşdeğer kaynak n1'e akım verir
        for c in inds:
            req = k * sys_.values[c.ref] / h
            b[sys_.row[c.ref]] = -req * il[c.ref] - (vl[c.ref] if method == "trap" else 0.0)
        x = lu_solve(lus[method], b) if linear else sys_.newton(mats[method], b, x)
        allv = sys_.all_voltages(x)
        for key, n1, n2, cap in sys_.caps:
            v_new = allv[n1] - allv[n2]
            g = k * cap / h
            ic[key] = g * (v_new - vc[key]) - (ic[key] if method == "trap" else 0.0)
            vc[key] = v_new
        for c in inds:
            n1, n2 = sys_.pins[c.ref]
            il[c.ref] = x[sys_.row[c.ref]]
            vl[c.ref] = allv[n1] - allv[n2]
        rows.append((x, values, dict(ic)))
        times.append(time)
    return _collect(sys_, rows, "tran", times, "s", label)


def ac_analysis(circuit: Circuit, freqs: List[float], label: str = "") -> Sweep:
    """Frekans taraması: önce DC çalışma noktası bulunur, doğrusal olmayan elemanlar o noktadaki
    küçük işaret iletkenlikleriyle yazılır. Kaynakların AC değeri kullanılır (DC kaynaklar AC'de
    sıfırdır)."""
    sys_ = System(circuit)
    if not any(src.ac_mag for src in sys_.sources.values()):
        raise CircuitError(t("an.no_ac_source"))
    x_op = sys_.dc()
    # çalışma noktasındaki küçük işaret iletkenlikleri (sınırlama olmadan)
    small = []
    for dev in sys_.devices:
        v = [x_op[sys_.index[n]] if n in sys_.index else 0.0 for n in dev.nodes]
        _, jac = dev.linearize(v)
        small.append((dev, jac))
    for op in sys_.opamps.values():
        u = sum(w * (x_op[sys_.index[n]] if n in sys_.index else 0.0) for n, w in op.drive())
        op.u = u
        op.k = op.clamp(u)[1]
    rows = []
    phasors = {ref: src.ac_phasor() for ref, src in sys_.sources.items()}
    lin = sys_.matrix(0j)
    sys_.stamp_linear(lin)
    for dev, jac in small:
        for k, nk in enumerate(dev.nodes):
            ik = sys_.index.get(nk)
            if ik is None:
                continue
            for j, nj in enumerate(dev.nodes):
                ij = sys_.index.get(nj)
                if ij is not None:
                    lin[ik][ij] += jac[k][j]
    for ref, op in sys_.opamps.items():
        row = sys_.row[ref]
        lin[row][sys_.index[op.out]] += 1
        for n, w in op.drive():
            if n in sys_.index:
                lin[row][sys_.index[n]] -= op.k * w
    for f in freqs:
        w = 2 * math.pi * f
        a, b = [r[:] for r in lin], [0j] * sys_.size
        for _, n1, n2, cap in sys_.caps:
            sys_.stamp_g(a, n1, n2, 1j * w * cap)
        for c in sys_.parts:
            if c.kind == "I":
                sys_.inject(b, *sys_.pins[c.ref], phasors[c.ref])
            elif c.kind == "V":
                b[sys_.row[c.ref]] = phasors[c.ref]
            elif c.kind == "L":
                a[sys_.row[c.ref]][sys_.row[c.ref]] -= 1j * w * sys_.values[c.ref]
        x = solve(a, b)
        allv = sys_.all_voltages(x)
        caps = {key: 1j * w * cap * (allv[n1] - allv[n2]) for key, n1, n2, cap in sys_.caps}
        rows.append((x, phasors, caps))
    sweep = _collect_ac(sys_, rows, freqs, label, small)
    return sweep


def _collect_ac(sys_: System, rows, freqs, label, small) -> Sweep:
    """AC: doğrusal olmayan elemanların uç akımları küçük işaret iletkenliğinden (J·v) hesaplanır."""
    sweep = _collect(sys_, rows, "ac", list(freqs), "Hz", label)
    for dev, jac in small:
        e = sweep.elements[dev.ref]
        pins_i = [[] for _ in dev.nodes]
        for x, _, _ in rows:
            allv = sys_.all_voltages(x)
            v = [allv.get(n, 0j) for n in dev.nodes]
            for k in range(len(dev.nodes)):
                pins_i[k].append(sum(jac[k][j] * v[j] for j in range(len(dev.nodes))))
        e["i"] = pins_i[0]
        if "pins" in e:
            e["pins"] = pins_i
        e["p"] = [0j] * len(rows)
    return sweep


def dc_sweep(circuit: Circuit, source: str, values: List[float], label: str = "") -> Sweep:
    sys_ = System(circuit)
    ref = next((r for r in sys_.sources if r.upper() == source.upper()), None)
    if ref is None:
        raise CircuitError(t("an.no_source", ref=source))
    rows = []
    base = {r: src.dc_value() for r, src in sys_.sources.items()}
    x = None
    for v in values:
        vals = {**base, ref: v}
        x = sys_.dc({ref: v}, x)                       # bir önceki çözüm iyi bir başlangıç tahmini
        rows.append((x, vals, None))
    unit = "V" if next(c for c in sys_.parts if c.ref == ref).kind == "V" else "A"
    return _collect(sys_, rows, "dc", list(values), unit, label)


def run_analysis(circuit: Circuit, directive: str) -> Optional[Sweep]:
    """Analiz komutunu çalıştırır; .op (ya da boş) için None döner."""
    from elektro.circuit.sources import ac_frequencies, dc_values, parse_directive
    an = parse_directive(directive)
    label = an.directive()
    if an.kind == "tran":
        return transient(circuit, an.tstop, an.tstep, label)
    if an.kind == "ac":
        return ac_analysis(circuit, ac_frequencies(an), label)
    if an.kind == "dc":
        return dc_sweep(circuit, an.source, dc_values(an), label)
    return None


def equivalent_resistance(circuit: Circuit, net_a: str, net_b: str) -> float:
    """İki düğüm arasındaki eşdeğer (Thevenin) direnç.

    Kaynaklar söndürülür: gerilim kaynağı ve bobin kısa devre, akım kaynağı ve kondansatör açık
    devre. Diyot, transistör ve op-amp hesaba katılmaz (açık devre sayılır). A'dan 1 A verilip B'den çekilir; R = V(A) − V(B). Yol yoksa sonsuz, kısaysa 0 döner.
    Toprak ya da kaynak gerekmez.
    """
    parent: Dict[str, str] = {}

    def find(n: str) -> str:
        parent.setdefault(n, n)
        while parent[n] != n:
            parent[n] = parent[parent[n]]
            n = parent[n]
        return n

    nets = circuit.nets()
    parts = [c for c in circuit.components if c.is_part]
    edges = []
    for c in parts:
        n1, n2 = (find(nets[p]) for p in c.pins())
        if c.kind in ("V", "L"):                     # kısa devre: düğümleri birleştir
            parent[find(n1)] = find(n2)
        elif c.kind == "R":
            try:
                r = c.number()
            except ValueError as e:
                raise CircuitError(str(e))
            if r <= 0:
                raise CircuitError(t("ckt.bad_value", ref=c.ref))
            edges.append((c, 1 / r))
    find(net_a), find(net_b)
    a, b = find(net_a), find(net_b)
    if a == b:
        return 0.0
    links = []
    for c, g in edges:
        n1, n2 = (find(nets[p]) for p in c.pins())
        if n1 != n2:
            links.append((n1, n2, g))
    # A'nın dirençlerle ulaşabildiği düğümler; B bunların arasında değilse açık devre
    reach, stack = {a}, [a]
    while stack:
        n = stack.pop()
        for n1, n2, _ in links:
            for x, y in ((n1, n2), (n2, n1)):
                if x == n and y not in reach:
                    reach.add(y)
                    stack.append(y)
    if b not in reach:
        return float("inf")
    nodes = sorted(reach - {b})                       # B referans (0 V)
    index = {n: i for i, n in enumerate(nodes)}
    m = [[0.0] * len(nodes) for _ in nodes]
    for n1, n2, g in links:
        if n1 not in reach:
            continue
        i, j = index.get(n1), index.get(n2)
        if i is not None:
            m[i][i] += g
        if j is not None:
            m[j][j] += g
        if i is not None and j is not None:
            m[i][j] -= g
            m[j][i] -= g
    rhs = [0.0] * len(nodes)
    rhs[index[a]] = 1.0
    return solve(m, rhs)[index[a]]
