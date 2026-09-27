<div align="center">
  <h1>⚡ ELEKTRO</h1>
  <p><i>A terminal toolkit for electrical & electronics engineering</i></p>

  **English** · [Türkçe](https://github.com/0anes0/elektro/blob/main/README.tr.md)

  ![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
  ![License](https://img.shields.io/badge/license-GPLv3-green.svg)
  ![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey.svg)
  ![Languages](https://img.shields.io/badge/lang-EN%20%7C%20TR%20%7C%20DE%20%7C%20RU-orange.svg)
  [![test](https://github.com/0anes0/elektro/actions/workflows/test.yml/badge.svg)](https://github.com/0anes0/elektro/actions/workflows/test.yml)
</div>

---

**Elektro** handles everyday electronics calculations from the terminal — Ohm's law, resistor
color codes, filter design, RF link budgets, 555 timers and more — and downloads component
datasheets with a single command.

All values accept engineering notation: `4k7`, `100n`, `2.2u`, `10M`, `1meg`, `1R5`, `100nF`, `1kΩ`

The interface is available in **English, Turkish, German and Russian**.

## 🛠️ Installation

```bash
curl -fsSL https://raw.githubusercontent.com/0anes0/elektro/main/install.sh | bash
```

The script creates an isolated virtual environment in `~/.local/share/elektro` and links the
`elektro` command into `~/.local/bin`. It does not touch your system Python and does not need
pipx. If you installed an older version with pipx, it removes it for you.

Requirement: **Python 3.9+** (on Debian/Ubuntu also `python3-venv`).

<details>
<summary>Install from the repo, update, uninstall</summary>

```bash
git clone https://github.com/0anes0/elektro.git
cd elektro
./install.sh                 # install
elektro update               # update to the latest version on GitHub
./install.sh --uninstall     # uninstall
```

Shell completion (bash/zsh/fish): `elektro --install-completion`
</details>

## 🌍 Language

By default elektro follows your system language (`LANG`), falling back to English.

```bash
elektro language             # list languages
elektro language de          # save German as the default
elektro --lang ru ohm -v 5 -r 1k   # one-off
ELEKTRO_LANG=tr elektro      # via environment variable
```

Priority: `--lang` → `ELEKTRO_LANG` → saved setting (`~/.config/elektro/config.json`) → system language → English.

## 🚀 Usage

Run `elektro` for the command menu, `elektro COMMAND --help` for details,
`elektro helpall` or `man elektro` for the full manual.

Every command accepts `--json` for machine-readable output:
`elektro ohm -v 12 -r 1k --json`

### Interactive mode, variables, history

```bash
elektro shell                        # type commands without "elektro"; Tab completes, ↑ recalls
elektro set vin 12                   # save a value …
elektro ohm -v @vin -r 1k            # … and use it as @vin in any command
elektro set rload 4k7 --local        # per project (./.elektro.json)
elektro calc "vin / 2"               # variables also work by name in calc
elektro vars                         # list variables
elektro history                      # previous calculations
elektro history --run 3              # run one again
```

### Basics

```bash
elektro ohm -v 12 -r 1k              # any two of V, I, R, P
elektro ohm                          # interactive wizard

elektro resistor bn bk rd gd         # color code → 1 kΩ ±5%  (3-6 bands)
elektro resistor yellow violet black brown brown
elektro resistor encode 4k7          # value → color code
elektro resistor smd 01C             # SMD code (103, 4R7, 1002, EIA-96)
elektro resistor table               # color table

elektro 555 astable --r1 1k --r2 10k --c 10u
elektro 555 astable -f 1k -d 60 --c 10n      # design R1/R2 from frequency
elektro 555 mono --t 5 --c 100u

elektro logic convert 0xFF           # decimal/hex/binary/octal
elektro logic convert --bits 8 -- -5 # two's complement
elektro logic truth xor
elektro logic expr "A & B | ~C"      # truth table of a boolean expression
elektro logic simplify "A&B | A&~B"  # minimal SOP + Karnaugh map
elektro logic simplify -m 1,3,7,11,15 -d 0,2,5

elektro opamp noninv --gain 11       # standard Rf/Rg pairs
elektro opamp inv --rf 47k --rin 4k7 --vin 0.5 --gbw 1M
elektro opamp diff --gain 5

elektro switch bjt --ic 500m -v 3.3  # base resistor for an NPN switch
elektro switch mosfet -v 10 --qg 40n -f 100k   # gate drive and losses
elektro charge --r 10k --c 100u --v 5 --to 3.3 # RC charge time + curve
```

Resistor colors can be given as IEC codes (`bk bn rd og ye gn bu vt gy wh gd sr`) or as names in
any of the four languages (`brown`, `kahverengi`, `braun`, `коричневый`).

### Passive components

```bash
elektro series 1k 2k2 470
elektro parallel 10u 22u --cap
elektro divider --vin 12 --r1 10k --r2 4k7
elektro divider --vin 5 --vout 3.3           # best E24 R1/R2 pairs
elektro led --vs 12 --vf 3.1 -i 15m -n 3     # LED resistor + power rating
elektro eseries 4k8                          # nearest standard values (E3-E192)
elektro cap 104                              # capacitor code ↔ value
elektro coil --l 1u --d 10                   # air-core coil turns (Wheeler)
elektro crystal --cl 12p                     # crystal load capacitors
```

### Power & wiring

```bash
elektro regulator lm317 --vout 5             # R2 for an adjustable regulator
elektro regulator 7805 --vin 12 -i 500m      # dissipation of a linear regulator
elektro battery 2000 -i 15m                  # battery life
elektro battery 1200 --active 45m --active-time 2 --sleep 20u --sleep-time 58
elektro thermal -p 5 --rth-jc 3 --ta 50      # required heatsink
elektro wire --awg 22 -l 3 -i 2              # AWG ↔ mm², voltage drop
elektro trace -i 3                           # PCB trace width (IPC-2221)
elektro rectifier --vac 12 -i 1 --ripple 1   # bridge rectifier + reservoir capacitor
elektro acpower --v 400 --p 15k --pf 0.82 --phases 3 --target-pf 0.95
elektro stardelta delta 10 20 30             # Δ → Y conversion
```

### Filters

```bash
elektro filter rc --r 1k --c 100n            # fc + frequency response (gain/phase)
elektro filter rc --fc 1k --c 10n            # give two values, get the third
elektro filter rc --r 10k --fc 50 --high
elektro filter rl --r 1k --l 10m
elektro filter lc --f 433.92M --c 10p
elektro filter rlc --r 10 --l 1m --c 100n
elektro filter notch --r 1k --l 1.013 --c 10u  # 50 Hz
elektro filter rc --r 1k --c 100n --plot bode.svg   # save a Bode plot
elektro charge --r 10k --c 100u --v 5 --plot charge.svg
```

Graphs are written as SVG without any extra dependency. For `.png` / `.pdf` install matplotlib
into elektro's environment: `~/.local/share/elektro/venv/bin/pip install matplotlib`.

### RF

A plain number is **MHz** for frequency and **km** for distance (`2.4G` and `800m` also work).

```bash
elektro rf fspl -f 868 -d 5
elektro rf link -f 868 -d 10 --tx 14 --sens -137   # link margin and max. range
elektro rf wave -f 433.92                          # wavelength, antenna lengths
elektro rf convert 14 dbm w
elektro rf convert 1.5 vswr                        # |Γ|, return loss, mismatch loss
elektro rf lora --sf 9 -p 20                       # LoRa time on air, sensitivity
elektro rf fresnel -f 868 -d 10                    # Fresnel zone / antenna height
elektro rf microstrip --z0 50 --h 1.6 --er 4.4     # 50 Ω trace width
elektro rf coax lmr400 -f 2.4G -l 20m              # cable loss
```

### Embedded

```bash
elektro uart -c 16M -b 115200                # baud register and error (avr/stm32)
elektro pwm -c 72M -f 20k -m stm32 -d 25     # prescaler, ARR, compare value
elektro adc -b 12 --vref 3.3 --code 2048     # ADC code ↔ voltage
elektro i2c --cb 200p -s 400k                # I²C pull-up range
elektro crc "01 03 00 00 00 0A"              # CRC-8/16/32, Modbus, checksums
```

### Tools

```bash
elektro calc "12V / (4k7 + 1k)"              # calculator with engineering notation
elektro calc "par(1k, 2k2, 4k7)" -u Ω
elektro unit 25 c                            # °C/°F/K, mil/mm, dB, AWG …
```

### Datasheet downloader

```bash
elektro datasheet lm358
elektro datasheet ams1117 --open       # download and open
elektro datasheet esp32 --list         # show candidates without downloading
elektro datasheet 2n2222 -o transistor.pdf
elektro datasheet --history            # previously downloaded (cached) datasheets
```

It checks manufacturer sites (TI, Espressif, onsemi, Diodes, Nexperia), then the LCSC/JLCPCB
parts database, and finally DuckDuckGo. The download is verified to be a real PDF; if no source
works, links for a manual search are printed. Downloads are cached in `~/.cache/elektro/`, so the
same part is available instantly next time.

## 🧪 Development

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

Translations live in `elektro/i18n/` (`en.py` is the source). The tests check that every language
has every key with the same placeholders.

Releasing to PyPI (package name `elektro-cli`): add a *Trusted Publisher* for this repository on
PyPI (workflow `publish.yml`, environment `pypi`), then push a tag matching `__version__`:
`git tag v0.4.0 && git push origin v0.4.0`.

## 📄 License

[GPLv3](https://github.com/0anes0/elektro/blob/main/LICENSE) © Ahmet Enes KAYMAK
