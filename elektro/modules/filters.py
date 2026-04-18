import typer
import math
from elektro.modules.utils import console, format_number, result_panel

app = typer.Typer(help="RC/RL/LC filtre analizi")

@app.command()
def rc(
    r: float = typer.Option(..., "--r", help="Dirench (Ohm)"),
    c: float = typer.Option(..., "--c", help="Kapasitans (Farad)"),
):
    """RC dusuk geciren filtre (Low-Pass)"""
    fc = 1 / (2 * math.pi * r * c)
    tau = r * c
    
    result_panel("RC Dusuk Geciren Filtre", {
        "Kesim Frekansi (fc)": format_number(fc, "Hz"),
        "Acisal Frekans (w)": format_number(2 * math.pi * fc, "rad/s"),
        "Zaman Sabiti (τ)": format_number(tau, "s"),
        "Dirench (R)": format_number(r, "Ohm"),
        "Kapasitans (C)": format_number(c, "F"),
    })
    
    console.print("\n[bold cyan]Teori:[/]")
    console.print("fc = 1 / (2πRC) -3dB kesim noktasi")
    console.print("τ = RC - Zaman sabiti (tau suresinde %63 yuklenir)\n")
    
    console.print("[bold]ASCII Bode Plot:[/]")
    for i in range(-3, 4):
        f = fc * (2 ** i)
        if f <= fc:
            gain = 0
            phase = -45 * (f/fc)
        else:
            gain = -20 * math.log10(f/fc)
            phase = -90
        
        bar = "█" * int(abs(gain)/3)
        marker = "▼" if i == 0 else " "
        console.print(f"{marker}{format_number(f,'Hz').rjust(12)} │{bar} {gain:5.1f} dB {phase:5.1f}°")

@app.command()
def rl(
    r: float = typer.Option(..., "--r", help="Dirench (Ohm)"),
    l: float = typer.Option(..., "--l", help="Enduktans (Henry)"),
):
    """RL yuksek geciren filtre (High-Pass)"""
    fc = r / (2 * math.pi * l)
    tau = l / r
    
    result_panel("RL Yuksek Geciren Filtre", {
        "Kesim Frekansi (fc)": format_number(fc, "Hz"),
        "Zaman Sabiti (τ)": format_number(tau, "s"),
        "Dirench (R)": format_number(r, "Ohm"),
        "Enduktans (L)": format_number(l, "H"),
    })
    
    console.print("\n[bold cyan]Teori:[/]")
    console.print("fc = R / (2πL) -3dB kesim noktasi")
    console.print("Yuksek frekanslar gecer, DC engellenir\n")

@app.command()
def lc(
    l: float = typer.Option(..., "--l", help="Enduktans (Henry)"),
    c: float = typer.Option(..., "--c", help="Kapasitans (Farad)"),
):
    """LC rezonans devresi (Band-Pass)"""
    fr = 1 / (2 * math.pi * math.sqrt(l * c))
    xl = 2 * math.pi * fr * l
    xc = 1 / (2 * math.pi * fr * c)
    
    result_panel("LC Rezonans Devresi", {
        "Rezonans Frekansi (fr)": format_number(fr, "Hz"),
        "Enduktif Reaktans (XL)": format_number(xl, "Ohm"),
        "Kapasitif Reaktans (XC)": format_number(xc, "Ohm"),
        "L": format_number(l, "H"),
        "C": format_number(c, "F"),
    })
    
    console.print("\n[bold cyan]Teori:[/]")
    console.print("fr = 1 / (2π√(LC)) - Rezonans frekansi")
    console.print("XL = XC oldugunda seri rezonans olusur")
    console.print("Bu frekansta empedans minimumdur (seri) veya maksimumdur (paralel)\n")
    
    console.print("[bold]Frekans Yaniti:[/]")
    for mult in [0.5, 0.7, 1.0, 1.4, 2.0]:
        f = fr * mult
        if mult == 1.0:
            marker = "★"
            z = "Min Z (Rezonans)"
        else:
            marker = " "
            detune = abs(mult - 1) * 100
            z = f"±{detune:.0}% sapma"
        console.print(f"{marker} {format_number(f,'Hz').rjust(12)} │ {z}")

