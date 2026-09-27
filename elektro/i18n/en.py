"""English (source language)."""

MESSAGES = {
    # --- general ---------------------------------------------------------------
    "fmt.pct": "{v}%",
    "ui.error": "Error",
    "ui.warning": "Warning",
    "ui.metavar.value": "VALUE",
    "ui.metavar.values": "VALUES...",
    "common.positive": "value must be positive",
    "common.positive_all": "values must be positive",
    "units.empty": "empty value",
    "units.invalid": "could not parse '{text}' (examples: 1k, 4k7, 100n, 2.2u, 1e-3)",
    "units.unknown_series": "unknown series '{name}' (options: {options})",

    # --- Typer / Click -----------------------------------------------------------
    "typer.options": "Options",
    "typer.arguments": "Arguments",
    "typer.commands": "Commands",
    "typer.error": "Error",
    "typer.aborted": "Aborted.",
    "typer.required": "[required]",
    "typer.default": "[default: {}]",
    "typer.try_help": "Try [blue]'{command_path} {help_option}'[/] for help.",
    "typer.help_option": "Show this message and exit.",

    # --- main CLI --------------------------------------------------------------------
    "cli.help": "Terminal toolkit for electrical & electronics engineering.",
    "cli.help_long": (
        "⚡ Terminal toolkit for electrical & electronics engineering calculations.\n\n"
        "Values can be written in engineering notation: 4k7, 100n, 2.2u, 10M, 1meg"
    ),
    "cli.opt.version": "Show version",
    "cli.opt.lang": "Interface language for this run (en, tr, de, ru)",
    "panel.basic": "Basics",
    "panel.passive": "Passive components",
    "panel.signal": "Signal & RF",
    "panel.tools": "Tools",
    "menu.ohm": "Ohm's law and power",
    "menu.resistor": "Color code, SMD code",
    "menu.555": "NE555 timer",
    "menu.logic": "Bases, gates, expressions",
    "menu.combine": "Series/parallel equivalent",
    "menu.divider": "Voltage divider",
    "menu.led": "LED series resistor",
    "menu.eseries": "Standard values",
    "menu.cap": "Capacitor code",
    "menu.filter": "RC/RL/LC/RLC filters",
    "menu.rf": "FSPL, link budget, antenna",
    "menu.datasheet": "Find & download datasheet",
    "menu.helpall": "Full manual",
    "menu.language": "Change language",
    "menu.update": "Update to latest version",
    "menu.subtitle": "elektro COMMAND --help",

    # --- language ----------------------------------------------------------------------
    "lang.help": (
        "Show or change the interface language.\n\n"
        "Examples:\n"
        "  elektro language          (list languages)\n"
        "  elektro language de       (save German as default)\n"
        "  elektro --lang ru ohm -v 5 -r 1k   (one-off)"
    ),
    "lang.arg": "Language code to save",
    "lang.usage": "Change: elektro language CODE   ·   one-off: elektro --lang CODE ...",
    "lang.unknown": "unknown language '{code}' (options: {options})",
    "lang.saved": "Language set to {name}.",
    "lang.save_failed": "could not write {path}: {error}",
    "lang.env_override": "Note: the ELEKTRO_LANG environment variable is set and takes precedence.",

    # --- manual / update ------------------------------------------------------------
    "manual.help": "Detailed manual of all commands (in a pager).",
    "manual.title": "User Manual",
    "manual.values": "Values can be written in engineering notation:",
    "upd.help": "Update elektro to the latest version on GitHub.",
    "upd.opt.force": "Reinstall even if the version is the same",
    "upd.fetch_failed": "Could not fetch version info from GitHub. Check your internet connection.",
    "upd.installed": "Installed",
    "upd.up_to_date": "Already up to date.",
    "upd.pipx": "Installed with pipx. To switch to the new installer:",
    "upd.dev": "Looks like a development install; run [cyan]git pull[/] in the repo folder.",
    "upd.updating": "Updating…",
    "upd.failed": "update failed",
    "upd.done": "elektro {version} installed.",

    # --- ohm -----------------------------------------------------------------------------
    "ohm.help": (
        "Ohm's law: give any two of V, I, R, P and get the rest.\n\n"
        "V = I·R    P = V·I = I²·R = V²/R\n\n"
        "Without arguments it asks interactively.\n\n"
        "Examples:\n"
        "  elektro ohm -v 12 -r 1k\n"
        "  elektro ohm -i 20m -p 0.5\n"
        "  elektro ohm"
    ),
    "ohm.opt.v": "Voltage (V)",
    "ohm.opt.i": "Current (A), e.g. 20m",
    "ohm.opt.r": "Resistance (Ω), e.g. 4k7",
    "ohm.opt.p": "Power (W)",
    "ohm.need_two": "at least 2 values are required",
    "ohm.negative": "resistance and power cannot be negative",
    "ohm.div_zero": "division by zero — circuit undefined with these values",
    "ohm.conflict": "The given values are inconsistent; the first two were used.",
    "ohm.title": "Ohm's Law",
    "ohm.voltage": "Voltage (V)",
    "ohm.current": "Current (I)",
    "ohm.resistance": "Resistance (R)",
    "ohm.power": "Power (P)",
    "ohm.wizard": "Ohm's Law Wizard — leave unknown values empty (Enter)",
    "ohm.ask.v": "Voltage V",
    "ohm.ask.i": "Current I",
    "ohm.ask.r": "Resistance R",
    "ohm.ask.p": "Power P",

    # --- resistor ------------------------------------------------------------------------
    "res.help": "Resistor color code, SMD code and standard values.",
    "res.help_long": (
        "Resistor color code decoder.\n\n"
        "Band order: digits → multiplier → tolerance → (temperature coefficient).\n"
        "Colors can be given as IEC codes (bk bn rd og ye gn bu vt gy wh gd sr),\n"
        "Turkish short codes, or names in English, Turkish, German or Russian.\n\n"
        "Examples:\n"
        "  elektro resistor bn bk rd gd          (1 kΩ ±5%)\n"
        "  elektro resistor yellow violet black brown brown\n"
        "  elektro resistor encode 4k7\n"
        "  elektro resistor smd 103"
    ),
    "res.decode.help": "Find the resistance from color bands.",
    "res.decode.arg": "Color bands (3-6)",
    "res.encode.help": "Generate the color code for a resistance.",
    "res.encode.arg": "Resistance, e.g. 4k7, 220, 1M",
    "res.encode.opt.bands": "Number of bands (4 or 5)",
    "res.encode.opt.tol": "Tolerance in % (default: 5 for 4 bands, 1 for 5 bands)",
    "res.encode.bad_bands": "number of bands must be 4 or 5",
    "res.encode.title": "Color Code",
    "res.smd.help": "Decode an SMD resistor marking (3/4 digits and EIA-96).",
    "res.smd.arg": "SMD code: 103, 4R7, 1002, 01C",
    "res.smd.title": "SMD Resistor",
    "res.table.help": "Color code reference table.",
    "res.table.title": "Resistor Color Codes",
    "res.table.footer": "Without a tolerance band: ±20%. Example: elektro resistor bn bk rd gd",
    "res.col.code": "Code",
    "res.col.color": "Color",
    "res.col.digit": "Digit",
    "res.col.mult": "Multiplier",
    "res.col.tol": "Tolerance",
    "res.unknown_color": "unknown color '{code}'",
    "res.band_count": "enter 3, 4, 5 or 6 bands",
    "res.bad_digit": "band {pos} ({color}) cannot be a digit band",
    "res.bad_mult": "multiplier band cannot be {color}",
    "res.bad_tol": "tolerance band cannot be {color}",
    "res.bad_tempco": "temperature coefficient band cannot be {color}",
    "res.cannot_encode": "{value} cannot be written as a color code",
    "res.bad_tol_value": "invalid tolerance {tol}% (options: {options})",
    "res.eia96_range": "EIA-96 code must be between 01 and 96",
    "res.smd_invalid": "could not parse SMD code '{code}' (examples: 103, 4R7, 1002, 01C)",
    "res.see_table": "Colors: elektro resistor table",
    "res.title": "Resistor",
    "res.value": "Value",
    "res.tolerance": "Tolerance",
    "res.range": "Range",
    "res.tempco": "Temp. coefficient",
    "res.bands": "Bands",
    "res.codes": "Codes",
    "res.code": "Code",
    "res.note": "Note",
    "res.rounded": "{value} cannot be written exactly with {bands} bands; rounded",
    "res.nearest_std": "Nearest standard",

    # --- series / parallel ------------------------------------------------------------
    "combine.series.help": (
        "Total of components in series (default: resistors).\n\n"
        "Examples:\n"
        "  elektro series 1k 2k2 470\n"
        "  elektro series 100n 100n --cap"
    ),
    "combine.parallel.help": (
        "Equivalent of components in parallel (default: resistors).\n\n"
        "Examples:\n"
        "  elektro parallel 1k 1k\n"
        "  elektro parallel 10u 22u --cap"
    ),
    "combine.arg.series": "Component values, e.g. 1k 2k2 470",
    "combine.arg.parallel": "Component values, e.g. 1k 1k",
    "combine.opt.cap": "Treat as capacitors",
    "combine.opt.ind": "Treat as inductors",
    "combine.item": "Component {n}",
    "combine.total": "Total",
    "combine.series_title": "Series Connection",
    "combine.parallel_title": "Parallel Connection",

    # --- divider -------------------------------------------------------------------------
    "div.help": (
        "Voltage divider: Vout = Vin · R2 / (R1 + R2)\n\n"
        "With R1 and R2 it computes the output; with --vout it suggests\n"
        "the best R1/R2 pairs from standard values.\n\n"
        "Examples:\n"
        "  elektro divider --vin 12 --r1 10k --r2 4k7\n"
        "  elektro divider --vin 5 --vout 3.3\n"
        "  elektro divider --vin 12 --vout 3.3 --series E12"
    ),
    "div.opt.vin": "Input voltage (V)",
    "div.opt.r1": "Top resistor (between Vin and output)",
    "div.opt.r2": "Bottom resistor (between output and ground)",
    "div.opt.vout": "Target output (for R1/R2 suggestions)",
    "div.opt.series": "E series for suggestions",
    "div.opt.load": "Load resistance on the output",
    "div.range": "0 < Vout < Vin is required",
    "div.need": "give --r1 and --r2, or --vout",
    "div.none": "no suitable pair found",
    "div.title": "Voltage Divider",
    "div.ratio": "Ratio",
    "div.current": "Current",
    "div.unloaded": "Unloaded Vout",
    "div.col.error": "Error",
    "div.col.current": "Current",

    # --- LED --------------------------------------------------------------------------------
    "led.help": (
        "LED series resistor calculation.\n\n"
        "Examples:\n"
        "  elektro led --vs 5\n"
        "  elektro led --vs 12 --vf 3.1 -i 15m -n 3"
    ),
    "led.opt.vs": "Supply voltage (V)",
    "led.opt.vf": "LED forward voltage (V). Red ~2, blue/white ~3",
    "led.opt.if": "LED current (A), e.g. 20m",
    "led.opt.count": "Number of LEDs in series",
    "led.opt.series": "E series for the suggestion",
    "led.supply_low": "supply ({vs} V) must be higher than the LED voltage drop ({drop} V)",
    "led.current_pos": "current must be positive",
    "led.title": "LED Resistor",
    "led.calc_r": "Calculated R",
    "led.suggested": "Suggested ({series})",
    "led.real_i": "Actual current",
    "led.power": "Resistor power",
    "led.rating": "Recommended rating",
    "led.rating_high": "> 10 W (consider another solution)",
    "led.efficiency": "Efficiency",

    # --- E series ----------------------------------------------------------------------------
    "eseries.help": (
        "Show the nearest standard (E3…E192) values to a value.\n\n"
        "Examples:\n"
        "  elektro eseries 4k8\n"
        "  elektro eseries 3.3u -s E12"
    ),
    "eseries.arg": "Value to look up, e.g. 4k8",
    "eseries.opt.series": "Only this series (e.g. E24)",
    "eseries.title": "Standard values for {value}",
    "eseries.col.series": "Series",
    "eseries.col.lower": "Lower",
    "eseries.col.upper": "Upper",
    "eseries.col.nearest": "Nearest",
    "eseries.col.error": "Error",

    # --- capacitor ------------------------------------------------------------------------
    "cap.help": (
        "Decode a ceramic capacitor code, or generate the code from a value.\n\n"
        "Examples:\n"
        "  elektro cap 104       → 100 nF\n"
        "  elektro cap 472K      → 4.7 nF ±10%\n"
        "  elektro cap 22n       → 223"
    ),
    "cap.arg": "Code (104, 472K) or value (100n)",
    "cap.bad_code": "3-digit code expected (e.g. 104, 472K)",
    "cap.title": "Capacitor",
    "cap.code": "Code",
    "cap.value": "Value",
    "cap.tolerance": "Tolerance",
    "cap.not_ceramic": "this value is probably not a ceramic capacitor",

    # --- filters -----------------------------------------------------------------------------
    "flt.help": "RC/RL/LC/RLC filter analysis and design.",
    "flt.response": "Frequency response",
    "flt.gain": "Gain",
    "flt.phase": "Phase",
    "flt.need_two": "give exactly two of {opts}",
    "flt.opt.r": "Resistance (Ω), e.g. 1k",
    "flt.opt.c": "Capacitance (F), e.g. 100n",
    "flt.opt.l": "Inductance (H), e.g. 10m",
    "flt.opt.fc": "Cutoff frequency (Hz), e.g. 1k",
    "flt.opt.f0": "Resonant frequency (Hz)",
    "flt.fc": "Cutoff frequency (fc)",
    "flt.omega": "Angular frequency (ωc)",
    "flt.tau": "Time constant (τ)",
    "flt.r": "Resistance (R)",
    "flt.c": "Capacitance (C)",
    "flt.l": "Inductance (L)",
    "flt.f0": "Resonant frequency (f₀)",
    "flt.center": "Center frequency (f₀)",
    "flt.bw": "Bandwidth (BW)",
    "flt.q": "Quality factor (Q)",
    "flt.lower": "Lower cutoff",
    "flt.upper": "Upper cutoff",
    "flt.rc.help": (
        "RC filter (low-pass by default). Give two of R, C, fc.\n\n"
        "fc = 1 / (2πRC)    τ = RC\n\n"
        "Examples:\n"
        "  elektro filter rc --r 1k --c 100n\n"
        "  elektro filter rc --fc 1k --c 10n          (finds R)\n"
        "  elektro filter rc --r 10k --fc 50 --high   (finds C)"
    ),
    "flt.rc.opt.high": "High-pass (C in series, R to ground)",
    "flt.rc.title_low": "RC Low-Pass Filter",
    "flt.rc.title_high": "RC High-Pass Filter",
    "flt.rc.note1": "At fc the gain is -3 dB and the phase {phase}; slope 20 dB/decade.",
    "flt.rc.note2": "The capacitor reaches 63% of its final value in τ, and is fully charged after ~5τ.",
    "flt.rl.help": (
        "RL filter (high-pass by default). Give two of R, L, fc.\n\n"
        "fc = R / (2πL)    τ = L / R\n\n"
        "Examples:\n"
        "  elektro filter rl --r 1k --l 10m\n"
        "  elektro filter rl --r 100 --fc 10k --low"
    ),
    "flt.rl.opt.low": "Low-pass (L in series, R to ground)",
    "flt.rl.title_low": "RL Low-Pass Filter",
    "flt.rl.title_high": "RL High-Pass Filter",
    "flt.lc.help": (
        "LC resonance. Give two of L, C, f.\n\n"
        "f₀ = 1 / (2π√(LC))    Z₀ = √(L/C)\n\n"
        "Examples:\n"
        "  elektro filter lc --l 10u --c 100n\n"
        "  elektro filter lc --f 433.92M --c 10p     (finds L)"
    ),
    "flt.lc.title": "LC Resonance",
    "flt.lc.reactance": "Reactance (XL = XC)",
    "flt.lc.z0": "Characteristic impedance",
    "flt.lc.note": "A series LC has minimum impedance at resonance, a parallel LC (tank) maximum.",
    "flt.rlc.help": (
        "Series RLC band-pass filter (output across R).\n\n"
        "f₀ = 1 / (2π√(LC))   BW = R / (2πL)   Q = f₀ / BW\n\n"
        "Example:\n"
        "  elektro filter rlc --r 10 --l 1m --c 100n"
    ),
    "flt.rlc.title": "Series RLC Band-Pass",
    "flt.rlc.note": "High Q → narrow band, high selectivity. Low Q → wide band.",
    "flt.notch.help": (
        "Band-stop (notch): parallel LC tank in the signal path, output across R.\n\n"
        "f₀ = 1 / (2π√(LC))   Q = R / (2πf₀L)\n\n"
        "Example (50 Hz mains hum):\n"
        "  elektro filter notch --r 1k --l 1.013 --c 10u"
    ),
    "flt.notch.opt.r": "Load resistance (Ω)",
    "flt.notch.title": "Band-Stop (Notch)",
    "flt.notch.f0": "Notch frequency (f₀)",
    "flt.notch.note": "With ideal components attenuation at f₀ is infinite; in practice coil resistance limits it.",
    "flt.theory.help": "Summary of filter types and formulas.",
    "flt.theory.title": "Filter Theory",
    "flt.theory.body": (
        "[bold]Low-pass[/]   RC: R series, C to ground   ·  RL: L series, R to ground\n"
        "[bold]High-pass[/]  RC: C series, R to ground   ·  RL: R series, L to ground\n"
        "[bold]Band-pass[/]  Series RLC, output across R (minimum Z at resonance)\n"
        "[bold]Band-stop[/]  Parallel LC tank in the signal path (maximum Z at resonance)\n\n"
        "fc(RC) = 1/(2πRC)     fc(RL) = R/(2πL)\n"
        "f₀(LC) = 1/(2π√(LC))  Q = f₀/BW\n"
        "1st-order filter: -3 dB at fc, 20 dB/decade slope"
    ),

    # --- RF ---------------------------------------------------------------------------------
    "rf.help": "RF: FSPL, link budget, wavelength and unit conversions.",
    "rf.metavar.freq": "FREQ",
    "rf.metavar.dist": "DIST",
    "rf.opt.freq": "Frequency. A plain number is MHz: 868, 2.4G, 433.92M",
    "rf.opt.dist": "Distance. A plain number is km: 5, 800m, 12km",
    "rf.bad_distance": "could not parse distance '{text}' (e.g. 5, 2.5km, 800m)",
    "rf.positive": "frequency and distance must be positive",
    "rf.freq": "Frequency",
    "rf.dist": "Distance",
    "rf.wavelength": "Wavelength",
    "rf.fspl.help": (
        "Free-space path loss (ITU-R P.525).\n\n"
        "FSPL(dB) = 20·log₁₀(d) + 20·log₁₀(f) + 20·log₁₀(4π/c)\n\n"
        "Examples:\n"
        "  elektro rf fspl -f 868 -d 5\n"
        "  elektro rf fspl -f 2.4G -d 300m"
    ),
    "rf.fspl.title": "Free-Space Path Loss",
    "rf.fspl.note": "For the link margin see: elektro rf link --help",
    "rf.link.help": (
        "Link budget: received power, link margin and theoretical maximum range.\n\n"
        "Prx = Ptx + Gtx + Grx − FSPL − losses\n\n"
        "Examples:\n"
        "  elektro rf link -f 868 -d 10 --tx 14 --sens -137\n"
        "  elektro rf link -f 2.4G -d 500m --tx 20 --gtx 5 --grx 5 --sens -90 --loss 3"
    ),
    "rf.link.opt.tx": "Transmitter power (dBm)",
    "rf.link.opt.gtx": "Transmit antenna gain (dBi)",
    "rf.link.opt.grx": "Receive antenna gain (dBi)",
    "rf.link.opt.sens": "Receiver sensitivity (dBm)",
    "rf.link.opt.loss": "Total cable/connector/environment losses (dB)",
    "rf.link.title": "Link Budget",
    "rf.link.prx": "Received power",
    "rf.link.sens": "Sensitivity",
    "rf.link.margin": "Link margin",
    "rf.link.solid": "solid",
    "rf.link.marginal": "marginal",
    "rf.link.no_link": "NO LINK",
    "rf.link.range0": "Max. range (0 dB margin)",
    "rf.link.range10": "Max. range (10 dB margin)",
    "rf.link.note1": "Assumes free space; obstacles, the Fresnel zone and fading reduce range considerably.",
    "rf.link.note2": "In practice a 10-20 dB margin is recommended.",
    "rf.wave.help": (
        "Wavelength and basic antenna lengths.\n\n"
        "Examples:\n"
        "  elektro rf wave -f 433.92\n"
        "  elektro rf wave -f 2.4G --vf 0.95"
    ),
    "rf.wave.opt.vf": "Velocity factor (coax ~0.66-0.85, wire antenna ~0.95)",
    "rf.wave.bad": "frequency must be positive and 0 < vf ≤ 1",
    "rf.wave.title": "Wavelength",
    "rf.wave.dipole": "λ/2 dipole (total)",
    "rf.wave.monopole": "λ/4 monopole / GP",
    "rf.conv.help": (
        "RF unit conversion (power and impedance match).\n\n"
        "Examples:\n"
        "  elektro rf convert 14 dbm w\n"
        "  elektro rf convert 0.1 w\n"
        "  elektro rf convert 1.5 vswr"
    ),
    "rf.conv.arg.value": "Value",
    "rf.conv.arg.src": "Source unit: dbm dbw w mw uw vswr rl gamma",
    "rf.conv.arg.dst": "Target unit (all if omitted)",
    "rf.conv.vswr": "VSWR must be ≥ 1",
    "rf.conv.rl": "return loss must be ≥ 0 dB",
    "rf.conv.gamma": "|Γ| must be between 0 and 1",
    "rf.conv.power_pos": "power must be positive",
    "rf.conv.no_path": "no conversion from {src} to {dst}",
    "rf.conv.unknown": "unknown unit '{unit}'",
    "rf.conv.l.rl": "Return loss",
    "rf.conv.l.mismatch": "Mismatch loss",
    "rf.conv.l.reflected": "Reflected power",

    # --- digital ---------------------------------------------------------------------------
    "dig.help": "Digital: number bases, logic gates, boolean expressions.",
    "dig.base_range": "base must be between 2 and 36",
    "dig.conv.help": (
        "Convert between number bases (2-36).\n\n"
        "Without a target it shows binary, octal, decimal and hexadecimal together.\n\n"
        "Examples:\n"
        "  elektro logic convert 255\n"
        "  elektro logic convert 0xFF -t 2\n"
        "  elektro logic convert 1010 -f 2\n"
        "  elektro logic convert --bits 8 -- -5"
    ),
    "dig.conv.arg": "Number: 255, 0xFF, 0b1010, 0o17, 1Fh",
    "dig.conv.opt.from": "Source base (default: from prefix, or 10)",
    "dig.conv.opt.to": "Only convert to this base",
    "dig.conv.opt.bits": "Bit width (two's complement for negatives)",
    "dig.conv.invalid": "'{value}' is not a valid number",
    "dig.conv.in_base": " (base {base})",
    "dig.conv.overflow": "{n} does not fit in {bits} bits ({lo} … {hi})",
    "dig.conv.base": "base {base}",
    "dig.conv.title": "Number Conversion",
    "dig.dec": "Decimal",
    "dig.hex": "Hexadecimal",
    "dig.bin": "Binary",
    "dig.oct": "Octal",
    "dig.bits": "Bits",
    "dig.unsigned": "Unsigned",
    "dig.truth.help": (
        "Logic gate output or (without inputs) truth table.\n\n"
        "Examples:\n"
        "  elektro logic truth xor\n"
        "  elektro logic truth nand -a 1 -b 1"
    ),
    "dig.truth.arg": "Gate: {gates}",
    "dig.truth.opt.a": "Input A (0/1)",
    "dig.truth.opt.b": "Input B (0/1)",
    "dig.truth.unknown": "unknown gate '{gate}' (options: {gates})",
    "dig.expr.help": (
        "Truth table and minterms of a boolean expression.\n\n"
        "Operators: & (AND), | (OR), ^ (XOR), ~ (NOT). and/or/xor/not also work.\n\n"
        "Examples:\n"
        "  elektro logic expr \"A & B | ~C\"\n"
        "  elektro logic expr \"(A xor B) and C\""
    ),
    "dig.expr.arg": "Boolean expression, e.g. \"A & B | ~C\"",
    "dig.expr.invalid": "could not parse expression: {expr}",
    "dig.expr.unsupported": "unsupported element: {node}",
    "dig.expr.const": "only 0 and 1 may be used as constants",
    "dig.expr.too_many": "at most 6 variables are supported",

    # --- 555 ----------------------------------------------------------------------------------
    "555.help": "NE555 timer: astable and monostable.",
    "555.astable.help": (
        "Astable (oscillator) mode.\n\n"
        "f = 1.44 / ((R1 + 2R2)·C)    D = (R1 + R2) / (R1 + 2R2)\n\n"
        "Examples:\n"
        "  elektro 555 astable --r1 1k --r2 10k --c 10u\n"
        "  elektro 555 astable -f 1k -d 60 --c 10n     (finds R1, R2)"
    ),
    "555.mono.help": (
        "Monostable (one-shot) mode. Give two of R, C, t.\n\n"
        "t = 1.1 · R · C\n\n"
        "Examples:\n"
        "  elektro 555 mono --r 100k --c 10u\n"
        "  elektro 555 mono --t 5 --c 100u     (finds R)"
    ),
    "555.opt.r1": "R1 (between VCC and DIS)",
    "555.opt.r2": "R2 (between DIS and THR/TRIG)",
    "555.opt.c": "Timing capacitor",
    "555.opt.r": "Timing resistor",
    "555.opt.t": "Pulse width (s)",
    "555.opt.freq": "Target frequency (design mode)",
    "555.opt.duty": "Target duty cycle in % (design mode)",
    "555.duty_range": ("in the classic 555 astable the duty cycle must be above 50% "
                       "(for lower values add a diode across R2)"),
    "555.need": "give --r1 and --r2, or --freq",
    "555.mono.need": "give exactly two of --r, --c, --t",
    "555.design.title": "555 Astable Design",
    "555.r1_calc": "R1 (calculated)",
    "555.r2_calc": "R2 (calculated)",
    "555.real_freq": "Actual frequency",
    "555.real_duty": "Actual duty cycle",
    "555.range_warn": "Warning: R1 ≥ 1 kΩ and R2 ≤ 1 MΩ are recommended; change the capacitor value.",
    "555.astable.title": "555 Astable",
    "555.freq": "Frequency",
    "555.period": "Period",
    "555.t_high": "High time",
    "555.t_low": "Low time",
    "555.duty": "Duty cycle",
    "555.mono.title": "555 Monostable",
    "555.pulse": "Pulse width",

    # --- datasheet ------------------------------------------------------------------------
    "ds.help": (
        "Find a component datasheet and download it to the current folder.\n\n"
        "Checks manufacturer sites first, then the LCSC parts database, and\n"
        "finally a DuckDuckGo search. The download is verified to be a real PDF.\n\n"
        "Examples:\n"
        "  elektro datasheet lm358\n"
        "  elektro datasheet ams1117 --open\n"
        "  elektro datasheet 2n2222 -o transistor.pdf\n"
        "  elektro datasheet esp32 --list"
    ),
    "ds.arg.part": "Part number, e.g. lm358, ne555, ams1117, esp32",
    "ds.opt.output": "Output path (default: <part>_datasheet.pdf)",
    "ds.opt.open": "Open the PDF after downloading",
    "ds.opt.list": "List candidates without downloading",
    "ds.opt.force": "Overwrite if the file exists",
    "ds.opt.max": "Maximum number of candidates to try",
    "ds.step.maker": "Checking manufacturer sites",
    "ds.step.lcsc": "Searching the LCSC/JLCPCB parts database",
    "ds.step.ddg": "Searching DuckDuckGo",
    "ds.step.ddg_blocked": "DuckDuckGo is showing bot protection right now, skipped",
    "ds.no_opener": "'{opener}' not found, open the file manually: {path}",
    "ds.empty": "part number cannot be empty",
    "ds.candidates": "Candidates for '{part}':",
    "ds.no_candidates": "No candidates found.",
    "ds.exists": "File already exists",
    "ds.use_force": "Use --force to download again.",
    "ds.no_dir": "folder does not exist: {path}",
    "ds.searching": "Searching datasheet for '{part}'",
    "ds.downloaded": "Downloaded",
    "ds.try_next": "Could not get a PDF, trying the next one",
    "ds.cancelled": "Cancelled.",
    "ds.nothing": "No results from any source.",
    "ds.check_net": "Check your internet connection or the part number.",
    "ds.all_failed": "Could not download a PDF from any of the candidates.",
    "ds.manual": "Search manually:",
}

