"""Faz 2: kaynak dalga şekilleri, analiz komutları, transient/AC/DC tarama, eğriler, grafik, sim."""

import asyncio
import csv
import json
import math

import pytest
from typer.testing import CliRunner

from elektro import cli, tui
from elektro.circuit import plot
from elektro.circuit import probes as prb
from elektro.circuit.model import Circuit, CircuitError, short_source
from elektro.circuit.solver import ac_analysis, dc_sweep, run_analysis, transient
from elektro.circuit.sources import ac_frequencies, dc_values, parse_directive, parse_source, spice_source
from elektro.ui import set_json, set_report

runner = CliRunner()


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "cfg"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.chdir(tmp_path)
    yield
    set_json(False)
    set_report(None)


def rc(source="PULSE(0 1 0 1n 1n 1 2)", r="1k", c="1u", second="C") -> Circuit:
    """V1 (A1-A3) → R1 (A1-D1) → C1/L1 (D1-D3) → toprak."""
    ckt = Circuit()
    ckt.add("V", 0, 0, rot=90, value=source)
    ckt.add("R", 0, 0, value=r)
    ckt.add(second, 3, 0, rot=90, value=c)
    ckt.add_wire((0, 2), (3, 2))
    ckt.add("GND", 0, 2)
    return ckt


# --- kaynaklar --------------------------------------------------------------------------------

@pytest.mark.parametrize("text,dc,ac,wave", [
    ("5", 5, 0, None), ("DC 5 AC 1", 5, 1, None), ("AC 2 90", None, 2, None), ("1Meg", 1e6, 0, None),
    ("SINE(0 1 1k)", None, 0, "SINE"), ("sin(1 2 50)", None, 0, "SINE"),
    ("PULSE(0 5 0 1u 1u 0.5m 1m)", None, 0, "PULSE"), ("DC 2 SINE(0 1 1k) AC 1", 2, 1, "SINE"),
])
def test_parse_source(text, dc, ac, wave):
    src = parse_source(text)
    assert src.dc == dc and src.ac_mag == ac and src.wave == wave


@pytest.mark.parametrize("bad", ["", "abc", "SINE(1)", "PULSE(1 2 3 4 5 6 7 8)", "5 6", "DC"])
def test_parse_source_rejects(bad):
    with pytest.raises(CircuitError):
        parse_source(bad)


def test_source_waveforms():
    sine = parse_source("SINE(1 2 1k 1m 0 90)")
    assert sine.at(0) == pytest.approx(1 + 2)                 # gecikme öncesi: faz 90°
    assert sine.at(1e-3 + 0.25e-3) == pytest.approx(1 + 0)    # 90° + 90° = 180°
    pulse = parse_source("PULSE(0 5 1m 1m 1m 2m 10m)")
    assert [round(pulse.at(x), 6) for x in (0, 1.5e-3, 3e-3, 4.5e-3, 6e-3, 11.5e-3)] == [0, 2.5, 5, 2.5, 0, 2.5]
    assert parse_source("AC 1 90").ac_phasor() == pytest.approx(1j)
    assert parse_source("SINE(2 1 1k)").dc_value() == 2       # DC yoksa t = 0 değeri


def test_spice_source_and_labels():
    assert spice_source("12") == "DC 12"
    assert spice_source("SINE(0 1 1k) AC 1") == "AC 1 SIN(0 1 1k)"
    assert short_source("SINE(0 1 1k) AC 1", "V") == "SIN 1kHz"
    assert short_source("PULSE(0 5 0 1u 1u 1m 2m)", "V") == "PULSE"
    assert short_source("12", "V") == "12V" and short_source("AC 1", "V") == "AC 1V"


# --- analiz komutları --------------------------------------------------------------------------

@pytest.mark.parametrize("text,norm", [
    ("", ".op"), (".op", ".op"), (".tran 10m", ".tran 10m"), ("tran 1u 10m", ".tran 1u 10m"),
    (".ac dec 100 10 100k", ".ac dec 100 10 100k"), (".AC LIN 10 1k 2k", ".ac lin 10 1k 2k"),
    (".dc v1 0 5 0.5", ".dc V1 0 5 500m"),
])
def test_parse_directive(text, norm):
    assert parse_directive(text).directive() == norm


