"""0.4 ile gelen komutlar: bilinen referans değerlerle doğrulama."""

import json

import pytest
from typer.testing import CliRunner

from elektro.cli import app
from elektro.modules import analog, datasheet, embedded, power, rf, tools, wiring
from elektro.ui import set_json

runner = CliRunner()


@pytest.fixture(autouse=True)
def _reset_json():
    yield
    set_json(False)


# --- hesaplar ---------------------------------------------------------------------------

@pytest.mark.parametrize("name,expected", [
    ("CRC-8", 0xF4), ("CRC-8/MAXIM", 0xA1), ("CRC-16/MODBUS", 0x4B37),
    ("CRC-16/CCITT-FALSE", 0x29B1), ("CRC-16/XMODEM", 0x31C3), ("CRC-32", 0xCBF43926),
])
def test_crc_check_values(name, expected):
    algo = next(a for a in embedded.CRC_ALGOS if a.name == name)
    assert embedded.crc_compute(algo, b"123456789") == expected


def test_crc_modbus_frame():
    algo = next(a for a in embedded.CRC_ALGOS if a.name == "CRC-16/MODBUS")
    assert embedded.crc_compute(algo, embedded.parse_hex_bytes("01 03 00 00 00 0A")) == 0xCDC5
    with pytest.raises(ValueError):
        embedded.parse_hex_bytes("0G")


def test_uart_avr_datasheet_table():
    # ATmega328P datasheet: 16 MHz, 115200 → UBRR 8 (-3.5%), U2X UBRR 16 (+2.1%)
    s = embedded.uart_settings(16e6, 115200, "avr")
    assert s[0]["value"] == 8 and s[0]["error"] == pytest.approx(-0.0355, abs=1e-3)
    assert s[1]["value"] == 16 and s[1]["error"] == pytest.approx(0.0212, abs=1e-3)


def test_uart_stm32():
    s = embedded.uart_settings(72e6, 921600, "stm32")
    assert s[0]["value"] == "0x4E"


def test_pwm():
    s = embedded.pwm_settings(16e6, 20e3, "avr", 16)
    assert s["prescaler"] == 1 and s["top"] == 799
    s = embedded.pwm_settings(72e6, 50, "stm32", 16)
    assert s["actual"] == pytest.approx(50, rel=1e-3) and s["top"] <= 65535


def test_i2c_range():
    r_min, r_max = embedded.i2c_pullup_range(3.3, 200e-12, 400e3)
    assert r_min == pytest.approx(966.7, rel=1e-3) and r_max == pytest.approx(1770, rel=1e-2)


def test_lora_airtime_matches_semtech_calculator():
    assert rf.lora_airtime(9, 125e3, 1, 20)["airtime"] == pytest.approx(0.18534, rel=1e-3)
    assert rf.lora_airtime(12, 125e3, 1, 51)["ldro"] is True
    assert rf.parse_cr("4/8") == 4 and rf.parse_cr("5") == 1


def test_microstrip_50_ohm_fr4():
    w_h = rf.microstrip_width(50, 4.4)
    assert w_h * 1.6 == pytest.approx(3.05, abs=0.1)
    assert rf.microstrip_z0(w_h, 4.4)[0] == pytest.approx(50, abs=0.01)


def test_coax_lmr400_datasheet():
    # Times Microwave LMR-400: 900 MHz ≈ 3.9 dB/100 ft = 12.8 dB/100 m
    assert rf.find_coax("lmr-400").attenuation(900) == pytest.approx(12.8, rel=0.03)
    with pytest.raises(ValueError):
        rf.find_coax("rg999")


def test_awg_and_trace():
    assert wiring.awg_diameter(22) * 1e3 == pytest.approx(0.644, abs=0.001)
    assert wiring.area_to_awg(0.3255e-6) == pytest.approx(22, abs=0.01)
    # 1 A, 10 °C, dış katman, 1 oz → ~12 mil
    area = wiring.ipc2221_area_mil2(1, 10, False)
    assert area / (34.8e-6 / 25.4e-6) == pytest.approx(11.9, abs=0.3)
    assert wiring.parse_length("50cm") == pytest.approx(0.5)
    assert wiring.parse_length("10ft") == pytest.approx(3.048)


def test_regulator():
    reg = power.find_regulator("lm317")
    assert power.adjustable_vout(reg, 240, 720) == pytest.approx(5.036, abs=1e-3)
    assert power.find_regulator("7805").vout == 5
    assert power.find_regulator("AMS1117-3.3").vout == 3.3
    with pytest.raises(ValueError):
        power.find_regulator("xyz")


def test_battery_average():
    assert power.average_current(45e-3, 2, 20e-6, 58) == pytest.approx(1.519e-3, rel=1e-3)


