"""0.5: op-amp, sadeleştirme, geçmiş, REPL, doğrultucu, bobin, kristal, AC güç, grafik, değişkenler."""

import json
import math

import pytest
from typer.testing import CliRunner

from elektro import cli, plot, state
from elektro.modules import digital, opamp, passive, power, tools
from elektro.ui import set_json

runner = CliRunner()


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "cfg"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.chdir(tmp_path)
    yield
    set_json(False)


# --- op-amp ---------------------------------------------------------------------------

def test_best_ratio_pairs():
    pairs = opamp.best_ratio_pairs(10, "E24")
    assert pairs[0]["error"] == 0 and pairs[0]["ratio"] == pytest.approx(10)
    pairs = opamp.best_ratio_pairs(3.3, "E12")
    assert pairs[0]["error"] < 0.02


@pytest.mark.parametrize("args,expect", [
    (["opamp", "noninv", "--gain", "11"], "11"),
    (["opamp", "noninv", "--rf", "100k", "--rg", "10k", "--gbw", "1M"], "90.91 kHz"),
    (["opamp", "inv", "--rf", "47k", "--rin", "4k7", "--vin", "0.5"], "-5 V"),
    (["opamp", "diff", "--gain", "5"], "R2 = R4"),
    (["opamp", "sum", "--rf", "10k", "--rin", "10k", "--vin", "1", "--rin", "20k", "--vin", "0.5"], "-1.25 V"),
])
def test_opamp_cli(args, expect):
    r = runner.invoke(cli.app, args, env={"COLUMNS": "120"})
    assert r.exit_code == 0, r.output
    assert expect in r.output


# --- sadeleştirme -------------------------------------------------------------------------

def _truth(terms, n):
    return {m for m in range(2 ** n) if any(digital._covers(p, m, n) for p in terms)}


@pytest.mark.parametrize("ones,dcs,n,expected_terms", [
    ([2, 3], [], 2, 1),                       # A
    ([0, 1, 2, 5, 6, 7], [], 3, 3),           # döngüsel örtü
    ([1, 3, 7, 11, 15], [0, 2, 5], 4, 2),     # A'D + CD
    (list(range(8)), [], 3, 1),               # 1
    ([0, 2, 8, 10], [], 4, 1),                # B'D'
])
def test_minimal_cover(ones, dcs, n, expected_terms):
    cover = digital.minimal_cover(ones, dcs, n)
    assert len(cover) == expected_terms
    got = _truth(cover, n)
    assert set(ones) <= got <= set(ones) | set(dcs)


def test_simplify_random_functions_are_equivalent():
    import random
    rnd = random.Random(1)
    for _ in range(40):
        n = rnd.randint(2, 5)
        ones = sorted(rnd.sample(range(2 ** n), rnd.randint(1, 2 ** n - 1)))
        cover = digital.minimal_cover(ones, [], n)
        assert _truth(cover, n) == set(ones)


def test_simplify_cli_and_expr_roundtrip():
    r = runner.invoke(cli.app, ["--json", "logic", "simplify", "A&B | A&~B"])
    data = json.loads(r.output)
    assert data["sop"] == "A"
    names, code = digital.parse_expr(data["sop"] if data["sop"] not in ("0", "1") else "A")
    r = runner.invoke(cli.app, ["logic", "simplify", "-m", "1,3,7,11,15", "-d", "0,2,5"], env={"COLUMNS": "120"})
    assert "A'D + CD" in r.output and "K-map" in r.output


# --- güç -------------------------------------------------------------------------------------

def test_rectifier():
    r = power.rectifier_calc(12, "bridge", 50, 0.7, 1, 1, None)
    assert r["vpeak"] == pytest.approx(12 * math.sqrt(2) - 1.4)
    assert r["c"] == pytest.approx(0.01)          # 1 A / (2·50 Hz·1 V)
    r = power.rectifier_calc(12, "half", 50, 0.7, 0.1, None, 1e-3)
    assert r["ripple"] == pytest.approx(2.0)


def test_acpower_and_correction():
    r = power.ac_power(400, 26.4, 0.82, 3)
    assert r["p"] == pytest.approx(15000, rel=1e-3)
    cc = power.correction_capacitor(15000, 0.82, 0.95, 400, 50, 3)
    assert cc["qc"] == pytest.approx(5540, rel=0.01)
    assert cc["c"] == pytest.approx(36.7e-6, rel=0.01)


