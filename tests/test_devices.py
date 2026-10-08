"""Faz 3: diyot, BJT, MOSFET, op-amp modelleri; Newton-Raphson; çizim; probe uçları."""

import asyncio
import math

import pytest

from elektro import tui
from elektro.circuit import probes as prb
from elektro.circuit.devices import LIBRARY, models_for, parse_model
from elektro.circuit.model import Circuit, CircuitError, addr, valid_value
from elektro.circuit.render import View, render
from elektro.circuit.solver import dc_operating_point, dc_sweep, run_analysis
from elektro.ui import set_json, set_report


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "cfg"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.chdir(tmp_path)
    yield
    set_json(False)
    set_report(None)


def series(src, r, kind, value, rot=90) -> Circuit:
    """V1 (A1-A3) — R1 (A1-D1) — eleman (D1-D3) — toprak."""
    c = Circuit()
    c.add("V", 0, 0, rot=90, value=src)
    c.add("R", 0, 0, value=r)
    c.add(kind, 3, 0, rot=rot, value=value)
    c.add_wire((0, 2), (3, 2))
    c.add("GND", 0, 2)
    return c


def common_emitter(rb="470k", rc="1k", model="2N2222", vcc="12") -> Circuit:
    c = Circuit()
    c.add("V", 0, 2, rot=90, value=vcc)
    c.add_wire((0, 2), (0, 0))
    c.add_wire((0, 0), (8, 0))
    c.add("R", 4, 0, rot=90, value=rb)
    c.add("R", 8, 0, rot=90, value=rc)
    c.add("Q", 8, 4, value=model)                    # C=(8,3) B=(7,4) E=(8,5)
    c.add_wire((4, 2), (4, 4))
    c.add_wire((4, 4), (7, 4))
    c.add_wire((8, 2), (8, 3))
    c.add_wire((0, 4), (0, 6))
    c.add_wire((0, 6), (8, 6))
    c.add_wire((8, 5), (8, 6))
    c.add("GND", 0, 6)
    return c


def noninverting(model="ideal", vin="0.5") -> Circuit:
    """Kazanç 11: Rf = 10k, Rg = 1k; çıkış F3."""
    c = Circuit()
    c.add("V", 0, 1, rot=90, value=vin)
    c.add("U", 3, 2, value=model)                    # çıkış (5,2), + (2,1), − (2,3)
    c.add_wire((0, 1), (2, 1))
    c.add("R", 2, 3, rot=90, value="1k")
    c.add("R", 2, 3, value="10k")
    c.add_wire((5, 3), (5, 2))
    c.add_wire((0, 3), (0, 5))
    c.add_wire((0, 5), (2, 5))
    c.add("GND", 0, 5)
    return c


# --- modeller -----------------------------------------------------------------------------------

def test_parse_model():
    m = parse_model("Q", "2N2222 BF=150")
    assert m.type == "NPN" and m.params["BF"] == 150
    assert parse_model("Q", "2n3906").type == "PNP"
    assert parse_model("Q", "PNP IS=1e-13").params["IS"] == 1e-13
    assert parse_model("M", "IRF9540").type == "PMOS"
    assert parse_model("D", "IS=1e-12 N=2").params["N"] == 2
    u = parse_model("U", "TL072 ±15")
    assert (u.vmin, u.vmax, u.params["GBW"]) == (-15, 15, 3e6)
    assert (parse_model("U", "LM358 0..5").vmin, parse_model("U", "ideal +-12").vmax) == (0, 12)
    assert parse_model("D", "").name == "D"                  # boş: varsayılan genel model
    for kind, bad in (("Q", "2N7000"), ("D", "XYZ"), ("M", "NMOS FOO=1"), ("U", "ideal 5..1"),
                      ("D", "IS=-1"), ("Q", "BF")):
        with pytest.raises(CircuitError):
            parse_model(kind, bad)
    assert valid_value("D", "LED") and not valid_value("D", "2N2222")
    assert "2N2222" in models_for("Q") and "TL072" in models_for("U")
    assert all(t in ("D", "NPN", "PNP", "NMOS", "PMOS", "OPAMP") for t, _ in LIBRARY.values())


# --- diyotlar ------------------------------------------------------------------------------------

