"""Devre modeli, Excel adresleri, DC çözücü, probe'lar ve `elektro sim`."""

import asyncio
import json

import pytest
from typer.testing import CliRunner

from elektro import cli, tui
from elektro.circuit import probes as prb
from elektro.circuit.model import Circuit, CircuitError, addr, col_name, parse_addr, spice_number
from elektro.circuit.render import View, render
from elektro.circuit.solver import dc_operating_point
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


def divider(v="12", r1="10k", r2="4k7") -> Circuit:
    """V1 (B2-B4), R1 (B2-E2), R2 (E2-E4), kablo B4-E4, GND B4."""
    c = Circuit()
    c.add("V", 1, 1, rot=90, value=v)
    c.add("R", 1, 1, value=r1)
    c.add("R", 4, 1, rot=90, value=r2)
    c.add_wire((1, 3), (4, 3))
    c.add("GND", 1, 3)
    return c


# --- adresler ---------------------------------------------------------------------------------

@pytest.mark.parametrize("x,name", [(0, "A"), (25, "Z"), (26, "AA"), (51, "AZ"), (52, "BA"), (701, "ZZ"), (702, "AAA")])
def test_col_name(x, name):
    assert col_name(x) == name
    assert parse_addr(f"{name}1") == (x, 0)


def test_addr_roundtrip():
    assert addr((2, 0)) == "C1" and addr((2, 9)) == "C10"
    assert parse_addr("c10") == (2, 9)
    assert parse_addr("C0") is None and parse_addr("1C") is None and parse_addr("") is None


# --- düğümler ---------------------------------------------------------------------------------

def test_nets_are_named_like_cells():
    c = divider()
    nets = c.nets()
    assert nets[(1, 1)] == "B2" and nets[(4, 1)] == "E2"
    assert nets[(1, 3)] == "0" and nets[(4, 3)] == "0"
    assert c.net_at((2, 3)) == "0"                  # kablonun ortası
    assert c.net_at((2, 1)) is None                 # direncin gövdesi düğüm değil


def test_crossing_wires_do_not_connect_but_t_junctions_do():
    c = Circuit()
    c.add_wire((0, 2), (4, 2))
    c.add_wire((2, 0), (2, 4))                      # artı şeklinde kesişme: bağlı değil
    nets = c.nets()
    assert nets[(0, 2)] != nets[(2, 0)]
    c.add_wire((2, 2), (2, 5))                      # ucu yatay kablonun ortasında: T bağlantısı
    nets = c.nets()
    assert nets[(0, 2)] == nets[(2, 5)] == nets[(2, 0)]


# --- DC çözücü --------------------------------------------------------------------------------

def test_divider():
    r = dc_operating_point(divider())
    assert r.voltages["E2"] == pytest.approx(12 * 4.7 / 14.7, rel=1e-6)
    assert r.elements["R1"]["i"] == pytest.approx(12 / 14.7e3, rel=1e-6)
    assert r.elements["V1"]["p"] == pytest.approx(-12 * 12 / 14.7e3, rel=1e-6)   # kaynak güç verir


def test_current_source_inductor_capacitor():
    c = Circuit()
    c.add("I", 0, 0, rot=90, value="2m")            # A1-A3, akım A1'den kaynağın içinden A3'e
    c.add("R", 0, 0, value="1k")                    # A1-D1
    c.add("L", 3, 0, rot=90)                        # D1-D3: DC'de kısa devre
    c.add("C", 0, 0, rot=0)
    c.components[-1].x, c.components[-1].y = 6, 0   # boşta kondansatör: uyarı, tekil değil
    c.add_wire((0, 2), (3, 2))
    c.add("GND", 0, 2)
    r = dc_operating_point(c)
    assert r.voltages["A1"] == pytest.approx(-2.0, rel=1e-6)
    assert r.elements["L1"]["i"] == pytest.approx(-2e-3, rel=1e-6)
    assert any("C1" in w for w in r.warnings)


