"""Dijital elektronik: sayı tabanları, mantık kapıları, boolean ifadeler."""

from __future__ import annotations

import ast
import itertools
from typing import List, Optional

import typer
from rich.table import Table

from elektro.i18n import t
from elektro.ui import console, emit, fail, json_mode, print_json, result_panel

app = typer.Typer(help=t("dig.help"), no_args_is_help=True)

_PREFIX_BASE = {"0x": 16, "0b": 2, "0o": 8}


def parse_int(text: str, base: Optional[int] = None) -> int:
    s = text.strip().lower().replace("_", "")
    neg = s.startswith("-")
    if neg:
        s = s[1:]
    if base is None:
        base = 10
        for prefix, b in _PREFIX_BASE.items():
            if s.startswith(prefix):
                base, s = b, s[2:]
                break
        else:
            if s.endswith("h") and all(c in "0123456789abcdef" for c in s[:-1]):
                base, s = 16, s[:-1]
    elif s[:2] in _PREFIX_BASE and _PREFIX_BASE[s[:2]] == base:
        s = s[2:]
    value = int(s, base)
    return -value if neg else value


def to_base(n: int, base: int) -> str:
    if not 2 <= base <= 36:
        raise ValueError(t("dig.base_range"))
    if n == 0:
        return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    neg, n = n < 0, abs(n)
    out = []
    while n:
        n, r = divmod(n, base)
        out.append(digits[r])
    return ("-" if neg else "") + "".join(reversed(out))


def group(s: str, size: int) -> str:
    s = s.lstrip("-")
    s = "0" * ((-len(s)) % size) + s
    return " ".join(s[i:i + size] for i in range(0, len(s), size))


@app.command(help=t("dig.conv.help"))
def convert(
    value: str = typer.Argument(..., help=t("dig.conv.arg")),
    from_base: Optional[int] = typer.Option(None, "--from", "-f", help=t("dig.conv.opt.from")),
    to_base_: Optional[int] = typer.Option(None, "--to", "-t", help=t("dig.conv.opt.to")),
    bits: Optional[int] = typer.Option(None, "--bits", "-b", min=1, help=t("dig.conv.opt.bits")),
):
    try:
        n = parse_int(value, from_base)
    except ValueError:
        fail(t("dig.conv.invalid", value=value) + (t("dig.conv.in_base", base=from_base) if from_base else ""))

    raw = n
    if bits:
        lo, hi = -(1 << (bits - 1)), (1 << bits) - 1
        if not lo <= n <= hi:
            fail(t("dig.conv.overflow", n=n, bits=bits, lo=lo, hi=hi))
        raw = n & ((1 << bits) - 1)

    if to_base_:
        try:
            if json_mode():
                print_json({"input": value, "value": n, "base": to_base_, "result": to_base(raw, to_base_)})
                return
            console.print(f"[cyan]{value}[/] = [bold green]{to_base(raw, to_base_)}[/] "
                          f"({t('dig.conv.base', base=to_base_)})")
        except ValueError as e:
            fail(str(e))
        return

    width = bits or max(raw.bit_length(), 1)
    b = to_base(raw, 2).lstrip("-").zfill(width)
    rows = {
        t("dig.dec"): str(n),
        t("dig.hex"): "0x" + to_base(raw, 16),
        t("dig.bin"): "0b " + group(b, 4),
        t("dig.oct"): "0o" + to_base(raw, 8),
        t("dig.bits"): str(width),
    }
    if bits:
        rows[t("dig.unsigned")] = str(raw)
    if 32 <= raw < 127:
        rows["ASCII"] = repr(chr(raw))
    result_panel(t("dig.conv.title"), rows, data={
        "value": n, "unsigned": raw, "bits": width, "hex": to_base(raw, 16), "bin": b, "oct": to_base(raw, 8)})


GATES = {
    "and": lambda a, b: a & b,
    "or": lambda a, b: a | b,
    "xor": lambda a, b: a ^ b,
    "nand": lambda a, b: 1 - (a & b),
    "nor": lambda a, b: 1 - (a | b),
    "xnor": lambda a, b: 1 - (a ^ b),
    "not": lambda a, b=0: 1 - a,
}


