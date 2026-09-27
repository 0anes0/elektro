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


# --- Sadeleştirme (Quine-McCluskey) --------------------------------------------------------

def _combine(a: str, b: str) -> Optional[str]:
    """'0-1' ve '0-0' gibi iki kalıp tek bitte farklıysa birleştirir."""
    diff = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    if len(diff) == 1 and "-" not in (a[diff[0]], b[diff[0]]):
        i = diff[0]
        return a[:i] + "-" + a[i + 1:]
    return None


def _covers(pattern: str, m: int, n: int) -> bool:
    bits = format(m, f"0{n}b")
    return all(p in ("-", b) for p, b in zip(pattern, bits))


def prime_implicants(minterms: List[int], dontcares: List[int], n: int) -> List[str]:
    current = {format(m, f"0{n}b") for m in set(minterms) | set(dontcares)}
    primes = set()
    while current:
        merged, used = set(), set()
        items = sorted(current)
        for i, a in enumerate(items):
            for b in items[i + 1:]:
                c = _combine(a, b)
                if c:
                    merged.add(c)
                    used.update((a, b))
        primes |= current - used
        current = merged
    return sorted(primes)


def _cost(terms) -> tuple:
    return (len(terms), sum(n.count("0") + n.count("1") for n in terms))


def minimal_cover(minterms: List[int], dontcares: List[int], n: int) -> List[str]:
    """En az terimli (eşitlikte en az literal) örtü: esas asal terimler + kalan için arama."""
    if not minterms:
        return []
    primes = prime_implicants(minterms, dontcares, n)
    remaining = set(minterms)
    chosen = []
    # Esas asal terimler
    for m in sorted(minterms):
        covering = [p for p in primes if _covers(p, m, n)]
        if len(covering) == 1 and covering[0] not in chosen:
            chosen.append(covering[0])
    for p in chosen:
        remaining -= {m for m in remaining if _covers(p, m, n)}
    if not remaining:
        return sorted(chosen, key=_literal_sort)
    candidates = [p for p in primes if p not in chosen and any(_covers(p, m, n) for m in remaining)]
    best = None
    if len(candidates) <= 18:
        for size in range(1, len(candidates) + 1):
            for combo in itertools.combinations(candidates, size):
                if all(any(_covers(p, m, n) for p in combo) for m in remaining):
                    if best is None or _cost(combo) < _cost(best):
                        best = combo
            if best is not None:
                break
    else:   # çok büyük: açgözlü seçim
        best, left = [], set(remaining)
        while left:
            p = max(candidates, key=lambda c: (sum(_covers(c, m, n) for m in left), -_cost([c])[1]))
            best.append(p)
            left -= {m for m in left if _covers(p, m, n)}
    return sorted(chosen + list(best), key=_literal_sort)


def _literal_sort(p: str):
    return (-p.count("-"), p.replace("-", "2"))


def to_expr(terms: List[str], names: List[str], style: str = "code") -> str:
    if not terms:
        return "0"
    if all(set(p) == {"-"} for p in terms):
        return "1"
    parts = []
    for p in terms:
        lits = []
        for bit, name in zip(p, names):
            if bit == "1":
                lits.append(name)
            elif bit == "0":
                lits.append(f"~{name}" if style == "code" else f"{name}'")
        parts.append((" & " if style == "code" else "").join(lits))
    if style == "code":
        return " | ".join(f"({x})" if " & " in x and len(parts) > 1 else x for x in parts)
    return " + ".join(parts)


GRAY = {1: ["0", "1"], 2: ["00", "01", "11", "10"]}


def kmap_table(names: List[str], ones: set, dcs: set) -> Optional[Table]:
    n = len(names)
    if not 2 <= n <= 4:
        return None
    row_bits, col_bits = n // 2, n - n // 2
    rows, cols = GRAY[row_bits], GRAY[col_bits]
    tbl = Table(title="K-map", show_lines=True)
    tbl.add_column("".join(names[:row_bits]) + " \\ " + "".join(names[row_bits:]), style="bold")
    for c in cols:
        tbl.add_column(c, justify="center")
    for r in rows:
        cells = []
        for c in cols:
            m = int(r + c, 2)
            cells.append("[bold green]1[/]" if m in ones else "[yellow]x[/]" if m in dcs else "[dim]0[/]")
        tbl.add_row(r, *cells)
    return tbl


def _parse_int_list(text: Optional[str]) -> List[int]:
    if not text:
        return []
    try:
        return sorted({int(x) for x in text.replace(" ", ",").split(",") if x})
    except ValueError:
        raise ValueError(t("dig.simp.bad_list"))


@app.command(help=t("dig.simp.help"))
def simplify(
    expression: Optional[str] = typer.Argument(None, help=t("dig.simp.arg")),
    minterms: Optional[str] = typer.Option(None, "--minterms", "-m", help=t("dig.simp.opt.minterms")),
    dontcare: Optional[str] = typer.Option(None, "--dontcare", "-d", help=t("dig.simp.opt.dontcare")),
    variables: Optional[str] = typer.Option(None, "--vars", "-v", help=t("dig.simp.opt.vars")),
):
    try:
        dcs = _parse_int_list(dontcare)
        if expression:
            names, code = parse_expr(expression)
            ones = [i for i, combo in enumerate(itertools.product((0, 1), repeat=len(names)))
                    if evaluate(code, dict(zip(names, combo)))]
        else:
            ones = _parse_int_list(minterms)
            if not ones and not minterms:
                fail(t("dig.simp.need"))
            top = max(ones + dcs + [1])
            count = max(1, top.bit_length())
            names = ([x.strip() for x in variables.split(",") if x.strip()] if variables
                     else [chr(ord("A") + i) for i in range(count)])
            if len(names) < count:
                fail(t("dig.simp.few_vars", n=count))
    except ValueError as e:
        fail(str(e))
    if len(names) > 8:
        fail(t("dig.simp.too_many"))
    n = len(names)
    dcs = [d for d in dcs if d not in ones and d < 2 ** n]
    cover = minimal_cover(ones, dcs, n)
    code_form, math_form = to_expr(cover, names, "code"), to_expr(cover, names, "math")
    if json_mode():
        print_json({"variables": names, "minterms": ones, "dontcares": dcs, "sop": code_form,
                    "sop_math": math_form, "prime_implicants": prime_implicants(ones, dcs, n) if ones else []})
        return
    km = kmap_table(names, set(ones), set(dcs))
    if km:
        console.print(km)
    result_panel(t("dig.simp.title"), {
        t("dig.simp.minterms"): f"Σm({', '.join(map(str, ones)) or '-'})" + (f" + d({', '.join(map(str, dcs))})" if dcs else ""),
        t("dig.simp.result"): f"[bold]{math_form}[/]",
        t("dig.simp.code"): code_form,
        t("dig.simp.cost"): t("dig.simp.cost_val", terms=len(cover),
                               lits=sum(p.count("0") + p.count("1") for p in cover)),
    })