@app.command()
def rlc(
    r: float = typer.Option(..., "--r", help="Dirench (Ohm)"),
    l: float = typer.Option(..., "--l", help="Enduktans (Henry)"),
    c: float = typer.Option(..., "--c", help="Kapasitans (Farad)"),
):
    """Seri RLC band-pass filtre"""
    fr = 1 / (2 * math.pi * math.sqrt(l * c))
    bw = r / (2 * math.pi * l)
    q = fr / bw if bw > 0 else float('inf')
    
    result_panel("Seri RLC Band-Pass Filtre", {
        "Rezonans Frekansi (fr)": format_number(fr, "Hz"),
        "Bant Genisligi (BW)": format_number(bw, "Hz"),
        "Kalite Faktoru (Q)": f"{q:.2f}",
        "Alt Kesim (fr - BW/2)": format_number(fr - bw/2, "Hz"),
        "Ust Kesim (fr + BW/2)": format_number(fr + bw/2, "Hz"),
    })
    
    console.print("\n[bold cyan]Teori:[/]")
    console.print("fr = 1 / (2π√(LC)) - Merkez frekans")
    console.print("BW = R / (2πL) - -3dB bant genisligi")
    console.print("Q = fr / BW - Selektivite (yuksek Q = dar bant)")
    console.print(f"\nBu filtre {format_number(fr-bw/2,'Hz')} ile {format_number(fr+bw/2,'Hz')} arasindaki frekanslari gecirir.")

@app.command()
def notch(
    r: float = typer.Option(..., "--r", help="Dirench (Ohm)"),
    l: float = typer.Option(..., "--l", help="Enduktans (Henry)"),
    c: float = typer.Option(..., "--c", help="Kapasitans (Farad)"),
):
    """Paralel RLC band-stop filtre (Notch)"""
    fr = 1 / (2 * math.pi * math.sqrt(l * c))
    q = r / (2 * math.pi * fr * l) if fr > 0 else 0
    
    result_panel("Paralel RLC Band-Stop Filtre (Notch)", {
        "Sondurme Frekansi (fr)": format_number(fr, "Hz"),
        "Kalite Faktoru (Q)": f"{q:.2f}",
        "Bant Genisligi": format_number(fr/q, "Hz") if q > 0 else "N/A",
    })
    
    console.print("\n[bold cyan]Teori:[/]")
    console.print("Paralel RLC devresi rezonansta maksimum empedans gosterir.")
    console.print("Bu frekansta akim minimumdur, sinyal sondurulur.")
    console.print("50/60 Hz gurultu eliminasyonu icin kullanilir.\n")
    
    console.print("[bold]Uygulama:[/] 50 Hz sebeke gurultusu filtreleme")
    console.print(f"Ornek: elektro filter notch --r 1000 --l 5.07 --c 10e-6")
    console.print(f"(L=5.07H, C=10uF → fr ≈ 50 Hz)")

@app.command()
def theory():
    """Filtre teorisi ozeti"""
    console.print(Panel(
        "[bold]FILTRE TIPLERI OZETI[/]\n\n"
        "[bold]1. Dusuk Geciren (Low-Pass):[/]\n"
        "   - RC: R seri, C paralel (toprak)\n"
        "   - RL: L seri, R paralel\n"
        "   - fc alti gecer, ustu zayiflar\n\n"
        "[bold]2. Yuksek Geciren (High-Pass):[/]\n"
        "   - RC: C seri, R paralel\n"
        "   - RL: R seri, L paralel\n"
        "   - fc ustu gecer, alti zayiflar\n\n"
        "[bold]3. Band-Pass:[/]\n"
        "   - Seri RLC: Rezonansta minimum Z\n"
        "   - Dar bant, yuksek Q\n\n"
        "[bold]4. Band-Stop (Notch):[/]\n"
        "   - Paralel RLC: Rezonansta maksimum Z\n"
        "   - Tek frekansi sondurur\n\n"
        "[bold]Formul Ozeti:[/]\n"
        "   fc(RC) = 1/(2πRC)    fc(RL) = R/(2πL)\n"
        "   fr(LC) = 1/(2π√(LC))  Q = fr/BW",
        border_style="bright_blue", title="[bold]Filtre Teorisi[/]"
    ))