@pytest.mark.parametrize("build,message", [
    (lambda c: None, "empty"),
    (lambda c: c.add("R", 0, 0), "ground"),
])
def test_solver_errors(build, message):
    c = Circuit()
    build(c)
    with pytest.raises(CircuitError):
        dc_operating_point(c)


def test_voltage_source_loop_is_singular():
    c = Circuit()
    c.add("V", 0, 0, rot=90, value="5")
    c.add("V", 3, 0, rot=90, value="3")
    c.add_wire((0, 0), (3, 0))
    c.add_wire((0, 2), (3, 2))
    c.add("GND", 0, 2)
    with pytest.raises(CircuitError):
        dc_operating_point(c)


# --- probe'lar --------------------------------------------------------------------------------

@pytest.mark.parametrize("text,norm", [
    ("c3", "V(C3)"), ("v( e2 )", "V(E2)"), ("i(b2, e2)", "I(B2,E2)"), ("I(R1)", "I(R1)"), ("p(r2)", "P(R2)"),
    ("V(B2;E2)", "V(B2,E2)"),
])
def test_probe_normalize(text, norm):
    assert prb.normalize(text) == norm


@pytest.mark.parametrize("bad", ["X(C3)", "V()", "P(B2,E2)", "V(C3", "hello world", "R(A1)"])
def test_probe_normalize_rejects(bad):
    with pytest.raises(CircuitError):
        prb.normalize(bad)


def test_probe_values():
    c = divider()
    r = dc_operating_point(c)
    i = 12 / 14.7e3
    v_e2 = 12 * 4.7 / 14.7
    assert prb.evaluate("V(E2)", c, r) == pytest.approx(v_e2, rel=1e-6)
    assert prb.evaluate("V(C4)", c, r) == 0                         # toprak kablosunun ortası
    assert prb.evaluate("V(B2,E2)", c, r) == pytest.approx(12 - v_e2, rel=1e-6)
    assert prb.evaluate("I(B2,E2)", c, r) == pytest.approx(i, rel=1e-6)
    assert prb.evaluate("I(E2,B2)", c, r) == pytest.approx(-i, rel=1e-6)
    assert prb.evaluate("I(B2,E4)", c, r) == pytest.approx(-i, rel=1e-6)   # V1 içinden: + uçtan çıkar
    assert prb.evaluate("I(R1)", c, r) == pytest.approx(i, rel=1e-6)
    assert prb.evaluate("P(R2)", c, r) == pytest.approx(v_e2 * i, rel=1e-6)
    for expr in ("V(Z9)", "I(B2,B3)", "I(E2,E2)", "I(R9)"):
        with pytest.raises(CircuitError):
            prb.evaluate(expr, c, r)


def test_parallel_elements_add_up():
    c = divider()
    c.add("R", 1, 1, value="10k")                   # R1 ile paralel ikinci direnç (aynı uçlar)
    r = dc_operating_point(c)
    assert prb.evaluate("I(B2,E2)", c, r) == pytest.approx(r.elements["R1"]["i"] * 2, rel=1e-6)


def test_read_all_without_result():
    c = divider()
    c.probes = ["V(E2)", "I(R1)"]
    readings = prb.read_all(c, None)
    assert [x.expr for x in readings] == ["V(E2)", "I(R1)"] and all(x.value is None for x in readings)


# --- dosya, SPICE, çizim -------------------------------------------------------------------

def test_save_load_roundtrip(tmp_path):
    c = divider()
    c.probes = ["V(E2)", "I(B2,E2)"]
    c.save(tmp_path / "d.json")
    d = Circuit.load(tmp_path / "d.json")
    assert d.to_dict() == c.to_dict()
    (tmp_path / "bad.json").write_text('{"components": [{"ref": "X1", "kind": "Z", "x": 0, "y": 0}]}')
    with pytest.raises(CircuitError):
        Circuit.load(tmp_path / "bad.json")


