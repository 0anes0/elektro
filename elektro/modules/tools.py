"""Genel araçlar: mühendislik hesap makinesi ve birim dönüştürücü."""

from __future__ import annotations

import ast
import math
import operator
import re
from typing import Optional

import typer
from rich.table import Table

from elektro.i18n import t
from elektro.modules.passive import parallel_sum
from elektro.modules.wiring import area_to_awg, awg_diameter
from elektro.ui import console, emit, fail, json_mode, print_json
from elektro.units import format_si, parse_value

# --- Hesap makinesi ----------------------------------------------------------------------

# Birim ekli sayılar: 4k7, 100n, 12V, 2.2uF, 1kΩ, 10MHz, 1e-3
_NUMBER = re.compile(
    r"(?<![\w.])((?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?(?:meg|[TGMkKRmuµμnpf])?\d*(?:ohms?|Ω|Hz|F|H|V|A|W|s)?)(?![\w.])"
)

_FUNCS = {
    "sqrt": math.sqrt, "exp": math.exp, "ln": math.log, "log": math.log10, "log10": math.log10,
    "log2": math.log2, "sin": math.sin, "cos": math.cos, "tan": math.tan, "asin": math.asin,
    "acos": math.acos, "atan": math.atan, "abs": abs, "round": round, "min": min, "max": max,
    "db": lambda x: 20 * math.log10(x), "dbp": lambda x: 10 * math.log10(x),
    "par": lambda *xs: parallel_sum(list(xs)), "deg": math.degrees, "rad": math.radians,
}
_CONSTS = {"pi": math.pi, "e": math.e, "c": 299_792_458.0}
_BINOPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
           ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod}
_UNARY = {ast.USub: operator.neg, ast.UAdd: operator.pos}


def evaluate(expression: str) -> float:
    src = expression.replace("^", "**").replace("×", "*").replace("·", "*").replace(",", ", ")

    def sub(m):
        try:
            return repr(parse_value(m.group(1)))
        except ValueError:
            return m.group(1)

    src = _NUMBER.sub(sub, src)
    try:
        tree = ast.parse(src, mode="eval")
    except SyntaxError:
        raise ValueError(t("calc.syntax"))
    return _eval(tree.body)


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
        return _BINOPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
        return _UNARY[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.Name):
        if node.id in _CONSTS:
            return _CONSTS[node.id]
        raise ValueError(t("calc.unknown_name", name=node.id))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and not node.keywords:
        if node.func.id not in _FUNCS:
            raise ValueError(t("calc.unknown_name", name=node.func.id))
        return _FUNCS[node.func.id](*[_eval(a) for a in node.args])
    raise ValueError(t("calc.unsupported"))


def calc(
    expression: str = typer.Argument(..., help=t("calc.arg")),
    unit: str = typer.Option("", "--unit", "-u", help=t("calc.opt.unit")),
):
    try:
        result = evaluate(expression)
    except ZeroDivisionError:
        fail(t("calc.div_zero"))
    except (ValueError, TypeError, OverflowError) as e:
        fail(str(e))
    if isinstance(result, complex):
        fail(t("calc.complex"))
    if json_mode():
        print_json({"expression": expression, "result": result, "unit": unit or None})
        return
    console.print(f"[dim]{expression} =[/]")
    console.print(f"[bold green]{format_si(result, unit, 6)}[/]   [dim]({result:.10g})[/]")


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
    value: float = typer.Argument(..., parser=parse_value, metavar=t("ui.metavar.value"), help=t("unit.arg.value")),
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