# --- 0.4: new commands ------------------------------------------------------------------
MESSAGES.update({
    "cli.opt.json": "Print results as JSON (for scripts)",
    "panel.power": "Power & wiring",
    "panel.embedded": "Embedded",
    "menu.switch": "Transistor as a switch",
    "menu.charge": "RC/RL charge curve",
    "menu.regulator": "Voltage regulator",
    "menu.battery": "Battery life",
    "menu.thermal": "Heat & heatsink",
    "menu.wire": "Wire gauge, voltage drop",
    "menu.trace": "PCB trace width",
    "menu.uart": "UART baud error",
    "menu.pwm": "Timer/PWM registers",
    "menu.adc": "ADC voltage ↔ code",
    "menu.i2c": "I²C pull-up resistor",
    "menu.crc": "CRC / checksum",
    "menu.calc": "Calculator with units",
    "menu.unit": "Unit converter",
    "time.min": "min",
    "time.hours": "hours",
    "time.days": "days",
    "time.months": "months",

    # regulator
    "reg.help": (
        "Voltage regulator: resistors for adjustable parts, dissipation for linear ones.\n\n"
        "Adjustable: lm317, lm1117, ams1117, lm2596, xl4015, mp1584\n"
        "Fixed: 7805, 7812, ams1117-3.3 …\n\n"
        "Examples:\n"
        "  elektro regulator lm317 --vout 5\n"
        "  elektro regulator lm317 --r1 240 --r2 720\n"
        "  elektro regulator 7805 --vin 12 -i 500m\n"
        "  elektro regulator ams1117-3.3 --vin 5 -i 300m"
    ),
    "reg.arg": "Regulator part, e.g. lm317, 7805, ams1117-3.3",
    "reg.opt.vout": "Target output voltage (adjustable parts)",
    "reg.opt.vin": "Input voltage",
    "reg.opt.iout": "Load current",
    "reg.opt.r1": "R1 (between OUT and ADJ/FB); default: datasheet value",
    "reg.opt.r2": "R2 (between ADJ/FB and ground) — computes Vout",
    "reg.unknown": "unknown regulator '{name}' (known: {options})",
    "reg.vout_low": "output must be above the reference voltage ({vref} V)",
    "reg.need_vout": "give --vout, or --r2 to compute the output",
    "reg.vout": "Output voltage",
    "reg.r2_calc": "R2 (calculated)",
    "reg.dropout": "Typical dropout",
    "reg.headroom": "Vin − Vout",
    "reg.dropout_warn": "Vin − Vout = {headroom} V is below the typical dropout ({dropout} V); output may sag.",
    "reg.power": "Dissipation",
    "reg.efficiency": "Efficiency",
    "reg.switching_note": "Switching regulator: dissipation depends on efficiency (typically 80-95%), see the datasheet.",
    "reg.heat_note": "Over 1 W needs a heatsink in most packages — check with: elektro thermal --help",

    # battery
    "bat.help": (
        "Battery life from capacity and average current (or an active/sleep profile).\n\n"
        "Examples:\n"
        "  elektro battery 2000 -i 15m\n"
        "  elektro battery 1200 --active 45m --active-time 2 --sleep 20u --sleep-time 58"
    ),
    "bat.arg": "Capacity in mAh",
    "bat.opt.current": "Average current (A), e.g. 15m",
    "bat.opt.active": "Current while active (A)",
    "bat.opt.active_time": "Time active per cycle (s)",
    "bat.opt.sleep": "Current while sleeping (A)",
    "bat.opt.sleep_time": "Time asleep per cycle (s)",
    "bat.opt.derate": "Usable fraction of the capacity (aging, temperature, cutoff)",
    "bat.need": "give -i, or all of --active --active-time --sleep --sleep-time",
    "bat.title": "Battery Life",
    "bat.capacity": "Capacity",
    "bat.usable": "Usable",
    "bat.avg_current": "Average current",
    "bat.life": "Estimated life",
    "bat.note": "Self-discharge and regulator quiescent current are not included.",

    # thermal
    "th.help": (
        "Junction temperature and required heatsink.\n\n"
        "Tj = Ta + P · (Rθjc + Rθcs + Rθsa)   or   Tj = Ta + P · Rθja\n\n"
        "Examples:\n"
        "  elektro thermal -p 2 --rth-ja 62 --ta 40          (no heatsink, TO-220)\n"
        "  elektro thermal -p 5 --rth-jc 3 --rth-sa 8\n"
        "  elektro thermal -p 5 --rth-jc 3 --ta 50           (required heatsink)"
    ),
    "th.opt.power": "Dissipated power (W)",
    "th.opt.ta": "Ambient temperature (°C)",
    "th.opt.tjmax": "Maximum junction temperature (°C)",
    "th.opt.rja": "Junction-to-ambient thermal resistance without heatsink (°C/W)",
    "th.opt.rjc": "Junction-to-case thermal resistance (°C/W)",
    "th.opt.rcs": "Case-to-heatsink (thermal pad/paste) (°C/W)",
    "th.opt.rsa": "Heatsink-to-ambient (°C/W)",
    "th.need": "give --rth-ja, or --rth-jc (with or without --rth-sa)",
    "th.title": "Thermal",
    "th.power": "Power",
    "th.total": "Total Rθ",
    "th.need_sa": "Required heatsink Rθsa ≤",
    "th.impossible": "impossible — reduce the power",
    "th.margin": "Margin to Tj max",
    "th.margin_note": "Choose a heatsink comfortably below this value (~20-30% margin).",
    "th.over": "The junction temperature exceeds the maximum!",

    # wire
    "wire.help": (
        "Copper wire: AWG ↔ mm², resistance, voltage drop and loss.\n\n"
        "Examples:\n"
        "  elektro wire --awg 22 -l 3 -i 2\n"
        "  elektro wire --mm2 1.5 -l 10 -i 10 --round-trip"
    ),
    "wire.opt.awg": "Wire gauge (AWG)",
    "wire.opt.mm2": "Cross-section (mm²)",
    "wire.opt.length": "Length (plain number = m): 3, 50cm, 10ft",
    "wire.opt.current": "Current (A)",
    "wire.opt.round_trip": "Count the length twice (supply + return conductor)",
    "wire.opt.temp": "Conductor temperature (°C)",
    "wire.metavar.length": "LENGTH",
    "wire.bad_length": "could not parse length '{text}' (e.g. 3, 50cm, 10ft)",
    "wire.need": "give either --awg or --mm2",
    "wire.title": "Copper Wire",
    "wire.diameter": "Diameter",
    "wire.area": "Cross-section",
    "wire.r_per_m": "Resistance per metre",
    "wire.resistance": "Resistance",
    "wire.drop": "Voltage drop",
    "wire.loss": "Power loss",
    "wire.density": "Current density",
    "wire.hot": "Current density is high; the wire may heat up (> 6 A/mm²).",
    "wire.note": "Solid copper; stranded wire has slightly higher resistance.",

    # trace
    "trace.help": (
        "PCB trace width by IPC-2221 (or the current a trace can carry).\n\n"
        "Examples:\n"
        "  elektro trace -i 3\n"
        "  elektro trace -i 5 --rise 20 --oz 2\n"
        "  elektro trace -w 0.5 --internal -l 40mm"
    ),
    "trace.opt.current": "Current (A)",
    "trace.opt.width": "Trace width in mm (computes the current)",
    "trace.opt.rise": "Allowed temperature rise (°C)",
    "trace.opt.oz": "Copper weight (oz/ft²): 0.5, 1, 2",
    "trace.opt.internal": "Internal layer (external by default)",
    "trace.opt.length": "Trace length (plain number = m): 40mm, 0.1",
    "trace.need": "give either -i or -w",
    "trace.title": "PCB Trace (IPC-2221)",
    "trace.width": "Width",
    "trace.current": "Current",
    "trace.thickness": "Copper",
    "trace.layer": "Layer",
    "trace.internal": "internal",
    "trace.external": "external",
    "trace.rise": "Temperature rise",
    "trace.note": "IPC-2221 is conservative; for high currents also check IPC-2152.",

    # transistor switch
    "sw.help": "Transistor as a switch: BJT base resistor, MOSFET gate drive.",
    "sw.opt.vdrive": "Drive voltage (e.g. GPIO 3.3 or 5 V)",
    "sw.bjt.help": (
        "BJT (NPN) saturated switch: base resistor and losses.\n\n"
        "Ib = Ic / hFE · k     Rb = (Vdrive − Vbe) / Ib\n\n"
        "Examples:\n"
        "  elektro switch bjt --ic 500m -v 3.3\n"
        "  elektro switch bjt --vcc 12 --rload 24 -v 5 --hfe 150"
    ),
    "sw.bjt.opt.ic": "Collector (load) current",
    "sw.bjt.opt.hfe": "Minimum current gain hFE (from the datasheet)",
    "sw.bjt.opt.overdrive": "Overdrive factor k for solid saturation (2-5)",
    "sw.bjt.opt.vbe": "Base-emitter voltage (V)",
    "sw.bjt.opt.vcesat": "Collector-emitter saturation voltage (V)",
    "sw.bjt.opt.vcc": "Supply voltage (with --rload, instead of --ic)",
    "sw.bjt.opt.rload": "Load resistance (with --vcc)",
    "sw.bjt.need": "give --ic, or --vcc and --rload",
    "sw.bjt.vdrive_low": "drive voltage must be above Vbe ({vbe} V)",
    "sw.bjt.title": "BJT Switch",
    "sw.bjt.ib": "Required Ib",
    "sw.bjt.rb_calc": "Rb (calculated)",
    "sw.bjt.rb_std": "Rb (E12, one lower)",
    "sw.bjt.forced_beta": "Forced β (Ic/Ib)",
    "sw.bjt.p_transistor": "Transistor loss",
    "sw.bjt.p_rb": "Rb power",
    "sw.bjt.gpio_warn": "Base current {ib} is too high for most MCU pins; use a Darlington or MOSFET.",
    "sw.bjt.note": "For inductive loads (relay, motor) add a flyback diode across the load.",
    "sw.fet.help": (
        "MOSFET gate drive: gate current, switching time and losses.\n\n"
        "Examples:\n"
        "  elektro switch mosfet -v 10 --qg 40n --rg 10 -f 100k\n"
        "  elektro switch mosfet -v 5 --qg 20n -f 20k --id 5 --rds 20m --vds 24"
    ),
    "sw.fet.opt.qg": "Total gate charge Qg (C), e.g. 40n",
    "sw.fet.opt.rg": "Gate resistor (Ω)",
    "sw.fet.opt.fsw": "Switching frequency (Hz)",
    "sw.fet.opt.id": "Drain current (A)",
    "sw.fet.opt.rds": "On-resistance Rds(on) (Ω)",
    "sw.fet.opt.vds": "Drain-source voltage when off (V)",
    "sw.fet.title": "MOSFET Gate Drive",
    "sw.fet.ipeak": "Peak gate current",
    "sw.fet.tsw": "Switching time (≈ Qg/Ig)",
    "sw.fet.pgate": "Gate drive power",
    "sw.fet.pcond": "Conduction loss",
    "sw.fet.psw": "Switching loss (approx.)",
    "sw.fet.ptotal": "Total loss",
    "sw.fet.slow": "Switching takes more than 10% of the period; use a gate driver or smaller Rg.",
    "sw.fet.logic_level": "Drive below 5 V: use a logic-level MOSFET (Rds(on) specified at 2.5-4.5 V).",
    "sw.fet.note": "Estimates; the real switching time also depends on the Miller plateau and the driver.",

    # charge
    "chg.help": (
        "RC capacitor charge / RL inductor current over time.\n\n"
        "v(t) = Vf + (V0 − Vf) · e^(−t/τ)\n\n"
        "Examples:\n"
        "  elektro charge --r 10k --c 100u --v 5\n"
        "  elektro charge --r 10k --c 100u --v 5 --to 3.3      (time to 3.3 V)\n"
        "  elektro charge --r 10k --c 100u --v 0 --v0 5 --t 1  (discharge)\n"
        "  elektro charge --r 10 --l 1m --v 12                 (RL current)"
    ),
    "chg.opt.r": "Resistance (Ω)",
    "chg.opt.c": "Capacitance (F) for RC",
    "chg.opt.l": "Inductance (H) for RL",
    "chg.opt.v": "Applied (final) voltage (V)",
    "chg.opt.v0": "Initial capacitor voltage (V)",
    "chg.opt.to": "Target voltage: how long until reached",
    "chg.opt.t": "Time (s): value at this moment",
    "chg.need": "give either --c (RC) or --l (RL)",
    "chg.unreachable": "the target is never reached (it is not between the start and final value)",
    "chg.title_rc": "RC Charge",
    "chg.title_rl": "RL Current",
    "chg.final": "Final value",
    "chg.value_at": "Value at {time}",
    "chg.time_to": "Time to {target}",
    "chg.note": "After 1τ {pct} of the change is done; after 5τ it is practically complete.",

    # microstrip
    "ms.help": (
        "Microstrip line: trace width for an impedance, or impedance of a width (Hammerstad).\n\n"
        "Examples:\n"
        "  elektro rf microstrip --z0 50                   (1.6 mm FR4)\n"
        "  elektro rf microstrip --z0 50 --h 0.2 --er 4.2 -f 2.4G\n"
        "  elektro rf microstrip -w 3"
    ),
    "ms.opt.z0": "Target impedance (Ω)",
    "ms.opt.width": "Trace width (mm) — computes Z0",
    "ms.opt.h": "Dielectric thickness to the ground plane (mm)",
    "ms.opt.er": "Relative permittivity εr (FR4 ≈ 4.2-4.6)",
    "ms.need": "give either --z0 or --width",
    "ms.range": "impedance out of the achievable range",
    "ms.title": "Microstrip",
    "ms.width": "Trace width",
    "ms.lambda": "Wavelength on the line",
    "ms.note": "Copper thickness and solder mask are ignored; use your fab's calculator for final values.",

    # LoRa
    "lora.help": (
        "LoRa time on air, bit rate, sensitivity and duty-cycle limit (Semtech AN1200.13).\n\n"
        "Examples:\n"
        "  elektro rf lora --sf 9 -p 20\n"
        "  elektro rf lora --sf 12 --bw 125k --cr 4/8 -p 51"
    ),
    "lora.opt.sf": "Spreading factor (7-12)",
    "lora.opt.bw": "Bandwidth (Hz): 125k, 250k, 500k",
    "lora.opt.cr": "Coding rate: 4/5 … 4/8",
    "lora.opt.payload": "Payload length (bytes)",
    "lora.opt.preamble": "Preamble length (symbols)",
    "lora.opt.no_crc": "Without payload CRC",
    "lora.opt.implicit": "Implicit header mode",
    "lora.opt.duty": "Duty cycle limit in % (EU 868 MHz: 1)",
    "lora.opt.nf": "Receiver noise figure (dB)",
    "lora.bad_cr": "coding rate must be 4/5, 4/6, 4/7 or 4/8",
    "lora.airtime": "Time on air",
    "lora.symbol": "Symbol time",
    "lora.bitrate": "Bit rate",
    "lora.sensitivity": "Sensitivity (approx.)",
    "lora.per_hour": "Packets/hour at {duty}",
    "lora.interval": "every",
    "lora.on": "on",
    "lora.off": "off",
    "lora.note": "LDRO (low data rate optimisation) is enabled automatically when the symbol time exceeds 16 ms.",

    # Fresnel
    "fresnel.help": (
        "First Fresnel zone and the antenna height needed for line of sight.\n\n"
        "r₁ = √(λ·d₁·d₂ / D)\n\n"
        "Examples:\n"
        "  elektro rf fresnel -f 868 -d 10\n"
        "  elektro rf fresnel -f 2.4G -d 3 --at 500m"
    ),
    "fresnel.opt.at": "Distance of the obstacle from the transmitter (default: midpoint)",
    "fresnel.opt.k": "Effective earth radius factor (standard atmosphere 4/3)",
    "fresnel.bad_at": "the point must lie between the two antennas",
    "fresnel.title": "Fresnel Zone",
    "fresnel.point": "Point (d₁ / d₂)",
    "fresnel.r1": "1st Fresnel radius",
    "fresnel.r60": "60% clearance",
    "fresnel.bulge": "Earth bulge",
    "fresnel.need": "Required clearance",
    "fresnel.note": "The line between the antennas must pass this height above obstacles at that point.",

    # coax
    "coax.help": (
        "Coaxial cable loss at a frequency (typical values).\n\n"
        "Cables: RG-58, RG-174, RG-316, RG-213, RG-6, LMR-195, LMR-240, LMR-400, LMR-600\n\n"
        "Examples:\n"
        "  elektro rf coax rg58 -f 868 -l 5\n"
        "  elektro rf coax lmr400 -f 2.4G -l 20m"
    ),
    "coax.arg": "Cable type, e.g. rg58, lmr400",
    "coax.opt.length": "Cable length (plain number = m): 5, 150cm, 30ft",
    "coax.metavar.length": "LENGTH",
    "coax.unknown": "unknown cable '{name}' (known: {options})",
    "coax.per100": "Loss per 100 m",
    "coax.loss": "Total loss",
    "coax.delivered": "Power delivered",
    "coax.delay": "Delay",
    "coax.electrical": "Electrical length",
    "coax.note": "Typical values; see the manufacturer's datasheet for your exact cable. Connectors add ~0.1-0.3 dB each.",

    # MCU common
    "mcu.opt.clock": "Peripheral clock (Hz), e.g. 16M, 72M",
    "mcu.opt.mcu": "Microcontroller family: avr, stm32, generic",
    "mcu.unknown": "unknown MCU family '{mcu}' (options: {options})",

    # UART
    "uart.help": (
        "UART baud rate register and error.\n\n"
        "Without --baud a table of common rates is shown.\n\n"
        "Examples:\n"
        "  elektro uart -c 16M -b 115200\n"
        "  elektro uart -c 16M\n"
        "  elektro uart -c 72M -b 921600 -m stm32"
    ),
    "uart.opt.baud": "Baud rate",
    "uart.opt.oversample": "Oversampling for --mcu generic",
    "uart.col.baud": "Baud",
    "uart.col.mode": "Mode",
    "uart.col.register": "Register",
    "uart.col.actual": "Actual",
    "uart.col.error": "Error",
    "uart.impossible": "not possible",
    "uart.note": "Errors up to ±2% usually work; keep it below ±1% for reliability.",

    # PWM
    "pwm.help": (
        "Timer/PWM prescaler and period register for a frequency.\n\n"
        "Examples:\n"
        "  elektro pwm -c 16M -f 20k                 (AVR Timer1)\n"
        "  elektro pwm -c 16M -f 1k --bits 8\n"
        "  elektro pwm -c 72M -f 20k -m stm32 -d 25"
    ),
    "pwm.opt.freq": "PWM frequency (Hz)",
    "pwm.opt.bits": "Timer width in bits (8, 16, 32)",
    "pwm.opt.duty": "Duty cycle in % (computes the compare value)",
    "pwm.bad": "clock and frequency must be positive; bits must be 8, 10, 16 or 32",
    "pwm.impossible": "this frequency cannot be produced with this clock/timer",
    "pwm.prescaler": "Prescaler",
    "pwm.actual": "Actual frequency",
    "pwm.error": "Error",
    "pwm.resolution": "Resolution",
    "pwm.steps": "steps",
    "pwm.compare": "Compare value for {duty}",
    "pwm.low_res": "Resolution is below 8 bits; lower the frequency or raise the clock.",

    # ADC
    "adc.help": (
        "ADC/DAC: LSB size, voltage ↔ code conversion, ideal SNR.\n\n"
        "V = code · Vref / 2ᴺ\n\n"
        "Examples:\n"
        "  elektro adc -b 12 --vref 3.3 --code 2048\n"
        "  elektro adc -b 10 --vref 5 --volt 1.2"
    ),
    "adc.opt.bits": "Resolution in bits",
    "adc.opt.vref": "Reference voltage (V)",
    "adc.opt.code": "Digital code → voltage",
    "adc.opt.volt": "Voltage → digital code",
    "adc.steps": "Steps",
    "adc.snr": "Ideal SNR",
    "adc.voltage_of": "Voltage of code {code}",
    "adc.code_of": "Code of {volt}",
    "adc.code_range": "code must be between 0 and {max}",
    "adc.clipped": "The voltage is outside 0 … Vref; the code is clipped.",
    "adc.note": "Some datasheets use 2ᴺ − 1 as divisor; the difference is 1 LSB.",

    # I2C
    "i2c.help": (
        "I²C pull-up resistor range from bus capacitance and speed.\n\n"
        "Rmin = (Vdd − 0.4 V) / Iol     Rmax = tr / (0.8473 · Cb)\n\n"
        "Examples:\n"
        "  elektro i2c --cb 200p\n"
        "  elektro i2c --vdd 5 --cb 100p -s 100k"
    ),
    "i2c.opt.vdd": "Pull-up supply voltage (V)",
    "i2c.opt.cb": "Total bus capacitance (F), e.g. 200p (≈10 pF per device + wiring)",
    "i2c.opt.speed": "Bus speed: 100k, 400k or 1M",
    "i2c.bad_speed": "speed must be 100k, 400k or 1M",
    "i2c.cb_limit": "The I²C standard allows at most 400 pF bus capacitance.",
    "i2c.impossible": "no valid resistor: bus capacitance too high for this speed",
    "i2c.suggested": "Suggested (E12)",
    "i2c.note": "Smaller R = faster edges but higher current; stay between Rmin and Rmax.",

    # CRC
    "crc.help": (
        "CRC and simple checksums of a byte sequence.\n\n"
        "Examples:\n"
        "  elektro crc \"01 03 00 00 00 0A\"\n"
        "  elektro crc 0x31323334 -a modbus\n"
        "  elektro crc \"123456789\" --text"
    ),
    "crc.arg": "Data as hex bytes (\"01 03 0A\", 0x01030A) or text with --text",
    "crc.opt.text": "Treat the data as text (UTF-8)",
    "crc.opt.algo": "Only this algorithm (e.g. modbus, crc-32)",
    "crc.bad_hex": "invalid hex data (use pairs of hex digits, e.g. \"01 03 0A\")",
    "crc.unknown": "unknown algorithm '{algo}' (options: {options})",
    "crc.title": "CRC of {n} bytes",
    "crc.col.algo": "Algorithm",
    "crc.col.bytes": "Bytes (transmit order)",

    # calc
    "calc.help": (
        "Calculator that understands engineering notation and units.\n\n"
        "Operators: + − * / ^ ( )   Functions: sqrt log ln exp sin cos tan db dbp par\n"
        "Constants: pi e c.  par(a, b, …) = parallel combination.\n\n"
        "Examples:\n"
        "  elektro calc \"12V / (4k7 + 1k)\"\n"
        "  elektro calc \"1 / (2*pi*sqrt(10u * 100n))\" -u Hz\n"
        "  elektro calc \"par(1k, 2k2, 4k7)\" -u Ω\n"
        "  elektro calc \"db(3.3 / 0.1)\""
    ),
    "calc.arg": "Expression (quote it in the shell)",
    "calc.opt.unit": "Unit to show with the result (V, A, Ω, Hz …)",
    "calc.syntax": "could not parse the expression",
    "calc.unknown_name": "unknown name '{name}'",
    "calc.unsupported": "unsupported element in the expression",
    "calc.div_zero": "division by zero",
    "calc.complex": "the result is complex",

    # unit
    "unit.help": (
        "Unit converter for everyday electronics.\n\n"
        "Temperature: c f k · Length: m cm mm um in mil ft · dB: db pratio vratio\n"
        "Wire: awg mm2 · Copper: oz · Angle: deg rad · Frequency: hz rpm\n\n"
        "Examples:\n"
        "  elektro unit 25 c\n"
        "  elektro unit 10 mil mm\n"
        "  elektro unit 6 db\n"
        "  elektro unit 22 awg"
    ),
    "unit.arg.value": "Value",
    "unit.arg.src": "Source unit ({units})",
    "unit.arg.dst": "Target unit (all if omitted)",
    "unit.unknown": "unknown unit '{unit}' (options: {options})",
    "unit.no_path": "no conversion from {src} to {dst}",
    "unit.below_zero": "below absolute zero",
    "unit.power_ratio": "power ratio",
    "unit.voltage_ratio": "voltage ratio",
    "unit.period": "period (s)",

    # datasheet cache
    "ds.opt.history": "List previously downloaded datasheets (cache)",
    "ds.from_cache": "Found in the cache, no download needed.",
    "ds.cache_source": "cache",
    "ds.cache_empty": "The datasheet cache is empty.",
    "ds.cache_title": "Downloaded datasheets",
    "ds.col.part": "Part",
    "ds.col.size": "Size",
    "ds.col.date": "Date",
})