def test_diode_forward_and_kcl():
    r = dc_operating_point(series("5", "1k", "D", "1N4148"))
    vd, i = r.voltages["D1"], r.elements["D1"]["i"]
    assert 0.6 < vd < 0.75
    assert i == pytest.approx((5 - vd) / 1e3, rel=1e-6)
    r = dc_operating_point(series("-5", "1k", "D", "1N4148"))
    assert -1e-8 < r.elements["D1"]["i"] < 0                 # ters: yalnız sızıntı


@pytest.mark.parametrize("model,lo,hi", [("LED", 1.8, 2.2), ("LED-GREEN", 2.1, 2.5), ("LED-BLUE", 2.8, 3.3)])
def test_led_forward_voltage(model, lo, hi):
    r = dc_operating_point(series("12", "680", "D", model))
    assert lo < r.voltages["D1"] < hi and 0.010 < r.elements["D1"]["i"] < 0.016


def test_zener_regulates():
    r = dc_operating_point(series("12", "1k", "D", "BZX5V1", rot=270))     # katot yukarıda
    assert r.voltages["D1"] == pytest.approx(5.15, abs=0.1)
    assert -r.elements["D1"]["i"] == pytest.approx((12 - r.voltages["D1"]) / 1e3, rel=1e-6)


def test_diode_iv_sweep_is_exponential():
    c = Circuit()
    c.add("V", 0, 0, rot=90, value="0")
    c.add("D", 0, 0, value="IS=1e-14 N=1")
    c.add_wire((3, 0), (3, 2))
    c.add_wire((0, 2), (3, 2))
    c.add("GND", 0, 2)
    w = dc_sweep(c, "V1", [0.5, 0.56])
    i1, i2 = w.elements["D1"]["i"]
    assert i2 / i1 == pytest.approx(math.exp(0.06 / 0.025852), rel=0.01)   # 60 mV ≈ 10 kat


# --- BJT ---------------------------------------------------------------------------------------

def test_bjt_active_region():
    r = dc_operating_point(common_emitter())
    q = r.elements["Q1"]
    ic, ib, ie = q["pins"]
    assert ic + ib + ie == pytest.approx(0, abs=1e-12)                     # KCL
    assert ib == pytest.approx((12 - 0.65) / 470e3, rel=0.02)
    vce = q["v"]
    assert ic / ib == pytest.approx(255.9 * (1 + (vce - 0.65) / 74.03), rel=0.01)   # β ve Early etkisi
    assert 1 < vce < 11


def test_bjt_saturation_and_pnp():
    q = dc_operating_point(common_emitter(rb="47k")).elements["Q1"]
    assert q["v"] < 0.2                                                     # doyum: Vce küçük
    q = dc_operating_point(common_emitter(model="2N3906", vcc="-12")).elements["Q1"]
    assert q["pins"][0] < 0 and q["pins"][1] < 0 and q["v"] < 0           # PNP: akımlar ters


def test_bjt_amplifier_ac_gain():
    c = Circuit()
    c.add("V", 0, 2, rot=90, value="12")
    c.add_wire((0, 2), (0, 0))
    c.add_wire((0, 0), (8, 0))
    c.add("R", 4, 0, rot=90, value="100k")
    c.add("R", 8, 0, rot=90, value="4k7")
    c.add("Q", 8, 4)
    c.add_wire((4, 2), (4, 4))
    c.add_wire((4, 4), (7, 4))
    c.add_wire((8, 2), (8, 3))
    c.add("R", 4, 4, rot=90, value="22k")
    c.add("R", 8, 5, rot=90, value="1k")
    c.add("C", 1, 4, value="10u")
    c.add("V", 1, 4, rot=90, value="AC 1")
    c.add_wire((0, 4), (0, 7))
    c.add_wire((0, 7), (8, 7))
    c.add_wire((4, 6), (4, 7))
    c.add_wire((1, 6), (1, 7))
    c.add("GND", 0, 7)
    ic = dc_operating_point(c).elements["Q1"]["pins"][0]
    w = run_analysis(c, ".ac dec 5 100 10k")
    k = min(range(len(w.x)), key=lambda i: abs(w.x[i] - 1e3))
    gain = w.voltages["I3"][k]
    assert abs(gain) == pytest.approx(4700 / (1000 + 0.025852 / ic), rel=0.02)
    assert abs(math.degrees(math.atan2(gain.imag, gain.real))) == pytest.approx(180, abs=1)


# --- MOSFET ------------------------------------------------------------------------------------

