"""Tüm komutların uçtan uca çalıştığını kontrol eder (ağ gerektirmez)."""

import pytest
from typer.testing import CliRunner

from elektro import __version__
from elektro.cli import app
from elektro.modules import datasheet

runner = CliRunner()


@pytest.mark.parametrize("args,expect", [
    ([], "ELEKTRO"),
    (["--version"], __version__),
    (["ohm", "-v", "12", "-r", "1k"], "12 mA"),
    (["resistor", "k", "s", "r", "a"], "1 kΩ"),
    (["resistor", "table"], "Brown"),
    (["resistor", "kahverengi", "siyah", "kırmızı", "altın"], "1 kΩ"),
    (["resistor", "braun", "schwarz", "rot", "gold"], "1 kΩ"),
    (["resistor", "коричневый", "чёрный", "красный", "золотой"], "1 kΩ"),
    (["resistor", "encode", "4k7"], "ye vt rd gd"),
    (["resistor", "smd", "103"], "10 kΩ"),
    (["series", "1k", "2k2"], "3.2 kΩ"),
    (["parallel", "1k", "1k"], "500 Ω"),
    (["divider", "--vin", "12", "--r1", "10k", "--r2", "10k"], "6 V"),
    (["divider", "--vin", "5", "--vout", "3.3"], "R1"),
    (["led", "--vs", "5"], "150 Ω"),
    (["eseries", "4k8"], "4.7 k"),
    (["cap", "104"], "100 nF"),
    (["filter", "rc", "--r", "1k", "--c", "100n"], "1.592 kHz"),
    (["filter", "rc", "--fc", "1k", "--c", "10n"], "15.92 kΩ"),
    (["filter", "rl", "--r", "1k", "--l", "10m"], "15.92 kHz"),
    (["filter", "lc", "--l", "10u", "--c", "100n"], "159.2 kHz"),
    (["filter", "rlc", "--r", "10", "--l", "1m", "--c", "100n"], "15.92 kHz"),
    (["filter", "notch", "--r", "1k", "--l", "1.013", "--c", "10u"], "50.01 Hz"),
    (["filter", "theory"], "Filter Theory"),
    (["rf", "fspl", "-f", "868", "-d", "5"], "105.20 dB"),
    (["rf", "link", "-f", "868", "-d", "10"], "Link margin"),
    (["rf", "wave", "-f", "433.92"], "172.7 mm"),
    (["rf", "convert", "14", "dbm", "w"], "25.12 mW"),
    (["logic", "convert", "255"], "0xFF"),
    (["logic", "truth", "xor"], "XOR"),
    (["logic", "expr", "A & ~B"], "Σm(2)"),
    (["555", "astable", "--r1", "1k", "--r2", "10k", "--c", "10u"], "6.87 Hz"),
    (["555", "mono", "--r", "100k", "--c", "10u"], "1.099 s"),
])
def test_command(args, expect):
    result = runner.invoke(app, args, env={"COLUMNS": "120"})
    assert result.exit_code == 0, result.output
    assert expect in result.output


@pytest.mark.parametrize("args", [
    ["ohm", "-v", "12", "-r", "0"],
    ["resistor", "x", "y", "z"],
    ["filter", "rc", "--r", "1k"],
    ["logic", "truth", "and", "-a", "5"],
    ["ohm", "-v", "abc", "-r", "1"],
])
def test_errors_are_clean(args):
    result = runner.invoke(app, args)
    assert result.exit_code != 0
    assert "Traceback" not in result.output


def test_find_pdf_link_in_lcsc_viewer():
    html = ('<a href="https://static.lcsc.com/viewer.html?file=https%3A%2F%2Fx.pdf">v</a>'
            '<script>u="https://datasheet.lcsc.com/datasheet/pdf/abc.pdf?productCode=C1"</script>')
    assert datasheet.find_pdf_link(html, "https://www.lcsc.com/datasheet/foo.pdf") == \
        "https://datasheet.lcsc.com/datasheet/pdf/abc.pdf?productCode=C1"


def test_ddg_unwrap():
    href = "//duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.ti.com%2Flit%2Fds%2Fsymlink%2Flm358.pdf&rut=x"
    assert datasheet._ddg_unwrap(href) == "https://www.ti.com/lit/ds/symlink/lm358.pdf"


def test_helpall_plain_when_not_tty():
    result = runner.invoke(app, ["helpall"], env={"MANPAGER": "sh -c 'col -bx | cat'"})
    assert result.exit_code == 0
    assert "elektro filter rc" in result.output
    assert "\x1b" not in result.output and "[92m" not in result.output
