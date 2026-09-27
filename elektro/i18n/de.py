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

# --- 0.4: neue Befehle ---------------------------------------------------------------------
MESSAGES.update({
    "cli.opt.json": "Ergebnisse als JSON ausgeben (für Skripte)",
    "panel.power": "Leistung & Leitungen",
    "panel.embedded": "Embedded",
    "menu.switch": "Transistor als Schalter",
    "menu.charge": "RC/RL-Ladekurve",
    "menu.regulator": "Spannungsregler",
    "menu.battery": "Akkulaufzeit",
    "menu.thermal": "Wärme & Kühlkörper",
    "menu.wire": "Leiterquerschnitt, Spannungsabfall",
    "menu.trace": "Leiterbahnbreite",
    "menu.uart": "UART-Baudfehler",
    "menu.pwm": "Timer/PWM-Register",
    "menu.adc": "ADC Spannung ↔ Code",
    "menu.i2c": "I²C-Pull-up-Widerstand",
    "menu.crc": "CRC / Prüfsumme",
    "menu.calc": "Rechner mit Einheiten",
    "menu.unit": "Einheitenumrechner",
    "time.min": "min",
    "time.hours": "Stunden",
    "time.days": "Tage",
    "time.months": "Monate",

    # Regler
    "reg.help": (
        "Spannungsregler: Widerstände bei einstellbaren, Verlustleistung bei linearen Reglern.\n\n"
        "Einstellbar: lm317, lm1117, ams1117, lm2596, xl4015, mp1584\n"
        "Fest: 7805, 7812, ams1117-3.3 …\n\n"
        "Beispiele:\n"
        "  elektro regulator lm317 --vout 5\n"
        "  elektro regulator lm317 --r1 240 --r2 720\n"
        "  elektro regulator 7805 --vin 12 -i 500m\n"
        "  elektro regulator ams1117-3.3 --vin 5 -i 300m"
    ),
    "reg.arg": "Regler, z. B. lm317, 7805, ams1117-3.3",
    "reg.opt.vout": "Gewünschte Ausgangsspannung (einstellbare Regler)",
    "reg.opt.vin": "Eingangsspannung",
    "reg.opt.iout": "Laststrom",
    "reg.opt.r1": "R1 (zwischen OUT und ADJ/FB); Standard: Datenblattwert",
    "reg.opt.r2": "R2 (zwischen ADJ/FB und Masse) — berechnet Vout",
    "reg.unknown": "unbekannter Regler '{name}' (bekannt: {options})",
    "reg.vout_low": "die Ausgangsspannung muss über der Referenzspannung ({vref} V) liegen",
    "reg.need_vout": "--vout angeben oder --r2, um die Ausgangsspannung zu berechnen",
    "reg.vout": "Ausgangsspannung",
    "reg.r2_calc": "R2 (berechnet)",
    "reg.dropout": "Typischer Dropout",
    "reg.headroom": "Vin − Vout",
    "reg.dropout_warn": "Vin − Vout = {headroom} V liegt unter dem typischen Dropout ({dropout} V); der Ausgang kann einbrechen.",
    "reg.power": "Verlustleistung",
    "reg.efficiency": "Wirkungsgrad",
    "reg.switching_note": "Schaltregler: Die Verluste hängen vom Wirkungsgrad ab (typisch 80-95 %), siehe Datenblatt.",
    "reg.heat_note": "Über 1 W braucht in den meisten Gehäusen einen Kühlkörper — prüfen mit: elektro thermal --help",

    # Akku
    "bat.help": (
        "Akkulaufzeit aus Kapazität und mittlerem Strom (oder einem Aktiv/Schlaf-Profil).\n\n"
        "Beispiele:\n"
        "  elektro battery 2000 -i 15m\n"
        "  elektro battery 1200 --active 45m --active-time 2 --sleep 20u --sleep-time 58"
    ),
    "bat.arg": "Kapazität in mAh",
    "bat.opt.current": "Mittlerer Strom (A), z. B. 15m",
    "bat.opt.active": "Strom im aktiven Zustand (A)",
    "bat.opt.active_time": "Aktive Zeit pro Zyklus (s)",
    "bat.opt.sleep": "Strom im Schlafmodus (A)",
    "bat.opt.sleep_time": "Schlafzeit pro Zyklus (s)",
    "bat.opt.derate": "Nutzbarer Anteil der Kapazität (Alterung, Temperatur, Abschaltspannung)",
    "bat.need": "-i angeben oder alle von --active --active-time --sleep --sleep-time",
    "bat.title": "Akkulaufzeit",
    "bat.capacity": "Kapazität",
    "bat.usable": "Nutzbar",
    "bat.avg_current": "Mittlerer Strom",
    "bat.life": "Geschätzte Laufzeit",
    "bat.note": "Selbstentladung und Ruhestrom des Reglers sind nicht berücksichtigt.",

    # Wärme
    "th.help": (
        "Sperrschichttemperatur und benötigter Kühlkörper.\n\n"
        "Tj = Ta + P · (Rθjc + Rθcs + Rθsa)   oder   Tj = Ta + P · Rθja\n\n"
        "Beispiele:\n"
        "  elektro thermal -p 2 --rth-ja 62 --ta 40          (ohne Kühlkörper, TO-220)\n"
        "  elektro thermal -p 5 --rth-jc 3 --rth-sa 8\n"
        "  elektro thermal -p 5 --rth-jc 3 --ta 50           (benötigter Kühlkörper)"
    ),
    "th.opt.power": "Verlustleistung (W)",
    "th.opt.ta": "Umgebungstemperatur (°C)",
    "th.opt.tjmax": "Maximale Sperrschichttemperatur (°C)",
    "th.opt.rja": "Wärmewiderstand Sperrschicht-Umgebung ohne Kühlkörper (°C/W)",
    "th.opt.rjc": "Wärmewiderstand Sperrschicht-Gehäuse (°C/W)",
    "th.opt.rcs": "Gehäuse-Kühlkörper (Wärmeleitpad/-paste) (°C/W)",
    "th.opt.rsa": "Kühlkörper-Umgebung (°C/W)",
    "th.need": "--rth-ja angeben oder --rth-jc (mit oder ohne --rth-sa)",
    "th.title": "Wärmeberechnung",
    "th.power": "Leistung",
    "th.total": "Gesamt-Rθ",
    "th.need_sa": "Benötigter Kühlkörper Rθsa ≤",
    "th.impossible": "nicht möglich — Leistung verringern",
    "th.margin": "Abstand zu Tj max",
    "th.margin_note": "Einen Kühlkörper deutlich unter diesem Wert wählen (~20-30 % Reserve).",
    "th.over": "Die Sperrschichttemperatur überschreitet das Maximum!",

    # Leitung
    "wire.help": (
        "Kupferleitung: AWG ↔ mm², Widerstand, Spannungsabfall und Verlust.\n\n"
        "Beispiele:\n"
        "  elektro wire --awg 22 -l 3 -i 2\n"
        "  elektro wire --mm2 1.5 -l 10 -i 10 --round-trip"
    ),
    "wire.opt.awg": "Leiterstärke (AWG)",
    "wire.opt.mm2": "Querschnitt (mm²)",
    "wire.opt.length": "Länge (reine Zahl = m): 3, 50cm, 10ft",
    "wire.opt.current": "Strom (A)",
    "wire.opt.round_trip": "Länge doppelt zählen (Hin- und Rückleiter)",
    "wire.opt.temp": "Leitertemperatur (°C)",
    "wire.metavar.length": "LÄNGE",
    "wire.bad_length": "Länge '{text}' nicht lesbar (z. B. 3, 50cm, 10ft)",
    "wire.need": "entweder --awg oder --mm2 angeben",
    "wire.title": "Kupferleitung",
    "wire.diameter": "Durchmesser",
    "wire.area": "Querschnitt",
    "wire.r_per_m": "Widerstand pro Meter",
    "wire.resistance": "Widerstand",
    "wire.drop": "Spannungsabfall",
    "wire.loss": "Verlustleistung",
    "wire.density": "Stromdichte",
    "wire.hot": "Hohe Stromdichte; die Leitung kann warm werden (> 6 A/mm²).",
    "wire.note": "Massiver Kupferleiter; Litzen haben einen etwas höheren Widerstand.",

    # Leiterbahn
    "trace.help": (
        "Leiterbahnbreite nach IPC-2221 (oder der Strom, den eine Bahn trägt).\n\n"
        "Beispiele:\n"
        "  elektro trace -i 3\n"
        "  elektro trace -i 5 --rise 20 --oz 2\n"
        "  elektro trace -w 0.5 --internal -l 40mm"
    ),
    "trace.opt.current": "Strom (A)",
    "trace.opt.width": "Bahnbreite in mm (berechnet den Strom)",
    "trace.opt.rise": "Zulässige Erwärmung (°C)",
    "trace.opt.oz": "Kupferauflage (oz/ft²): 0.5, 1, 2",
    "trace.opt.internal": "Innenlage (Standard: Außenlage)",
    "trace.opt.length": "Bahnlänge (reine Zahl = m): 40mm, 0.1",
    "trace.need": "entweder -i oder -w angeben",
    "trace.title": "Leiterbahn (IPC-2221)",
    "trace.width": "Breite",
    "trace.current": "Strom",
    "trace.thickness": "Kupfer",
    "trace.layer": "Lage",
    "trace.internal": "innen",
    "trace.external": "außen",
    "trace.rise": "Erwärmung",
    "trace.note": "IPC-2221 ist konservativ; bei hohen Strömen auch IPC-2152 prüfen.",

    # Transistorschalter
    "sw.help": "Transistor als Schalter: BJT-Basiswiderstand, MOSFET-Gate-Ansteuerung.",
    "sw.opt.vdrive": "Ansteuerspannung (z. B. GPIO 3.3 oder 5 V)",
    "sw.bjt.help": (
        "BJT (NPN) als gesättigter Schalter: Basiswiderstand und Verluste.\n\n"
        "Ib = Ic / hFE · k     Rb = (Vansteuer − Vbe) / Ib\n\n"
        "Beispiele:\n"
        "  elektro switch bjt --ic 500m -v 3.3\n"
        "  elektro switch bjt --vcc 12 --rload 24 -v 5 --hfe 150"
    ),
    "sw.bjt.opt.ic": "Kollektor-(Last-)Strom",
    "sw.bjt.opt.hfe": "Minimale Stromverstärkung hFE (aus dem Datenblatt)",
    "sw.bjt.opt.overdrive": "Übersteuerungsfaktor k für sichere Sättigung (2-5)",
    "sw.bjt.opt.vbe": "Basis-Emitter-Spannung (V)",
    "sw.bjt.opt.vcesat": "Kollektor-Emitter-Sättigungsspannung (V)",
    "sw.bjt.opt.vcc": "Versorgungsspannung (mit --rload, statt --ic)",
    "sw.bjt.opt.rload": "Lastwiderstand (mit --vcc)",
    "sw.bjt.need": "--ic angeben oder --vcc und --rload",
    "sw.bjt.vdrive_low": "die Ansteuerspannung muss über Vbe ({vbe} V) liegen",
    "sw.bjt.title": "BJT-Schalter",
    "sw.bjt.ib": "Benötigter Ib",
    "sw.bjt.rb_calc": "Rb (berechnet)",
    "sw.bjt.rb_std": "Rb (E12, eine Stufe kleiner)",
    "sw.bjt.forced_beta": "Erzwungenes β (Ic/Ib)",
    "sw.bjt.p_transistor": "Transistorverlust",
    "sw.bjt.p_rb": "Leistung an Rb",
    "sw.bjt.gpio_warn": "Basisstrom {ib} ist für die meisten MCU-Pins zu hoch; Darlington oder MOSFET verwenden.",
    "sw.bjt.note": "Bei induktiven Lasten (Relais, Motor) eine Freilaufdiode parallel zur Last vorsehen.",
    "sw.fet.help": (
        "MOSFET-Gate-Ansteuerung: Gatestrom, Schaltzeit und Verluste.\n\n"
        "Beispiele:\n"
        "  elektro switch mosfet -v 10 --qg 40n --rg 10 -f 100k\n"
        "  elektro switch mosfet -v 5 --qg 20n -f 20k --id 5 --rds 20m --vds 24"
    ),
    "sw.fet.opt.qg": "Gesamte Gateladung Qg (C), z. B. 40n",
    "sw.fet.opt.rg": "Gatewiderstand (Ω)",
    "sw.fet.opt.fsw": "Schaltfrequenz (Hz)",
    "sw.fet.opt.id": "Drainstrom (A)",
    "sw.fet.opt.rds": "Durchlasswiderstand Rds(on) (Ω)",
    "sw.fet.opt.vds": "Drain-Source-Spannung im Sperrzustand (V)",
    "sw.fet.title": "MOSFET-Gate-Ansteuerung",
    "sw.fet.ipeak": "Spitzen-Gatestrom",
    "sw.fet.tsw": "Schaltzeit (≈ Qg/Ig)",
    "sw.fet.pgate": "Ansteuerleistung",
    "sw.fet.pcond": "Durchlassverlust",
    "sw.fet.psw": "Schaltverlust (ca.)",
    "sw.fet.ptotal": "Gesamtverlust",
    "sw.fet.slow": "Das Schalten dauert über 10 % der Periode; Gate-Treiber oder kleineres Rg verwenden.",
    "sw.fet.logic_level": "Ansteuerung unter 5 V: Logic-Level-MOSFET verwenden (Rds(on) bei 2.5-4.5 V spezifiziert).",
    "sw.fet.note": "Schätzung; die reale Schaltzeit hängt auch vom Miller-Plateau und vom Treiber ab.",

    # Laden
    "chg.help": (
        "Kondensatorladung (RC) bzw. Spulenstrom (RL) über der Zeit.\n\n"
        "v(t) = Vend + (V0 − Vend) · e^(−t/τ)\n\n"
        "Beispiele:\n"
        "  elektro charge --r 10k --c 100u --v 5\n"
        "  elektro charge --r 10k --c 100u --v 5 --to 3.3      (Zeit bis 3.3 V)\n"
        "  elektro charge --r 10k --c 100u --v 0 --v0 5 --t 1  (Entladung)\n"
        "  elektro charge --r 10 --l 1m --v 12                 (RL-Strom)"
    ),
    "chg.opt.r": "Widerstand (Ω)",
    "chg.opt.c": "Kapazität (F) für RC",
    "chg.opt.l": "Induktivität (H) für RL",
    "chg.opt.v": "Angelegte (End-)Spannung (V)",
    "chg.opt.v0": "Anfangsspannung des Kondensators (V)",
    "chg.opt.to": "Zielspannung: Zeit bis zum Erreichen",
    "chg.opt.t": "Zeit (s): Wert zu diesem Zeitpunkt",
    "chg.need": "entweder --c (RC) oder --l (RL) angeben",
    "chg.unreachable": "das Ziel wird nie erreicht (liegt nicht zwischen Anfangs- und Endwert)",
    "chg.title_rc": "RC-Ladung",
    "chg.title_rl": "RL-Strom",
    "chg.final": "Endwert",
    "chg.value_at": "Wert bei {time}",
    "chg.time_to": "Zeit bis {target}",
    "chg.note": "Nach 1τ sind {pct} der Änderung erreicht; nach 5τ ist sie praktisch abgeschlossen.",

    # Microstrip
    "ms.help": (
        "Mikrostreifenleitung: Bahnbreite für eine Impedanz oder Impedanz einer Breite (Hammerstad).\n\n"
        "Beispiele:\n"
        "  elektro rf microstrip --z0 50                   (1.6 mm FR4)\n"
        "  elektro rf microstrip --z0 50 --h 0.2 --er 4.2 -f 2.4G\n"
        "  elektro rf microstrip -w 3"
    ),
    "ms.opt.z0": "Zielimpedanz (Ω)",
    "ms.opt.width": "Bahnbreite (mm) — berechnet Z0",
    "ms.opt.h": "Dielektrikumsdicke bis zur Massefläche (mm)",
    "ms.opt.er": "Relative Permittivität εr (FR4 ≈ 4.2-4.6)",
    "ms.need": "entweder --z0 oder --width angeben",
    "ms.range": "Impedanz außerhalb des erreichbaren Bereichs",
    "ms.title": "Mikrostreifenleitung",
    "ms.width": "Bahnbreite",
    "ms.lambda": "Wellenlänge auf der Leitung",
    "ms.note": "Kupferdicke und Lötstopplack werden vernachlässigt; für Endwerte den Rechner des Leiterplattenherstellers verwenden.",

    # LoRa
    "lora.help": (
        "LoRa-Sendedauer, Datenrate, Empfindlichkeit und Duty-Cycle-Grenze (Semtech AN1200.13).\n\n"
        "Beispiele:\n"
        "  elektro rf lora --sf 9 -p 20\n"
        "  elektro rf lora --sf 12 --bw 125k --cr 4/8 -p 51"
    ),
    "lora.opt.sf": "Spreizfaktor (7-12)",
    "lora.opt.bw": "Bandbreite (Hz): 125k, 250k, 500k",
    "lora.opt.cr": "Coderate: 4/5 … 4/8",
    "lora.opt.payload": "Nutzdatenlänge (Byte)",
    "lora.opt.preamble": "Präambellänge (Symbole)",
    "lora.opt.no_crc": "Ohne Nutzdaten-CRC",
    "lora.opt.implicit": "Impliziter Header",
    "lora.opt.duty": "Duty-Cycle-Grenze in % (EU 868 MHz: 1)",
    "lora.opt.nf": "Rauschzahl des Empfängers (dB)",
    "lora.bad_cr": "die Coderate muss 4/5, 4/6, 4/7 oder 4/8 sein",
    "lora.airtime": "Sendedauer (Time on Air)",
    "lora.symbol": "Symboldauer",
    "lora.bitrate": "Datenrate",
    "lora.sensitivity": "Empfindlichkeit (ca.)",
    "lora.per_hour": "Pakete/Stunde bei {duty}",
    "lora.interval": "alle",
    "lora.on": "an",
    "lora.off": "aus",
    "lora.note": "LDRO (Low Data Rate Optimization) wird automatisch aktiviert, wenn die Symboldauer 16 ms übersteigt.",

    # Fresnel
    "fresnel.help": (
        "Erste Fresnelzone und benötigte Antennenhöhe für Sichtverbindung.\n\n"
        "r₁ = √(λ·d₁·d₂ / D)\n\n"
        "Beispiele:\n"
        "  elektro rf fresnel -f 868 -d 10\n"
        "  elektro rf fresnel -f 2.4G -d 3 --at 500m"
    ),
    "fresnel.opt.at": "Abstand des Hindernisses vom Sender (Standard: Mitte)",
    "fresnel.opt.k": "Faktor für den effektiven Erdradius (Standardatmosphäre 4/3)",
    "fresnel.bad_at": "der Punkt muss zwischen den beiden Antennen liegen",
    "fresnel.title": "Fresnelzone",
    "fresnel.point": "Punkt (d₁ / d₂)",
    "fresnel.r1": "Radius 1. Fresnelzone",
    "fresnel.r60": "60 % Freiraum",
    "fresnel.bulge": "Erdkrümmung",
    "fresnel.need": "Benötigter Freiraum",
    "fresnel.note": "Die Verbindungslinie muss an diesem Punkt mindestens so hoch über Hindernissen verlaufen.",

    # Koax
    "coax.help": (
        "Dämpfung eines Koaxialkabels bei einer Frequenz (typische Werte).\n\n"
        "Kabel: RG-58, RG-174, RG-316, RG-213, RG-6, LMR-195, LMR-240, LMR-400, LMR-600\n\n"
        "Beispiele:\n"
        "  elektro rf coax rg58 -f 868 -l 5\n"
        "  elektro rf coax lmr400 -f 2.4G -l 20m"
    ),
    "coax.arg": "Kabeltyp, z. B. rg58, lmr400",
    "coax.opt.length": "Kabellänge (reine Zahl = m): 5, 150cm, 30ft",
    "coax.metavar.length": "LÄNGE",
    "coax.unknown": "unbekanntes Kabel '{name}' (bekannt: {options})",
    "coax.per100": "Dämpfung pro 100 m",
    "coax.loss": "Gesamtdämpfung",
    "coax.delivered": "Übertragene Leistung",
    "coax.delay": "Laufzeit",
    "coax.electrical": "Elektrische Länge",
    "coax.note": "Typische Werte; für das genaue Kabel das Herstellerdatenblatt verwenden. Jeder Stecker kostet ~0.1-0.3 dB.",

    # MCU
    "mcu.opt.clock": "Peripherietakt (Hz), z. B. 16M, 72M",
    "mcu.opt.mcu": "Mikrocontroller-Familie: avr, stm32, generic",
    "mcu.unknown": "unbekannte MCU-Familie '{mcu}' (Optionen: {options})",

    # UART
    "uart.help": (
        "UART-Baudratenregister und Fehler.\n\n"
        "Ohne --baud wird eine Tabelle üblicher Baudraten angezeigt.\n\n"
        "Beispiele:\n"
        "  elektro uart -c 16M -b 115200\n"
        "  elektro uart -c 16M\n"
        "  elektro uart -c 72M -b 921600 -m stm32"
    ),
    "uart.opt.baud": "Baudrate",
    "uart.opt.oversample": "Überabtastung für --mcu generic",
    "uart.col.baud": "Baud",
    "uart.col.mode": "Modus",
    "uart.col.register": "Register",
    "uart.col.actual": "Tatsächlich",
    "uart.col.error": "Fehler",
    "uart.impossible": "nicht möglich",
    "uart.note": "Fehler bis ±2 % funktionieren meist; für Zuverlässigkeit unter ±1 % bleiben.",

    # PWM
    "pwm.help": (
        "Timer/PWM-Vorteiler und Periodenregister für eine Frequenz.\n\n"
        "Beispiele:\n"
        "  elektro pwm -c 16M -f 20k                 (AVR Timer1)\n"
        "  elektro pwm -c 16M -f 1k --bits 8\n"
        "  elektro pwm -c 72M -f 20k -m stm32 -d 25"
    ),
    "pwm.opt.freq": "PWM-Frequenz (Hz)",
    "pwm.opt.bits": "Timerbreite in Bit (8, 16, 32)",
    "pwm.opt.duty": "Tastverhältnis in % (berechnet den Vergleichswert)",
    "pwm.bad": "Takt und Frequenz müssen positiv sein; Bits müssen 8, 10, 16 oder 32 sein",
    "pwm.impossible": "diese Frequenz ist mit diesem Takt/Timer nicht erzeugbar",
    "pwm.prescaler": "Vorteiler",
    "pwm.actual": "Tatsächliche Frequenz",
    "pwm.error": "Fehler",
    "pwm.resolution": "Auflösung",
    "pwm.steps": "Stufen",
    "pwm.compare": "Vergleichswert für {duty}",
    "pwm.low_res": "Auflösung unter 8 Bit; Frequenz senken oder Takt erhöhen.",

    # ADC
    "adc.help": (
        "ADC/DAC: LSB-Größe, Umrechnung Spannung ↔ Code, ideales SNR.\n\n"
        "V = Code · Vref / 2ᴺ\n\n"
        "Beispiele:\n"
        "  elektro adc -b 12 --vref 3.3 --code 2048\n"
        "  elektro adc -b 10 --vref 5 --volt 1.2"
    ),
    "adc.opt.bits": "Auflösung in Bit",
    "adc.opt.vref": "Referenzspannung (V)",
    "adc.opt.code": "Digitaler Code → Spannung",
    "adc.opt.volt": "Spannung → digitaler Code",
    "adc.steps": "Stufen",
    "adc.snr": "Ideales SNR",
    "adc.voltage_of": "Spannung von Code {code}",
    "adc.code_of": "Code für {volt}",
    "adc.code_range": "der Code muss zwischen 0 und {max} liegen",
    "adc.clipped": "Die Spannung liegt außerhalb 0 … Vref; der Code wird begrenzt.",
    "adc.note": "Manche Datenblätter teilen durch 2ᴺ − 1; der Unterschied beträgt 1 LSB.",

    # I2C
    "i2c.help": (
        "Bereich des I²C-Pull-up-Widerstands aus Buskapazität und Geschwindigkeit.\n\n"
        "Rmin = (Vdd − 0.4 V) / Iol     Rmax = tr / (0.8473 · Cb)\n\n"
        "Beispiele:\n"
        "  elektro i2c --cb 200p\n"
        "  elektro i2c --vdd 5 --cb 100p -s 100k"
    ),
    "i2c.opt.vdd": "Pull-up-Versorgungsspannung (V)",
    "i2c.opt.cb": "Gesamte Buskapazität (F), z. B. 200p (≈10 pF pro Teilnehmer + Leitungen)",
    "i2c.opt.speed": "Busgeschwindigkeit: 100k, 400k oder 1M",
    "i2c.bad_speed": "die Geschwindigkeit muss 100k, 400k oder 1M sein",
    "i2c.cb_limit": "Der I²C-Standard erlaubt höchstens 400 pF Buskapazität.",
    "i2c.impossible": "kein gültiger Widerstand: Buskapazität für diese Geschwindigkeit zu hoch",
    "i2c.suggested": "Vorschlag (E12)",
    "i2c.note": "Kleineres R = schnellere Flanken, aber mehr Strom; zwischen Rmin und Rmax bleiben.",

    # CRC
    "crc.help": (
        "CRC und einfache Prüfsummen einer Bytefolge.\n\n"
        "Beispiele:\n"
        "  elektro crc \"01 03 00 00 00 0A\"\n"
        "  elektro crc 0x31323334 -a modbus\n"
        "  elektro crc \"123456789\" --text"
    ),
    "crc.arg": "Daten als Hex-Bytes (\"01 03 0A\", 0x01030A) oder Text mit --text",
    "crc.opt.text": "Daten als Text behandeln (UTF-8)",
    "crc.opt.algo": "Nur dieser Algorithmus (z. B. modbus, crc-32)",
    "crc.bad_hex": "ungültige Hex-Daten (Paare aus Hex-Ziffern verwenden, z. B. \"01 03 0A\")",
    "crc.unknown": "unbekannter Algorithmus '{algo}' (Optionen: {options})",
    "crc.title": "CRC von {n} Byte",
    "crc.col.algo": "Algorithmus",
    "crc.col.bytes": "Bytes (Senderreihenfolge)",

    # Rechner
    "calc.help": (
        "Rechner, der technische Schreibweise und Einheiten versteht.\n\n"
        "Operatoren: + − * / ^ ( )   Funktionen: sqrt log ln exp sin cos tan db dbp par\n"
        "Konstanten: pi e c.  par(a, b, …) = Parallelschaltung.\n\n"
        "Beispiele:\n"
        "  elektro calc \"12V / (4k7 + 1k)\"\n"
        "  elektro calc \"1 / (2*pi*sqrt(10u * 100n))\" -u Hz\n"
        "  elektro calc \"par(1k, 2k2, 4k7)\" -u Ω\n"
        "  elektro calc \"db(3.3 / 0.1)\""
    ),
    "calc.arg": "Ausdruck (in der Shell in Anführungszeichen)",
    "calc.opt.unit": "Einheit für das Ergebnis (V, A, Ω, Hz …)",
    "calc.syntax": "Ausdruck nicht lesbar",
    "calc.unknown_name": "unbekannter Name '{name}'",
    "calc.unsupported": "nicht unterstütztes Element im Ausdruck",
    "calc.div_zero": "Division durch null",
    "calc.complex": "das Ergebnis ist komplex",

    # Einheiten
    "unit.help": (
        "Einheitenumrechner für den Elektronik-Alltag.\n\n"
        "Temperatur: c f k · Länge: m cm mm um in mil ft · dB: db pratio vratio\n"
        "Leitung: awg mm2 · Kupfer: oz · Winkel: deg rad · Frequenz: hz rpm\n\n"
        "Beispiele:\n"
        "  elektro unit 25 c\n"
        "  elektro unit 10 mil mm\n"
        "  elektro unit 6 db\n"
        "  elektro unit 22 awg"
    ),
    "unit.arg.value": "Wert",
    "unit.arg.src": "Quelleinheit ({units})",
    "unit.arg.dst": "Zieleinheit (ohne Angabe: alle)",
    "unit.unknown": "unbekannte Einheit '{unit}' (Optionen: {options})",
    "unit.no_path": "keine Umrechnung von {src} nach {dst}",
    "unit.below_zero": "unter dem absoluten Nullpunkt",
    "unit.power_ratio": "Leistungsverhältnis",
    "unit.voltage_ratio": "Spannungsverhältnis",
    "unit.period": "Periode (s)",

    # Datenblatt-Cache
    "ds.opt.history": "Bereits geladene Datenblätter auflisten (Cache)",
    "ds.from_cache": "Im Cache gefunden, kein Download nötig.",
    "ds.cache_source": "Cache",
    "ds.cache_empty": "Der Datenblatt-Cache ist leer.",
    "ds.cache_title": "Geladene Datenblätter",
    "ds.col.part": "Bauteil",
    "ds.col.size": "Größe",
    "ds.col.date": "Datum",
})