def fet_switch(vg, model="2N7000") -> Circuit:
    c = Circuit()
    c.add("V", 0, 0, rot=90, value="12")
    c.add("R", 0, 0, value="1k")
    c.add("M", 3, 2, value=model)                    # D=(3,1) G=(2,2) S=(3,3)
    c.add_wire((3, 0), (3, 1))
    c.add("V", 1, 2, rot=90, value=vg)
    c.add_wire((1, 2), (2, 2))
    c.add_wire((0, 2), (0, 5))
    c.add_wire((0, 5), (3, 5))
    c.add_wire((3, 3), (3, 5))
    c.add_wire((1, 4), (1, 5))
    c.add("GND", 0, 5)
    return c


def test_mosfet_regions():
    off = dc_operating_point(fet_switch("1")).elements["M1"]
    assert off["pins"][0] == pytest.approx(0, abs=1e-9) and off["v"] == pytest.approx(12, abs=1e-6)
    on = dc_operating_point(fet_switch("5")).elements["M1"]
    assert on["v"] < 0.05 and on["pins"][1] == 0                         # kapı akımı yok
    # doyum bölgesi: Id = KP/2·(Vgs − Vt)²·(1 + λVds)
    c = fet_switch("2.1")
    c.components[1].value = "100"                                        # küçük direnç: Vds büyük kalsın
    m = dc_operating_point(c).elements["M1"]
    assert m["pins"][0] == pytest.approx(0.16 * 0.1 ** 2 * (1 + 0.01 * m["v"]), rel=1e-3)


def test_pmos_and_power_mosfet():
    on = dc_operating_point(fet_switch("10", "IRFZ44N")).elements["M1"]
    assert on["v"] < 1e-3
    c = fet_switch("-5", "BS250")
    c.components[0].value = "-12"
    m = dc_operating_point(c).elements["M1"]
    assert m["pins"][0] < -0.01 and m["v"] > -0.5                        # P kanal iletimde


# --- op-amp ------------------------------------------------------------------------------------

@pytest.mark.parametrize("model,vin,expected", [
    ("ideal", "0.5", 5.5), ("LM358", "0.5", 5.5), ("TL072 ±12", "1", 11), ("TL072 ±12", "2", 12),
    ("ideal ±12", "-3", -12), ("ideal 0..5", "0.3", 3.3), ("LM358 0..5", "1", 5), ("LM358 0..5", "-1", 0),
])
def test_opamp_dc(model, vin, expected):
    assert dc_operating_point(noninverting(model, vin)).voltages["F3"] == pytest.approx(expected, abs=2e-3)


def test_opamp_bandwidth_and_clipping():
    w = run_analysis(noninverting("LM358", "AC 1"), ".ac dec 50 1k 10meg")
    g = [abs(v) for v in w.voltages["F3"]]
    f3 = next(f for f, x in zip(w.x, g) if x < g[0] / math.sqrt(2))
    assert f3 == pytest.approx(1e6 / 11, rel=0.1)                         # GBW / kazanç
    w = run_analysis(noninverting("TL072 ±12", "SINE(0 1.5 1k)"), ".tran 3m")
    out = w.voltages["F3"]
    assert max(out) == pytest.approx(12, abs=0.01) and min(out) == pytest.approx(-12, abs=0.01)
    assert abs(out[-1]) < 0.2                                             # doyumdan hızlı çıkar


# --- transient: doğrultucu -----------------------------------------------------------------------

