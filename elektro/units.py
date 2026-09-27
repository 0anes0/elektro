"""Mühendislik birimleri: ayrıştırma, biçimlendirme ve standart (E-serisi) değerler."""

from __future__ import annotations

import math
import re

from elektro.i18n import t

_PREFIXES = {
    "T": 1e12, "G": 1e9, "M": 1e6, "meg": 1e6, "k": 1e3, "K": 1e3,
    "R": 1.0, "r": 1.0,
    "m": 1e-3, "u": 1e-6, "µ": 1e-6, "μ": 1e-6, "n": 1e-9, "p": 1e-12, "f": 1e-15,
}

# Sayının sonunda yazılabilecek birim adları (ön ekten sonra atılır).
_UNITS = ("ohms", "ohm", "Ω", "hz", "Hz", "HZ", "F", "H", "V", "A", "W", "s")

_NUMBER_RE = re.compile(
    r"^(?P<num>[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)"
    r"(?P<prefix>meg|[TGMkKRrmuµμnpf])?"
    r"(?P<frac>\d*)$"
)


def parse_value(text: str | float | int) -> float:
    """'4k7', '100n', '2.2uF', '1kΩ', '10MHz', '1e-3' gibi girdileri float'a çevirir.

    Büyük/küçük harf önemlidir: 'M' mega, 'm' mili.
    """
    if isinstance(text, (int, float)):
        return float(text)
    s = str(text).strip().replace(" ", "").replace(",", ".")
    if not s:
        raise ValueError(t("units.empty"))
    try:
        return float(s)
    except ValueError:
        pass

    for unit in _UNITS:
        if s.endswith(unit) and len(s) > len(unit):
            s = s[: -len(unit)]
            break

    m = _NUMBER_RE.match(s)
    if not m:
        raise ValueError(t("units.invalid", text=text))
    num, prefix, frac = m.group("num"), m.group("prefix"), m.group("frac")
    if frac:
        # 4k7 -> 4.7k, 1R5 -> 1.5
        if not prefix or "." in num or "e" in num.lower():
            raise ValueError(t("units.invalid", text=text))
        num = f"{num}.{frac}"
    return float(num) * _PREFIXES.get(prefix or "", 1.0)


_SI = [
    (1e12, "T"), (1e9, "G"), (1e6, "M"), (1e3, "k"), (1.0, ""),
    (1e-3, "m"), (1e-6, "µ"), (1e-9, "n"), (1e-12, "p"), (1e-15, "f"),
]


def format_si(value: float, unit: str = "", digits: int = 4) -> str:
    """Değeri SI ön ekiyle yazar: 1591.55 -> '1.592 kHz'."""
    if value is None:
        return "-"
    if math.isnan(value):
        return "NaN"
    if math.isinf(value):
        return ("-" if value < 0 else "") + "∞" + (f" {unit}" if unit else "")
    if value == 0:
        return f"0 {unit}".strip()
    a = abs(value)
    for factor, prefix in _SI:
        if a >= factor * 0.99995:
            scaled = value / factor
            break
    else:
        factor, prefix = _SI[-1]
        scaled = value / factor
    # 999.96 k gibi yuvarlanma taşmalarını düzelt
    txt = f"{scaled:.{digits}g}"
    if "e" in txt:
        txt = f"{scaled:.{digits - 1}f}".rstrip("0").rstrip(".")
    return f"{txt} {prefix}{unit}".strip()


# --- E serileri ------------------------------------------------------------

E_SERIES_BASE = {
    "E3": [1.0, 2.2, 4.7],
    "E6": [1.0, 1.5, 2.2, 3.3, 4.7, 6.8],
    "E12": [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2],
    "E24": [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
            3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1],
}


def _computed_series(n: int) -> list[float]:
    vals = [round(10 ** (i / n), 2) for i in range(n)]
    # IEC 60063'te hesaplanan değerden sapan tek değer
    return [9.20 if abs(v - 9.19) < 1e-9 else v for v in vals]


for _n in (48, 96, 192):
    E_SERIES_BASE[f"E{_n}"] = _computed_series(_n)

SERIES_NAMES = list(E_SERIES_BASE)


def normalize_series(name: str) -> str:
    key = name.upper()
    if not key.startswith("E"):
        key = "E" + key
    if key not in E_SERIES_BASE:
        raise ValueError(t("units.unknown_series", name=name, options=", ".join(SERIES_NAMES)))
    return key


def series_neighbors(value: float, series: str = "E24") -> tuple[float, float]:
    """Değerin hemen altındaki ve üstündeki (veya eşit) standart değerler."""
    if value <= 0:
        raise ValueError(t("common.positive"))
    base = E_SERIES_BASE[normalize_series(series)]
    decade = math.floor(math.log10(value))
    candidates = []
    for d in (decade - 1, decade, decade + 1):
        candidates.extend(b * 10 ** d for b in base)
    candidates = sorted(round(c, 12) for c in candidates)
    eps = value * 1e-9
    lower = max(c for c in candidates if c <= value + eps)
    upper = min(c for c in candidates if c >= value - eps)
    return lower, upper


def nearest_standard(value: float, series: str = "E24") -> float:
    """Logaritmik olarak en yakın standart değer."""
    lower, upper = series_neighbors(value, series)
    return lower if math.log(value / lower) <= math.log(upper / value) else upper


def series_values(series: str, lo: float, hi: float) -> list[float]:
    """[lo, hi] aralığındaki tüm standart değerler."""
    base = E_SERIES_BASE[normalize_series(series)]
    out = []
    for d in range(math.floor(math.log10(lo)) - 1, math.ceil(math.log10(hi)) + 1):
        for b in base:
            v = round(b * 10 ** d, 12)
            if lo <= v <= hi:
                out.append(v)
    return sorted(out)
