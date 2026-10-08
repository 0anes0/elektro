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

# --- 0.6 ---------------------------------------------------------------------------------
MESSAGES.update({
    # report output
    "cli.opt.md": "Print the result as Markdown (tables for notes and reports)",
    "cli.opt.latex": "Print the result as LaTeX",
    "cli.opt.report": "Append the result to a report file (.md or .tex)",
    "cli.opt.copy": "Copy the output to the clipboard",
    "report.conflict": "--md, --latex/--report and --json cannot be combined",
    "report.quantity": "Quantity",
    "report.value": "Value",
    "report.appended": "Added to report: {path}",
    "report.copied": "Copied to the clipboard.",
    "report.no_clipboard": "no clipboard tool found (install wl-clipboard or xclip)",

    # calc: complex numbers
    "calc.opt.freq": "Frequency (Hz) — shows a complex impedance as R + L or R + C",
    "calc.need_real": "{name}() needs a real number",
    "calc.rect": "Rectangular",
    "calc.polar": "Polar",
    "calc.mag": "Magnitude",
    "calc.angle": "Angle",
    "calc.eq_r": "Series R @ {f}",
    "calc.eq_l": "Series L",
    "calc.eq_c": "Series C",

    "calc.help": (
        "Calculator that understands engineering notation, units and complex numbers.\n\n"
        "Operators: + − * / ^ ( )  ||  (parallel)   Functions: sqrt log ln exp sin cos tan db dbp par\n"
        "Complex: j, 3+j4, 10∠30 (degrees), polar(r, deg), re im abs arg conj\n"
        "Impedance: zl(L, f) = jωL, zc(C, f) = 1/(jωC).  Constants: pi e c\n\n"
        "Examples:\n"
        "  elektro calc \"12V / (4k7 + 1k)\"\n"
        "  elektro calc \"par(1k, 2k2, 4k7)\" -u Ω\n"
        "  elektro calc \"230∠0 / (10 + zl(100m, 50))\" -u A\n"
        "  elektro calc \"100 + zl(10m, 1k) || zc(1u, 1k)\" -u Ω -f 1k"
    ),

    # panels / menu
    "panel.install": "Installation & machines",
    "menu.cable": "Cable cross-section",
    "menu.breaker": "Circuit breaker / fuse",
    "menu.shortcircuit": "Short-circuit current",
    "menu.transformer": "Transformer",
    "menu.motor": "Induction motor",
    "menu.wave": "RMS, average, crest factor",
    "menu.fft": "Spectrum of a CSV (THD)",
    "menu.pinout": "IC / transistor pinout",
    "menu.report": "Markdown / LaTeX report",

    # cable
    "cable.help": (
        "Select a low-voltage cable cross-section by current capacity and voltage drop (IEC 60364-5-52).\n\n"
        "Installation methods: A1 (in conduit in an insulated wall), B1 (in conduit on/in a wall),\n"
        "C (clipped direct), D (in the ground).\n\n"
        "Examples:\n"
        "  elektro cable -i 16 -l 25\n"
        "  elektro cable -p 9k --phases 3 --pf 0.85 -l 40 --method C\n"
        "  elektro cable -i 120 --phases 3 -l 80 --material al --insulation xlpe --group 3\n"
        "  elektro cable -i 20 -l 30 --mm2 2.5          (check a given section)"
    ),
    "cable.opt.current": "Load current Ib (A)",
    "cable.opt.power": "Load power (W) — computes the current",
    "cable.opt.v": "Voltage (V); default 230 (1-phase) / 400 (3-phase)",
    "cable.opt.length": "Cable length one way, e.g. 25 (m), 120m",
    "cable.opt.drop": "Allowed voltage drop (%)",
    "cable.opt.method": "Installation method: A1, B1, C, D",
    "cable.opt.material": "Conductor: cu or al",
    "cable.opt.insulation": "Insulation: pvc (70 °C) or xlpe (90 °C)",
    "cable.opt.ta": "Ambient temperature (°C); default 30 in air, 20 in the ground",
    "cable.opt.group": "Number of circuits run together (grouping factor)",
    "cable.opt.mm2": "Check this cross-section (mm²) instead of selecting one",
    "cable.bad_choice": "invalid value '{value}' (options: {options})",
    "cable.too_hot": "the ambient temperature must be below {tmax} °C",
    "cable.need": "give the current (-i) or the power (-p)",
    "cable.bad_section": "not a standard cross-section (options: {options})",
    "cable.none": "even 300 mm² is not enough; use parallel cables or a higher voltage",
    "cable.title": "Cable Selection",
    "cable.system": "System",
    "cable.ib": "Load current Ib",
    "cable.section": "Cross-section",
    "cable.iz": "Current capacity Iz",
    "cable.drop": "Voltage drop",
    "cable.loss": "Cable loss",
    "cable.temp": "Conductor temperature",
    "cable.by_ampacity": "By capacity alone",
    "cable.mcb": "Suitable MCB (Ib ≤ In ≤ Iz)",
    "cable.no_mcb": "none — choose a larger cable",
    "cable.not_ok": "this cross-section does not meet the requirements",
    "cable.note1": "Capacities: IEC 60364-5-52 (copper/PVC); XLPE and aluminium use approximate factors.",
    "cable.note2": "Typical limits: 3% lighting, 5% other loads (TR regulation: 1.5% lighting, 3% power).",

    # breaker
    "brk.help": (
        "Select a circuit breaker (MCB) or gG fuse and check the cable protection.\n\n"
        "Conditions: Ib ≤ In ≤ Iz and I2 ≤ 1.45·Iz.  Fault disconnection: Zs ≤ U0 / Ia.\n\n"
        "Examples:\n"
        "  elektro breaker -i 14 --iz 21\n"
        "  elektro breaker -i 14 --iz 21 --curve B --mm2 2.5 -l 30\n"
        "  elektro breaker -i 40 --iz 50 --type fuse"
    ),
    "brk.opt.current": "Load current Ib (A)",
    "brk.opt.iz": "Current capacity of the cable Iz (A) — see: elektro cable",
    "brk.opt.type": "Device: mcb or fuse (gG)",
    "brk.opt.curve": "MCB curve: B, C or D",
    "brk.opt.zs": "Measured earth fault loop impedance Zs (Ω)",
    "brk.opt.mm2": "Cable cross-section (mm²) — computes Zs and the maximum length",
    "brk.opt.length": "Cable length (m) — computes Zs",
    "brk.opt.ze": "External loop impedance Ze (Ω) for the Zs calculation",
    "brk.opt.u0": "Phase-to-earth voltage U0 (V)",
    "brk.too_big": "the current is above the largest standard rating",
    "brk.title": "Protection Device",
    "brk.device": "Device",
    "brk.magnetic": "Instantaneous trip",
    "brk.zs_max": "Max. loop impedance Zs",
    "brk.zs_calc": "Loop impedance Zs (calc.)",
    "brk.ik_min": "Earth fault current",
    "brk.lmax": "Max. length ({mm2} mm²)",
    "brk.not_ok": "the cable is not protected; use at most {max} A or a larger cable",
    "brk.no_device": "no standard device protects this cable at this load current",
    "brk.note.curve": "B: resistive loads, lighting · C: general, motors · D: transformers, high inrush.",
    "brk.note.zs": "Zs from the cable uses Ze = {ze} Ω and a PE conductor equal to the phase conductor.",
    "brk.note.fuse": "gG fuse: I2 = 1.6·In (In ≥ 16 A); check the disconnection time on the fuse curve.",

    # short circuit
    "sc.help": (
        "Short-circuit current of a low-voltage network fed by a transformer (IEC 60909, simplified).\n\n"
        "Examples:\n"
        "  elektro shortcircuit --kva 630\n"
        "  elektro shortcircuit --kva 1000 --uk 6 --pk 10.5k --mm2 240 -l 60 --parallel 2\n"
        "  elektro shortcircuit --kva 400 --mm2 16 -l 80 --time 0.4"
    ),
    "sc.opt.kva": "Transformer rating (kVA)",
    "sc.opt.uk": "Short-circuit voltage uk (%); default 4 (≤ 630 kVA) or 6",
    "sc.opt.v": "Secondary line voltage (V)",
    "sc.opt.pk": "Copper (load) losses Pk (W); default ur = 1%",
    "sc.opt.sk": "Upstream fault level Sk'' (MVA); 0 = infinite",
    "sc.opt.mm2": "Cable cross-section to the fault point (mm²)",
    "sc.opt.length": "Cable length to the fault point (m)",
    "sc.opt.parallel": "Number of parallel cables",
    "sc.opt.time": "Disconnection time (s) — checks the cable's thermal withstand",
    "sc.need_cable": "give both --mm2 and --length",
    "sc.bad_pk": "the copper losses are too high for this uk",
    "sc.title": "Short-circuit Current",
    "sc.trafo": "Transformer",
    "sc.in": "Rated current",
    "sc.zq": "Network Zq ({sk} MVA)",
    "sc.zc": "Cable Zc ({cable})",
    "sc.icu": "Breaking capacity",
    "sc.smin": "Min. section ({t}, k = {k})",
    "sc.note1": "Ik3 max with c = 1.05 and conductors at 20 °C; Ik1 min (phase–neutral) with c = 0.95.",
    "sc.note2": "Use Ik3 for the breaking capacity and Ik1 to check that the protection trips.",

    # transformer
    "tr.help": (
        "Transformer: turns ratio, currents and winding data of a small mains transformer.\n\n"
        "Examples:\n"
        "  elektro transformer --v1 230 --v2 12\n"
        "  elektro transformer --v1 230 --v2 24 --va 100\n"
        "  elektro transformer --v1 34.5k --v2 400 --va 630k --phases 3"
    ),
    "tr.opt.v1": "Primary voltage (V)",
    "tr.opt.v2": "Secondary voltage (V, at load)",
    "tr.opt.va": "Rated power (VA), e.g. 50, 1k, 630k",
    "tr.opt.b": "Peak flux density (T): 1.0–1.4 for silicon steel",
    "tr.opt.j": "Current density (A/mm²): 2–3.5",
    "tr.opt.eff": "Efficiency",
    "tr.opt.area": "Core cross-section (cm²); default ≈ √P",
    "tr.opt.reg": "Extra secondary turns for the load voltage drop (%)",
    "tr.title": "Transformer",
    "tr.ratio": "Turns ratio",
    "tr.kind": "Type",
    "tr.step_down": "step-down",
    "tr.step_up": "step-up",
    "tr.hint": "Add --va for the currents and winding data.",
    "tr.power": "Power",
    "tr.three_note": "Currents are line currents. Winding design is only computed for single-phase transformers.",
    "tr.area": "Core cross-section",
    "tr.tpv": "Turns per volt",
    "tr.wire1": "Primary wire",
    "tr.wire2": "Secondary wire",
    "tr.big": "Rules of thumb are meant for small transformers (up to a few hundred VA).",
    "tr.note1": "Computed with B = {b} T and J = {j} A/mm²; the window must hold both windings.",
    "tr.note2": "N/V = 1 / (4.44 · f · B · A).  Too high B overheats the core and draws a large no-load current.",

    # motor
    "mot.help": (
        "Induction motor: current, torque, slip, losses and starting current.\n\n"
        "Examples:\n"
        "  elektro motor -p 7.5k --rpm 1450\n"
        "  elektro motor -p 15k --pf 0.86 --eff 0.92 --poles 2 --rpm 2940\n"
        "  elektro motor -p 750 --v 230 --phases 1 --pf 0.75 --eff 0.7"
    ),
    "mot.opt.power": "Rated output (shaft) power (W), e.g. 7.5k",
    "mot.opt.v": "Voltage (V; line-to-line for 3-phase)",
    "mot.opt.eff": "Efficiency",
    "mot.opt.poles": "Number of poles (2, 4, 6 …)",
    "mot.opt.rpm": "Rated speed from the nameplate (rpm)",
    "mot.opt.start": "Starting current / rated current (direct-on-line)",
    "mot.bad_poles": "the number of poles must be even and at least 2",
    "mot.bad_rpm": "the speed must be between 0 and the synchronous speed ({ns} rpm)",
    "mot.title": "Induction Motor",
    "mot.power": "Output power",
    "mot.ns": "Synchronous speed",
    "mot.poles": "poles",
    "mot.speed": "Rated speed",
    "mot.assumed": "assumed 4% slip",
    "mot.slip": "Slip",
    "mot.torque": "Rated torque",
    "mot.pin": "Input power",
    "mot.losses": "Losses",
    "mot.current": "Rated current",
    "mot.start_dol": "Starting current (DOL)",
    "mot.start_yd": "Starting current (Y-Δ)",
    "mot.note1": "Size the cable for the rated current and the protection for the starting current (curve C/D).",
    "mot.note2": "Star-delta starting reduces the starting current and torque to 1/3.",
    "mot.note_single": "Single-phase motors need a run (and often a start) capacitor.",

    # wave
    "wave.help": (
        "RMS, average, rectified average, crest and form factor of a waveform.\n\n"
        "Shapes: sine, square, triangle, sawtooth, pwm (0…Vp), halfwave, fullwave (rectified sine)\n\n"
        "Examples:\n"
        "  elektro wave sine --vp 325\n"
        "  elektro wave sine --rms 230\n"
        "  elektro wave pwm --vp 12 -d 25 -r 10\n"
        "  elektro wave square --vpp 5 --offset 2.5 -f 1k --plot square.svg"
    ),
    "wave.arg": "Waveform",
    "wave.opt.vp": "Peak amplitude",
    "wave.opt.vpp": "Peak-to-peak value",
    "wave.opt.rms": "RMS value (without offset) — computes the amplitude",
    "wave.opt.offset": "DC offset",
    "wave.opt.duty": "Duty cycle (%) for pwm and square",
    "wave.opt.freq": "Frequency (Hz) — shows the period",
    "wave.opt.load": "Load resistance (Ω) — computes the power",
    "wave.opt.unit": "Unit of the values (V, A …)",
    "wave.bad_shape": "unknown waveform (options: {options})",
    "wave.need": "give exactly one of --vp, --vpp or --rms",
    "wave.bad": "the duty cycle must be between 0 and 100 %, frequency and load positive",
    "wave.title": "Waveform",
    "wave.shape": "Shape",
    "wave.kind.sine": "sine",
    "wave.kind.square": "square",
    "wave.kind.triangle": "triangle",
    "wave.kind.sawtooth": "sawtooth",
    "wave.kind.pwm": "PWM",
    "wave.kind.halfwave": "half-wave rectified sine",
    "wave.kind.fullwave": "full-wave rectified sine",
    "wave.peak": "Max / min",
    "wave.vpp": "Peak-to-peak",
    "wave.dc": "Average (DC)",
    "wave.rms": "RMS (true)",
    "wave.ac_rms": "RMS (AC only)",
    "wave.rect": "Rectified average",
    "wave.crest": "Crest factor",
    "wave.form": "Form factor",
    "wave.period": "Period",
    "wave.t_high": "High time",
    "wave.power": "Power in {r}",
    "wave.note1": "RMS = √(DC² + AC_rms²).  Average-responding meters show 1.111 × rectified average.",
    "wave.note2": "Such meters are only correct for sine waves; use a true-RMS meter for other shapes.",

    # fft
    "fft.help": (
        "Spectrum of a sampled signal from a CSV file (oscilloscope or logger export).\n\n"
        "Finds the fundamental, the largest peaks, THD and THD+N. The sample rate is taken from the\n"
        "time column, an 'Increment' header (Rigol) or --rate.\n\n"
        "Examples:\n"
        "  elektro fft scope.csv\n"
        "  elektro fft data.csv --column 3 --window flattop\n"
        "  elektro fft adc.txt --rate 48k --plot spectrum.svg"
    ),
    "fft.arg": "CSV / text file with numeric columns",
    "fft.opt.column": "Column of the signal (1 = first); default 2 if there is a time column",
    "fft.opt.rate": "Sample rate (Hz) if there is no time column",
    "fft.opt.window": "Window: {options}",
    "fft.opt.peaks": "Number of peaks to list",
    "fft.no_data": "no numeric data found in the file",
    "fft.too_short": "at least 16 samples are needed",
    "fft.bad_window": "unknown window (options: {options})",
    "fft.bad_column": "the column must be between 1 and {n}",
    "fft.src.rate": "--rate",
    "fft.src.header": "file header",
    "fft.src.time": "time column",
    "fft.need_rate": "the sample rate is unknown; give --rate",
    "fft.index_col": "the first column looks like a sample index (step 1); give --rate if it is not time",
    "fft.title": "Spectrum (FFT)",
    "fft.file": "File",
    "fft.fs": "Sample rate",
    "fft.samples": "Samples",
    "fft.resolution": "Resolution",
    "fft.fundamental": "Fundamental",
    "fft.peaks": "Largest peaks",
    "fft.amp": "Amplitude",
    "fft.note": "Window: {window}. Amplitudes are peak values; dBc is relative to the fundamental.",

    # pinout
    "pin.help": (
        "Pinout of common ICs and transistors (offline).\n\n"
        "Examples:\n"
        "  elektro pinout              (list of parts)\n"
        "  elektro pinout ne555\n"
        "  elektro pinout 74hc595\n"
        "  elektro pinout bc547"
    ),
    "pin.arg": "Part name, e.g. ne555, lm358, 7805",
    "pin.tab": "tab",
    "pin.col.part": "Part",
    "pin.col.package": "Package",
    "pin.col.desc": "Description",
    "pin.col.aliases": "Same pinout",
    "pin.usage": "Show one: elektro pinout NAME",
    "pin.unknown": "'{name}' is not in the list (see: elektro pinout). Try: elektro datasheet {name}",
    "pin.note.dip": "Top view; pin 1 is next to the notch / dot, numbering runs counter-clockwise.",
    "pin.note.front": "Front view (printed side towards you, legs down). Manufacturers differ — check the datasheet.",
    "pin.same": "Same pinout: {parts}",
    "pin.desc.ne555": "Timer",
    "pin.desc.lm358": "Dual op-amp",
    "pin.desc.ua741": "Single op-amp",
    "pin.desc.lm386": "Audio power amplifier",
    "pin.desc.attiny85": "8-bit AVR microcontroller",
    "pin.desc.pc817": "Optocoupler",
    "pin.desc.74hc00": "Quad 2-input NAND gate",
    "pin.desc.74hc04": "Hex inverter",
    "pin.desc.74hc595": "8-bit shift register with output latch",
    "pin.desc.cd4017": "Decade counter / divider",
    "pin.desc.l293d": "Dual H-bridge motor driver",
    "pin.desc.atmega328p": "8-bit AVR microcontroller (Arduino Uno)",
    "pin.desc.78xx": "Positive fixed regulator",
    "pin.desc.79xx": "Negative fixed regulator",
    "pin.desc.lm317": "Adjustable positive regulator",
    "pin.desc.ams1117": "LDO regulator",
    "pin.desc.irfz44n": "N-channel power MOSFET",
    "pin.desc.bc547": "NPN transistor",
    "pin.desc.2n2222": "NPN transistor",
    "pin.desc.lm35": "Temperature sensor (10 mV/°C)",
    "pin.desc.ds18b20": "1-Wire digital temperature sensor",
    "pin.desc.tl431": "Adjustable shunt reference",
})

