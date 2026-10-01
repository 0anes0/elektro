"""0.6: karmaşık sayılar, tesisat, makineler, sinyal (wave/fft), pinout, rapor çıktısı."""

import cmath
import json
import math

import pytest
from typer.testing import CliRunner

from elektro import cli, ui
from elektro.modules import installation, machines, pinout, signal, tools

runner = CliRunner()


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "cfg"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.chdir(tmp_path)
    yield
    ui.set_json(False)
    ui.set_report(None)


def invoke(args):
    r = runner.invoke(cli.app, args, env={"COLUMNS": "140"})
    assert r.exit_code == 0, r.output
    return r.output


# --- calc: karmaşık sayılar --------------------------------------------------------------

@pytest.mark.parametrize("expr,expected", [
    ("3+4j", 3 + 4j),
    ("3+j4", 3 + 4j),
    ("10∠90", 10j),
    ("10∠30°", cmath.rect(10, math.radians(30))),
    ("sqrt(-4)", 2j),
    ("abs(3+j4)", 5),
    ("arg(1+j)", 45),
    ("zl(10m, 50)", 1j * 2 * math.pi * 50 * 10e-3),
    ("zc(1u, 1k)", 1 / (1j * 2 * math.pi * 1e3 * 1e-6)),
    ("1k || 1k", 500),
    ("100 + 1k || 1k", 600),
    ("4k7j", 4700j),
    ("(1+2j)*(1-2j)", 5),
    ("e^(j*pi)", -1),
    ("conj(polar(2, 30))", cmath.rect(2, math.radians(-30))),
    ("12V / (4k7 + 1k)", 12 / 5700),
])
def test_complex_evaluate(expr, expected):
    assert tools.evaluate(expr) == pytest.approx(expected)


def test_complex_results_are_tidy():
    assert isinstance(tools.evaluate("(1+2j)*(1-2j)"), float)
    assert tools.evaluate("10∠90").real == 0


def test_complex_cli_and_equivalent():
    out = invoke(["calc", "100 + zl(10m, 1k)", "-u", "Ω", "-f", "1k"])
    assert "100 + j62.832 Ω" in out and "10 mH" in out
    data = json.loads(invoke(["--json", "calc", "3+j4"]))
    assert data["result"]["mag"] == pytest.approx(5)
    assert data["result"]["deg"] == pytest.approx(53.130102)
    eq = tools.equivalent(complex(0, -159.15494), 1e3)
    assert eq["c"] == pytest.approx(1e-6, rel=1e-6)


# --- kablo / koruma / kısa devre -------------------------------------------------------------

def test_ampacity_and_factors():
    assert installation.ampacity(2.5, "B1", 1) == 24
    assert installation.ampacity(2.5, "B1", 3) == 21
    assert installation.ampacity(2.5, "B1", 1, ta=40) == pytest.approx(24 * math.sqrt(30 / 40))
    assert installation.grouping_factor(3) == 0.70
    assert installation.grouping_factor(10) == 0.45      # bir üst tablo değeri (güvenli taraf)
    assert installation.grouping_factor(50) == 0.38


def test_voltage_drop():
    # 16 A, 25 m, 2.5 mm² Cu, cosφ = 1, 20 °C: 2·25·16·0.017241/2.5
    du = installation.voltage_drop(2.5, 16, 25, 1, 1.0, "cu", 20)
    assert du == pytest.approx(2 * 25 * 16 * 0.017241 / 2.5)
    du3 = installation.voltage_drop(2.5, 16, 25, 3, 1.0, "cu", 20)
    assert du3 == pytest.approx(du * math.sqrt(3) / 2)


def test_cable_selection():
    rows = installation.select_cable(16, 25, 230, 1, 1.0, 3, "B1", "cu", "pvc", None, 1)
    chosen = next(r for r in rows if r["ok"])
    assert chosen["mm2"] == 2.5
    rows = installation.select_cable(16, None, 230, 1, 1.0, 3, "B1", "cu", "pvc", None, 1)
    assert next(r for r in rows if r["ok"])["mm2"] == 1.5
    rows = installation.select_cable(100, None, 400, 3, 1.0, 3, "B1", "al", "pvc", None, 1)
    assert min(r["mm2"] for r in rows) == 16              # alüminyum en az 16 mm²


@pytest.mark.parametrize("args,expect", [
    (["cable", "-i", "16", "-l", "25"], "2.5 mm²"),
    (["cable", "-p", "9k", "--phases", "3", "--pf", "0.85", "-l", "40"], "15.28 A"),
    (["cable", "-i", "20", "-l", "30", "--mm2", "2.5"], "4.13%"),
    (["breaker", "-i", "14", "--iz", "21", "--curve", "B", "--mm2", "2.5", "-l", "30"], "MCB B16"),
    (["breaker", "-i", "40", "--iz", "50", "--type", "fuse"], "gG 40 A"),
    (["shortcircuit", "--kva", "630"], "23.08 kA"),
    (["shortcircuit", "--kva", "400", "--mm2", "16", "-l", "80", "--time", "0.4"], "14.3 mm²"),
])
def test_installation_cli(args, expect):
    assert expect in invoke(args)


