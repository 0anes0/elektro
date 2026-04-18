import typer
import subprocess
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from elektro.modules import basic, resistor, filters, rf, digital, datasheet as datasheet_modul

app = typer.Typer(
    name="elektro",
    help="Terminal tabanli Elektrik-Elektronik Muhendisligi araci",
    add_completion=False,
)
console = Console()

app.add_typer(basic.app, name="ohm", help="[Temel] Ohm kanunu ve guc")
app.add_typer(resistor.app, name="resistor", help="[Temel] Dirench renk kodu")
app.add_typer(filters.app, name="filter", help="[Sinyal] RC/RL/LC filtreler")
app.add_typer(rf.app, name="rf", help="[RF] Link budget ve birim donusumleri")
app.add_typer(digital.app, name="logic", help="[Dijital] Sayi sistemleri ve boolean")

@app.command()
def datasheet(
    component: str = typer.Argument(..., help="Komponent adi (ornek: lm358, ne555, 2n2222)"),
    output: str = typer.Option(None, "--output", "-o", help="Kaydetme adi (varsayilan: komponent_datasheet.pdf)"),
    max_try: int = typer.Option(10, "--max-try", "-n", help="Maksimum deneme", hidden=True),
):
    """
    Komponent datasheet'ini otomatik bul ve indir.
    
    Ornekler:
        elektro datasheet lm358
        elektro datasheet ne555
        elektro datasheet "2n2222a" -o transistor.pdf
    """
    success = datasheet_modul.download_datasheet(component, output=output, max_try=max_try)
    if not success:
        raise typer.Exit(1)


def show_menu():
    table = Table(show_header=False, box=box.ROUNDED, border_style="bright_blue")
    table.add_column("Komut", style="bold cyan", no_wrap=True)
    table.add_column("Kategori", style="bold yellow", no_wrap=True)
    table.add_column("Ornek", style="white")
    
    table.add_row("ohm", "[Temel]", "elektro ohm -v 12 -r 1000")
    table.add_row("resistor", "[Temel]", "elektro resistor k s r a")
    table.add_row("filter", "[Sinyal]", "elektro filter rc --r 1k --c 100n")
    table.add_row("rf", "[RF]", "elektro rf fspl -f 868 -d 5")
    table.add_row("logic", "[Dijital]", "elektro logic convert 255 -t 16")
    table.add_row("datasheet", "[Arac]", "elektro datasheet [KOMPONENT]")
    table.add_row("helpall", "[Yardim]", "elektro helpall")
    
    console.print(Panel(table, title="[bold yellow]⚡ ELEKTRO v0.1.0[/]", 
                       subtitle="[dim]elektro [komut] --help[/]",
                       border_style="bright_blue"))

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Elektro - EE Terminal Araci"""
    if ctx.invoked_subcommand is None:
        show_menu()

@app.command()
def menu():
    """Ana menuyu goster"""
    show_menu()

def get_help_text():
    """Man sayfasi formatinda yardim metni"""
    text = """
ELEKTRO(1)                    Kullanici Komutlari                    ELEKTRO(1)

ISIM
       elektro - Terminal tabanli Elektrik-Elektronik Muhendisligi araci

KULLANIM
       elektro [KOMUT] [SECENEKLER]
       elektro helpall

KOMUTLAR
       ohm
           Ohm kanunu ve guc hesaplamalari

       resistor
           Dirench renk kodu cozucu

       filter
           RC/RL/LC filtre analizi

       rf
           RF link budget ve birim donusumleri

       logic
           Dijital elektronik araclari

       menu
           Ana menuyu goster

       helpall
           Bu yardim sayfasini goster (man tarzinda)

===============================================================================
                              TEMEL KOMUTLAR
===============================================================================

OHM KANUNU
       elektro ohm [SECENEKLER]

       Ohm kanunu: V = I × R
       Guc formulu: P = V × I = I² × R = V² / R

       Secenekler:
           -v, --voltage      Gerilim (Volt)
           -i, --current      Akim (Amper)
           -r, --resistance   Dirench (Ohm)
           -p, --power        Guc (Watt)

       Ornekler:
           elektro ohm -v 12 -r 1000
               12V ve 1kOhm girilir, akim ve guc hesaplanir

           elektro ohm -i 0.01 -p 0.5
               10mA ve 0.5W girilir, gerilim ve dirench hesaplanir

           elektro ohm interactive
               Sorularla interaktif mod

DIRENC RENK KODU
       elektro resistor [BANT1] [BANT2] [CARPAN] [TOLERANS] [BANT3]

       4 veya 5 bantli direnclerin degerini renk kodlarindan hesaplar.

       Kisa Kodlar:
           s   = Siyah     (0)
           k   = Kahverengi (1, x10, ±1%)
           r   = Kirmizi   (2, x100, ±2%)
           t   = Turuncu   (3, x1000)
           sa  = Sari      (4, x10000)
           y   = Yesil     (5, x100000, ±0.5%)
           m   = Mavi      (6, x1M, ±0.25%)
           mo  = Mor       (7, x10M, ±0.1%)
           g   = Gri       (8, ±0.05%)
           b   = Beyaz     (9)
           a   = Altin     (x0.1, ±5%)
           gu  = Gumus     (x0.01, ±10%)

       Ornekler:
           elektro resistor k s r a
               1kOhm ±5% (Kahverengi-Siyah-Kirmizi-Altin)

           elektro resistor table
               Tum renk kodu tablosunu goster

