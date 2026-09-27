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