def test_spice_export():
    text = divider(r2="1meg").to_spice("t")
    assert "V1 B2 0 DC 12" in text and "R1 B2 E2 10k" in text and "R2 E2 0 1Meg" in text
    assert spice_number(4700) == "4.7k" and spice_number(1e-7) == "100n"


def test_render_headers_and_probes():
    c = divider()
    r = dc_operating_point(c)
    lines = [ln.plain for ln in render(c, View(width=40, height=12, cursor=(4, 1), voltages=r.voltages,
                                               probe_points={(4, 1)}))]
    assert lines[0].split()[:5] == ["A", "B", "C", "D", "E"]
    assert lines[2].split()[0] == "1" and lines[4].split()[0] == "2"
    text = "\n".join(lines)
    assert "[R1 10k]" in text and "[GND]" in text and "3.837V" in text


# --- elektro sim ----------------------------------------------------------------------------

def test_sim_cli(tmp_path):
    c = divider()
    c.probes = ["V(E2)"]
    c.save(tmp_path / "d.json")
    r = runner.invoke(cli.app, ["sim", str(tmp_path / "d.json"), "-p", "I(B2,E2)"], env={"COLUMNS": "120"})
    assert r.exit_code == 0, r.output
    assert "3.837 V" in r.output and "816.3 µA" in r.output and "I(B2,E2)" in r.output
    data = json.loads(runner.invoke(cli.app, ["--json", "sim", str(tmp_path / "d.json")]).output)
    assert data["voltages"]["E2"] == pytest.approx(3.8367, rel=1e-4)
    assert data["probes"][0]["expr"] == "V(E2)"
    spice = runner.invoke(cli.app, ["sim", str(tmp_path / "d.json"), "--spice"]).output
    assert spice.startswith("* d") and ".op" in spice
    assert runner.invoke(cli.app, ["sim", str(tmp_path / "d.json"), "-p", "X(1)"]).exit_code != 0


# --- editörde probe -----------------------------------------------------------------------------

def test_editor_probes(tmp_path):
    divider().save(tmp_path / "d.json")

    async def scenario():
        app = tui.ElektroApp(tmp_path / "d.json")
        async with app.run_test(size=(150, 40)) as pilot:
            await pilot.pause()
            ed = app.query_one("#editor")
            ed.cursor = (4, 1)
            await pilot.press("p")                         # E2 gerilimi
            ed.cursor = (1, 1)
            await pilot.press("a")
            ed.cursor = (4, 1)
            await pilot.press("a")                         # B2 → E2 akımı
            ed.cursor = (2, 1)
            await pilot.press("p")                         # R1 akımı
            await pilot.press("P")
            await pilot.pause()
            app.screen.query_one("#prompt-input").value = "v(b2,e2)"
            await pilot.press("enter")
            await pilot.pause()
            assert ed.circuit.probes == ["V(E2)", "I(B2,E2)", "I(R1)", "V(B2,E2)"]
            readings = prb.read_all(ed.circuit, ed.result)
            assert readings[1].value == pytest.approx(12 / 14.7e3, rel=1e-6)
            ed.cursor = (4, 1)
            await pilot.press("p")                         # tekrar basınca kalkar
            assert "V(E2)" not in ed.circuit.probes
            await pilot.press("P")
            await pilot.pause()
            app.screen.query_one("#prompt-input").value = "-"
            await pilot.press("enter")
            await pilot.pause()
            assert ed.circuit.probes == []
            await pilot.press("ctrl+z")
            assert len(ed.circuit.probes) == 3
    asyncio.run(scenario())


# --- eşdeğer direnç -------------------------------------------------------------------------