# --- 0.7: terminal arayüzü ---------------------------------------------------------------
MESSAGES.update({
    "tui.help": "Terminal user interface: pick a command, fill in the form, see the result.\n\nKeys: Ctrl+R run · Ctrl+F search · F2/F3/F4 tabs · Ctrl+L clear · Ctrl+Q quit",
    "tui.need_textual": "the terminal interface needs Textual: {pip}",
    "menu.tui": "Terminal interface",
    "tui.key.run": "Run",
    "tui.key.clear": "Clear",
    "tui.key.search": "Search",
    "tui.key.quit": "Quit",
    "tui.tab.calc": "Calculations",
    "tui.tab.circuit": "Circuit",
    "tui.tab.history": "History",
    "tui.search": "Search commands…",
    "tui.commands": "Commands",
    "tui.pick": "Pick a command on the left",
    "tui.cmdline": "Command line — edit or type a command and press Enter",
    "tui.run": "▶ Run",
    "tui.welcome": "Pick a command, fill in the fields and press Enter or Ctrl+R. You can also type any elektro command in the command line.",
    "tui.blocked": "'{cmd}' cannot be run inside the interface",
    "tui.hist.hint": "Enter: load the command into the Calculations tab",
    "tui.col.time": "Time",
    "tui.col.command": "Command",
    "tui.help_examples": "Help and examples",
})

