import typer
import math
from elektro.modules.utils import console, format_number, result_panel

app = typer.Typer(help="RF link budget ve birim donusumleri")

@app.command()
def fspl(
    freq: float = typer.Option(..., "--freq", "-f", help="Frekans (MHz)"),
    dist: float = typer.Option(..., "--dist", "-d", help="Mesafe (km)"),
):
    """Free Space Path Loss (ITU-R P.525-4)"""
    fspl = 32.45 + 20 * math.log10(freq) + 20 * math.log10(dist)
    result_panel("FSPL Hesaplama", {
        "Frekans": format_number(freq, "MHz"),
        "Mesafe": format_number(dist, "km"),
        "FSPL": f"{fspl:.2f} dB",
    })
    
    rx = 14 + 2 + 2 - fspl
    margin = rx - (-120)
    color = "green" if margin > 10 else "red"
    console.print(f"\n[bold]Ornek Link Margin:[/] [{color}]{margin:.1f} dB[/]")

@app.command()
def convert(
    value: float = typer.Argument(..., help="Deger"),
    from_u: str = typer.Argument(..., help="Kaynak (dbm, watt, vswr)"),
    to_u: str = typer.Argument(..., help="Hedef (watt, dbm, rl)"),
):
    """Birim donusumu"""
    f = from_u.lower()
    t = to_u.lower()
    
    if f == "dbm" and t == "watt":
        res = (10 ** (value/10)) / 1000
        console.print(f"{value} dBm = {format_number(res, 'W')}")
    elif f == "watt" and t == "dbm":
        res = 10 * math.log10(value * 1000)
        console.print(f"{format_number(value, 'W')} = {res:.2f} dBm")
    elif f == "vswr" and t == "rl":
        if value < 1:
            console.print("[red]VSWR >= 1 olmali![/]")
            return
        res = -20 * math.log10((value-1)/(value+1))
        console.print(f"VSWR {value} = {res:.2f} dB Return Loss")
    else:
        console.print("[red]Desteklenmiyor:[/] dbm<->watt, vswr->rl")