def test_breaker_rules():
    r = installation.breaker_calc(14, 21, "mcb", "C")
    assert r["in_a"] == 16 and r["in_ok"] and r["i2_ok"]
    assert r["trip_min_a"] == 80 and r["trip_max_a"] == 160
    r = installation.breaker_calc(20, 18, "mcb", "C")
    assert not r["in_ok"] and r["max_in_a"] == 16
    r = installation.breaker_calc(30, 32, "fuse", "C")
    assert r["in_a"] == 32 and not r["i2_ok"]           # 1.6·32 > 1.45·32


def test_short_circuit_at_terminals():
    r = installation.short_circuit(630, 4, 400, 1, None, None, None, "cu", 1)
    # Ik ≈ c · In / uk
    assert r["ik3_a"] == pytest.approx(1.05 * r["in_a"] / 0.04, rel=1e-6)
    assert 1.02 <= r["kappa"] <= 2


def test_cable_errors():
    r = runner.invoke(cli.app, ["cable", "-l", "10"])
    assert r.exit_code != 0
    r = runner.invoke(cli.app, ["cable", "-i", "10", "--method", "Z"])
    assert r.exit_code != 0 and "A1" in r.output


# --- trafo / motor ----------------------------------------------------------------------------

def test_transformer_design():
    d = machines.transformer_design(50, 230, 12, 50, 1.2, 2.5, 0.9, None, 5)
    assert d["area_cm2"] == pytest.approx(math.sqrt(50 / 0.9))
    assert d["turns_per_volt"] == pytest.approx(1e4 / (4.44 * 50 * 1.2 * d["area_cm2"]))
    assert d["n2"] / d["n1"] == pytest.approx(12 / 230 * 1.05)
    out = invoke(["transformer", "--v1", "230", "--v2", "12", "--va", "50"])
    assert "19.17 : 1" in out and "1159" in out


def test_motor():
    r = machines.motor_calc(7500, 400, 3, 0.85, 0.9, 50, 4, 1450, 7)
    assert r["ns_rpm"] == 1500
    assert r["slip"] == pytest.approx(1 / 30)
    assert r["torque_nm"] == pytest.approx(7500 / (2 * math.pi * 1450 / 60))
    assert r["current_a"] == pytest.approx(7500 / 0.9 / (math.sqrt(3) * 400 * 0.85))
    assert r["star_delta_current_a"] == pytest.approx(r["start_current_a"] / 3)
    assert runner.invoke(cli.app, ["motor", "-p", "1k", "--poles", "3"]).exit_code != 0
    assert runner.invoke(cli.app, ["motor", "-p", "1k", "--rpm", "1600"]).exit_code != 0


# --- dalga şekilleri ---------------------------------------------------------------------------

@pytest.mark.parametrize("shape,rms,rect,crest", [
    ("sine", 1 / math.sqrt(2), 2 / math.pi, math.sqrt(2)),
    ("square", 1, 1, 1),
    ("triangle", 1 / math.sqrt(3), 0.5, math.sqrt(3)),
    ("sawtooth", 1 / math.sqrt(3), 0.5, math.sqrt(3)),
    ("halfwave", 0.5, 1 / math.pi, 2),
    ("fullwave", 1 / math.sqrt(2), 2 / math.pi, math.sqrt(2)),
])
def test_wave_closed_forms(shape, rms, rect, crest):
    s = signal.wave_stats(shape, 1.0)
    assert s["rms"] == pytest.approx(rms, rel=1e-6)
    assert s["rect_avg"] == pytest.approx(rect, rel=1e-6)
    assert s["crest"] == pytest.approx(crest, rel=1e-6)


def test_wave_pwm_and_offset():
    s = signal.wave_stats("pwm", 12, 0.25)
    assert s["dc"] == pytest.approx(3) and s["rms"] == pytest.approx(6)
    assert s["ac_rms"] == pytest.approx(math.sqrt(36 - 9))
    s = signal.wave_stats("sine", 1, 0.5, 2)
    assert s["dc"] == pytest.approx(2) and s["rms"] == pytest.approx(math.sqrt(4 + 0.5))
    out = invoke(["wave", "sine", "--rms", "230"])
    assert "325.3 V" in out and "1.111" in out
    assert runner.invoke(cli.app, ["wave", "sine"]).exit_code != 0


# --- FFT -----------------------------------------------------------------------------------------

def _signal(n, fs):
    return [0.5 + 2 * math.sin(2 * math.pi * 1000 * i / fs) + 0.2 * math.sin(2 * math.pi * 3000 * i / fs)
            for i in range(n)]


def test_fft_matches_dft():
    x = [complex(math.sin(i) + 0.3 * i, 0) for i in range(16)]
    ref = [sum(x[n] * cmath.exp(-2j * math.pi * k * n / 16) for n in range(16)) for k in range(16)]
    assert signal.fft(x) == pytest.approx(ref)


def test_analyze_thd():
    r = signal.analyze(_signal(4096, 100e3), 100e3)
    f0 = r["fundamental"]
    assert f0["f_hz"] == pytest.approx(1000, abs=2)
    assert f0["amplitude"] == pytest.approx(2, rel=0.01)
    assert r["thd"] == pytest.approx(0.1, rel=0.02)
    assert r["time"]["dc"] == pytest.approx(0.5, abs=0.01)


