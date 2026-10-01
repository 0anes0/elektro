"""Genel araçlar: mühendislik hesap makinesi ve birim dönüştürücü."""

from __future__ import annotations

import ast
import cmath
import math
import operator
import re
from typing import Optional

import typer
from rich.table import Table

from elektro.i18n import t
from elektro.modules.passive import parallel_sum
from elektro.modules.wiring import area_to_awg, awg_diameter
from elektro.state import all_vars
from elektro.ui import cli_parser, console, emit, fail, json_mode, print_json
from elektro.units import format_si, parse_value

# --- Hesap makinesi ----------------------------------------------------------------------

# Birim ekli sayılar: 4k7, 100n, 12V, 2.2uF, 1kΩ, 10MHz, 1e-3
_NUMBER = re.compile(
    r"(?<![\w.])((?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?(?:meg|[TGMkKRmuµμnpf])?\d*(?:ohms?|Ω|Hz|F|H|V|A|W|s)?)"
    r"(j?)(?![\w.])"
)

def _cm(real_fn, complex_fn):
    """Gerçel girişte math, karmaşık veya tanım dışı girişte cmath kullanır (sqrt(-1) = j)."""
    def fn(x):
        if isinstance(x, complex):
            return _tidy(complex_fn(x))
        try:
            return real_fn(x)
        except ValueError:
            return _tidy(complex_fn(x))
    return fn


def _tidy(z):
    """Yuvarlama artığı sanal/gerçel kısımları temizler: 1e-17 + 2j → 2j."""
    if not isinstance(z, complex):
        return z
    re_, im = z.real, z.imag
    scale = max(abs(re_), abs(im))
    if abs(im) <= scale * 1e-12:
        return re_
    if abs(re_) <= scale * 1e-12:
        re_ = 0.0
    return complex(re_, im)


def _real(name):
    def check(x):
        if isinstance(x, complex):
            raise ValueError(t("calc.need_real", name=name))
        return x
    return check


def _deg_fn(fn, inverse=False):
    return lambda x: math.degrees(fn(_real("deg")(x))) if inverse else fn(math.radians(_real("deg")(x)))


def polar(magnitude, degrees):
    return _tidy(cmath.rect(_real("polar")(magnitude), math.radians(_real("polar")(degrees))))


def _arg(z):
    return math.degrees(cmath.phase(z))


_TWO_PI = 2 * math.pi

_FUNCS = {
    "sqrt": _cm(math.sqrt, cmath.sqrt), "exp": _cm(math.exp, cmath.exp), "ln": _cm(math.log, cmath.log),
    "log": _cm(math.log10, cmath.log10), "log10": _cm(math.log10, cmath.log10),
    "log2": lambda x: math.log2(_real("log2")(x)),
    "sin": _cm(math.sin, cmath.sin), "cos": _cm(math.cos, cmath.cos), "tan": _cm(math.tan, cmath.tan),
    "asin": _cm(math.asin, cmath.asin), "acos": _cm(math.acos, cmath.acos), "atan": _cm(math.atan, cmath.atan),
    "sind": _deg_fn(math.sin), "cosd": _deg_fn(math.cos), "tand": _deg_fn(math.tan),
    "abs": abs, "round": round, "min": min, "max": max,
    "db": lambda x: 20 * math.log10(abs(x)), "dbp": lambda x: 10 * math.log10(abs(x)),
    "par": lambda *xs: _tidy(parallel_sum(list(xs))), "deg": math.degrees, "rad": math.radians,
    # karmaşık sayılar ve fazörler
    "re": lambda z: complex(z).real, "real": lambda z: complex(z).real,
    "im": lambda z: complex(z).imag, "imag": lambda z: complex(z).imag,
    "arg": _arg, "angle": _arg, "conj": lambda z: _tidy(complex(z).conjugate()), "polar": polar,
    # empedanslar: zl(L, f) = jωL, zc(C, f) = 1/(jωC)
    "zl": lambda l, f: complex(0, _TWO_PI * f * l),
    "zc": lambda c, f: complex(0, -1 / (_TWO_PI * f * c)),
}
_CONSTS = {"pi": math.pi, "e": math.e, "c": 299_792_458.0, "j": 1j}
_BINOPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
           ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
           # ∠ ve || ifadeleri ayrıştırmadan önce @ ve // işleçlerine çevrilir
           ast.MatMult: polar, ast.FloorDiv: lambda a, b: _tidy(parallel_sum([a, b]))}
_UNARY = {ast.USub: operator.neg, ast.UAdd: operator.pos}

