"""Faz 4: düğüm etiketleri, SPICE içe aktarma, örnek devreler."""

import asyncio
import json

import pytest
from typer.testing import CliRunner

from elektro import cli, tui
from elektro.circuit import examples
from elektro.circuit import probes as prb
from elektro.circuit.model import Circuit, CircuitError, valid_value
from elektro.circuit.render import View, render
from elektro.circuit.solver import dc_operating_point, run_analysis
from elektro.circuit.spice import is_spice, parse_spice
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


# --- düğüm etiketleri ---------------------------------------------------------------------------

def labelled_divider() -> Circuit:
    """Kablosuz bölücü: her şey etiketle bağlı, toprak da "GND" etiketiyle."""
    c = Circuit()
    c.add("V", 0, 0, rot=90, value="10")
    c.add("N", 0, 0, value="VCC")
    c.add("N", 0, 2, value="gnd")
    c.add("R", 4, 0, rot=90, value="1k")
    c.add("N", 4, 0, value="vcc")                      # büyük/küçük harf farketmez
    c.add("N", 4, 2, value="OUT")
    c.add("R", 8, 0, rot=90, value="1k")
    c.add("N", 8, 0, value="OUT")
    c.add("N", 8, 2, value="GND")
    return c


def test_labels_connect_and_name_nodes():
    c = labelled_divider()
    nets = c.nets()
    assert nets[(0, 0)] == nets[(4, 0)] == "VCC"
    assert nets[(0, 2)] == nets[(8, 2)] == "0"
    assert nets[(4, 2)] == nets[(8, 0)] == "OUT"
    r = dc_operating_point(c)
    assert r.voltages["OUT"] == pytest.approx(5, rel=1e-6) and not r.warnings


def test_label_probes_and_validation():
    c = labelled_divider()
    c.probes = [prb.normalize(x) for x in ("out", "V(VCC,OUT)", "I(VCC,OUT)", "R(OUT,GND)", "V(nope)")]
    assert c.probes[0] == "V(OUT)"
    vals = prb.read_all(c, dc_operating_point(c))
    assert vals[0].value == pytest.approx(5, rel=1e-6)
    assert vals[1].value == pytest.approx(5, rel=1e-6)
    assert vals[2].value == pytest.approx(5e-3, rel=1e-6)
    assert vals[3].value == pytest.approx(500, rel=1e-6)
    assert vals[4].error
    assert valid_value("N", "OUT") and valid_value("N", "v_ref2")
    assert not valid_value("N", "2out") and not valid_value("N", "a b") and not valid_value("N", "")


def test_label_drawing():
    c = labelled_divider()
    c.components[5].rot = 180
    text = "\n".join(ln.plain for ln in render(c, View(width=60, height=10)))
    assert "◂VCC" in text and "OUT▸" in text and "◂GND" in text


def test_label_only_ground_and_no_ground():
    c = labelled_divider()
    for comp in c.components:
        if comp.kind == "N" and comp.value.upper() == "GND":
            comp.value = "BOTTOM"
    with pytest.raises(CircuitError):
        dc_operating_point(c)                          # toprak yok


# --- SPICE içe aktarma --------------------------------------------------------------------------

CE = """common emitter
* comment
VCC vcc 0 DC 12
VIN in 0 SINE(0 10m 1k) AC 1
C1 in base 10u
R1 vcc base 100k
R2 base 0 22k
RC vcc out 4.7k
RE emit 0 1k
Q1 out base emit Q2N2222 ; inline comment
.model Q2N2222 NPN(IS=14.34f BF=255.9 BR=6.092
+ VAF=74.03 CJE=22p)
.include x.lib
.tran 3m
.end
"""


def test_parse_spice_common_emitter():
    c, warnings = parse_spice(CE)
    refs = {x.ref: x for x in c.components if x.is_part}
    assert set(refs) == {"VCC", "VIN", "C1", "R1", "R2", "RC", "RE", "Q1"}
    assert refs["Q1"].value == "NPN IS=14.34f BF=255.9 BR=6.092 VAF=74.03"
    assert c.analysis == ".tran 3m"
    assert any("CJE" in w for w in warnings) and any(".include" in w for w in warnings)
    r = dc_operating_point(c)
    assert r.voltages["out"] == pytest.approx(5.37, abs=0.05)
    w = run_analysis(c, ".ac dec 5 100 10k")
    k = min(range(len(w.x)), key=lambda i: abs(w.x[i] - 1e3))
    assert abs(w.voltages["out"][k]) == pytest.approx(4.6, abs=0.1)


def test_parse_spice_numeric_nodes_library_models_and_opamp():
    text = """t
V1 1 0 10
R1 1 2 1k
D1 2 0 D1N4148
E1 out 0 2 3 1e5
R2 3 0 1k
R3 3 out 1k
"""
    c, warnings = parse_spice(text)
    assert next(x for x in c.components if x.kind == "D").value == "1N4148"     # D1N4148 → kütüphane
    assert next(x for x in c.components if x.kind == "U").value == "ideal A=1e5"
    assert {x.value for x in c.components if x.kind == "N"} >= {"N1", "N2", "N3", "out"}
    r = dc_operating_point(c)
    vd = r.voltages["N2"]
    assert 0.6 < vd < 0.8 and r.voltages["out"] == pytest.approx(2 * vd, rel=1e-3)   # kazanç 2