def test_fft_csv_formats(tmp_path):
    fs, n = 100e3, 2048
    x = _signal(n, fs)
    (tmp_path / "plain.csv").write_text("time,CH1\n" + "".join(f"{i / fs:.9e},{v:.6f}\n" for i, v in enumerate(x)))
    (tmp_path / "rigol.csv").write_text("X,CH1,Start,Increment,\nSequence,Volt,0,1.000000e-05,\n"
                                        + "".join(f"{i},{v:.6f},\n" for i, v in enumerate(x)))
    (tmp_path / "semi.csv").write_text("".join(f"{i / fs:.9f};{v:.6f}\n".replace(".", ",") for i, v in enumerate(x)))
    (tmp_path / "raw.txt").write_text("".join(f"{v:.6f}\n" for v in x))
    for name in ("plain.csv", "rigol.csv", "semi.csv"):
        data = json.loads(invoke(["--json", "fft", str(tmp_path / name)]))
        assert data["fs_hz"] == pytest.approx(fs, rel=1e-6), name
        assert data["thd"] == pytest.approx(0.1, rel=0.02), name
    assert runner.invoke(cli.app, ["fft", str(tmp_path / "raw.txt")]).exit_code != 0
    out = invoke(["fft", str(tmp_path / "raw.txt"), "--rate", "100k", "--plot", str(tmp_path / "s.svg")])
    assert "THD" in out and (tmp_path / "s.svg").read_text().startswith("<svg")


# --- pinout --------------------------------------------------------------------------------------

@pytest.mark.parametrize("name,expect", [
    ("ne555", "ne555"), ("NE555P", "ne555"), ("sn74hc595n", "74hc595"), ("lm7812", "78xx"),
    ("7905", "79xx"), ("tl072", "lm358"), ("atmega328p-pu", "atmega328p"), ("lm35", "lm35"),
    ("lm358", "lm358"), ("lm3580", None), ("xyz", None),
])
def test_find_part(name, expect):
    part = pinout.find_part(name)
    assert (part.key if part else None) == expect


def test_pinout_data_is_consistent():
    for p in pinout.PARTS:
        n = int(p.package[3:]) if p.package.startswith("DIP") else 3
        assert len(p.pins) == n, p.key


def test_pinout_cli():
    out = invoke(["pinout", "ne555"])
    assert "TRIG 2" in out and "7 DIS" in out
    out = invoke(["pinout", "bc547"])
    assert "C" in out and "TO-92" in out
    assert "ATmega328P" in invoke(["pinout"])
    assert json.loads(invoke(["--json", "pinout", "ne555"]))["pins"]["8"] == "VCC"
    assert runner.invoke(cli.app, ["pinout", "nope"]).exit_code != 0


# --- rapor çıktısı ------------------------------------------------------------------------------

def test_markdown_output():
    out = invoke(["--md", "ohm", "-v", "12", "-r", "1k"])
    assert "| Quantity | Value |" in out and "| 12 mA |" in out
    assert "╭" not in out


def test_latex_output():
    out = invoke(["--latex", "filter", "rc", "--r", "1k", "--c", "100n"])
    assert "\\begin{tabular}" in out and "k$\\Omega$" in out and "█" not in out


def test_report_file_and_execute_hoisting(tmp_path, capsys):
    report = tmp_path / "lab.md"
    assert cli.execute(["ohm", "-v", "12", "-r", "1k", "--report", str(report)]) == 0
    assert cli.execute(["cap", "104", "--report", str(report)]) == 0
    text = report.read_text()
    assert "`$ elektro ohm -v 12 -r 1k`" in text and "`$ elektro cap 104`" in text
    assert "--report" not in text
    out = capsys.readouterr().out
    assert "╭" in out                     # terminalde normal çıktı da var
    tex = tmp_path / "lab.tex"
    assert cli.execute(["wave", "sine", "--vp", "1", "--report", str(tex)]) == 0
    assert "\\begin{table}" in tex.read_text()


def test_markdown_plot_embeds_image(tmp_path):
    out = invoke(["--md", "filter", "rc", "--r", "1k", "--c", "1u", "--plot", str(tmp_path / "b.svg")])
    assert f"![b]({tmp_path / 'b.svg'})" in out


def test_report_conflicts():
    assert runner.invoke(cli.app, ["--md", "--latex", "cap", "104"]).exit_code != 0
    assert runner.invoke(cli.app, ["--json", "--md", "cap", "104"]).exit_code != 0


def test_copy(monkeypatch):
    copied = []
    monkeypatch.setattr(ui, "copy_to_clipboard", lambda text: copied.append(text) or True)
    invoke(["--copy", "cap", "104"])
    invoke(["--md", "--copy", "cap", "104"])
    assert "100 nF" in copied[0] and "| Value |" in copied[1]


def test_latex_escape():
    assert ui.latex_escape("50% & 10 Ω_x") == "50\\% \\& 10 $\\Omega$\\_x"