@pytest.mark.parametrize("bad", [".tran", ".tran -1", ".tran 1 1m", ".ac dec 0 1 2", ".ac dec 10 5 1",
                                 ".ac foo 10 1 2", ".dc V1 0 5 -1", ".dc V1 0 5 0", ".foo", ".op 1"])
def test_parse_directive_rejects(bad):
    with pytest.raises(CircuitError):
        parse_directive(bad)


def test_sweep_points():
    assert len(ac_frequencies(parse_directive(".ac dec 10 10 100k"))) == 41
    lin = ac_frequencies(parse_directive(".ac lin 5 1k 2k"))
    assert lin == pytest.approx([1000, 1250, 1500, 1750, 2000])
    assert dc_values(parse_directive(".dc V1 5 0 -2.5")) == [5, 2.5, 0]


# --- analizler (analitik sonuçlarla) ------------------------------------------------------------

def _at(sweep, x):
    return min(range(len(sweep.x)), key=lambda k: abs(sweep.x[k] - x))


def test_rc_charging():
    w = transient(rc(), 5e-3, 1e-6)
    k = _at(w, 1e-3)
    assert w.voltages["D1"][k] == pytest.approx(1 - math.exp(-1), abs=1e-5)
    assert w.elements["C1"]["i"][k] == pytest.approx(math.exp(-1) / 1e3, rel=1e-3)
    assert w.voltages["D1"][-1] == pytest.approx(1 - math.exp(-5), abs=1e-5)


def test_rl_rise():
    w = transient(rc(r="10", c="10m", second="L"), 5e-3, 1e-6)
    assert w.elements["L1"]["i"][_at(w, 1e-3)] == pytest.approx(0.1 * (1 - math.exp(-1)), rel=1e-4)