def test_half_wave_rectifier():
    c = Circuit()
    c.add("V", 0, 0, rot=90, value="SINE(0 10 50)")
    c.add("D", 0, 0, value="1N4007")
    c.add("C", 3, 0, rot=90, value="100u")
    c.add("R", 3, 0, rot=90, value="1k")
    c.add_wire((0, 2), (3, 2))
    c.add("GND", 0, 2)
    w = run_analysis(c, ".tran 100m")
    late = w.voltages["D1"][len(w.x) // 2:]
    assert 9.1 < max(late) < 9.5                                          # tepe − diyot düşümü
    assert 1.0 < max(late) - min(late) < 2.0                              # dalgalanma ≈ I/(f·C)
    assert min(w.elements["D1"]["i"]) > -1e-6                             # ters yönde akım yok


# --- probe uçları, SPICE, çizim -----------------------------------------------------------------

def test_pin_current_probes():
    c = common_emitter()
    c.probes = ["I(Q1)", "I(Q1.B)", "I(Q1.E)", "I(Q1.X)", "P(Q1)"]
    r = dc_operating_point(c)
    vals = prb.read_all(c, r)
    q = r.elements["Q1"]
    assert vals[0].value == q["pins"][0] and vals[1].value == q["pins"][1] and vals[2].value == q["pins"][2]
    assert vals[3].error and vals[4].value == pytest.approx(q["v"] * q["pins"][0] + 0.65 * q["pins"][1], rel=0.05)
    assert prb.normalize("i(q1.b)") == "I(Q1.B)"
    for bad in ("V(Q1.B)", "I(Q1.B,C3)", "P(Q1.B)"):
        with pytest.raises(CircuitError):
            prb.normalize(bad)
    w = run_analysis(noninverting("LM358", "AC 1"), ".ac dec 2 10 100")
    c = noninverting("LM358", "AC 1")
    c.probes = ["P(R1)", "V(F3)"]
    trs = prb.traces(c, w)
    assert trs[0].error and trs[1].values is not None                    # AC'de güç yok


def test_three_pin_geometry():
    c = Circuit()
    q = c.add("Q", 5, 5)
    assert [addr(p) for p in q.pins()] == ["F5", "E6", "F7"]
    q.rot = 90
    assert [addr(p) for p in q.pins()] == ["G6", "F5", "E6"]
    u = c.add("U", 5, 5)
    assert [addr(p) for p in u.pins()] == ["H6", "E5", "E7"]
    u.rot = 180
    assert [addr(p) for p in u.pins()] == ["D6", "G5", "G7"]
    assert c.component_at((6, 4)) is u


def test_render_devices():
    c = common_emitter()
    c.add("D", 12, 1, rot=90, value="LED")
    lines = [ln.plain for ln in render(c, View(width=90, height=20))]
    text = "\n".join(lines)
    assert "[Q1 2N2222]" in text and "┤" in text and "↓" in text           # NPN oku dışarı
    assert "[▼D1 LED]" in text


def test_spice_export_devices():
    c = common_emitter()
    c.add("D", 12, 1, value="1N4148")
    c.add("U", 15, 3, value="TL072 ±15")
    text = c.to_spice("t")
    assert "Q1 I3 E3 0 Q1_2N2222" in text and ".model Q1_2N2222 NPN(" in text
    assert "D1 M2 P2 D1_1N4148" in text and ".model D1_1N4148 D(" in text
    assert "EU1 R4 0 O3 O5 200k" in text


def test_nonconvergence_is_reported():
    c = series("5", "1", "D", "1N4148")
    c.components[1].value = "1u"                                          # neredeyse kısa devre
    try:
        r = dc_operating_point(c)
        assert r.elements["D1"]["i"] > 0                                  # çözülürse de mantıklı olmalı
    except CircuitError:
        pass


# --- editör --------------------------------------------------------------------------------------

def test_editor_places_devices(tmp_path):
    common_emitter().save(tmp_path / "ce.json")

    async def scenario():
        app = tui.ElektroApp(tmp_path / "ce.json")
        async with app.run_test(size=(150, 46)) as pilot:
            await pilot.pause()
            ed = app.query_one("#editor")
            ed.cursor = (14, 2)
            await pilot.press("d")
            ed.cursor = (14, 7)
            await pilot.press("u")
            ed.cursor = (20, 7)
            await pilot.press("f")
            ed.cursor = (20, 2)
            await pilot.press("q", "ctrl+r")
            kinds = {c.ref: (c.kind, c.value, c.rot) for c in ed.circuit.components}
            assert kinds["D1"] == ("D", "1N4148", 90) and kinds["U1"][:2] == ("U", "ideal")
            assert kinds["M1"][:2] == ("M", "2N7000") and kinds["Q2"] == ("Q", "2N2222", 90)
            ed.cursor = (14, 7)
            await pilot.press("e")
            await pilot.pause()
            app.screen.query_one("#prompt-input").value = "NOPE"
            await pilot.press("enter")
            await pilot.pause()
            assert "NOPE" in str(app.screen.query_one("#prompt-error").render())
            app.screen.query_one("#prompt-input").value = "TL072 ±15"
            await pilot.press("enter")
            await pilot.pause()
            assert next(c for c in ed.circuit.components if c.ref == "U1").value == "TL072 ±15"
            ed.cursor = (8, 4)
            await pilot.press("p")                                        # transistör gövdesi → I(Q1)
            await pilot.pause()
            assert "I(Q1)" in ed.circuit.probes and ed.result is not None
    asyncio.run(scenario())