===============================================================================
                              FILTRELER
===============================================================================

RC DUSUK GECIREN FILTRE (Low-Pass)
       elektro filter rc --r DIRENC --c KAPASITANS

       Bir dirench ve bir kapasitorden olusan dusuk geciren filtre.
       Dusuk frekanslar gecer, yuksek frekanslar zayiflar.

       Matematiksel Model:
           H(s) = 1 / (1 + sRC)
           fc = 1 / (2πRC)    [Kesim frekansi, -3dB]
           τ = RC             [Zaman sabiti]

       Ornek:
           elektro filter rc --r 1000 --c 100e-9
               R=1kOhm, C=100nF → fc ≈ 1.59 kHz

       Uygulamalar:
           - Guc kaynagi yumusatma
           - Yuksek frekans gurultu filtreleme
           - Anti-aliasing filtreleri

RL YUKSEK GECIREN FILTRE (High-Pass)
       elektro filter rl --r DIRENC --l ENDUKTANS

       Bir dirench ve bir bobinden olusan yuksek geciren filtre.
       Yuksek frekanslar gecer, dusuk frekanslar (DC) engellenir.

       Matematiksel Model:
           H(s) = sL / (R + sL)
           fc = R / (2πL)

       Uygulamalar:
           - DC engelleme (kondansator mikrofonlari)
           - AC kuplaj
           - RF devrelerinde DC engelleme

LC REZONANS DEVRESI (Band-Pass)
       elektro filter lc --l ENDUKTANS --c KAPASITANS

       Bir bobin ve bir kapasitorden olusan rezonans devresi.
       Sadece belirli bir frekansta maksimum iletim saglar.

       Matematiksel Model:
           fr = 1 / (2π√(LC))     [Rezonans frekansi]
           XL = 2πfrL             [Enduktif reaktans]
           XC = 1/(2πfrC)         [Kapasitif reaktans]

       Ornek:
           elektro filter lc --l 10e-6 --c 100e-9
               L=10uH, C=100nF → fr ≈ 159 kHz

       Uygulamalar:
           - Radyo alicilari (tuning devreleri)
           - Osilatorler
           - Dar bantli filtreler

SERI RLC BAND-PASS FILTRE
       elektro filter rlc --r DIRENC --l ENDUKTANS --c KAPASITANS

       Seri bagli RLC elemanlarindan olusan band-pass filtre.

       Matematiksel Model:
           fr = 1 / (2π√(LC))         [Merkez frekansi]
           BW = R / (2πL)             [Bant genisligi]
           Q = fr / BW                [Kalite faktoru]

       Q Faktoru:
           Yuksek Q → Dar bant, yuksek selektivite
           Dusuk Q → Genis bant, dusuk selektivite

PARALEL RLC BAND-STOP FILTRE (NOTCH)
       elektro filter notch --r DIRENC --l ENDUKTANS --c KAPASITANS

       Paralel RLC devresi, rezonans frekansinda sinyali sondurur.

       Uygulamalar:
           - 50/60 Hz sebeke gurultusu eliminasyonu
           - Tek frekansi sondurme (interferans)

       Ornek (50 Hz notch):
           elektro filter notch --r 1000 --l 5.07 --c 10e-6

===============================================================================
                              RF HESAPLAMALARI
===============================================================================

FREE SPACE PATH LOSS (FSPL)
       elektro rf fspl --freq MHZ --dist KM

       Serbest uzayda sinyal zayiflamasini hesaplar.
       ITU-R P.525-4 standardina gore:

       Formul:
           FSPL(dB) = 32.45 + 20×log₁₀(f) + 20×log₁₀(d)

       Parametreler:
           f = Frekans (MHz)
           d = Mesafe (km)

       Ornek:
           elektro rf fspl --freq 868 --dist 5
               868 MHz, 5 km → ~106 dB kayip

       Link Butcesi Hesaplama:
           TX Gucu: 14 dBm (tipik LoRa)
           Anten Kazanci: +2 dBi (her iki taraf)
           Toplam: 18 dBm
           FSPL (868MHz, 5km): -106 dB
           RX Seviyesi: -88 dBm
           RX Hassasiyeti: -120 dBm
           Link Margin: 32 dB (Guvenli!)

BIRIM DONUSUMLERI
       elektro rf convert DEGER KAYNAK HEDEF

       Desteklenen donusumler:
           dbm → watt
           watt → dbm
           vswr → rl (return loss)

       Ornekler:
           elektro rf convert 14 dbm watt      → 0.025 W
           elektro rf convert 0.1 watt dbm     → 20 dBm
           elektro rf convert 1.5 vswr rl      → 14 dB