# --- 0.5 ---------------------------------------------------------------------------------
MESSAGES.update({
    "menu.opamp": "OPV-Verstärker",
    "menu.coil": "Luftspule",
    "menu.crystal": "Quarz-Lastkondensatoren",
    "menu.rectifier": "Gleichrichter + Siebkondensator",
    "menu.acpower": "Wechselstromleistung, Blindstromkompensation",
    "menu.shell": "Interaktiver Modus",
    "menu.vars": "Gespeicherte Variablen",
    "menu.history": "Rechenverlauf",

    # OPV
    "op.help": "Operationsverstärker: nichtinvertierend, invertierend, Differenz, Summierer.",
    "op.noninv.help": (
        "Nichtinvertierender Verstärker.  G = 1 + Rf / Rg\n\n"
        "Mit --gain werden Normwert-Paare Rf/Rg vorgeschlagen; mit --rf und --rg wird die Verstärkung berechnet.\n\n"
        "Beispiele:\n"
        "  elektro opamp noninv --gain 11\n"
        "  elektro opamp noninv --rf 100k --rg 10k --vin 0.2 --gbw 1M"
    ),
    "op.inv.help": (
        "Invertierender Verstärker.  G = −Rf / Rin\n\n"
        "Beispiele:\n"
        "  elektro opamp inv --gain 10\n"
        "  elektro opamp inv --rf 47k --rin 4k7 --vin 0.5 --vcc 12"
    ),
    "op.diff.help": (
        "Differenzverstärker (R1 = R3, R2 = R4).  Vout = (R2/R1) · (V+ − V−)\n\n"
        "Beispiel:\n"
        "  elektro opamp diff --gain 5"
    ),
    "op.sum.help": (
        "Invertierender Summierer.  Vout = −Rf · Σ(Vi / Ri)\n\n"
        "Beispiel:\n"
        "  elektro opamp sum --rf 10k --rin 10k --vin 1 --rin 20k --vin 0.5"
    ),
    "op.opt.gain": "Gewünschte Verstärkung (V/V)",
    "op.opt.gain_inv": "Betrag der gewünschten Verstärkung (Vorzeichen immer negativ)",
    "op.opt.rf": "Rückkopplungswiderstand Rf",
    "op.opt.rg": "Widerstand gegen Masse Rg",
    "op.opt.rin": "Eingangswiderstand Rin",
    "op.opt.vin": "Eingangsspannung (berechnet den Ausgang)",
    "op.opt.vcc": "Versorgungsspannung (warnt bei Übersteuerung)",
    "op.opt.gbw": "Verstärkungs-Bandbreite-Produkt des OPV (Hz), z. B. 1M",
    "op.need": "--gain oder beide Widerstände angeben",
    "op.noninv.min": "ein nichtinvertierender Verstärker kann keine Verstärkung unter 1 haben",
    "op.follower": "Spannungsfolger: Ausgang direkt mit dem −-Eingang verbinden",
    "op.pairs": "Normwert-Widerstandspaare",
    "op.gain": "Verstärkung",
    "op.col.error": "Fehler",
    "op.bandwidth": "Bandbreite (−3 dB)",
    "op.zin": "Eingangsimpedanz",
    "op.note": "Hinweis",
    "op.clip": "Ausgang {vout} überschreitet die Versorgung ({vcc}); er wird begrenzt.",
    "op.noninv.title": "Nichtinvertierender Verstärker",
    "op.inv.title": "Invertierender Verstärker",
    "op.sum.title": "Summierverstärker",
    "op.noninv.note": "Für geringen Offset Rf ∥ Rg ≈ Quellwiderstand wählen; 1k-100k sind üblich.",
    "op.inv.note": "Die Eingangsimpedanz entspricht Rin; Rin passend zur Quelle groß genug wählen.",
    "op.diff.note": "Die Gleichtaktunterdrückung hängt von der Widerstandspaarung ab; möglichst 0,1-%-Widerstände verwenden.",
    "op.sum.opt.rin": "Eingangswiderstand (für jeden Eingang einmal angeben)",
    "op.sum.opt.vin": "Eingangsspannung (für jeden Eingang einmal, gleiche Reihenfolge)",
    "op.sum.mismatch": "gleich viele --rin und --vin angeben",

    # Vereinfachung
    "dig.simp.help": (
        "Boolesche Funktion zu einer minimalen disjunktiven Normalform vereinfachen (Quine-McCluskey).\n\n"
        "Zeigt für 2-4 Variablen das KV-Diagramm.\n\n"
        "Beispiele:\n"
        "  elektro logic simplify \"A&B | A&~B\"\n"
        "  elektro logic simplify -m 0,1,2,5,6,7 -v A,B,C\n"
        "  elektro logic simplify -m 1,3,7,11,15 -d 0,2,5"
    ),
    "dig.simp.arg": "Boolescher Ausdruck (oder --minterms verwenden)",
    "dig.simp.opt.minterms": "Minterm-Liste, z. B. 0,2,5,7",
    "dig.simp.opt.dontcare": "Don't-Care-Terme, z. B. 1,3",
    "dig.simp.opt.vars": "Variablennamen, z. B. A,B,C,D (MSB zuerst)",
    "dig.simp.need": "einen Ausdruck oder --minterms angeben",
    "dig.simp.bad_list": "die Liste muss durch Kommas getrennte ganze Zahlen enthalten",
    "dig.simp.few_vars": "für diese Minterme sind mindestens {n} Variablen nötig",
    "dig.simp.too_many": "höchstens 8 Variablen werden unterstützt",
    "dig.simp.title": "Vereinfacht",
    "dig.simp.minterms": "Funktion",
    "dig.simp.result": "Minimale DNF",
    "dig.simp.code": "Als Ausdruck",
    "dig.simp.cost": "Aufwand",
    "dig.simp.cost_val": "Terme: {terms}, Literale: {lits}",

    # Gleichrichter
    "rect.help": (
        "Transformator + Gleichrichter + Siebkondensator.\n\n"
        "ΔV = I / (k · f · C)   (k = 2 Vollweg, 1 Einweg)\n\n"
        "Beispiele:\n"
        "  elektro rectifier --vac 12 -i 1 --ripple 1\n"
        "  elektro rectifier --vac 9 -i 500m --c 2200u --vmains 230\n"
        "  elektro rectifier --vac 15 --type half -i 100m --ripple 0.5"
    ),
    "rect.opt.vac": "Sekundärspannung (V eff.)",
    "rect.opt.type": "Gleichrichter: bridge (Brücke), center (Mittelpunkt), half (Einweg)",
    "rect.opt.freq": "Netzfrequenz (Hz)",
    "rect.opt.iload": "Laststrom (A)",
    "rect.opt.ripple": "Zulässige Brummspannung (V Spitze-Spitze) — berechnet C",
    "rect.opt.c": "Siebkondensator — berechnet die Brummspannung",
    "rect.opt.vdiode": "Flussspannung pro Diode (V)",
    "rect.opt.vmains": "Primärspannung (V eff.) — berechnet das Windungsverhältnis",
    "rect.bad_type": "der Gleichrichtertyp muss einer von diesen sein: {options}",
    "rect.too_low": "die Sekundärspannung ist kleiner als die Diodenspannungen",
    "rect.title": "Gleichrichter",
    "rect.type": "Typ",
    "rect.kind.bridge": "Vollweg-Brücke",
    "rect.kind.center": "Vollweg-Mittelpunkt",
    "rect.kind.half": "Einweg",
    "rect.vpeak": "Spitzen-DC (ohne Last)",
    "rect.piv": "Dioden-Sperrspannung (PIV)",
    "rect.ripple_freq": "Brummfrequenz",
    "rect.c": "Kondensator",
    "rect.ripple": "Brummspannung (SS)",
    "rect.cap_voltage": "Spannungsfestigkeit des Kondensators",
    "rect.ratio": "Windungsverhältnis",
    "rect.diode_i": "Strom pro Diode",
    "rect.hint": "Für den Siebkondensator -i und --ripple (oder --c) angeben.",
    "rect.note": "Der Rippelstrom des Kondensators ist hoch; einen dafür ausgelegten Low-ESR-Typ wählen.",

    # Wechselstromleistung
    "ac.help": (
        "Ein- oder dreiphasige Wechselstromleistung und Blindstromkompensation.\n\n"
        "P = V·I·cosφ (1-phasig)   P = √3·V·I·cosφ (3-phasig, V Außenleiterspannung)\n\n"
        "Beispiele:\n"
        "  elektro acpower --v 230 --i 10 --pf 0.8\n"
        "  elektro acpower --v 400 --p 15k --pf 0.82 --phases 3\n"
        "  elektro acpower --i 10 --pf 0.75 --target-pf 0.95"
    ),
    "ac.opt.v": "Spannung (V eff.; bei 3 Phasen Außenleiterspannung)",
    "ac.opt.i": "Strom (A eff.)",
    "ac.opt.p": "Wirkleistung (W) — berechnet den Strom",
    "ac.opt.pf": "Leistungsfaktor cosφ",
    "ac.opt.phases": "Anzahl der Phasen: 1 oder 3",
    "ac.opt.target": "Ziel-Leistungsfaktor — berechnet den Kompensationskondensator",
    "ac.bad_phases": "die Phasenzahl muss 1 oder 3 sein",
    "ac.bad_pf": "die Spannung muss positiv sein und 0 < cosφ ≤ 1",
    "ac.bad_target": "der Ziel-Leistungsfaktor muss über dem aktuellen liegen und höchstens 1 sein",
    "ac.need": "--i oder --p angeben",
    "ac.title": "Wechselstromleistung",
    "ac.system": "System",
    "ac.single": "einphasig",
    "ac.three": "dreiphasig",
    "ac.current": "Strom",
    "ac.p": "Wirkleistung P",
    "ac.q": "Blindleistung Q",
    "ac.s": "Scheinleistung S",
    "ac.qc": "Kompensation Qc",
    "ac.cap": "Kompensationskondensator",
    "ac.cap_delta": "Kondensator pro Phase (Δ)",
    "ac.new_current": "Strom nach Kompensation",
    "ac.three_note": "Für eine Kondensatorbank in Sternschaltung die Kapazität mit 3 multiplizieren.",

    # Stern-Dreieck
    "sd.help": (
        "Stern (Y) ↔ Dreieck (Δ) Umrechnung von drei Widerständen/Impedanzen.\n\n"
        "Beispiele:\n"
        "  elektro stardelta delta 10 20 30     (Rab Rbc Rca → Ra Rb Rc)\n"
        "  elektro stardelta star 5 10 15       (Ra Rb Rc → Rab Rbc Rca)"
    ),
    "sd.arg.mode": "Gegebene Schaltung: delta oder star",
    "sd.arg.values": "Drei Werte: Rab Rbc Rca (delta) oder Ra Rb Rc (star)",
    "sd.bad": "Aufruf: stardelta delta|star R1 R2 R3",
    "sd.note": "Ra ist der Widerstand am Knoten A, Rab der zwischen A und B.",

    # Spule
    "coil.help": (
        "Einlagige Luftspule (Wheeler-Formel).\n\n"
        "Beispiele:\n"
        "  elektro coil --l 1u --d 10               (Windungen für 1 µH auf 10-mm-Körper)\n"
        "  elektro coil --l 330n --d 6 --wire 0.8\n"
        "  elektro coil --n 12 --d 8 --length 15"
    ),
    "coil.opt.l": "Gewünschte Induktivität (H), z. B. 1u",
    "coil.opt.n": "Windungszahl — berechnet L",
    "coil.opt.d": "Durchmesser des Spulenkörpers (mm)",
    "coil.opt.wire": "Drahtdurchmesser (mm)",
    "coil.opt.length": "Wickellänge (mm); Standard: dicht gewickelt",
    "coil.need": "entweder --l oder --n angeben",
    "coil.title": "Luftspule",
    "coil.turns": "Windungen",
    "coil.inductance": "Induktivität",
    "coil.length": "Wickellänge",
    "coil.mean_d": "Mittlerer Durchmesser",
    "coil.wire_len": "Drahtlänge",
    "coil.short": "Die Spule ist im Verhältnis zum Durchmesser sehr kurz; die Formel ist ungenauer.",
    "coil.note": "Die Wheeler-Formel ist für Länge > 0,8 × Radius auf ~1 % genau. Draht für die Anschlüsse zugeben.",

    # Quarz
    "xtal.help": (
        "Lastkondensatoren für einen Quarzoszillator (Pierce).\n\n"
        "C1 = C2 = 2 · (CL − Cstreu)\n\n"
        "Beispiele:\n"
        "  elektro crystal --cl 12p\n"
        "  elektro crystal --cl 18p --cstray 3p\n"
        "  elektro crystal --c 22p                  (welches CL ergeben 22 pF?)"
    ),
    "xtal.opt.cl": "Lastkapazität laut Quarz-Datenblatt (F)",
    "xtal.opt.cstray": "Streukapazität von Pins und Leiterbahnen (F), typ. 2-5p",
    "xtal.opt.c": "Vorhandener Kondensatorwert — berechnet CL",
    "xtal.need": "entweder --cl oder --c angeben",
    "xtal.too_small": "CL ist kleiner als die Streukapazität; keine Kondensatoren nötig (oder Cstray prüfen)",
    "xtal.title": "Quarz-Lastkondensatoren",
    "xtal.standard": "Normwert (E12)",
    "xtal.note": "Zu viel Kapazität senkt die Frequenz und kann den Oszillator stoppen.",

    # Grafik
    "plot.opt": "Grafik speichern: .svg (eingebaut), .png / .pdf (benötigt matplotlib)",
    "plot.saved": "Grafik gespeichert: {path}",
    "plot.bad_suffix": "die Grafikdatei muss auf .svg, .png oder .pdf enden",
    "plot.need_mpl": "PNG/PDF benötigt matplotlib: {pip}   (oder .svg verwenden)",
    "plot.freq": "Frequenz",
    "plot.time": "Zeit",
    "plot.voltage": "Spannung (V)",
    "plot.current": "Strom (A)",
    "plot.metavar": "DATEI",

    "calc.var_not_number": "die Variable '{name}' ist keine Zahl",

    # Variablen
    "vars.help": (
        "Gespeicherte Variablen auflisten.\n\n"
        "Variablen werden in jedem Befehl als @name verwendet:\n"
        "  elektro set vin 12\n"
        "  elektro ohm -v @vin -r 1k\n"
        "  elektro calc \"vin / 2\"\n\n"
        "Mit --local werden sie in ./.elektro.json gespeichert (pro Projekt, auch in übergeordneten Ordnern gesucht)."
    ),
    "vars.set.help": "Variable speichern: elektro set NAME WERT (als @NAME verwenden).",
    "vars.unset.help": "Variable löschen.",
    "vars.arg.name": "Variablenname (Buchstaben, Ziffern, _)",
    "vars.arg.value": "Wert, z. B. 12, 4k7, 100n",
    "vars.opt.local": "In ./.elektro.json für dieses Projekt speichern",
    "vars.bad_name": "ungültiger Variablenname '{name}'",
    "vars.unknown": "unbekannte Variable @{name} (siehe: elektro vars)",
    "vars.removed": "gelöscht",
    "vars.empty": "Noch keine Variablen. Beispiel: elektro set vin 12",
    "vars.col.name": "Name",
    "vars.col.value": "Wert",
    "vars.col.scope": "Geltung",
    "vars.global": "global",
    "vars.local": "Projekt",
    "vars.overridden": "überschrieben",

    # Verlauf
    "hist.help": (
        "Rechenverlauf.\n\n"
        "Beispiele:\n"
        "  elektro history\n"
        "  elektro history -s filter\n"
        "  elektro history --run 12\n"
        "  elektro history --clear"
    ),
    "hist.opt.n": "Anzahl der angezeigten Einträge",
    "hist.opt.search": "Nur Einträge mit diesem Text",
    "hist.opt.run": "Eintrag mit dieser Nummer erneut ausführen",
    "hist.opt.clear": "Gesamten Verlauf löschen",
    "hist.bad_id": "kein Eintrag mit dieser Nummer (1 … {max})",
    "hist.cleared": "Verlauf gelöscht.",
    "hist.empty": "Der Verlauf ist leer.",
    "hist.col.command": "Befehl",
    "hist.rerun": "Erneut ausführen: elektro history --run NUMMER",

    # Shell
    "shell.help": (
        "Interaktiver Modus: Befehle ohne 'elektro' eingeben.\n\n"
        "Tab vervollständigt Befehle, ↑/↓ blättert durch frühere Eingaben.\n"
        "Eingebaut: help, clear, exit"
    ),
    "shell.welcome": "interaktiver Modus. 'help' zeigt die Befehle, 'exit' beendet.",
})