@app.command(help=t("dig.truth.help"))
def truth(
    gate: str = typer.Argument(..., help=t("dig.truth.arg", gates=", ".join(GATES))),
    a: Optional[int] = typer.Option(None, "--a", "-a", min=0, max=1, help=t("dig.truth.opt.a")),
    b: Optional[int] = typer.Option(None, "--b", "-b", min=0, max=1, help=t("dig.truth.opt.b")),
):
    gate = gate.lower()
    if gate not in GATES:
        fail(t("dig.truth.unknown", gate=gate, gates=", ".join(GATES)))
    fn = GATES[gate]
    unary = gate == "not"

    if a is not None and (unary or b is not None):
        out = fn(a) if unary else fn(a, b)
        args = f"A={a}" if unary else f"A={a}, B={b}"
        if json_mode():
            print_json({"gate": gate, "a": a, "b": None if unary else b, "out": out})
            return
        console.print(f"[cyan]{gate.upper()}[/]({args}) = [bold green]{out}[/]")
        return

    tbl = Table(title=gate.upper())
    tbl.add_column("A", justify="center")
    if not unary:
        tbl.add_column("B", justify="center")
    tbl.add_column("Y", justify="center", style="bold green")
    records = []
    for inp in ([(0,), (1,)] if unary else itertools.product((0, 1), repeat=2)):
        tbl.add_row(*map(str, inp), str(fn(*inp)))
        records.append({**dict(zip("ab", inp)), "out": fn(*inp)})
    emit(tbl, records)


# --- Boolean ifade -----------------------------------------------------------------

_ALLOWED = (ast.Expression, ast.BoolOp, ast.BinOp, ast.UnaryOp, ast.Name, ast.Load,
            ast.And, ast.Or, ast.Not, ast.BitAnd, ast.BitOr, ast.BitXor, ast.Invert,
            ast.Constant)

# Operatör olarak yazılabilen kelimeler (tüm dillerde)
_WORDS = {
    "and": "&", "or": "|", "xor": "^", "not": "~",
    "ve": "&", "veya": "|", "değil": "~",
    "und": "&", "oder": "|", "nicht": "~",
    "и": "&", "или": "|", "не": "~",
}


def parse_expr(expr: str):
    """Güvenli boolean ifade ayrıştırıcı. Değişkenleri ve derlenmiş ifadeyi döndürür."""
    src = expr.replace("·", "&").replace("*", "&").replace("+", "|").replace("!", "~")
    src = " ".join(_WORDS.get(w.lower(), w) for w in src.split())
    try:
        tree = ast.parse(src, mode="eval")
    except SyntaxError:
        raise ValueError(t("dig.expr.invalid", expr=expr))
    names = set()
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED):
            raise ValueError(t("dig.expr.unsupported", node=type(node).__name__))
        if isinstance(node, ast.Constant) and node.value not in (0, 1):
            raise ValueError(t("dig.expr.const"))
        if isinstance(node, ast.Name):
            names.add(node.id)
    return sorted(names), compile(tree, "<expr>", "eval")


def evaluate(code, env: dict) -> int:
    return int(eval(code, {"__builtins__": {}}, env)) & 1


@app.command(help=t("dig.expr.help"))
def expr(expression: str = typer.Argument(..., help=t("dig.expr.arg"))):
    try:
        names, code = parse_expr(expression)
    except ValueError as e:
        fail(str(e))
    if len(names) > 6:
        fail(t("dig.expr.too_many"))

    tbl = Table(title=expression)
    for n in names:
        tbl.add_column(n, justify="center")
    tbl.add_column("Y", justify="center", style="bold green")
    minterms: List[int] = []
    rows = []
    for idx, combo in enumerate(itertools.product((0, 1), repeat=len(names))):
        out = evaluate(code, dict(zip(names, combo)))
        if out:
            minterms.append(idx)
        tbl.add_row(*map(str, combo), str(out))
        rows.append({**dict(zip(names, combo)), "Y": out})
    if json_mode():
        print_json({"expression": expression, "variables": names, "rows": rows, "minterms": minterms})
        return
    console.print(tbl)
    console.print(f"[cyan]Σm[/]({', '.join(map(str, minterms)) or '-'})")
