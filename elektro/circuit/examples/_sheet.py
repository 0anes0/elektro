"""Örnek devreleri okunur biçimde çizmek için küçük yardımcı.

Koordinatlar ızgara birimidir. İki uçlu elemanlar:
    yatay  ("h"):  uçlar (x, y) – (x+3, y)
    dikey  ("v"):  uçlar (x, y) – (x, y+2)   (kaynakta + üstte, diyotta yön ayrıca verilir)
"""

from __future__ import annotations

from typing import Optional, Tuple

from elektro.circuit.model import Circuit, Component

Point = Tuple[int, int]
DIODE_ROT = {">": 0, "v": 90, "<": 180, "^": 270}       # iletim yönü: anottan katoda
LABEL_ROT = {"r": 0, "d": 90, "l": 180, "u": 270}         # etiket yazısının noktaya göre yeri


class Sheet:
    def __init__(self) -> None:
        self.c = Circuit()

    # --- iki uçlular ---
    def _two(self, kind: str, x: int, y: int, value: str, d: str, ref: Optional[str]) -> Component:
        comp = self.c.add(kind, x, y, rot=0 if d == "h" else 90, value=value)
        if ref:
            comp.ref = ref
        return comp

    def r(self, x, y, value, d="h", ref=None):
        return self._two("R", x, y, value, d, ref)

    def cap(self, x, y, value, d="v", ref=None):
        return self._two("C", x, y, value, d, ref)

    def ind(self, x, y, value, d="h", ref=None):
        return self._two("L", x, y, value, d, ref)

    def v(self, x, y, value, d="v", ref=None, flip=False):
        """Gerilim kaynağı; + ucu üstte (dikey) ya da solda (yatay). flip: ters."""
        comp = self._two("V", x, y, value, d, ref)
        if flip:
            comp.rot += 180
        return comp

    def i(self, x, y, value, d="v", ref=None, flip=False):
        """Akım kaynağı; akım 1. uçtan (üst/sol) kaynağın içinden 2. uca akar."""
        comp = self._two("I", x, y, value, d, ref)
        if flip:
            comp.rot += 180
        return comp

    def d(self, x, y, value="1N4148", way=">", ref=None):
        """Diyot; way: '>' '<' (yatay) ya da 'v' '^' (dikey) iletim yönü.
        Konum her zaman sol/üst uçtur."""
        comp = self.c.add("D", x, y, rot=DIODE_ROT[way], value=value)
        if ref:
            comp.ref = ref
        return comp

    # --- üç uçlular (konum gövdenin ortası) ---
    def q(self, x, y, value="2N2222", rot=0, ref=None):
        """BJT; rot 0: C (x, y−1), B (x−1, y), E (x, y+1)."""
        comp = self.c.add("Q", x, y, rot=rot, value=value)
        if ref:
            comp.ref = ref
        return comp

    def m(self, x, y, value="2N7000", rot=0, ref=None):
        """MOSFET; rot 0: D (x, y−1), G (x−1, y), S (x, y+1)."""
        comp = self.c.add("M", x, y, rot=rot, value=value)
        if ref:
            comp.ref = ref
        return comp

    def u(self, x, y, value="TL072 ±15", flip=False, mirror=False, ref=None):
        """Op-amp; çıkış (x+2, y), + (x−1, y−1), − (x−1, y+1). flip: − üstte; mirror: çıkış solda."""
        rot = {(False, False): 0, (True, False): 90, (False, True): 180, (True, True): 270}[(flip, mirror)]
        comp = self.c.add("U", x, y, rot=rot, value=value)
        if ref:
            comp.ref = ref
        return comp

    # --- bağlantılar ---
    def gnd(self, x, y):
        return self.c.add("GND", x, y)

    def lab(self, x, y, name, side="r"):
        return self.c.add("N", x, y, rot=LABEL_ROT[side], value=name)

    def w(self, *points: Point) -> None:
        """Noktaları sırayla kablo ile birleştirir (ardışık noktalar aynı satır/sütunda olmalı)."""
        for a, b in zip(points, points[1:]):
            if a[0] != b[0] and a[1] != b[1]:
                raise ValueError(f"çapraz kablo {a} → {b}")
            self.c.add_wire(a, b)

    def done(self, probes=(), analysis: str = "") -> Circuit:
        self.c.probes = list(probes)
        self.c.analysis = analysis
        return self.c
