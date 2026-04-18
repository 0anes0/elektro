import typer
from typing import Optional
from rich.prompt import Prompt
from elektro.modules.utils import console, format_number, result_panel

app = typer.Typer(help="Ohm kanunu ve guc hesaplamalari")

@app.callback(invoke_without_command=True)
def ohm(
    ctx: typer.Context,
    v: Optional[float] = typer.Option(None, "--voltage", "-v", help="Gerilim (V)"),
    i: Optional[float] = typer.Option(None, "--current", "-i", help="Akim (A)"),
    r: Optional[float] = typer.Option(None, "--resistance", "-r", help="Dirench (Ohm)"),
    p: Optional[float] = typer.Option(None, "--power", "-p", help="Guc (W)"),
):
    """Ohm kanunu: 2 parametre girin. Ornek: elektro ohm -v 12 -r 1000"""
    if ctx.invoked_subcommand is not None:
        return
    
    known = sum(x is not None for x in [v, i, r, p])
    if known == 0:
        console.print("[dim]Ornek: elektro ohm -v 12 -r 1000[/]")
        raise typer.Exit()
    if known < 2:
        console.print("[bold red]Hata:[/] En az 2 parametre girmelisiniz!")
        raise typer.Exit(1)
    
    if v is not None and i is not None:
        r_calc, p_calc = v / i, v * i
        if r is not None and abs(r - r_calc) > 0.01 * r:
            console.print("[yellow]Uyari: Girilen R ile hesaplanan R tutarsiz![/]")
        r, p = r_calc, p_calc
    elif v is not None and r is not None:
        i, p = v / r, v ** 2 / r
    elif i is not None and r is not None:
        v, p = i * r, i ** 2 * r
    elif v is not None and p is not None:
        i, r = p / v, v ** 2 / p
    elif i is not None and p is not None:
        v, r = p / i, p / i ** 2
    elif r is not None and p is not None:
        v, i = (p * r) ** 0.5, (p / r) ** 0.5
    
    result_panel("Ohm Kanunu Sonuclari", {
        "Gerilim (V)": format_number(v, "V"),
        "Akim (I)": format_number(i, "A"),
        "Dirench (R)": format_number(r, "Ohm"),
        "Guc (P)": format_number(p, "W"),
    })

@app.command()
def interactive():
    """Interaktif Ohm sihirbazi"""
    console.print("[bold]Ohm Kanunu Sihirbazi[/] (x = bilinmeyen)\n")
    
    v = Prompt.ask("Gerilim V (Volt)", default="x")
    i = Prompt.ask("Akim I (Amper)", default="x")
    r = Prompt.ask("Dirench R (Ohm)", default="x")
    
    vals = {}
    for key, val in [("v", v), ("i", i), ("r", r)]:
        vals[key] = float(val) if val.lower() != "x" else None
    
    known = sum(1 for v in vals.values() if v is not None)
    if known != 2:
        console.print("[red]Tam olarak 2 deger girmelisiniz![/]")
        return
    
    ohm(v=vals.get("v"), i=vals.get("i"), r=vals.get("r"))