# --- 0.5 ---------------------------------------------------------------------------------
MESSAGES.update({
    "menu.opamp": "Op-amp amplifiers",
    "menu.coil": "Air-core coil",
    "menu.crystal": "Crystal load capacitors",
    "menu.rectifier": "Rectifier + filter capacitor",
    "menu.acpower": "AC power, PF correction",
    "menu.shell": "Interactive mode",
    "menu.vars": "Saved variables",
    "menu.history": "Calculation history",

    # op-amp
    "op.help": "Op-amp amplifiers: non-inverting, inverting, difference, summing.",
    "op.noninv.help": (
        "Non-inverting amplifier.  G = 1 + Rf / Rg\n\n"
        "With --gain it suggests standard Rf/Rg pairs; with --rf and --rg it computes the gain.\n\n"
        "Examples:\n"
        "  elektro opamp noninv --gain 11\n"
        "  elektro opamp noninv --rf 100k --rg 10k --vin 0.2 --gbw 1M"
    ),
    "op.inv.help": (
        "Inverting amplifier.  G = −Rf / Rin\n\n"
        "Examples:\n"
        "  elektro opamp inv --gain 10\n"
        "  elektro opamp inv --rf 47k --rin 4k7 --vin 0.5 --vcc 12"
    ),
    "op.diff.help": (
        "Difference amplifier (R1 = R3, R2 = R4).  Vout = (R2/R1) · (V+ − V−)\n\n"
        "Example:\n"
        "  elektro opamp diff --gain 5"
    ),
    "op.sum.help": (
        "Inverting summing amplifier.  Vout = −Rf · Σ(Vi / Ri)\n\n"
        "Example:\n"
        "  elektro opamp sum --rf 10k --rin 10k --vin 1 --rin 20k --vin 0.5"
    ),
    "op.opt.gain": "Target gain (V/V)",
    "op.opt.gain_inv": "Target gain magnitude (the sign is always negative)",
    "op.opt.rf": "Feedback resistor Rf",
    "op.opt.rg": "Resistor to ground Rg",
    "op.opt.rin": "Input resistor Rin",
    "op.opt.vin": "Input voltage (computes the output)",
    "op.opt.vcc": "Supply rail (warns if the output clips)",
    "op.opt.gbw": "Gain-bandwidth product of the op-amp (Hz), e.g. 1M",
    "op.need": "give --gain, or both resistors",
    "op.noninv.min": "a non-inverting amplifier cannot have a gain below 1",
    "op.follower": "voltage follower: connect the output directly to the − input",
    "op.pairs": "Standard resistor pairs",
    "op.gain": "Gain",
    "op.col.error": "Error",
    "op.bandwidth": "Bandwidth (−3 dB)",
    "op.zin": "Input impedance",
    "op.note": "Note",
    "op.clip": "Output {vout} exceeds the supply ({vcc}); it will clip.",
    "op.noninv.title": "Non-inverting Amplifier",
    "op.inv.title": "Inverting Amplifier",
    "op.sum.title": "Summing Amplifier",
    "op.noninv.note": "Keep Rf ∥ Rg ≈ source resistance for low offset; 1k-100k values are typical.",
    "op.inv.note": "The input impedance equals Rin; pick Rin large enough for the source.",
    "op.diff.note": "Resistor matching sets the common-mode rejection; use 0.1% resistors if possible.",
    "op.sum.opt.rin": "Input resistor (repeat once per input)",
    "op.sum.opt.vin": "Input voltage (repeat once per input, same order)",
    "op.sum.mismatch": "give the same number of --rin and --vin",

    # simplify
    "dig.simp.help": (
        "Simplify a boolean function to a minimal sum of products (Quine-McCluskey).\n\n"
        "Shows the Karnaugh map for 2-4 variables.\n\n"
        "Examples:\n"
        "  elektro logic simplify \"A&B | A&~B\"\n"
        "  elektro logic simplify -m 0,1,2,5,6,7 -v A,B,C\n"
        "  elektro logic simplify -m 1,3,7,11,15 -d 0,2,5"
    ),
    "dig.simp.arg": "Boolean expression (or use --minterms)",
    "dig.simp.opt.minterms": "Minterm list, e.g. 0,2,5,7",
    "dig.simp.opt.dontcare": "Don't-care terms, e.g. 1,3",
    "dig.simp.opt.vars": "Variable names, e.g. A,B,C,D (MSB first)",
    "dig.simp.need": "give an expression or --minterms",
    "dig.simp.bad_list": "the list must contain integers separated by commas",
    "dig.simp.few_vars": "at least {n} variables are needed for these minterms",
    "dig.simp.too_many": "at most 8 variables are supported",
    "dig.simp.title": "Simplified",
    "dig.simp.minterms": "Function",
    "dig.simp.result": "Minimal SOP",
    "dig.simp.code": "As expression",
    "dig.simp.cost": "Cost",
    "dig.simp.cost_val": "terms: {terms}, literals: {lits}",

    # rectifier
    "rect.help": (
        "Transformer + rectifier + reservoir capacitor.\n\n"
        "ΔV = I / (k · f · C)   (k = 2 full-wave, 1 half-wave)\n\n"
        "Examples:\n"
        "  elektro rectifier --vac 12 -i 1 --ripple 1\n"
        "  elektro rectifier --vac 9 -i 500m --c 2200u --vmains 230\n"
        "  elektro rectifier --vac 15 --type half -i 100m --ripple 0.5"
    ),
    "rect.opt.vac": "Secondary voltage (V RMS)",
    "rect.opt.type": "Rectifier: bridge, center (center-tap), half",
    "rect.opt.freq": "Mains frequency (Hz)",
    "rect.opt.iload": "Load current (A)",
    "rect.opt.ripple": "Allowed ripple (V p-p) — computes C",
    "rect.opt.c": "Reservoir capacitor — computes the ripple",
    "rect.opt.vdiode": "Forward voltage per diode (V)",
    "rect.opt.vmains": "Primary voltage (V RMS) — computes the turns ratio",
    "rect.bad_type": "rectifier type must be one of: {options}",
    "rect.too_low": "the secondary voltage is below the diode drops",
    "rect.title": "Rectifier",
    "rect.type": "Type",
    "rect.kind.bridge": "full-wave bridge",
    "rect.kind.center": "full-wave center-tap",
    "rect.kind.half": "half-wave",
    "rect.vpeak": "Peak DC (no load)",
    "rect.piv": "Diode reverse voltage (PIV)",
    "rect.ripple_freq": "Ripple frequency",
    "rect.c": "Capacitor",
    "rect.ripple": "Ripple (p-p)",
    "rect.cap_voltage": "Capacitor voltage rating",
    "rect.ratio": "Turns ratio",
    "rect.diode_i": "Current per diode",
    "rect.hint": "Add -i and --ripple (or --c) to size the reservoir capacitor.",
    "rect.note": "The capacitor ripple current is high; choose a low-ESR type rated for it.",

    # AC power
    "ac.help": (
        "Single- or three-phase AC power, and power factor correction.\n\n"
        "P = V·I·cosφ (1-phase)   P = √3·V·I·cosφ (3-phase, V line-to-line)\n\n"
        "Examples:\n"
        "  elektro acpower --v 230 --i 10 --pf 0.8\n"
        "  elektro acpower --v 400 --p 15k --pf 0.82 --phases 3\n"
        "  elektro acpower --i 10 --pf 0.75 --target-pf 0.95"
    ),
    "ac.opt.v": "Voltage (V RMS; line-to-line for 3-phase)",
    "ac.opt.i": "Current (A RMS)",
    "ac.opt.p": "Active power (W) — computes the current",
    "ac.opt.pf": "Power factor cosφ",
    "ac.opt.phases": "Number of phases: 1 or 3",
    "ac.opt.target": "Target power factor — computes the correction capacitor",
    "ac.bad_phases": "phases must be 1 or 3",
    "ac.bad_pf": "the voltage must be positive and 0 < cosφ ≤ 1",
    "ac.bad_target": "the target power factor must be above the current one and at most 1",
    "ac.need": "give --i or --p",
    "ac.title": "AC Power",
    "ac.system": "System",
    "ac.single": "single-phase",
    "ac.three": "three-phase",
    "ac.current": "Current",
    "ac.p": "Active power P",
    "ac.q": "Reactive power Q",
    "ac.s": "Apparent power S",
    "ac.qc": "Compensation Qc",
    "ac.cap": "Correction capacitor",
    "ac.cap_delta": "Capacitor per phase (Δ)",
    "ac.new_current": "Current after correction",
    "ac.three_note": "For a star-connected capacitor bank multiply the capacitance by 3.",

    # star-delta
    "sd.help": (
        "Star (Y) ↔ delta (Δ) conversion of three resistors/impedances.\n\n"
        "Examples:\n"
        "  elektro stardelta delta 10 20 30     (Rab Rbc Rca → Ra Rb Rc)\n"
        "  elektro stardelta star 5 10 15       (Ra Rb Rc → Rab Rbc Rca)"
    ),
    "sd.arg.mode": "What you give: delta or star",
    "sd.arg.values": "Three values: Rab Rbc Rca (delta) or Ra Rb Rc (star)",
    "sd.bad": "use: stardelta delta|star R1 R2 R3",
    "sd.note": "Ra is the resistor on node A, Rab the one between A and B.",

    # coil
    "coil.help": (
        "Single-layer air-core coil (Wheeler formula).\n\n"
        "Examples:\n"
        "  elektro coil --l 1u --d 10               (turns for 1 µH on a 10 mm form)\n"
        "  elektro coil --l 330n --d 6 --wire 0.8\n"
        "  elektro coil --n 12 --d 8 --length 15"
    ),
    "coil.opt.l": "Target inductance (H), e.g. 1u",
    "coil.opt.n": "Number of turns — computes L",
    "coil.opt.d": "Coil form diameter (mm)",
    "coil.opt.wire": "Wire diameter (mm)",
    "coil.opt.length": "Winding length (mm); default: close-wound",
    "coil.need": "give either --l or --n",
    "coil.title": "Air-core Coil",
    "coil.turns": "Turns",
    "coil.inductance": "Inductance",
    "coil.length": "Winding length",
    "coil.mean_d": "Mean diameter",
    "coil.wire_len": "Wire length",
    "coil.short": "The coil is very short compared to its diameter; the formula is less accurate.",
    "coil.note": "Wheeler's formula is ~1% accurate for length > 0.8 × radius. Leave extra wire for the leads.",

    # crystal
    "xtal.help": (
        "Load capacitors for a crystal oscillator (Pierce).\n\n"
        "C1 = C2 = 2 · (CL − Cstray)\n\n"
        "Examples:\n"
        "  elektro crystal --cl 12p\n"
        "  elektro crystal --cl 18p --cstray 3p\n"
        "  elektro crystal --c 22p                  (which CL do 22 pF give?)"
    ),
    "xtal.opt.cl": "Load capacitance from the crystal datasheet (F)",
    "xtal.opt.cstray": "Stray capacitance of pins and traces (F), typically 2-5p",
    "xtal.opt.c": "Existing capacitor value — computes CL",
    "xtal.need": "give either --cl or --c",
    "xtal.too_small": "CL is smaller than the stray capacitance; no capacitors needed (or check Cstray)",
    "xtal.title": "Crystal Load Capacitors",
    "xtal.standard": "Standard (E12)",
    "xtal.note": "Too much capacitance lowers the frequency and can stop the oscillator.",

    # plot
    "plot.opt": "Save a graph: .svg (built in), .png / .pdf (needs matplotlib)",
    "plot.saved": "Graph saved: {path}",
    "plot.bad_suffix": "the graph file must end in .svg, .png or .pdf",
    "plot.need_mpl": "PNG/PDF needs matplotlib: {pip}   (or use .svg)",
    "plot.freq": "Frequency",
    "plot.time": "Time",
    "plot.voltage": "Voltage (V)",
    "plot.current": "Current (A)",
    "plot.metavar": "FILE",

    # calc
    "calc.var_not_number": "variable '{name}' is not a number",

    # variables
    "vars.help": (
        "List saved variables.\n\n"
        "Variables are used as @name in any command:\n"
        "  elektro set vin 12\n"
        "  elektro ohm -v @vin -r 1k\n"
        "  elektro calc \"vin / 2\"\n\n"
        "--local stores them in ./.elektro.json (per project, found in parent folders too)."
    ),
    "vars.set.help": "Save a variable: elektro set NAME VALUE (use as @NAME).",
    "vars.unset.help": "Delete a variable.",
    "vars.arg.name": "Variable name (letters, digits, _)",
    "vars.arg.value": "Value, e.g. 12, 4k7, 100n",
    "vars.opt.local": "Save in ./.elektro.json for this project",
    "vars.bad_name": "invalid variable name '{name}'",
    "vars.unknown": "unknown variable @{name} (see: elektro vars)",
    "vars.removed": "removed",
    "vars.empty": "No variables yet. Example: elektro set vin 12",
    "vars.col.name": "Name",
    "vars.col.value": "Value",
    "vars.col.scope": "Scope",
    "vars.global": "global",
    "vars.local": "project",
    "vars.overridden": "overridden",

    # history
    "hist.help": (
        "Calculation history.\n\n"
        "Examples:\n"
        "  elektro history\n"
        "  elektro history -s filter\n"
        "  elektro history --run 12\n"
        "  elektro history --clear"
    ),
    "hist.opt.n": "How many entries to show",
    "hist.opt.search": "Only entries containing this text",
    "hist.opt.run": "Run the entry with this number again",
    "hist.opt.clear": "Delete the whole history",
    "hist.bad_id": "no entry with this number (1 … {max})",
    "hist.cleared": "History cleared.",
    "hist.empty": "The history is empty.",
    "hist.col.command": "Command",
    "hist.rerun": "Run again: elektro history --run NUMBER",

    # shell
    "shell.help": (
        "Interactive mode: type commands without 'elektro'.\n\n"
        "Tab completes commands, ↑/↓ browse previous lines.\n"
        "Built-ins: help, clear, exit"
    ),
    "shell.welcome": "interactive mode. Type 'help' for commands, 'exit' to leave.",
})
