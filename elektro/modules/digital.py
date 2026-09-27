"""Dijital elektronik: sayı tabanları, mantık kapıları, boolean ifadeler."""

from __future__ import annotations

import ast
import itertools
from typing import List, Optional

import typer
from rich.table import Table

from elektro.ui import console, fail, result_panel

app = typer.Typer(help="Dijital: sayı tabanları, mantık kapıları, boolean ifadeler.", no_args_is_help=True)

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
        raise ValueError("taban 2 ile 36 arasında olmalı")
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
    pad = (-len(s)) % size
    s = "0" * pad + s
    return " ".join(s[i:i + size] for i in range(0, len(s), size))


@app.command()
def convert(
    value: str = typer.Argument(..., help="Sayı: 255, 0xFF, 0b1010, 0o17, 1Fh"),
    from_base: Optional[int] = typer.Option(None, "--from", "-f", help="Kaynak taban (varsayılan: önekten ya da 10)"),
    to_base_: Optional[int] = typer.Option(None, "--to", "-t", help="Sadece bu tabana çevir"),
    bits: Optional[int] = typer.Option(None, "--bits", "-b", help="Bit genişliği (negatifler için ikiye tümleyen)"),
):
    """Sayı tabanları arası dönüşüm (2-36).

    Hedef verilmezse ikili, sekizli, onlu ve onaltılı gösterimi birlikte verir.

    Örnekler:
      elektro logic convert 255
      elektro logic convert 0xFF -t 2
      elektro logic convert 1010 -f 2
      elektro logic convert --bits 8 -- -5
    """
    try:
        n = parse_int(value, from_base)
    except ValueError:
        fail(f"'{value}' geçerli bir sayı değil" + (f" (taban {from_base})" if from_base else ""))

    raw = n
    if bits:
        lo, hi = -(1 << (bits - 1)), (1 << bits) - 1
        if not lo <= n <= hi:
            fail(f"{n} değeri {bits} bite sığmaz ({lo} … {hi})")
        raw = n & ((1 << bits) - 1)

    if to_base_:
        try:
            console.print(f"[cyan]{value}[/] = [bold green]{to_base(raw, to_base_)}[/] (taban {to_base_})")
        except ValueError as e:
            fail(str(e))
        return

    width = bits or max(raw.bit_length(), 1)
    b = to_base(raw, 2).lstrip("-").zfill(width)
    rows = {
        "Onlu": str(n),
        "Onaltılı": "0x" + to_base(raw, 16),
        "İkili": "0b " + group(b, 4),
        "Sekizli": "0o" + to_base(raw, 8),
        "Bit sayısı": str(width),
    }
    if bits:
        rows["İşaretsiz"] = str(raw)
    if 32 <= raw < 127:
        rows["ASCII"] = repr(chr(raw))
    result_panel("Sayı Dönüşümü", rows)


GATES = {
    "and": lambda a, b: a & b,
    "or": lambda a, b: a | b,
    "xor": lambda a, b: a ^ b,
    "nand": lambda a, b: 1 - (a & b),
    "nor": lambda a, b: 1 - (a | b),
    "xnor": lambda a, b: 1 - (a ^ b),
    "not": lambda a, b=0: 1 - a,
}


@app.command()
def truth(
    gate: str = typer.Argument(..., help="Kapı: " + ", ".join(GATES)),
    a: Optional[int] = typer.Option(None, "--a", "-a", min=0, max=1, help="Giriş A (0/1)"),
    b: Optional[int] = typer.Option(None, "--b", "-b", min=0, max=1, help="Giriş B (0/1)"),
):
    """Mantık kapısı çıkışı veya (giriş verilmezse) doğruluk tablosu.

    Örnekler:
      elektro logic truth xor
      elektro logic truth nand -a 1 -b 1
    """
    gate = gate.lower()
    if gate not in GATES:
        fail(f"bilinmeyen kapı '{gate}' (seçenekler: {', '.join(GATES)})")
    fn = GATES[gate]
    unary = gate == "not"

    if a is not None and (unary or b is not None):
        out = fn(a) if unary else fn(a, b)
        args = f"A={a}" if unary else f"A={a}, B={b}"
        console.print(f"[cyan]{gate.upper()}[/]({args}) = [bold green]{out}[/]")
        return

    t = Table(title=gate.upper())
    t.add_column("A", justify="center")
    if not unary:
        t.add_column("B", justify="center")
    t.add_column("Y", justify="center", style="bold green")
    for inp in ([(0,), (1,)] if unary else itertools.product((0, 1), repeat=2)):
        t.add_row(*map(str, inp), str(fn(*inp)))
    console.print(t)


# --- Boolean ifade -----------------------------------------------------------------

_ALLOWED = (ast.Expression, ast.BoolOp, ast.BinOp, ast.UnaryOp, ast.Name, ast.Load,
            ast.And, ast.Or, ast.Not, ast.BitAnd, ast.BitOr, ast.BitXor, ast.Invert,
            ast.Constant)


def parse_expr(expr: str):
    """Güvenli boolean ifade ayrıştırıcı. Değişkenleri ve derlenmiş ifadeyi döndürür."""
    src = (expr.replace("·", "&").replace("*", "&").replace("+", "|")
           .replace("!", "~"))
    src = " ".join(
        {"and": "&", "or": "|", "xor": "^", "not": "~", "ve": "&", "veya": "|", "değil": "~"}.get(w.lower(), w)
        for w in src.split()
    )
    try:
        tree = ast.parse(src, mode="eval")
    except SyntaxError:
        raise ValueError(f"ifade anlaşılamadı: {expr}")
    names = set()
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED):
            raise ValueError(f"desteklenmeyen öğe: {type(node).__name__}")
        if isinstance(node, ast.Constant) and node.value not in (0, 1):
            raise ValueError("sabit olarak sadece 0 ve 1 kullanılabilir")
        if isinstance(node, ast.Name):
            names.add(node.id)
    return sorted(names), compile(tree, "<ifade>", "eval")


def evaluate(code, env: dict) -> int:
    return int(eval(code, {"__builtins__": {}}, env)) & 1


@app.command()
def expr(
    expression: str = typer.Argument(..., help='Boolean ifade, örn: "A & B | ~C"'),
):
    """Boolean ifadenin doğruluk tablosu ve minterm listesi.

    Operatörler: & (VE), | (VEYA), ^ (XOR), ~ (DEĞİL). and/or/not/xor da yazılabilir.

    Örnekler:
      elektro logic expr "A & B | ~C"
      elektro logic expr "(A xor B) and C"
    """
    try:
        names, code = parse_expr(expression)
    except ValueError as e:
        fail(str(e))
    if len(names) > 6:
        fail("en fazla 6 değişken destekleniyor")

    t = Table(title=expression)
    for n in names:
        t.add_column(n, justify="center")
    t.add_column("Y", justify="center", style="bold green")
    minterms: List[int] = []
    for idx, combo in enumerate(itertools.product((0, 1), repeat=len(names))):
        env = dict(zip(names, combo))
        out = evaluate(code, env)
        if out:
            minterms.append(idx)
        t.add_row(*map(str, combo), str(out))
    console.print(t)
    console.print(f"[cyan]Σm[/]({', '.join(map(str, minterms)) or '-'})")