# Sayıya bitişik sanal birim: 3j, 2.5j, 4k7j, j10 (ikincisi elektrikçi yazımı)
_J_BEFORE = re.compile(r"(?<![\w.])j(?=\d|\.\d|\()")


def evaluate(expression: str):
    src = (expression.replace("^", "**").replace("×", "*").replace("·", "*").replace(",", ", ")
           .replace("∠", "@").replace("°", "").replace("||", "//"))
    src = _J_BEFORE.sub("j*", src)          # j10 → j*10,  j(…) → j*(…)

    def sub(m):
        try:
            value = repr(parse_value(m.group(1)))
        except ValueError:
            return m.group(0)
        return f"({value}*j)" if m.group(2) else value

    src = _NUMBER.sub(sub, src)
    try:
        tree = ast.parse(src, mode="eval")
    except SyntaxError:
        raise ValueError(t("calc.syntax"))
    return _tidy(_eval(tree.body))


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, complex)) \
            and not isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
        return _tidy(_BINOPS[type(node.op)](_eval(node.left), _eval(node.right)))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
        return _UNARY[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.Name):
        if node.id in _CONSTS:
            return _CONSTS[node.id]
        variables = all_vars()          # `elektro set vin 12` ile tanımlananlar
        if node.id in variables:
            try:
                return evaluate(str(variables[node.id]))
            except (ValueError, RecursionError):
                raise ValueError(t("calc.var_not_number", name=node.id))
        raise ValueError(t("calc.unknown_name", name=node.id))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and not node.keywords:
        if node.func.id not in _FUNCS:
            raise ValueError(t("calc.unknown_name", name=node.func.id))
        return _tidy(_FUNCS[node.func.id](*[_eval(a) for a in node.args]))
    raise ValueError(t("calc.unsupported"))


def complex_parts(z: complex) -> dict:
    return {"re": z.real, "im": z.imag, "mag": abs(z), "deg": _arg(z)}


def format_complex(z: complex, unit: str = "", digits: int = 5) -> tuple:
    """(dikdörtgen, kutupsal) gösterim: '3 + j4 Ω', '5 Ω ∠ 53.13°'."""
    re_, im = z.real, z.imag
    sign = "−" if im < 0 else "+"
    if re_ == 0:
        rect = f"{'−' if im < 0 else ''}j{format_si(abs(im), unit, digits)}"
    else:
        rect = f"{format_si(re_, '', digits)} {sign} j{format_si(abs(im), '', digits)} {unit}".rstrip()
    pol = f"{format_si(abs(z), unit, digits)} ∠ {_arg(z):.{max(digits - 1, 2)}g}°"
    return rect, pol


def equivalent(z: complex, freq: float) -> dict:
    """Empedansın verilen frekanstaki seri eşdeğeri: R + L veya R + C."""
    w = _TWO_PI * freq
    out = {"r": z.real}
    if z.imag > 0:
        out["l"] = z.imag / w
    elif z.imag < 0:
        out["c"] = -1 / (w * z.imag)
    return out


def calc(
    expression: str = typer.Argument(..., help=t("calc.arg")),
    unit: str = typer.Option("", "--unit", "-u", help=t("calc.opt.unit")),
    freq: Optional[float] = typer.Option(None, "--freq", "-f", parser=cli_parser(parse_value),
                                         metavar=t("ui.metavar.value"), help=t("calc.opt.freq")),
):
    try:
        result = evaluate(expression)
    except ZeroDivisionError:
        fail(t("calc.div_zero"))
    except (ValueError, TypeError, OverflowError) as e:
        fail(str(e))
    if isinstance(result, complex):
        _print_complex(expression, result, unit, freq)
        return
    if json_mode():
        print_json({"expression": expression, "result": result, "unit": unit or None})
        return
    console.print(f"[dim]{expression} =[/]")
    console.print(f"[bold green]{format_si(result, unit, 6)}[/]   [dim]({result:.10g})[/]")


