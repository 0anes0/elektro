import typer
from rich.table import Table
from elektro.modules.utils import console

app = typer.Typer(help="Dijital elektronik araclari")

@app.command()
def convert(
    value: str = typer.Argument(..., help="Sayi (ornek: 255, FF, 1111)"),
    from_base: int = typer.Option(10, "--from", "-f", help="Kaynak taban (2,8,10,16)"),
    to_base: int = typer.Option(2, "--to", "-t", help="Hedef taban (2,8,10,16)"),
):
    """Sayi sistemleri arasi donusum"""
    try:
        decimal = int(value, from_base)
    except ValueError:
        console.print(f"[red]Gecersiz sayi '{value}' taban {from_base} icin[/]")
        return
    
    if to_base == 2:
        result = bin(decimal)[2:]
    elif to_base == 8:
        result = oct(decimal)[2:]
    elif to_base == 10:
        result = str(decimal)
    elif to_base == 16:
        result = hex(decimal)[2:].upper()
    else:
        console.print("[red]Desteklenen tabanlar: 2, 8, 10, 16[/]")
        return
    
    console.print(f"[cyan]{value}[/] (taban {from_base}) = [bold green]{result}[/] (taban {to_base})")

@app.command()
def truth(
    gate: str = typer.Argument(..., help="Kapı: and, or, not, nand, nor, xor, xnor"),
    a: int = typer.Option(0, "--a", help="Giris A (0 veya 1)"),
    b: int = typer.Option(0, "--b", help="Giris B (0 veya 1)"),
    all_table: bool = typer.Option(False, "--all", help="Tam dogruluk tablosu"),
):
    """Mantik kapilari dogruluk tablosu"""
    gate = gate.lower()
    valid = ["and", "or", "not", "nand", "nor", "xor", "xnor"]
    
    if gate not in valid:
        console.print(f"[red]Gecersiz kapı: {gate}[/]")
        console.print(f"[dim]Desteklenenler: {', '.join(valid)}[/]")
        return
    
    if all_table:
        console.print(f"\n[bold]{gate.upper()} Dogruluk Tablosu[/]")
        table = Table(show_header=True, border_style="cyan")
        table.add_column("A", style="bold")
        if gate != "not":
            table.add_column("B", style="bold")
        table.add_column("Cikis", style="bold green")
        
        inputs = [(0,0), (0,1), (1,0), (1,1)] if gate != "not" else [(0,), (1,)]
        
        for inp in inputs:
            a_val = inp[0]
            b_val = inp[1] if len(inp) > 1 else 0
            out = calculate_gate(gate, a_val, b_val)
            if gate == "not":
                table.add_row(str(a_val), str(int(out)))
            else:
                table.add_row(str(a_val), str(b_val), str(int(out)))
        console.print(table)
    else:
        out = calculate_gate(gate, a, b)
        console.print(f"[cyan]{gate.upper()}[/](A={a}, B={b}) = [bold green]{int(out)}[/]")

def calculate_gate(gate, a, b):
    if gate == "and": return a & b
    if gate == "or": return a | b
    if gate == "not": return not a
    if gate == "nand": return not (a & b)
    if gate == "nor": return not (a | b)
    if gate == "xor": return a ^ b
    if gate == "xnor": return not (a ^ b)
    return 0