def test_star_delta_roundtrip():
    y = power.star_delta("delta", 10, 20, 30)
    assert power.star_delta("star", *y) == pytest.approx((10, 20, 30))


def test_coil_and_crystal():
    n = passive.coil_turns(1e-6, 10e-3, 0.5e-3)
    assert 8 < n < 11
    assert passive.wheeler_l(n, 10.5e-3, n * 0.5e-3) == pytest.approx(1e-6, rel=1e-3)
    r = runner.invoke(cli.app, ["crystal", "--cl", "12p"], env={"COLUMNS": "120"})
    assert "14 pF" in r.output and "15 pF" in r.output


@pytest.mark.parametrize("args,expect", [
    (["rectifier", "--vac", "12", "-i", "1", "--ripple", "1"], "10 mF"),
    (["acpower", "--v", "400", "--p", "15k", "--pf", "0.82", "--phases", "3", "--target-pf", "0.95"], "36.74 µF"),
    (["stardelta", "delta", "10", "20", "30"], "3.333 Ω"),
    (["coil", "--n", "12", "--d", "8", "--length", "15"], "544 nH"),
])
def test_power_cli(args, expect):
    r = runner.invoke(cli.app, args, env={"COLUMNS": "120"})
    assert r.exit_code == 0, r.output
    assert expect in r.output


# --- grafik ------------------------------------------------------------------------------------

def test_svg_plots(tmp_path):
    for args in (["filter", "rc", "--r", "1k", "--c", "100n"], ["filter", "notch", "--r", "1k", "--l", "1", "--c", "10u"],
                 ["charge", "--r", "10k", "--c", "100u", "--v", "5"]):
        out = tmp_path / f"{args[1]}.svg"
        r = runner.invoke(cli.app, args + ["--plot", str(out)])
        assert r.exit_code == 0, r.output
        text = out.read_text()
        assert text.startswith("<svg") and "<polyline" in text and text.rstrip().endswith("</svg>")


def test_plot_path_validation():
    with pytest.raises(ValueError):
        plot.plot_path("x.txt")
    assert plot.plot_path("a.svg").suffix == ".svg"
    r = runner.invoke(cli.app, ["filter", "rc", "--r", "1k", "--c", "1u", "--plot", "a.bmp"])
    assert r.exit_code != 0 and ".svg" in r.output


# --- değişkenler / geçmiş ----------------------------------------------------------------------

def test_variables(tmp_path):
    state.set_var("vin", "12")
    state.set_var("r", "4k7", local=True)
    assert (tmp_path / ".elektro.json").exists()
    assert state.expand_vars(["-v", "@vin", "--r=@r"]) == ["-v", "12", "--r=4k7"]
    with pytest.raises(KeyError):
        state.expand_vars(["@yok"])
    with pytest.raises(ValueError):
        state.set_var("1bad", "3")
    assert tools.evaluate("vin / 2") == 6
    state.set_var("vin", "5", local=True)          # yerel, geneli ezer
    assert state.all_vars()["vin"] == "5"
    assert state.unset_var("vin") and "vin" not in state.all_vars()


def test_execute_records_history(capsys):
    state.set_var("vin", "12")
    assert cli.execute(["ohm", "-v", "@vin", "-r", "1k"]) == 0
    assert cli.execute(["--lang", "en", "cap", "104"]) == 0
    assert cli.execute(["vars"]) == 0                       # yönetim komutu: kaydedilmez
    assert cli.execute(["ohm", "-v", "1x", "-r", "1k"]) != 0  # hatalı: kaydedilmez
    assert cli.execute(["ohm", "-v", "@yok"]) == 1
    hist = [e["args"] for e in state.read_history()]
    assert hist == [["ohm", "-v", "@vin", "-r", "1k"], ["cap", "104"]]
    capsys.readouterr()
    assert cli.execute(["history", "--run", "2"]) == 0
    assert "104" in capsys.readouterr().out


def test_shell(monkeypatch, capsys):
    lines = iter(["ohm -v 5 -r 1k", "elektro cap 104", 'logic simplify "A&B | A&~B"', "bogus-cmd", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(lines))
    assert cli.execute(["shell"]) == 0
    out = capsys.readouterr()
    assert "5 mA" in out.out and "100 nF" in out.out
    assert [e["args"][0] for e in state.read_history()] == ["ohm", "cap", "logic"]
