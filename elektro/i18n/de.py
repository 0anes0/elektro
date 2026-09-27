"""Deutsch."""

MESSAGES = {
    # --- allgemein ----------------------------------------------------------------
    "fmt.pct": "{v} %",
    "ui.error": "Fehler",
    "ui.warning": "Warnung",
    "ui.metavar.value": "WERT",
    "ui.metavar.values": "WERTE...",
    "common.positive": "der Wert muss positiv sein",
    "common.positive_all": "die Werte müssen positiv sein",
    "units.empty": "leerer Wert",
    "units.invalid": "'{text}' konnte nicht gelesen werden (Beispiele: 1k, 4k7, 100n, 2.2u, 1e-3)",
    "units.unknown_series": "unbekannte Reihe '{name}' (Optionen: {options})",

    # --- Typer / Click ---------------------------------------------------------------
    "typer.options": "Optionen",
    "typer.arguments": "Argumente",
    "typer.commands": "Befehle",
    "typer.error": "Fehler",
    "typer.aborted": "Abgebrochen.",
    "typer.required": "[erforderlich]",
    "typer.default": "[Standard: {}]",
    "typer.try_help": "Hilfe mit [blue]'{command_path} {help_option}'[/].",
    "typer.help_option": "Diese Hilfe anzeigen und beenden.",

    # --- Haupt-CLI ------------------------------------------------------------------------
    "cli.help": "Terminal-Werkzeug für Elektrotechnik und Elektronik.",
    "cli.help_long": (
        "⚡ Terminal-Werkzeug für Berechnungen in Elektrotechnik und Elektronik.\n\n"
        "Werte können in technischer Schreibweise angegeben werden: 4k7, 100n, 2.2u, 10M, 1meg"
    ),
    "cli.opt.version": "Version anzeigen",
    "cli.opt.lang": "Sprache für diesen Aufruf (en, tr, de, ru)",
    "panel.basic": "Grundlagen",
    "panel.passive": "Passive Bauelemente",
    "panel.signal": "Signal & HF",
    "panel.tools": "Werkzeuge",
    "menu.ohm": "Ohmsches Gesetz und Leistung",
    "menu.resistor": "Farbcode, SMD-Code",
    "menu.555": "NE555-Timer",
    "menu.logic": "Zahlensysteme, Gatter, Ausdrücke",
    "menu.combine": "Reihen-/Parallelschaltung",
    "menu.divider": "Spannungsteiler",
    "menu.led": "LED-Vorwiderstand",
    "menu.eseries": "Normwerte",
    "menu.cap": "Kondensator-Code",
    "menu.filter": "RC/RL/LC/RLC-Filter",
    "menu.rf": "Freiraumdämpfung, Link-Budget, Antenne",
    "menu.datasheet": "Datenblatt suchen und laden",
    "menu.helpall": "Vollständiges Handbuch",
    "menu.language": "Sprache ändern",
    "menu.update": "Auf neueste Version aktualisieren",
    "menu.subtitle": "elektro BEFEHL --help",

    # --- Sprache ----------------------------------------------------------------------------
    "lang.help": (
        "Sprache der Oberfläche anzeigen oder ändern.\n\n"
        "Beispiele:\n"
        "  elektro language          (Sprachen auflisten)\n"
        "  elektro language de       (Deutsch als Standard speichern)\n"
        "  elektro --lang ru ohm -v 5 -r 1k   (einmalig)"
    ),
    "lang.arg": "Zu speichernder Sprachcode",
    "lang.usage": "Ändern: elektro language CODE   ·   einmalig: elektro --lang CODE ...",
    "lang.unknown": "unbekannte Sprache '{code}' (Optionen: {options})",
    "lang.saved": "Sprache auf {name} gesetzt.",
    "lang.save_failed": "{path} konnte nicht geschrieben werden: {error}",
    "lang.env_override": "Hinweis: Die Umgebungsvariable ELEKTRO_LANG ist gesetzt und hat Vorrang.",

    # --- Handbuch / Update ---------------------------------------------------------------
    "manual.help": "Ausführliches Handbuch aller Befehle (im Pager).",
    "manual.title": "Handbuch",
    "manual.values": "Werte können in technischer Schreibweise angegeben werden:",
    "upd.help": "elektro auf die neueste Version von GitHub aktualisieren.",
    "upd.opt.force": "Auch bei gleicher Version neu installieren",
    "upd.fetch_failed": "Versionsinfo von GitHub nicht abrufbar. Internetverbindung prüfen.",
    "upd.installed": "Installiert",
    "upd.up_to_date": "Bereits aktuell.",
    "upd.pipx": "Mit pipx installiert. Zum Wechsel auf das neue Installationsskript:",
    "upd.dev": "Offenbar eine Entwicklungsinstallation; im Repo-Ordner genügt [cyan]git pull[/].",
    "upd.updating": "Aktualisiere…",
    "upd.failed": "Aktualisierung fehlgeschlagen",
    "upd.done": "elektro {version} installiert.",

    # --- Ohm ----------------------------------------------------------------------------------
    "ohm.help": (
        "Ohmsches Gesetz: zwei beliebige Größen aus V, I, R, P angeben, der Rest wird berechnet.\n\n"
        "V = I·R    P = V·I = I²·R = V²/R\n\n"
        "Ohne Parameter wird interaktiv nachgefragt.\n\n"
        "Beispiele:\n"
        "  elektro ohm -v 12 -r 1k\n"
        "  elektro ohm -i 20m -p 0.5\n"
        "  elektro ohm"
    ),
    "ohm.opt.v": "Spannung (V)",
    "ohm.opt.i": "Strom (A), z. B. 20m",
    "ohm.opt.r": "Widerstand (Ω), z. B. 4k7",
    "ohm.opt.p": "Leistung (W)",
    "ohm.need_two": "mindestens 2 Werte erforderlich",
    "ohm.negative": "Widerstand und Leistung dürfen nicht negativ sein",
    "ohm.div_zero": "Division durch null — Schaltung mit diesen Werten nicht definiert",
    "ohm.conflict": "Die angegebenen Werte widersprechen sich; die ersten beiden wurden verwendet.",
    "ohm.title": "Ohmsches Gesetz",
    "ohm.voltage": "Spannung (V)",
    "ohm.current": "Strom (I)",
    "ohm.resistance": "Widerstand (R)",
    "ohm.power": "Leistung (P)",
    "ohm.wizard": "Assistent Ohmsches Gesetz — unbekannte Werte leer lassen (Enter)",
    "ohm.ask.v": "Spannung V",
    "ohm.ask.i": "Strom I",
    "ohm.ask.r": "Widerstand R",
    "ohm.ask.p": "Leistung P",

    # --- Widerstand -----------------------------------------------------------------------
    "res.help": "Widerstands-Farbcode, SMD-Code und Normwerte.",
    "res.help_long": (
        "Decoder für Widerstands-Farbcodes.\n\n"
        "Reihenfolge der Ringe: Ziffern → Multiplikator → Toleranz → (Temperaturkoeffizient).\n"
        "Farben als IEC-Code (bk bn rd og ye gn bu vt gy wh gd sr) oder als Name\n"
        "auf Deutsch, Englisch, Türkisch oder Russisch.\n\n"
        "Beispiele:\n"
        "  elektro resistor bn bk rd gd          (1 kΩ ±5 %)\n"
        "  elektro resistor gelb violett schwarz braun braun\n"
        "  elektro resistor encode 4k7\n"
        "  elektro resistor smd 103"
    ),
    "res.decode.help": "Widerstandswert aus den Farbringen bestimmen.",
    "res.decode.arg": "Farbringe (3-6)",
    "res.encode.help": "Farbcode zu einem Widerstandswert erzeugen.",
    "res.encode.arg": "Widerstand, z. B. 4k7, 220, 1M",
    "res.encode.opt.bands": "Anzahl der Ringe (4 oder 5)",
    "res.encode.opt.tol": "Toleranz in % (Standard: 5 bei 4 Ringen, 1 bei 5 Ringen)",
    "res.encode.bad_bands": "Anzahl der Ringe muss 4 oder 5 sein",
    "res.encode.title": "Farbcode",
    "res.smd.help": "SMD-Widerstandsaufdruck entschlüsseln (3/4 Ziffern und EIA-96).",
    "res.smd.arg": "SMD-Code: 103, 4R7, 1002, 01C",
    "res.smd.title": "SMD-Widerstand",
    "res.table.help": "Referenztabelle der Farbcodes.",
    "res.table.title": "Widerstands-Farbcodes",
    "res.table.footer": "Ohne Toleranzring: ±20 %. Beispiel: elektro resistor bn bk rd gd",
    "res.col.code": "Code",
    "res.col.color": "Farbe",
    "res.col.digit": "Ziffer",
    "res.col.mult": "Multiplikator",
    "res.col.tol": "Toleranz",
    "res.unknown_color": "unbekannte Farbe '{code}'",
    "res.band_count": "3, 4, 5 oder 6 Ringe angeben",
    "res.bad_digit": "Ring {pos} ({color}) kann kein Ziffernring sein",
    "res.bad_mult": "Multiplikatorring kann nicht {color} sein",
    "res.bad_tol": "Toleranzring kann nicht {color} sein",
    "res.bad_tempco": "Temperaturkoeffizient-Ring kann nicht {color} sein",
    "res.cannot_encode": "{value} lässt sich nicht als Farbcode darstellen",
    "res.bad_tol_value": "ungültige Toleranz {tol} % (Optionen: {options})",
    "res.eia96_range": "EIA-96-Code muss zwischen 01 und 96 liegen",
    "res.smd_invalid": "SMD-Code '{code}' nicht lesbar (Beispiele: 103, 4R7, 1002, 01C)",
    "res.see_table": "Farben: elektro resistor table",
    "res.title": "Widerstand",
    "res.value": "Wert",
    "res.tolerance": "Toleranz",
    "res.range": "Bereich",
    "res.tempco": "Temperaturkoeff.",
    "res.bands": "Ringe",
    "res.codes": "Codes",
    "res.code": "Code",
    "res.note": "Hinweis",
    "res.rounded": "{value} ist mit {bands} Ringen nicht exakt darstellbar; gerundet",
    "res.nearest_std": "Nächster Normwert",

    # --- Reihe / Parallel ---------------------------------------------------------------
    "combine.series.help": (
        "Summe von Bauelementen in Reihe (Standard: Widerstände).\n\n"
        "Beispiele:\n"
        "  elektro series 1k 2k2 470\n"
        "  elektro series 100n 100n --cap"
    ),
    "combine.parallel.help": (
        "Ersatzwert von parallel geschalteten Bauelementen (Standard: Widerstände).\n\n"
        "Beispiele:\n"
        "  elektro parallel 1k 1k\n"
        "  elektro parallel 10u 22u --cap"
    ),
    "combine.arg.series": "Bauteilwerte, z. B. 1k 2k2 470",
    "combine.arg.parallel": "Bauteilwerte, z. B. 1k 1k",
    "combine.opt.cap": "Als Kondensatoren rechnen",
    "combine.opt.ind": "Als Spulen rechnen",
    "combine.item": "Bauteil {n}",
    "combine.total": "Gesamt",
    "combine.series_title": "Reihenschaltung",
    "combine.parallel_title": "Parallelschaltung",

    # --- Spannungsteiler ---------------------------------------------------------------
    "div.help": (
        "Spannungsteiler: Vout = Vin · R2 / (R1 + R2)\n\n"
        "Mit R1 und R2 wird die Ausgangsspannung berechnet; mit --vout werden\n"
        "die besten R1/R2-Paare aus Normwerten vorgeschlagen.\n\n"
        "Beispiele:\n"
        "  elektro divider --vin 12 --r1 10k --r2 4k7\n"
        "  elektro divider --vin 5 --vout 3.3\n"
        "  elektro divider --vin 12 --vout 3.3 --series E12"
    ),
    "div.opt.vin": "Eingangsspannung (V)",
    "div.opt.r1": "Oberer Widerstand (zwischen Vin und Ausgang)",
    "div.opt.r2": "Unterer Widerstand (zwischen Ausgang und Masse)",
    "div.opt.vout": "Zielspannung (für R1/R2-Vorschläge)",
    "div.opt.series": "E-Reihe für Vorschläge",
    "div.opt.load": "Lastwiderstand am Ausgang",
    "div.range": "0 < Vout < Vin erforderlich",
    "div.need": "--r1 und --r2 oder --vout angeben",
    "div.none": "kein passendes Paar gefunden",
    "div.title": "Spannungsteiler",
    "div.ratio": "Verhältnis",
    "div.current": "Strom",
    "div.unloaded": "Vout ohne Last",
    "div.col.error": "Fehler",
    "div.col.current": "Strom",

    # --- LED ------------------------------------------------------------------------------
    "led.help": (
        "Berechnung des LED-Vorwiderstands.\n\n"
        "Beispiele:\n"
        "  elektro led --vs 5\n"
        "  elektro led --vs 12 --vf 3.1 -i 15m -n 3"
    ),
    "led.opt.vs": "Versorgungsspannung (V)",
    "led.opt.vf": "LED-Flussspannung (V). Rot ~2, blau/weiß ~3",
    "led.opt.if": "LED-Strom (A), z. B. 20m",
    "led.opt.count": "Anzahl LEDs in Reihe",
    "led.opt.series": "E-Reihe für den Vorschlag",
    "led.supply_low": "Versorgung ({vs} V) muss größer als der LED-Spannungsabfall ({drop} V) sein",
    "led.current_pos": "der Strom muss positiv sein",
    "led.title": "LED-Vorwiderstand",
    "led.calc_r": "Berechnetes R",
    "led.suggested": "Vorschlag ({series})",
    "led.real_i": "Tatsächlicher Strom",
    "led.power": "Widerstandsleistung",
    "led.rating": "Empfohlene Belastbarkeit",
    "led.rating_high": "> 10 W (andere Lösung erwägen)",
    "led.efficiency": "Wirkungsgrad",

    # --- E-Reihe -------------------------------------------------------------------------
    "eseries.help": (
        "Nächstgelegene Normwerte (E3…E192) zu einem Wert anzeigen.\n\n"
        "Beispiele:\n"
        "  elektro eseries 4k8\n"
        "  elektro eseries 3.3u -s E12"
    ),
    "eseries.arg": "Gesuchter Wert, z. B. 4k8",
    "eseries.opt.series": "Nur diese Reihe (z. B. E24)",
    "eseries.title": "Normwerte für {value}",
    "eseries.col.series": "Reihe",
    "eseries.col.lower": "Unten",
    "eseries.col.upper": "Oben",
    "eseries.col.nearest": "Nächster",
    "eseries.col.error": "Fehler",

    # --- Kondensator ----------------------------------------------------------------------
    "cap.help": (
        "Keramikkondensator-Code entschlüsseln oder aus einem Wert erzeugen.\n\n"
        "Beispiele:\n"
        "  elektro cap 104       → 100 nF\n"
        "  elektro cap 472K      → 4.7 nF ±10 %\n"
        "  elektro cap 22n       → 223"
    ),
    "cap.arg": "Code (104, 472K) oder Wert (100n)",
    "cap.bad_code": "3-stelliger Code erwartet (z. B. 104, 472K)",
    "cap.title": "Kondensator",
    "cap.code": "Code",
    "cap.value": "Wert",
    "cap.tolerance": "Toleranz",
    "cap.not_ceramic": "dieser Wert ist vermutlich kein Keramikkondensator",

    # --- Filter ------------------------------------------------------------------------------
    "flt.help": "Analyse und Entwurf von RC/RL/LC/RLC-Filtern.",
    "flt.response": "Frequenzgang",
    "flt.gain": "Verstärkung",
    "flt.phase": "Phase",
    "flt.need_two": "genau zwei von {opts} angeben",
    "flt.opt.r": "Widerstand (Ω), z. B. 1k",
    "flt.opt.c": "Kapazität (F), z. B. 100n",
    "flt.opt.l": "Induktivität (H), z. B. 10m",
    "flt.opt.fc": "Grenzfrequenz (Hz), z. B. 1k",
    "flt.opt.f0": "Resonanzfrequenz (Hz)",
    "flt.fc": "Grenzfrequenz (fc)",
    "flt.omega": "Kreisfrequenz (ωc)",
    "flt.tau": "Zeitkonstante (τ)",
    "flt.r": "Widerstand (R)",
    "flt.c": "Kapazität (C)",
    "flt.l": "Induktivität (L)",
    "flt.f0": "Resonanzfrequenz (f₀)",
    "flt.center": "Mittenfrequenz (f₀)",
    "flt.bw": "Bandbreite (BW)",
    "flt.q": "Güte (Q)",
    "flt.lower": "Untere Grenze",
    "flt.upper": "Obere Grenze",
    "flt.rc.help": (
        "RC-Filter (standardmäßig Tiefpass). Zwei von R, C, fc angeben.\n\n"
        "fc = 1 / (2πRC)    τ = RC\n\n"
        "Beispiele:\n"
        "  elektro filter rc --r 1k --c 100n\n"
        "  elektro filter rc --fc 1k --c 10n          (berechnet R)\n"
        "  elektro filter rc --r 10k --fc 50 --high   (berechnet C)"
    ),
    "flt.rc.opt.high": "Hochpass (C in Reihe, R gegen Masse)",
    "flt.rc.title_low": "RC-Tiefpass",
    "flt.rc.title_high": "RC-Hochpass",
    "flt.rc.note1": "Bei fc beträgt die Verstärkung -3 dB und die Phase {phase}; Steilheit 20 dB/Dekade.",
    "flt.rc.note2": "Nach τ erreicht der Kondensator 63 % des Endwerts, nach ~5τ ist er voll geladen.",
    "flt.rl.help": (
        "RL-Filter (standardmäßig Hochpass). Zwei von R, L, fc angeben.\n\n"
        "fc = R / (2πL)    τ = L / R\n\n"
        "Beispiele:\n"
        "  elektro filter rl --r 1k --l 10m\n"
        "  elektro filter rl --r 100 --fc 10k --low"
    ),
    "flt.rl.opt.low": "Tiefpass (L in Reihe, R gegen Masse)",
    "flt.rl.title_low": "RL-Tiefpass",
    "flt.rl.title_high": "RL-Hochpass",
    "flt.lc.help": (
        "LC-Resonanz. Zwei von L, C, f angeben.\n\n"
        "f₀ = 1 / (2π√(LC))    Z₀ = √(L/C)\n\n"
        "Beispiele:\n"
        "  elektro filter lc --l 10u --c 100n\n"
        "  elektro filter lc --f 433.92M --c 10p     (berechnet L)"
    ),
    "flt.lc.title": "LC-Resonanz",
    "flt.lc.reactance": "Blindwiderstand (XL = XC)",
    "flt.lc.z0": "Wellenwiderstand",
    "flt.lc.note": "Ein Reihen-LC hat bei Resonanz minimale, ein Parallel-LC (Schwingkreis) maximale Impedanz.",
    "flt.rlc.help": (
        "Reihen-RLC-Bandpass (Ausgang über R).\n\n"
        "f₀ = 1 / (2π√(LC))   BW = R / (2πL)   Q = f₀ / BW\n\n"
        "Beispiel:\n"
        "  elektro filter rlc --r 10 --l 1m --c 100n"
    ),
    "flt.rlc.title": "Reihen-RLC-Bandpass",
    "flt.rlc.note": "Hohe Güte → schmalbandig, hohe Selektivität. Niedrige Güte → breitbandig.",
    "flt.notch.help": (
        "Bandsperre (Notch): Parallel-LC-Kreis im Signalweg, Ausgang über R.\n\n"
        "f₀ = 1 / (2π√(LC))   Q = R / (2πf₀L)\n\n"
        "Beispiel (50-Hz-Netzbrummen):\n"
        "  elektro filter notch --r 1k --l 1.013 --c 10u"
    ),
    "flt.notch.opt.r": "Lastwiderstand (Ω)",
    "flt.notch.title": "Bandsperre (Notch)",
    "flt.notch.f0": "Sperrfrequenz (f₀)",
    "flt.notch.note": "Mit idealen Bauteilen ist die Dämpfung bei f₀ unendlich; real begrenzt der Spulenwiderstand.",
    "flt.theory.help": "Übersicht über Filtertypen und Formeln.",
    "flt.theory.title": "Filtertheorie",
    "flt.theory.body": (
        "[bold]Tiefpass[/]    RC: R in Reihe, C gegen Masse  ·  RL: L in Reihe, R gegen Masse\n"
        "[bold]Hochpass[/]    RC: C in Reihe, R gegen Masse  ·  RL: R in Reihe, L gegen Masse\n"
        "[bold]Bandpass[/]    Reihen-RLC, Ausgang über R (minimale Z bei Resonanz)\n"
        "[bold]Bandsperre[/]  Parallel-LC-Kreis im Signalweg (maximale Z bei Resonanz)\n\n"
        "fc(RC) = 1/(2πRC)     fc(RL) = R/(2πL)\n"
        "f₀(LC) = 1/(2π√(LC))  Q = f₀/BW\n"
        "Filter 1. Ordnung: -3 dB bei fc, Steilheit 20 dB/Dekade"
    ),

    # --- HF -----------------------------------------------------------------------------------
    "rf.help": "HF: Freiraumdämpfung, Link-Budget, Wellenlänge und Einheitenumrechnung.",
    "rf.metavar.freq": "FREQ",
    "rf.metavar.dist": "DIST",
    "rf.opt.freq": "Frequenz. Reine Zahl = MHz: 868, 2.4G, 433.92M",
    "rf.opt.dist": "Entfernung. Reine Zahl = km: 5, 800m, 12km",
    "rf.bad_distance": "Entfernung '{text}' nicht lesbar (z. B. 5, 2.5km, 800m)",
    "rf.positive": "Frequenz und Entfernung müssen positiv sein",
    "rf.freq": "Frequenz",
    "rf.dist": "Entfernung",
    "rf.wavelength": "Wellenlänge",
    "rf.fspl.help": (
        "Freiraumdämpfung (ITU-R P.525).\n\n"
        "FSPL(dB) = 20·log₁₀(d) + 20·log₁₀(f) + 20·log₁₀(4π/c)\n\n"
        "Beispiele:\n"
        "  elektro rf fspl -f 868 -d 5\n"
        "  elektro rf fspl -f 2.4G -d 300m"
    ),
    "rf.fspl.title": "Freiraumdämpfung",
    "rf.fspl.note": "Für die Linkreserve siehe: elektro rf link --help",
    "rf.link.help": (
        "Link-Budget: Empfangsleistung, Linkreserve und theoretische Maximalreichweite.\n\n"
        "Prx = Ptx + Gtx + Grx − FSPL − Verluste\n\n"
        "Beispiele:\n"
        "  elektro rf link -f 868 -d 10 --tx 14 --sens -137\n"
        "  elektro rf link -f 2.4G -d 500m --tx 20 --gtx 5 --grx 5 --sens -90 --loss 3"
    ),
    "rf.link.opt.tx": "Sendeleistung (dBm)",
    "rf.link.opt.gtx": "Gewinn der Sendeantenne (dBi)",
    "rf.link.opt.grx": "Gewinn der Empfangsantenne (dBi)",
    "rf.link.opt.sens": "Empfängerempfindlichkeit (dBm)",
    "rf.link.opt.loss": "Summe der Kabel-/Stecker-/Umgebungsverluste (dB)",
    "rf.link.title": "Link-Budget",
    "rf.link.prx": "Empfangsleistung",
    "rf.link.sens": "Empfindlichkeit",
    "rf.link.margin": "Linkreserve",
    "rf.link.solid": "stabil",
    "rf.link.marginal": "grenzwertig",
    "rf.link.no_link": "KEINE VERBINDUNG",
    "rf.link.range0": "Max. Reichweite (0 dB Reserve)",
    "rf.link.range10": "Max. Reichweite (10 dB Reserve)",
    "rf.link.note1": "Annahme: freier Raum; Hindernisse, Fresnelzone und Fading verringern die Reichweite deutlich.",
    "rf.link.note2": "In der Praxis wird eine Reserve von 10-20 dB empfohlen.",
    "rf.wave.help": (
        "Wellenlänge und grundlegende Antennenlängen.\n\n"
        "Beispiele:\n"
        "  elektro rf wave -f 433.92\n"
        "  elektro rf wave -f 2.4G --vf 0.95"
    ),
    "rf.wave.opt.vf": "Verkürzungsfaktor (Koax ~0.66-0.85, Drahtantenne ~0.95)",
    "rf.wave.bad": "Frequenz muss positiv sein und 0 < vf ≤ 1",
    "rf.wave.title": "Wellenlänge",
    "rf.wave.dipole": "λ/2-Dipol (gesamt)",
    "rf.wave.monopole": "λ/4-Monopol / GP",
    "rf.conv.help": (
        "HF-Einheitenumrechnung (Leistung und Anpassung).\n\n"
        "Beispiele:\n"
        "  elektro rf convert 14 dbm w\n"
        "  elektro rf convert 0.1 w\n"
        "  elektro rf convert 1.5 vswr"
    ),
    "rf.conv.arg.value": "Wert",
    "rf.conv.arg.src": "Quelleinheit: dbm dbw w mw uw vswr rl gamma",
    "rf.conv.arg.dst": "Zieleinheit (ohne Angabe: alle)",
    "rf.conv.vswr": "VSWR muss ≥ 1 sein",
    "rf.conv.rl": "Rückflussdämpfung muss ≥ 0 dB sein",
    "rf.conv.gamma": "|Γ| muss zwischen 0 und 1 liegen",
    "rf.conv.power_pos": "die Leistung muss positiv sein",
    "rf.conv.no_path": "keine Umrechnung von {src} nach {dst}",
    "rf.conv.unknown": "unbekannte Einheit '{unit}'",
    "rf.conv.l.rl": "Rückflussdämpfung",
    "rf.conv.l.mismatch": "Fehlanpassungsverlust",
    "rf.conv.l.reflected": "Reflektierte Leistung",

    # --- Digital ----------------------------------------------------------------------------
    "dig.help": "Digital: Zahlensysteme, Logikgatter, boolesche Ausdrücke.",
    "dig.base_range": "die Basis muss zwischen 2 und 36 liegen",
    "dig.conv.help": (
        "Umrechnung zwischen Zahlensystemen (2-36).\n\n"
        "Ohne Ziel werden Binär, Oktal, Dezimal und Hexadezimal zusammen angezeigt.\n\n"
        "Beispiele:\n"
        "  elektro logic convert 255\n"
        "  elektro logic convert 0xFF -t 2\n"
        "  elektro logic convert 1010 -f 2\n"
        "  elektro logic convert --bits 8 -- -5"
    ),
    "dig.conv.arg": "Zahl: 255, 0xFF, 0b1010, 0o17, 1Fh",
    "dig.conv.opt.from": "Quellbasis (Standard: aus Präfix oder 10)",
    "dig.conv.opt.to": "Nur in diese Basis umrechnen",
    "dig.conv.opt.bits": "Bitbreite (Zweierkomplement für negative Zahlen)",
    "dig.conv.invalid": "'{value}' ist keine gültige Zahl",
    "dig.conv.in_base": " (Basis {base})",
    "dig.conv.overflow": "{n} passt nicht in {bits} Bit ({lo} … {hi})",
    "dig.conv.base": "Basis {base}",
    "dig.conv.title": "Zahlenumrechnung",
    "dig.dec": "Dezimal",
    "dig.hex": "Hexadezimal",
    "dig.bin": "Binär",
    "dig.oct": "Oktal",
    "dig.bits": "Bits",
    "dig.unsigned": "Vorzeichenlos",
    "dig.truth.help": (
        "Ausgang eines Logikgatters oder (ohne Eingänge) Wahrheitstabelle.\n\n"
        "Beispiele:\n"
        "  elektro logic truth xor\n"
        "  elektro logic truth nand -a 1 -b 1"
    ),
    "dig.truth.arg": "Gatter: {gates}",
    "dig.truth.opt.a": "Eingang A (0/1)",
    "dig.truth.opt.b": "Eingang B (0/1)",
    "dig.truth.unknown": "unbekanntes Gatter '{gate}' (Optionen: {gates})",
    "dig.expr.help": (
        "Wahrheitstabelle und Minterme eines booleschen Ausdrucks.\n\n"
        "Operatoren: & (UND), | (ODER), ^ (XOR), ~ (NICHT). Auch and/or/xor/not und und/oder/nicht.\n\n"
        "Beispiele:\n"
        "  elektro logic expr \"A & B | ~C\"\n"
        "  elektro logic expr \"(A xor B) und C\""
    ),
    "dig.expr.arg": "Boolescher Ausdruck, z. B. \"A & B | ~C\"",
    "dig.expr.invalid": "Ausdruck nicht lesbar: {expr}",
    "dig.expr.unsupported": "nicht unterstütztes Element: {node}",
    "dig.expr.const": "als Konstanten sind nur 0 und 1 erlaubt",
    "dig.expr.too_many": "höchstens 6 Variablen werden unterstützt",

    # --- 555 ---------------------------------------------------------------------------------
    "555.help": "NE555-Timer: astabil und monostabil.",
    "555.astable.help": (
        "Astabiler Betrieb (Oszillator).\n\n"
        "f = 1.44 / ((R1 + 2R2)·C)    D = (R1 + R2) / (R1 + 2R2)\n\n"
        "Beispiele:\n"
        "  elektro 555 astable --r1 1k --r2 10k --c 10u\n"
        "  elektro 555 astable -f 1k -d 60 --c 10n     (berechnet R1, R2)"
    ),
    "555.mono.help": (
        "Monostabiler Betrieb (Monoflop). Zwei von R, C, t angeben.\n\n"
        "t = 1.1 · R · C\n\n"
        "Beispiele:\n"
        "  elektro 555 mono --r 100k --c 10u\n"
        "  elektro 555 mono --t 5 --c 100u     (berechnet R)"
    ),
    "555.opt.r1": "R1 (zwischen VCC und DIS)",
    "555.opt.r2": "R2 (zwischen DIS und THR/TRIG)",
    "555.opt.c": "Zeitkondensator",
    "555.opt.r": "Zeitwiderstand",
    "555.opt.t": "Impulsdauer (s)",
    "555.opt.freq": "Zielfrequenz (Entwurfsmodus)",
    "555.opt.duty": "Ziel-Tastverhältnis in % (Entwurfsmodus)",
    "555.duty_range": ("beim klassischen astabilen 555 muss das Tastverhältnis über 50 % liegen "
                       "(für kleinere Werte eine Diode parallel zu R2 verwenden)"),
    "555.need": "--r1 und --r2 oder --freq angeben",
    "555.mono.need": "genau zwei von --r, --c, --t angeben",
    "555.design.title": "555 astabil – Entwurf",
    "555.r1_calc": "R1 (berechnet)",
    "555.r2_calc": "R2 (berechnet)",
    "555.real_freq": "Tatsächliche Frequenz",
    "555.real_duty": "Tatsächliches Tastverhältnis",
    "555.range_warn": "Warnung: R1 ≥ 1 kΩ und R2 ≤ 1 MΩ empfohlen; Kondensatorwert ändern.",
    "555.astable.title": "555 astabil",
    "555.freq": "Frequenz",
    "555.period": "Periode",
    "555.t_high": "High-Zeit",
    "555.t_low": "Low-Zeit",
    "555.duty": "Tastverhältnis",
    "555.mono.title": "555 monostabil",
    "555.pulse": "Impulsdauer",

    # --- Datenblatt ---------------------------------------------------------------------------
    "ds.help": (
        "Datenblatt eines Bauteils suchen und in den aktuellen Ordner laden.\n\n"
        "Zuerst Herstellerseiten, dann die LCSC-Bauteildatenbank, zuletzt eine\n"
        "DuckDuckGo-Suche. Es wird geprüft, dass die Datei wirklich ein PDF ist.\n\n"
        "Beispiele:\n"
        "  elektro datasheet lm358\n"
        "  elektro datasheet ams1117 --open\n"
        "  elektro datasheet 2n2222 -o transistor.pdf\n"
        "  elektro datasheet esp32 --list"
    ),
    "ds.arg.part": "Teilenummer, z. B. lm358, ne555, ams1117, esp32",
    "ds.opt.output": "Zielpfad (Standard: <teil>_datasheet.pdf)",
    "ds.opt.open": "PDF nach dem Download öffnen",
    "ds.opt.list": "Kandidaten auflisten, ohne herunterzuladen",
    "ds.opt.force": "Vorhandene Datei überschreiben",
    "ds.opt.max": "Maximale Anzahl zu versuchender Kandidaten",
    "ds.step.maker": "Herstellerseiten werden geprüft",
    "ds.step.lcsc": "LCSC/JLCPCB-Bauteildatenbank wird durchsucht",
    "ds.step.ddg": "DuckDuckGo wird durchsucht",
    "ds.step.ddg_blocked": "DuckDuckGo zeigt gerade einen Bot-Schutz, übersprungen",
    "ds.no_opener": "'{opener}' nicht gefunden, Datei bitte manuell öffnen: {path}",
    "ds.empty": "Teilenummer darf nicht leer sein",
    "ds.candidates": "Kandidaten für '{part}':",
    "ds.no_candidates": "Keine Kandidaten gefunden.",
    "ds.exists": "Datei existiert bereits",
    "ds.use_force": "Mit --force erneut herunterladen.",
    "ds.no_dir": "Ordner existiert nicht: {path}",
    "ds.searching": "Suche Datenblatt für '{part}'",
    "ds.downloaded": "Heruntergeladen",
    "ds.try_next": "Kein PDF erhalten, nächster Kandidat",
    "ds.cancelled": "Abgebrochen.",
    "ds.nothing": "Keine Ergebnisse aus allen Quellen.",
    "ds.check_net": "Internetverbindung oder Teilenummer prüfen.",
    "ds.all_failed": "Von keinem Kandidaten konnte ein PDF geladen werden.",
    "ds.manual": "Manuell suchen:",
}
