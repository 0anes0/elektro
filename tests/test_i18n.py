import string
import subprocess
import sys

import pytest

from elektro import i18n


def _placeholders(text):
    return sorted({f for _, f, _, _ in string.Formatter().parse(text) if f is not None})


@pytest.mark.parametrize("lang", ["tr", "de", "ru"])
def test_catalog_complete(lang):
    en, other = i18n.catalogs()["en"], i18n.catalogs()[lang]
    assert set(other) == set(en)
    for key in en:
        assert _placeholders(other[key]) == _placeholders(en[key]), key


@pytest.mark.parametrize("value,expected", [
    ("tr_TR.UTF-8", "tr"), ("de-DE", "de"), ("RU", "ru"), ("en_US", "en"), ("fr_FR", None), ("", None),
])
def test_normalize(value, expected):
    assert i18n.normalize(value) == expected


def test_detect_priority(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.delenv("ELEKTRO_LANG", raising=False)
    monkeypatch.setenv("LANG", "de_DE.UTF-8")
    monkeypatch.delenv("LC_ALL", raising=False)
    monkeypatch.delenv("LC_MESSAGES", raising=False)
    assert i18n.detect([]) == "de"                       # sistem dili
    i18n.save_language("ru")
    assert i18n.detect([]) == "ru"                       # kayıtlı ayar
    monkeypatch.setenv("ELEKTRO_LANG", "tr")
    assert i18n.detect([]) == "tr"                       # ortam değişkeni
    assert i18n.detect(["--lang", "en", "ohm"]) == "en"  # komut satırı
    assert i18n.detect(["--lang=de"]) == "de"
    assert i18n.detect(["logic", "--", "--lang", "de"]) == "tr"


@pytest.mark.parametrize("lang,expect", [
    ("en", "Resistor"), ("tr", "Direnç"), ("de", "Widerstand"), ("ru", "Резистор"),
])
def test_cli_language(lang, expect):
    out = subprocess.run([sys.executable, "-m", "elektro", "--lang", lang, "resistor", "bn", "bk", "rd", "gd"],
                         capture_output=True, text=True, env={"PATH": "", "COLUMNS": "100"})
    assert out.returncode == 0, out.stderr
    assert expect in out.stdout


@pytest.mark.parametrize("lang", ["en", "tr", "de", "ru"])
def test_every_help_page_renders(lang):
    """Her komutun yardımı her dilde hatasız açılmalı."""
    out = subprocess.run([sys.executable, "-m", "elektro", "--lang", lang, "helpall"],
                         capture_output=True, text=True, env={"PATH": "", "COLUMNS": "100"})
    assert out.returncode == 0, out.stderr
    assert "elektro filter notch" in out.stdout and "Traceback" not in out.stderr