===============================================================================
                              DIJITAL ELEKTRONIK
===============================================================================

SAYI SISTEMLERI DONUSUMU
       elektro logic convert SAYI [SECENEKLER]

       2'lik (Binary), 8'lik (Octal), 10'luk (Decimal), 
       16'lik (Hexadecimal) arasi donusum.

       Secenekler:
           -f, --from      Kaynak taban (2, 8, 10, 16) [varsayilan: 10]
           -t, --to        Hedef taban (2, 8, 10, 16) [varsayilan: 2]

       Ornekler:
           elektro logic convert 255 --to 16
               255 (decimal) → FF (hexadecimal)

           elektro logic convert FF --from 16 --to 2
               FF (hex) → 11111111 (binary)

           elektro logic convert 1010 --from 2
               1010 (binary) → 10 (decimal)

MANTIK KAPILARI
       elektro logic truth KAPI [SECENEKLER]

       Boolean mantik kapilarinin dogruluk tablolarini gosterir.

       Kapilar: and, or, not, nand, nor, xor, xnor

       Secenekler:
           -a, --a         Giris A (0 veya 1)
           -b, --b         Giris B (0 veya 1)
           --all           Tam dogruluk tablosu

       Ornekler:
           elektro logic truth and --a 1 --b 0
               AND(1, 0) = 0

           elektro logic truth xor --all
               XOR kapisi icin tam dogruluk tablosu

===============================================================================
                         KOMPONENT DATASHEET INDIRICI
===============================================================================

DATASHEET INDIRME
       elektro datasheet KOMPONENT [SECENEKLER]

       DuckDuckGo uzerinden otomatik datasheet aramasi yapar ve
       bulundugunuz klasore PDF olarak indirir. Bot korumasi olan
       siteleri atlayarak bir sonraki adaya gecer. Basarili olana
       kadar durmaz.

       Secenekler:
           -o, --output    Kaydetme adi (varsayilan: komponent_datasheet.pdf)

       Ornekler:
           elektro datasheet lm358
               lm358_datasheet.pdf olarak bulunulan klasore indirir

           elektro datasheet ne555
               ne555_datasheet.pdf olarak indirir

           elektro datasheet "2n2222a" -o transistor.pdf
               transistor.pdf olarak kaydeder

       Nasil Calisir:
           1. DuckDuckGo'da "komponent datasheet filetype:pdf" arar
           2. Ilk 15 sonucu tek tek ziyaret eder
           3. Gercek PDF linkini bulur
           4. Progress bar ile indirir
           5. Bulundugunuz klasore kaydeder

       Not:
           Bazi uretici siteleri (TI, ST, Microchip) bot korumasi
           kullanabilir. Bu durumda otomatik olarak diger kaynaklara
           gecilir.


===============================================================================
                              ORNEK SENARYOLAR
===============================================================================

Senaryo 1: LED Dirench Hesaplama
       5V Arduino, 2V 20mA LED icin dirench:
           elektro ohm -v 3 -i 0.02
           Sonuc: R = 150 Ohm

Senaryo 2: RC Filtre Tasarimi
       1kHz kesim frekansi, 10k dirench ile:
           C = 1 / (2π × 10000 × 1000) ≈ 15.9 nF
           elektro filter rc --r 10000 --c 15.9e-9

Senaryo 3: Teknofest Roket Link Budget
       868 MHz, 10 km mesafe, 14 dBm TX:
           elektro rf fspl -f 868 -d 10
           Link margin hesapla, anten secimini optimize et

Senaryo 4: 50 Hz Gurultu Filtreleme
       Sebeke gurultusunu sondurmek icin:
           elektro filter notch --r 1000 --l 5.07 --c 10e-6

Senaryo 5: Hizli Datasheet Bulma
       Yeni bir komponent calisacaksiniz:
           elektro datasheet mcp3008
           Direkt bulundugunuz klasore mcp3008_datasheet.pdf gelir


HAKKINDA
       Elektro v0.1.0 - Elektrik-Elektronik Muhendisligi Terminal Araci
       Yazar: [Ahmet Enes KAYMAK] by Kimi Ai
       GitHub: 

       Lisans: MIT License

                                  2026                               ELEKTRO(1)
"""
    return text

@app.command()
def helpall():
    """Detayli kullanim kilavuzu (man tarzinda)"""
    help_text = get_help_text()
    
    # less kullanarak goster
    try:
        # less varsa kullan
        pager = subprocess.Popen(['less', '-R'], stdin=subprocess.PIPE)
        pager.stdin.write(help_text.encode('utf-8'))
        pager.stdin.close()
        pager.wait()
    except FileNotFoundError:
        # less yoksa direkt yazdir
        console.print(help_text)
    except Exception:
        # Hata olursa direkt yazdir
        console.print(help_text)

if __name__ == "__main__":
    app()