def bridge(r5="5k") -> Circuit:
    """Dengeli Wheatstone köprüsü: üst 1k-1k, alt 2k-2k, köprü R5 (D1-D3). Uçlar A1 ve G1."""
    c = Circuit()
    c.add("R", 0, 0, value="1k")
    c.add("R", 3, 0, value="1k")
    c.add_wire((0, 0), (0, 2))
    c.add("R", 0, 2, value="2k")
    c.add("R", 3, 2, value="2k")
    c.add_wire((6, 0), (6, 2))
    c.add("R", 3, 0, rot=90, value=r5)
    return c


def test_equivalent_resistance_series_parallel():
    from elektro.circuit.solver import equivalent_resistance as req
    c = Circuit()
    c.add("R", 0, 0, value="1k")
    c.add("R", 0, 0, value="1k")                    # paralel
    c.add("R", 3, 0, value="2k")                    # seri
    assert req(c, "A1", "G1") == pytest.approx(2500)
    assert req(c, "A1", "D1") == pytest.approx(500)
    assert req(c, "A1", "A1") == 0
    c.add("R", 0, 2, value="5k")                    # bağlantısız direnç
    assert req(c, "A1", "A3") == float("inf")


def test_equivalent_resistance_bridge_and_sources():
    from elektro.circuit.solver import equivalent_resistance as req
    assert req(bridge(), "A1", "G1") == pytest.approx(1 / (1 / 2000 + 1 / 4000))
    assert req(bridge("1"), "A1", "G1") == pytest.approx(req(bridge("1meg"), "A1", "G1"), rel=1e-3)
    # Thevenin: bölücünün çıkışından bakınca 10k ∥ 4k7 (gerilim kaynağı kısa devre)
    c = divider()
    assert req(c, "E2", "0") == pytest.approx(1 / (1 / 10e3 + 1 / 4.7e3))
    assert prb.evaluate("R(E2,E4)", c, None) == pytest.approx(1 / (1 / 10e3 + 1 / 4.7e3))
    assert req(c, "B2", "0") == 0                    # kaynağın uçları


def test_r_probe_without_source(tmp_path):
    c = bridge()
    c.probes = ["R(A1,G1)", "R(A1,D1)"]
    readings = prb.read_all(c, None)
    assert readings[0].value == pytest.approx(1333.333, rel=1e-6) and readings[0].unit == "Ω"
    assert prb.normalize("r(a1, g1)") == "R(A1,G1)"
    with pytest.raises(CircuitError):
        prb.normalize("R(A1)")
    c.save(tmp_path / "b.json")
    r = runner.invoke(cli.app, ["sim", str(tmp_path / "b.json")], env={"COLUMNS": "120"})
    assert r.exit_code == 0, r.output
    assert "1.333 kΩ" in r.output
    c.probes = []
    c.save(tmp_path / "b.json")
    assert runner.invoke(cli.app, ["sim", str(tmp_path / "b.json")]).exit_code != 0
    r = runner.invoke(cli.app, ["--json", "sim", str(tmp_path / "b.json"), "-p", "R(A1,G1)"])
    assert json.loads(r.output)["probes"][0]["value"] == pytest.approx(1333.333, rel=1e-6)


def test_editor_resistance_probe(tmp_path):
    bridge().save(tmp_path / "b.json")

    async def scenario():
        app = tui.ElektroApp(tmp_path / "b.json")
        async with app.run_test(size=(150, 40)) as pilot:
            await pilot.pause()
            ed = app.query_one("#editor")
            await pilot.press("f5")
            assert ed.error is None and ed.result is None        # kaynak yok: hata değil
            ed.cursor = (0, 0)
            await pilot.press("o")
            ed.cursor = (6, 1)                                  # G2: sağdaki kablonun ortası
            await pilot.press("enter")
            assert ed.circuit.probes == ["R(A1,G2)"]
            readings = prb.read_all(ed.circuit, ed.result)
            assert readings[0].value == pytest.approx(1333.333, rel=1e-6)
    asyncio.run(scenario())