@pytest.mark.parametrize("expr,value", [
    ("12V / (4k7 + 1k)", 12 / 5700), ("2^10", 1024), ("par(1k, 1k)", 500),
    ("db(10)", 20), ("sqrt(4) * pi", 2 * 3.141592653589793), ("-3 + 1u", -3 + 1e-6),
])
def test_calc(expr, value):
    assert tools.evaluate(expr) == pytest.approx(value)


@pytest.mark.parametrize("bad", ["__import__('os')", "open('x')", "a + 1", "(1"])
def test_calc_rejects(bad):
    with pytest.raises(ValueError):
        tools.evaluate(bad)


def test_unit_convert():
    assert tools.convert_unit(25, "c", "f")["°F"] == pytest.approx(77)
    assert tools.convert_unit(10, "mil", "mm")["mm"] == pytest.approx(0.254)
    assert tools.convert_unit(20, "db", None)["voltage ratio"] == pytest.approx(10)
    with pytest.raises(ValueError):
        tools.convert_unit(-300, "c", None)


# --- komut satırı -------------------------------------------------------------------------

@pytest.mark.parametrize("args,expect", [
    (["regulator", "lm317", "--vout", "5"], "R2 (E96)"),
    (["regulator", "7805", "--vin", "12", "-i", "500m"], "3.5 W"),
    (["battery", "2000", "-i", "15m"], "4.4 days"),
    (["thermal", "-p", "5", "--rth-jc", "3", "--ta", "50"], "16.50"),
    (["wire", "--awg", "22", "-l", "3", "-i", "2"], "0.644 mm"),
    (["trace", "-i", "1"], "0.302 mm"),
    (["switch", "bjt", "--ic", "500m", "-v", "3.3"], "150 Ω"),
    (["switch", "mosfet", "-v", "10", "--qg", "40n", "-f", "100k"], "40 ns"),
    (["charge", "--r", "10k", "--c", "100u", "--v", "5", "--to", "3.3"], "1.079 s"),
    (["rf", "microstrip", "--z0", "50"], "3.083 mm"),
    (["rf", "lora", "--sf", "9", "-p", "20"], "185.3 ms"),
    (["rf", "fresnel", "-f", "868", "-d", "10"], "29.38 m"),
    (["rf", "coax", "lmr400", "-f", "900", "-l", "100"], "dB"),
    (["uart", "-c", "16M"], "115200"),
    (["pwm", "-c", "72M", "-f", "20k", "-m", "stm32", "-d", "25"], "900"),
    (["adc", "-b", "12", "--vref", "3.3", "--code", "2048"], "1.65 V"),
    (["i2c", "--cb", "200p"], "1.2 kΩ"),
    (["crc", "123456789", "--text", "-a", "crc-32"], "0xCBF43926"),
    (["calc", "par(1k, 2k2, 4k7)", "-u", "Ω"], "599.768 Ω"),
    (["unit", "25", "c"], "298.15"),
])
def test_new_commands(args, expect):
    result = runner.invoke(app, args, env={"COLUMNS": "120"})
    assert result.exit_code == 0, result.output
    assert expect in result.output


@pytest.mark.parametrize("args,key", [
    (["--json", "ohm", "-v", "12", "-r", "1k"], "current_a"),
    (["--json", "rf", "lora", "--sf", "9"], "airtime_s"),
    (["--json", "eseries", "4k8"], None),
    (["--json", "filter", "rc", "--r", "1k", "--c", "100n"], "response"),
    (["--json", "logic", "expr", "A & B"], "minterms"),
    (["--json", "calc", "1k*2"], "result"),
])
def test_json_output_is_valid(args, key):
    result = runner.invoke(app, args)
    assert result.exit_code == 0, result.output
    data = json.loads(result.output)
    if key:
        assert key in data


def test_json_flag_anywhere(monkeypatch, capsys):
    from elektro import cli
    monkeypatch.setattr("sys.argv", ["elektro", "ohm", "-v", "5", "-r", "1k", "--json"])
    with pytest.raises(SystemExit) as exc:
        cli.run()
    assert exc.value.code == 0
    assert json.loads(capsys.readouterr().out)["current_a"] == pytest.approx(0.005)


def test_datasheet_cache(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    monkeypatch.chdir(tmp_path)
    datasheet.cache_dir().mkdir(parents=True)
    (datasheet.cache_dir() / "lm358.pdf").write_bytes(b"%PDF-1.4 test")
    result = runner.invoke(app, ["datasheet", "LM358"])      # ağa çıkmadan önbellekten gelmeli
    assert result.exit_code == 0, result.output
    assert (tmp_path / "lm358_datasheet.pdf").read_bytes() == b"%PDF-1.4 test"
    result = runner.invoke(app, ["datasheet", "--history"], env={"COLUMNS": "120"})
    assert "lm358" in result.output


def test_manpage():
    result = runner.invoke(app, ["manpage"])
    assert result.exit_code == 0
    assert result.output.startswith(".TH ELEKTRO 1")
    assert ".SS elektro rf lora" in result.output