def test_parse_spice_errors():
    with pytest.raises(CircuitError):
        parse_spice("only title\n.op\n")
    c, warnings = parse_spice("t\nR1 a 0 1k\nX1 a b sub\n")
    assert any("X1" in w for w in warnings)


def test_spice_roundtrip(tmp_path):
    original = examples.build("common_emitter")
    (tmp_path / "ce.cir").write_text(original.to_spice("ce"))
    assert is_spice(tmp_path / "ce.cir")
    imported = Circuit.load(tmp_path / "ce.cir")
    a = dc_operating_point(original).voltages["OUT"]
    b = dc_operating_point(imported).voltages["OUT"]
    assert a == pytest.approx(b, rel=1e-6)


def test_sim_cli_reads_spice(tmp_path):
    (tmp_path / "ce.cir").write_text(CE)
    out = runner.invoke(cli.app, ["sim", str(tmp_path / "ce.cir"), "-p", "V(out)"], env={"COLUMNS": "120"})
    assert out.exit_code == 0, out.output
    assert ".tran 3m" in out.output and "V(out)" in out.output and "CJE" in out.output


# --- örnekler --------------------------------------------------------------------------------

@pytest.mark.parametrize("name", examples.names())
def test_every_example_solves_cleanly(name):
    c = examples.build(name)
    assert min(x.x for x in c.components) == 2                     # etiketler kenara taşmasın
    has_source = any(x.kind in ("V", "I") for x in c.components)
    result = dc_operating_point(c) if has_source else None
    assert result is None or not result.warnings
    assert not [r.error for r in prb.read_all(c, result) if r.error]
    if c.analysis:
        sweep = run_analysis(c, c.analysis)
        assert not [tr.error for tr in prb.traces(c, sweep) if tr.error]


@pytest.mark.parametrize("name,expr,check", [
    ("divider", "V(OUT)", lambda v: v == pytest.approx(12 * 4.7 / 14.7, rel=1e-6)),
    ("bridge", "R(A,B)", lambda v: v == pytest.approx(4000 / 3, rel=1e-6)),
])
def test_example_values(name, expr, check):
    c = examples.build(name)
    has_source = any(x.kind in ("V", "I") for x in c.components)
    reading = next(r for r in prb.read_all(c, dc_operating_point(c) if has_source else None) if r.expr == expr)
    assert check(reading.value)


def test_example_physics():
    c = examples.build("bridge_rectifier")
    out = run_analysis(c, c.analysis).voltages["OUT"]
    assert 10.2 < max(out[len(out) // 2:]) < 10.7                  # 12 V − 2 diyot
    c = examples.build("integrator")
    tr = prb.traces(c, run_analysis(c, c.analysis))[1].values
    late = tr[len(tr) // 2:]
    assert max(late) == pytest.approx(-min(late), rel=0.05)         # sıfır etrafında üçgen
    c = examples.build("comparator")
    tr = prb.traces(c, run_analysis(c, c.analysis))[2].values
    assert max(tr) == pytest.approx(5, abs=0.01) and min(tr) == pytest.approx(0, abs=0.01)


def test_examples_cli(tmp_path):
    out = runner.invoke(cli.app, ["examples"], env={"COLUMNS": "120"})
    assert out.exit_code == 0 and "rc_lowpass" in out.output
    data = json.loads(runner.invoke(cli.app, ["--json", "examples"]).output)
    assert len(data) == len(examples.names())
    out = runner.invoke(cli.app, ["examples", "zener", "-o", str(tmp_path / "z.json")])
    assert out.exit_code == 0
    assert Circuit.load(tmp_path / "z.json").analysis == ".dc V1 0 15 0.1"
    assert runner.invoke(cli.app, ["examples", "nope"]).exit_code != 0


# --- editör ------------------------------------------------------------------------------------

def test_editor_labels_examples_and_import(tmp_path):
    (tmp_path / "ce.cir").write_text(CE)

    async def scenario():
        app = tui.ElektroApp()
        async with app.run_test(size=(150, 46)) as pilot:
            await pilot.press("f3")
            ed = app.query_one("#editor")
            ed.cursor = (3, 3)
            await pilot.press("n")
            await pilot.pause()
            app.screen.query_one("#prompt-input").value = "2bad"
            await pilot.press("enter")
            await pilot.pause()
            assert "2bad" in str(app.screen.query_one("#prompt-error").render())
            app.screen.query_one("#prompt-input").value = "OUT"
            await pilot.press("enter")
            await pilot.pause()
            assert [(c.kind, c.value) for c in ed.circuit.components] == [("N", "OUT")]
            await pilot.press("p")
            assert ed.circuit.probes == ["V(OUT)"]
            await pilot.press("ctrl+e")
            await pilot.pause()
            options = app.screen.query_one("#examples")
            while options.get_option_at_index(options.highlighted).id != "divider":
                await pilot.press("down")
            await pilot.press("enter")
            await pilot.pause()
            await app.workers.wait_for_complete()
            await pilot.pause()
            assert ed.path.name == "divider.json" and ed.result is not None
            assert ed.result.voltages["OUT"] == pytest.approx(3.837, rel=1e-3)
            await pilot.press("ctrl+z")                                  # örnekten önceki devre geri gelir
            assert [c.value for c in ed.circuit.components] == ["OUT"]
            ed.load(tmp_path / "ce.cir")
            assert ed.path.suffix == ".json" and ed.dirty and "ce.cir" in ed.message
    asyncio.run(scenario())
