import typer
from rich.table import Table
from elektro.modules.utils import console

app = typer.Typer(help="Dirench renk kodu cozucu")

CODE_MAP = {
    "s":  ("siyah", 0, 1, None),
    "k":  ("kahverengi", 1, 10, 1),
    "r":  ("kirmizi", 2, 100, 2),
    "t":  ("turuncu", 3, 1000, None),
    "sa": ("sari", 4, 10000, None),
    "y":  ("yesil", 5, 100000, 0.5),
    "m":  ("mavi", 6, 1000000, 0.25),
    "mo": ("mor", 7, 10000000, 0.1),
    "g":  ("gri", 8, None, 0.05),
    "b":  ("beyaz", 9, None, None),
    "a":  ("altin", None, 0.1, 5),
    "gu": ("gumus", None, 0.01, 10),
}

RICH = {"siyah": "black", "kahverengi": "rgb(139,69,19)", "kirmizi": "red",
        "turuncu": "bright_red", "sari": "yellow", "yesil": "green",
        "mavi": "blue", "mor": "purple", "gri": "grey",
        "beyaz": "white", "altin": "gold1", "gumus": "grey70"}

def resolve(code: str):
    code = code.lower()
    if code in CODE_MAP:
        return CODE_MAP[code]
    for k, v in CODE_MAP.items():
        if v[0] == code:
            return v
    return None

@app.callback(invoke_without_command=True)
def resistor(
    ctx: typer.Context,
    b1: str = typer.Argument(None, help="1. bant kodu"),
    b2: str = typer.Argument(None, help="2. bant kodu"),
    mult: str = typer.Argument(None, help="Carpan kodu"),
    tol: str = typer.Argument(None, help="Tolerans kodu"),
    b3: str = typer.Argument(None, help="3. bant (5 bantli)"),
):
    """Dirench renk kodu: elektro resistor k s r a"""
    if ctx.invoked_subcommand is not None:
        return
    
    if b1 is None:
        show_table()
        return
    
    c1 = resolve(b1)
    c2 = resolve(b2)
    c_mult = resolve(mult)
    c_tol = resolve(tol)
    c3 = resolve(b3) if b3 else None
    
    if None in [c1, c2, c_mult, c_tol]:
        console.print("[red]Gecersiz renk kodu![/]")
        console.print("[dim]Ornek: k s r a -> 1kOhm ±5%[/]")
        console.print("[dim]Tablo icin: elektro resistor table[/]")
        return
    
    digit1, digit2 = c1[1], c2[1]
    multiplier = c_mult[2]
    tolerance = c_tol[3]
    
    if c3:
        value = (digit1 * 100 + digit2 * 10 + c3[1]) * multiplier
    else:
        value = (digit1 * 10 + digit2) * multiplier
    
    if value >= 1e6:
        val_str = f"{value/1e6:.2f} MOhm"
    elif value >= 1e3:
        val_str = f"{value/1e3:.2f} kOhm"
    else:
        val_str = f"{value:.2f} Ohm"
    
    min_v = value * (1 - tolerance/100)
    max_v = value * (1 + tolerance/100)
    
    table = Table(title="Dirench Degeri", border_style="green")
    table.add_column("Ozellik", style="cyan")
    table.add_column("Deger", style="bold yellow")
    table.add_row("Nominal", val_str)
    table.add_row("Tolerans", f"±{tolerance}%")
    table.add_row("Aralik", f"{min_v:.2f} - {max_v:.2f} Ohm")
    
    names = [c1[0], c2[0]]
    if c3:
        names.append(c3[0])
    names.extend([c_mult[0], c_tol[0]])
    
    visual = " ".join(f"[{RICH.get(n,'white')}]{n[:3].upper()}[/]" for n in names)
    table.add_row("Bantlar", visual)
    console.print(table)

@app.command()
def table():
    """Renk kodu referans tablosu"""
    show_table()

def show_table():
    t = Table(title="Dirench Renk Kodlari")
    t.add_column("Kod", style="bold cyan")
    t.add_column("Renk", style="bold")
    t.add_column("Rakam")
    t.add_column("Carpan")
    t.add_column("Tolerans")
    
    for code, (name, digit, mult, tol) in CODE_MAP.items():
        t.add_row(
            code,
            f"[{RICH.get(name,'white')}]{name.title()}[/]",
            str(digit) if digit is not None else "-",
            str(mult) if mult is not None else "-",
            f"{tol}%" if tol is not None else "-"
        )
    console.print(t)