def test_lc_oscillation_keeps_energy():
    ckt = Circuit()
    ckt.add("V", 0, 0, rot=90, value="PULSE(1 0 0 1n 1n 1 2)")
    ckt.add("R", 0, 0, value="1m")
    ckt.add("L", 3, 0, value="1m")
    ckt.add("C", 6, 0, rot=90, value="1u")
    ckt.add_wire((0, 2), (6, 2))
    ckt.add("GND", 0, 2)
    w = transient(ckt, 2e-3, 1e-7)
    late = w.voltages["G1"][len(w.x) // 2:]
    assert max(late) == pytest.approx(1, abs=0.01) and min(late) == pytest.approx(-1, abs=0.01)


def test_ac_lowpass():
    fc = 1 / (2 * math.pi * 1e3 * 1e-6)
    w = ac_analysis(rc("AC 1"), [fc / 100, fc, fc * 100])
    v = w.voltages["D1"]
    assert 20 * math.log10(abs(v[0])) == pytest.approx(0, abs=0.01)
    assert 20 * math.log10(abs(v[1])) == pytest.approx(-3.0103, abs=1e-3)
    assert math.degrees(math.atan2(v[1].imag, v[1].real)) == pytest.approx(-45, abs=1e-6)
    assert 20 * math.log10(abs(v[2])) == pytest.approx(-40, abs=0.01)
    with pytest.raises(CircuitError):
        ac_analysis(rc("5"), [1e3])                             # AC kaynak yok


def test_dc_sweep():
    ckt = rc("5", c="1k", second="R")                          # 1k / 1k bölücü
    w = dc_sweep(ckt, "v1", [0, 2, 4])
    assert w.voltages["D1"] == pytest.approx([0, 1, 2])
    assert w.x_unit == "V"
    with pytest.raises(CircuitError):
        dc_sweep(ckt, "V9", [0])


def test_run_analysis_and_traces():
    ckt = rc("SINE(0 1 1k) AC 1", c="100n")
    assert run_analysis(ckt, "") is None and run_analysis(ckt, ".op") is None
    w = run_analysis(ckt, ".tran 2m")
    assert w.kind == "tran" and len(w.x) == 1001 and w.label == ".tran 2m"
    assert [tr.expr for tr in prb.traces(ckt, w)] == ["V(A1)", "V(D1)"]      # probe yok: tüm düğümler
    ckt.probes = ["V(D1)", "I(R1)", "R(A1,D1)", "V(Z9)"]
    trs = prb.traces(ckt, w)
    assert [tr.expr for tr in trs] == ["V(D1)", "I(R1)", "V(Z9)"]          # R çizilmez
    assert trs[2].error and trs[0].values[0] == 0
    ac = run_analysis(ckt, ".ac dec 10 10 100k")
    assert isinstance(prb.traces(ckt, ac)[0].values[0], complex)


# --- grafik -------------------------------------------------------------------------------------

def test_plot_render():
    ckt = rc("SINE(0 1 1k) AC 1", c="100n")
    ckt.probes = ["V(D1)", "I(R1)"]
    w = run_analysis(ckt, ".tran 2m")
    lines = plot.render(plot.series_from(prb.traces(ckt, w)), w.x, 80, 14, x_unit="s", cursor=10, title="T")
    assert len(lines) == 14 and all(len(ln.plain) <= 80 for ln in lines)
    text = "\n".join(ln.plain for ln in lines)
    assert "V(D1)" in text and "I(R1)" in text and "x = " in text
    assert any("⠀" < ch <= "⣿" for ch in text)                 # braille noktaları
    assert "1ms" in lines[-1].plain
    ac = run_analysis(ckt, ".ac dec 10 10 100k")
    mag = plot.series_from(prb.traces(ckt, ac), "mag")
    phase = plot.series_from(prb.traces(ckt, ac), "phase")
    assert mag[0].unit == "dBV" and phase[0].unit == "°"
    lines = plot.render(mag, ac.x, 80, 12, log_x=True, x_unit="Hz")
    assert "100Hz" in lines[-1].plain and "10kHz" in lines[-1].plain
    empty = plot.render([], [], 60, 8, title="x", hint="hint")
    assert "hint" in "\n".join(ln.plain for ln in empty)


# --- elektro sim -------------------------------------------------------------------------------

def test_sim_analyses(tmp_path):
    ckt = rc("SINE(0 1 1k) AC 1", c="159n")
    ckt.probes = ["V(D1)"]
    ckt.analysis = ".tran 2m"
    ckt.save(tmp_path / "rc.json")
    out = runner.invoke(cli.app, ["sim", str(tmp_path / "rc.json"), "--plot", str(tmp_path / "t.svg"),
                                  "--csv", str(tmp_path / "t.csv")], env={"COLUMNS": "120"})
    assert out.exit_code == 0, out.output
    assert ".tran 2m" in out.output and "V(D1)" in out.output
    assert (tmp_path / "t.svg").read_text().count("<polyline") == 1
    rows = list(csv.reader(open(tmp_path / "t.csv")))
    assert rows[0] == ["s", "V(D1) (V)"] and len(rows) == 1002
    out = runner.invoke(cli.app, ["sim", str(tmp_path / "rc.json"), "-a", ".ac dec 10 10 100k", "-p", "V(A1)",
                                  "--csv", str(tmp_path / "a.csv")], env={"COLUMNS": "120"})
    assert out.exit_code == 0, out.output and "dB" in out.output
    assert list(csv.reader(open(tmp_path / "a.csv")))[0][1:] == ["V(D1) |V|", "V(D1) phase(deg)", "V(A1) |V|",
                                                                  "V(A1) phase(deg)"]
    data = json.loads(runner.invoke(cli.app, ["--json", "sim", str(tmp_path / "rc.json"), "-a",
                                              ".dc V1 0 2 1"]).output)
    assert data["x"] == [0, 1, 2] and data["traces"][0]["values"] == pytest.approx([0, 1, 2])
    out = runner.invoke(cli.app, ["sim", str(tmp_path / "rc.json"), "-a", ".op"], env={"COLUMNS": "120"})
    assert "B2" not in out.output and "V(D1)" in out.output                  # yalnız DC
    assert runner.invoke(cli.app, ["sim", str(tmp_path / "rc.json"), "-a", ".tran x"]).exit_code != 0
    spice = runner.invoke(cli.app, ["sim", str(tmp_path / "rc.json"), "--spice"]).output
    assert "V1 A1 0 AC 1 SIN(0 1 1k)" in spice and ".tran 2m" in spice


def test_file_keeps_analysis(tmp_path):
    ckt = rc()
    ckt.analysis = ".ac dec 10 1 1k"
    ckt.save(tmp_path / "x.json")
    assert Circuit.load(tmp_path / "x.json").analysis == ".ac dec 10 1 1k"


# --- arayüz ------------------------------------------------------------------------------------

def test_tui_analysis_and_plot(tmp_path):
    ckt = rc("SINE(0 1 1k) AC 1", c="100n")
    ckt.probes = ["V(D1)"]
    ckt.analysis = ".tran 2m"
    ckt.save(tmp_path / "rc.json")

    async def scenario():
        app = tui.ElektroApp(tmp_path / "rc.json")
        async with app.run_test(size=(150, 46)) as pilot:
            await pilot.pause()
            await pilot.press("f5")
            await app.workers.wait_for_complete()
            await pilot.pause()
            ed, pv = app.query_one("#editor"), app.query_one("#plot")
            assert pv.sweep is not None and pv.sweep.kind == "tran" and pv.traces[0].expr == "V(D1)"
            await pilot.press("s")
            await pilot.pause()
            app.screen.query_one("#an-directive").value = ".ac dec 20 10 100k"
            await pilot.pause()
            assert app.screen.query_one("#an-kind").value == "ac"
            assert app.screen.query_one("#an-fstop").value == "100k"
            app.screen.query_one("#an-points").value = "30"            # form → komut satırı
            await pilot.pause()
            assert app.screen.query_one("#an-directive").value == ".ac dec 30 10 100k"
            await pilot.press("enter")
            await pilot.pause()
            await app.workers.wait_for_complete()
            await pilot.pause()
            assert ed.circuit.analysis == ".ac dec 30 10 100k" and pv.sweep.kind == "ac"
            await pilot.press("tab")
            assert app.focused is pv
            before = pv.cursor
            await pilot.press("right")
            assert pv.cursor > before
            await pilot.press("m")
            assert pv.mode == "phase"
            await pilot.press("f6")
            assert pv.has_class("big")
            await pilot.press("f6", "f6")
            assert not pv.has_class("hidden") and not pv.has_class("big")
            ed.focus()
            ed.cursor = (3, 1)                                         # C1'in gövdesi
            await pilot.press("x")                                     # sil → canlı çözüm
            await app.workers.wait_for_complete()
            await pilot.pause()
            assert pv.sweep is not None
    asyncio.run(scenario())


def test_tui_values_follow_plot_cursor(tmp_path):
    """Analiz varken probe tablosu ve şema etiketleri grafik imlecindeki değeri gösterir."""
    from rich.console import Console
    ckt = rc("SINE(0 1 1k) AC 1", c="159n")
    ckt.probes = ["V(A1)", "V(D1)"]
    ckt.analysis = ".tran 3m"
    ckt.save(tmp_path / "rc.json")

    def panel(app) -> str:
        con = Console(width=70, color_system=None, record=True)
        con.print(app.query_one("#editor").info())
        return con.export_text()

    async def scenario():
        app = tui.ElektroApp(tmp_path / "rc.json")
        async with app.run_test(size=(150, 46)) as pilot:
            await pilot.pause()
            await pilot.press("f5")
            await app.workers.wait_for_complete()
            await pilot.pause()
            ed = app.query_one("#editor")
            assert ed.plot_cursor == 500
            text = panel(app)
            assert "1.5 ms" in text and "706.8 mV" in text                 # RMS = 1/√2
            assert ed._label_voltages()["D1"] == pytest.approx(ed.sweep.voltages["D1"][500])
            await pilot.press("tab", "right", "right")
            await pilot.pause()
            assert ed.plot_cursor > 500 and "1.5 ms" not in panel(app)
            ed.circuit.analysis = ".ac dec 20 10 100k"
            ed.run_simulation(quiet=True)
            await app.workers.wait_for_complete()
            await pilot.pause()
            text = panel(app)
            assert "∠" in text and "-45" in text                           # fc ≈ 1 kHz'de −45°
    asyncio.run(scenario())