def _print_complex(expression: str, z: complex, unit: str, freq: Optional[float]) -> None:
    rect, pol = format_complex(z, unit)
    eq = equivalent(z, freq) if freq and freq > 0 else None
    if json_mode():
        data = {"expression": expression, "result": complex_parts(z), "unit": unit or None}
        if eq:
            data["equivalent"] = {"freq_hz": freq, "r_ohm": eq["r"], "l_h": eq.get("l"), "c_f": eq.get("c")}
        print_json(data)
        return
    tbl = Table(show_header=False, box=None, padding=(0, 1))
    tbl.add_column(style="cyan", justify="right")
    tbl.add_column(style="bold green")
    tbl.add_row(t("calc.rect"), rect)
    tbl.add_row(t("calc.polar"), pol)
    tbl.add_row(t("calc.mag"), format_si(abs(z), unit, 6))
    tbl.add_row(t("calc.angle"), f"{_arg(z):.6g}°  ({cmath.phase(z):.6g} rad)")
    if eq:
        tbl.add_row(t("calc.eq_r", f=format_si(freq, "Hz")), format_si(eq["r"], "Ω"))
        if "l" in eq:
            tbl.add_row(t("calc.eq_l"), format_si(eq["l"], "H"))
        if "c" in eq:
            tbl.add_row(t("calc.eq_c"), format_si(eq["c"], "F"))
    console.print(f"[dim]{expression} =[/]")
    console.print(tbl)


# --- Birim dönüştürücü --------------------------------------------------------------------

LENGTH = {"m": 1.0, "km": 1e3, "cm": 1e-2, "mm": 1e-3, "um": 1e-6, "µm": 1e-6,
          "in": 0.0254, "inch": 0.0254, "mil": 25.4e-6, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344}
TEMPERATURE = ("c", "f", "k")
COPPER = {"oz": 34.8e-6}      # bakır ağırlığı → kalınlık


def convert_unit(value: float, src: str, dst: Optional[str]) -> dict:
    s = src.lower().replace("°", "")
    d = dst.lower().replace("°", "") if dst else None

    if s in TEMPERATURE:
        kelvin = {"c": value + 273.15, "f": (value - 32) * 5 / 9 + 273.15, "k": value}[s]
        if kelvin < 0:
            raise ValueError(t("unit.below_zero"))
        out = {"°C": kelvin - 273.15, "°F": (kelvin - 273.15) * 9 / 5 + 32, "K": kelvin}
    elif s in LENGTH:
        meters = value * LENGTH[s]
        out = {u: meters / f for u, f in LENGTH.items() if u not in ("inch", "µm", "yd", "mi", "km")}
    elif s == "db":
        out = {t("unit.power_ratio"): 10 ** (value / 10), t("unit.voltage_ratio"): 10 ** (value / 20)}
    elif s in ("pratio", "vratio"):
        if value <= 0:
            raise ValueError(t("common.positive"))
        out = {"dB": (10 if s == "pratio" else 20) * math.log10(value)}
    elif s == "awg":
        dia = awg_diameter(value)
        out = {"mm": dia * 1e3, "mm²": math.pi * dia ** 2 / 4 * 1e6, "mil": dia / 25.4e-6}
    elif s in ("mm2", "mm²"):
        if value <= 0:
            raise ValueError(t("common.positive"))
        out = {"AWG": area_to_awg(value * 1e-6), "mm": math.sqrt(4 * value / math.pi)}
    elif s == "oz":
        out = {"µm": value * COPPER["oz"] * 1e6, "mil": value * COPPER["oz"] / 25.4e-6}
    elif s in ("deg", "rad"):
        out = {"deg": math.degrees(value) if s == "rad" else value,
               "rad": math.radians(value) if s == "deg" else value}
    elif s in ("hz", "rpm"):
        hz = value if s == "hz" else value / 60
        if hz <= 0:
            raise ValueError(t("common.positive"))
        out = {"Hz": hz, "rpm": hz * 60, "rad/s": 2 * math.pi * hz, t("unit.period"): 1 / hz}
    else:
        raise ValueError(t("unit.unknown", unit=src, options=UNIT_LIST))

    if d:
        match = {k: v for k, v in out.items() if k.lower().replace("°", "") == d}
        if not match:
            raise ValueError(t("unit.no_path", src=src, dst=dst))
        return match
    return out


UNIT_LIST = "c f k · m cm mm um in mil ft · db pratio vratio · awg mm2 oz · deg rad · hz rpm"


def unit(
    value: float = typer.Argument(..., parser=cli_parser(parse_value), metavar=t("ui.metavar.value"), help=t("unit.arg.value")),
    src: str = typer.Argument(..., help=t("unit.arg.src", units=UNIT_LIST)),
    dst: Optional[str] = typer.Argument(None, help=t("unit.arg.dst")),
):
    try:
        res = convert_unit(value, src, dst)
    except ValueError as e:
        fail(str(e))
    tbl = Table(show_header=False, box=None)
    tbl.add_column(style="bold green", justify="right")
    tbl.add_column(style="cyan")
    for k, v in res.items():
        tbl.add_row(f"{v:.6g}", k)
    emit(tbl, {"value": value, "unit": src, "results": res})