# --- 0.7: devre editörü ve simülatör ------------------------------------------------------
MESSAGES.update({
    "ckt.bad_file": "not a valid elektro circuit file",
    "ckt.singular": "the circuit cannot be solved: a floating part, a loop of voltage sources/inductors or a current source in series with a capacitor",
    "ckt.empty": "the circuit is empty",
    "ckt.no_ground": "the circuit has no ground (GND)",
    "ckt.shorted": "{ref} is shorted (both pins on the same node)",
    "ckt.open_pin": "{ref} has an unconnected pin",
    "ckt.bad_value": "invalid value for {ref}",
    "ckt.key.wire": "Wire",
    "ckt.key.rotate": "Rotate",
    "ckt.key.undo": "Undo",
    "ckt.key.simulate": "Solve",
    "ckt.key.save": "Save",
    "ckt.key.open": "Open",
    "ckt.msg.placed": "{ref} placed — e: value, Ctrl+R: rotate, m: move",
    "ckt.msg.wire": "Wire: move the cursor, Enter/w sets a corner, Esc ends",
    "ckt.msg.move": "Moving {ref}: arrows move, Enter/m drops, Esc cancels",
    "ckt.msg.undone": "Undone.",
    "ckt.msg.solved": "DC operating point solved. The result updates as you edit.",
    "ckt.msg.saved": "Saved: {path}",
    "ckt.msg.opened": "Opened: {path}",
    "ckt.msg.new": "New circuit (Ctrl+Z brings the old one back).",
    "ckt.prompt.value": "Value of {ref} ({unit}) — e.g. 4k7, 100n, 12",
    "ckt.prompt.save": "Save as (JSON file)",
    "ckt.prompt.open": "Open circuit file",
    "ckt.untitled": "untitled",
    "ckt.mode.normal": "edit",
    "ckt.mode.wire": "WIRE",
    "ckt.mode.move": "MOVE",
    "ckt.kind.R": "resistor",
    "ckt.kind.C": "capacitor",
    "ckt.kind.L": "inductor",
    "ckt.kind.V": "voltage source",
    "ckt.kind.I": "current source",
    "ckt.kind.GND": "ground",
    "ckt.nodes": "Nodes",
    "ckt.node": "Node",
    "ckt.op_title": "DC operating point",
    "tui.arg": "Circuit file to open in the Circuit tab",
    "menu.sim": "Solve a circuit file",
    "sim.arg": "Circuit file (.json, saved from elektro tui)",
    "sim.opt.spice": "Print the SPICE netlist instead of solving",
    "sim.nodes": "Node voltages",
    "sim.elements": "Components",
    "sim.note": "DC: capacitors are open, inductors are shorts. P > 0 consumes, P < 0 delivers power.",
    "ckt.key.probe": "Probe",
    "ckt.msg.probe_added": "Probe added: {expr}",
    "ckt.msg.probe_removed": "Probe removed: {expr}",
    "ckt.msg.nothing": "Nothing to measure here: move onto a node, a wire or a component.",
    "ckt.msg.probe_from": "Current probe from {a}: move to the other node, press a/Enter (Esc cancels)",
    "ckt.probes": "Probes",
    "ckt.probe.no_net": "{addr} is not on a node",
    "ckt.probe.no_part": "no component named {ref}",
    "ckt.probe.same": "{a} and {b} are on the same node",
    "ckt.probe.no_path": "no component connects {a} and {b} directly",
    "sim.opt.probe": "Extra probe, e.g. -p \"V(C3)\" -p \"I(C1,C10)\" (can be repeated)",
    "ckt.mode.probe": "CURRENT PROBE",
    "ckt.msg.req_from": "Equivalent resistance from {a}: move to the other point, press o/Enter (Esc cancels)",
    "ckt.msg.no_source": "No source in the circuit: nothing to solve for DC, resistance probes R(A,B) still work (o).",
    "sim.need_req": "the circuit has no source; add a probe like -p \"R(A1,D1)\" for the equivalent resistance",
    "src.bad": "invalid source value '{text}' (examples: 5, DC 5 AC 1, SINE(0 1 1k), PULSE(0 5 0 1u 1u 0.5m 1m))",
    "src.bad_number": "not a number: '{text}'",
    "src.bad_wave": "wrong number of {name} parameters",
    "an.bad": "invalid analysis '{text}' (examples: .op, .tran 10m, .ac dec 100 10 100k, .dc V1 0 5 0.1)",
    "an.bad_tran": ".tran needs a positive stop time (and a step not larger than it)",
    "an.bad_ac": ".ac needs points ≥ 1 and 0 < start < stop frequency",
    "an.bad_dc": ".dc: the step must lead from start to stop",
    "an.no_ac_source": "no AC source: give a source an AC value, e.g. 'AC 1' or 'DC 0 AC 1'",
    "an.no_source": "no voltage/current source named {ref}",
    "an.title": "Analysis — type an LTspice command or fill in the form",
    "an.kind": "Analysis",
    "an.kind.op": "DC operating point (.op)",
    "an.kind.tran": "Transient (.tran)",
    "an.kind.ac": "AC sweep (.ac)",
    "an.kind.dc": "DC sweep (.dc)",
    "an.tstop": "Stop time",
    "an.tstep": "Time step",
    "an.auto": "automatic",
    "an.sweep": "Sweep",
    "an.points": "Points (per dec/oct)",
    "an.fstart": "Start frequency",
    "an.fstop": "Stop frequency",
    "an.source": "Source",
    "an.start": "Start",
    "an.stop": "Stop",
    "an.step": "Step",
    "an.ok": "OK",
    "an.cancel": "Cancel",
    "plot.key.mode": "Mag/phase",
    "plot.key.size": "Plot size",
    "plot.hint": "No analysis yet: press s in the editor (.tran/.ac/.dc), then F5. Probes (p) become curves.",
    "ckt.key.analysis": "Analysis",
    "ckt.msg.analysis": "Analysis: {directive}",
    "ckt.prompt.source": "Value of {ref} ({unit}) — e.g. 5 · AC 1 · SINE(0 1 1k) · PULSE(0 5 0 1u 1u 0.5m 1m)",
    "ckt.analysis": "Analysis",
    "ckt.running": "running…",
    "sim.opt.analysis": "Run this analysis instead of the one in the file, e.g. \".tran 5m\" (\".op\": DC only)",
    "sim.opt.csv": "Save the curves as CSV",
    "sim.points": "points",
    "sim.max_db": "max",
    "sim.at": "at",
    "sim.last": "last",
    "sim.sweep_x": "Sweep",
    "sim.csv_saved": "CSV saved: {path}",
    "sim.help": "Solve a circuit file drawn in the TUI: DC operating point and the analysis saved in the file (.tran, .ac, .dc).\n\nNodes are named like spreadsheet cells (B2, E7). Probes: V(C3), V(C3,E7), I(C1,C10), I(R1), P(R1), R(A1,D1). Sources: 5, AC 1, SINE(0 1 1k), PULSE(0 5 0 1u 1u 0.5m 1m).\n\nExamples:\n  elektro sim divider.json -p \"V(E2)\"\n  elektro sim rc.json -a \".tran 5m\" --plot rc.svg\n  elektro sim filter.json -a \".ac dec 50 10 1meg\" --csv bode.csv\n  elektro sim divider.json --spice > divider.cir",
    "dev.unknown": "unknown model '{name}' (models: {options}; or parameters like IS=1e-14)",
    "dev.bad_rail": "invalid output limit '{text}' (examples: ±15, 0..5)",
    "dev.bad_param": "invalid parameter '{text}'",
    "ckt.no_converge": "the solution did not converge (check the circuit: a source driving a diode/transistor directly, a missing resistor, …)",
    "ckt.probe.no_pin": "{ref} has no pin '{pin}' (pins: {pins})",
    "ckt.probe.no_ac_power": "power is not shown in AC analysis",
    "ckt.prompt.model.D": "Diode {ref}: {models} — or IS=… N=… RS=… BV=…",
    "ckt.prompt.model.Q": "Transistor {ref}: {models} — or NPN/PNP BF=… IS=… VAF=…",
    "ckt.prompt.model.M": "MOSFET {ref}: {models} — or NMOS/PMOS VTO=… KP=… LAMBDA=…",
    "ckt.prompt.model.U": "Op-amp {ref}: {models} — output limit e.g. 'TL072 ±15', 'LM358 0..5'",
    "ckt.kind.D": "diode",
    "ckt.kind.Q": "bipolar transistor",
    "ckt.kind.M": "MOSFET",
    "ckt.kind.U": "op-amp",
    "ckt.prompt.probe": "Probe: V(C3) · V(C3,E7) · I(C1,C10) · I(R1) · I(Q1.B) · P(R1) · R(A1,D1)   (-2 deletes #2, - deletes all)",
    "ckt.probe.bad": "invalid probe '{expr}' (examples: V(C3), V(C3,E7), I(C1,C10), I(R1), I(Q1.B), P(R1), R(A1,D1))",
    "tui.circuit.keys": "r R · c C · l L · v V · i I · d diode · q BJT · f MOSFET · u op-amp · n label · g GND · w wire · e/Enter value · Ctrl+R rotate · m move · x delete · p probe · a current between 2 nodes · o resistance · P type a probe · s analysis · F5 solve · F6 plot size · Tab plot (←/→ cursor, m mag/phase) · Ctrl+Z undo · Ctrl+S save · Ctrl+O open · Ctrl+N new · Ctrl+E examples",
    "ckt.probes_at": "Probes at {x}",
    "ckt.col.peak": "peak",
    "ckt.kind.N": "net label",
    "ckt.prompt.label": "Net label name (e.g. VCC, OUT, IN); points with the same name are connected",
    "ckt.bad_label": "invalid name '{name}' (letters, digits, _; must start with a letter)",
    "ckt.msg.label": "Label {name} placed",
    "spice.dropped": "{model}: parameters not modelled were ignored: {params}",
    "spice.unknown_model": "model '{model}' not found; a generic model is used",
    "spice.skipped": "line skipped: {line}",
    "spice.empty": "no supported elements in the netlist",
    "ckt.msg.imported": "Imported from {path} (parts placed automatically, connected by labels)",
    "ex.divider": "Voltage divider (12 V → 3.84 V)",
    "ex.bridge": "Wheatstone bridge, equivalent resistance",
    "ex.rc_charge": "RC charging curve",
    "ex.rc_lowpass": "RC low-pass filter (Bode)",
    "ex.rlc_bandpass": "Series RLC band-pass (1.6 kHz)",
    "ex.half_wave": "Half-wave rectifier + filter",
    "ex.bridge_rectifier": "Bridge rectifier",
    "ex.zener": "Zener regulator (input sweep)",
    "ex.led_driver": "Transistor LED driver",
    "ex.common_emitter": "Common-emitter amplifier",
    "ex.mosfet_switch": "MOSFET PWM switch",
    "ex.non_inverting": "Non-inverting amplifier (×11)",
    "ex.inverting": "Inverting amplifier (×−10)",
    "ex.integrator": "Integrator (square → triangle)",
    "ex.comparator": "Comparator (sine → square)",
    "ex.cat.basic": "Basics",
    "ex.cat.filters": "Filters",
    "ex.cat.power": "Power",
    "ex.cat.transistor": "Transistors",
    "ex.cat.opamp": "Op-amps",
    "ex.help": "Ready-made example circuits.\n\nExamples:\n  elektro examples                 (list)\n  elektro examples rc_lowpass      (save rc_lowpass.json)\n  elektro examples zener -o z.json\n\nIn the Circuit tab of `elektro tui`: Ctrl+E.",
    "ex.arg": "Example name (leave empty for the list)",
    "ex.opt.output": "File to write (default: NAME.json)",
    "ex.saved": "Example saved: {path}",
    "ex.unknown": "unknown example '{name}' (examples: {options})",
    "ex.usage": "Save one: elektro examples NAME   ·   in the editor: Ctrl+E",
    "ex.title": "Example circuits — Enter opens, Esc cancels",
    "ckt.key.examples": "Examples",
    "ckt.msg.example": "Example: {title} (Ctrl+S saves it)",
    "menu.examples": "Example circuits",
})
