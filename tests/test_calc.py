import math

import pytest

from elektro.modules import digital, filters, ohm, passive, resistor, rf, timer555
from elektro.units import format_si, nearest_standard, parse_value, series_neighbors


@pytest.mark.parametrize("text,expected", [
    ("1k", 1e3), ("4k7", 4.7e3), ("100n", 100e-9), ("2.2uF", 2.2e-6), ("1kΩ", 1e3),
    ("10MHz", 10e6), ("1e-3", 1e-3), ("1R5", 1.5), ("1meg", 1e6), ("0,5", 0.5),
    ("1M", 1e6), ("1m", 1e-3), (".5k", 500), ("47", 47), ("10µ", 10e-6),
])
def test_parse_value(text, expected):
    assert parse_value(text) == pytest.approx(expected)


@pytest.mark.parametrize("bad", ["", "abc", "1x", "4.2k7", "k"])
def test_parse_value_rejects(bad):
    with pytest.raises(ValueError):
        parse_value(bad)


def test_format_si():
    assert format_si(1591.549, "Hz") == "1.592 kHz"
    assert format_si(999.96e3, "Hz") == "1 MHz"
    assert format_si(0, "V") == "0 V"
    assert format_si(4.7e-9, "F") == "4.7 nF"


def test_eseries():
    assert series_neighbors(4800, "E24") == (4700, 5100)
    assert nearest_standard(4800, "E12") == 4700
    assert nearest_standard(1e3, "E96") == 1e3


def test_ohm_solve():
    r = ohm.solve(v=12, r=1000)
    assert r["i"] == pytest.approx(0.012) and r["p"] == pytest.approx(0.144)
    r = ohm.solve(p=0.5, r=50)
    assert r["v"] == pytest.approx(5) and r["i"] == pytest.approx(0.1)
    with pytest.raises(ValueError):
        ohm.solve(v=12, r=0)
    with pytest.raises(ValueError):
        ohm.solve(v=12)
    assert ohm.solve(v=12, i=0.012, r=500).get("_conflicts") == ["r"]


def test_resistor_decode():
    assert resistor.decode_bands(["k", "s", "r", "a"])["value"] == 1000
    res = resistor.decode_bands(["sari", "mor", "siyah", "kahverengi", "kahverengi"])
    assert res["value"] == 4700 and res["tolerance"] == 1
    assert resistor.decode_bands(["k", "s", "s", "r", "k"])["value"] == 10e3     # 5 bant: 100 × 100
    assert resistor.decode_bands(["red", "red", "gold"])["tolerance"] == 20      # 3 bant
    assert resistor.decode_bands(["k", "s", "s", "k", "k", "r"])["tempco"] == 50
    with pytest.raises(ValueError):
        resistor.decode_bands(["s", "s", "s", "s"])          # siyah tolerans olamaz
    with pytest.raises(ValueError):
        resistor.decode_bands(["a", "s", "r", "a"])          # altın rakam olamaz


@pytest.mark.parametrize("value", [4.7, 10, 220, 4700, 1e6, 0.47, 12.4e3])
def test_resistor_encode_roundtrip(value):
    for bands in (4, 5):
        colors = resistor.encode_value(value, bands, 5 if bands == 4 else 1)
        decoded = resistor.decode_bands([c.key for c in colors])["value"]
        # 4 bant 2 anlamlı hane taşır (12.4k -> 12k), 5 bant 3 hane
        assert decoded == pytest.approx(value, rel=0.05 if bands == 4 else 1e-9)


@pytest.mark.parametrize("code,value", [
    ("103", 10e3), ("4R7", 4.7), ("R47", 0.47), ("1002", 10e3), ("01C", 10e3), ("68X", 49.9),
])
def test_smd(code, value):
    assert resistor.decode_smd(code) == pytest.approx(value)


def test_series_parallel():
    assert passive.series_sum([1e3, 2.2e3]) == pytest.approx(3.2e3)
    assert passive.parallel_sum([1e3, 1e3]) == pytest.approx(500)
    assert passive.parallel_sum([0, 1e3]) == 0


def test_divider_design():
    best = passive.best_divider(5, 3.3, "E24")
    assert best and best[0]["error"] < 0.002
    b = best[0]
    assert 5 * b["r2"] / (b["r1"] + b["r2"]) == pytest.approx(b["vout"])


def test_led():
    assert passive.led_resistor(5, 2, 0.02) == pytest.approx(150)
    with pytest.raises(ValueError):
        passive.led_resistor(5, 2, 0.02, count=3)


def test_cap_code():
    assert passive.decode_cap("104")[0] == pytest.approx(100e-9)
    assert passive.decode_cap("472K") == (pytest.approx(4.7e-9), "±%10")
    assert passive.encode_cap(parse_value("100n")) == "104"
    assert passive.encode_cap(parse_value("22p")) == "220"


def test_rf():
    assert rf.fspl_db(868e6, 5e3) == pytest.approx(105.2, abs=0.05)
    assert rf.max_distance(868e6, rf.fspl_db(868e6, 5e3)) == pytest.approx(5e3)
    assert rf.parse_freq("868") == 868e6 and rf.parse_freq("2.4G") == 2.4e9
    assert rf.parse_distance("5") == 5e3 and rf.parse_distance("800m") == 800
    assert rf.convert_units(14, "dbm", "w")["w"] == pytest.approx(0.02512, rel=1e-3)
    assert rf.convert_units(1.5, "vswr", "rl")["rl"] == pytest.approx(13.98, abs=0.01)


def test_digital():
    assert digital.parse_int("0xFF") == 255
    assert digital.parse_int("1010", 2) == 10
    assert digital.parse_int("1Fh") == 31
    assert digital.to_base(255, 16) == "FF"
    names, code = digital.parse_expr("A & B | ~C")
    assert names == ["A", "B", "C"]
    assert digital.evaluate(code, dict(A=0, B=0, C=0)) == 1
    assert digital.evaluate(code, dict(A=0, B=0, C=1)) == 0
    with pytest.raises(ValueError):
        digital.parse_expr("__import__('os')")


def test_555():
    t = timer555.astable_timing(1e3, 10e3, 10e-6)
    assert t["freq"] == pytest.approx(1.44 / (21e3 * 10e-6), rel=0.01)
    r1, r2 = timer555.astable_design(1e3, 0.6, 10e-9)
    t = timer555.astable_timing(r1, r2, 10e-9)
    assert t["freq"] == pytest.approx(1e3) and t["duty"] == pytest.approx(0.6)


def test_filter_db():
    assert filters.db(1 / math.sqrt(2)) == pytest.approx(-3.01, abs=0.01)
