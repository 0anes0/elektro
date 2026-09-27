"""Çok dilli metinler (en, tr, de, ru).

Dil şu sırayla belirlenir:
  1. Komut satırında --lang XX
  2. ELEKTRO_LANG ortam değişkeni
  3. `elektro language XX` ile kaydedilen ayar
  4. Sistem dili (LC_ALL / LC_MESSAGES / LANG)
  5. İngilizce

Yardım metinleri komutlar tanımlanırken üretildiği için dil, modül ilk
içe aktarıldığında belirlenir.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Optional

from elektro.i18n import de, en, ru, tr

LANGUAGES = {"en": "English", "tr": "Türkçe", "de": "Deutsch", "ru": "Русский"}
DEFAULT = "en"
_CATALOGS = {"en": en.MESSAGES, "tr": tr.MESSAGES, "de": de.MESSAGES, "ru": ru.MESSAGES}


def config_path() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    return Path(base) / "elektro" / "config.json"


def normalize(code: Optional[str]) -> Optional[str]:
    """'tr_TR.UTF-8', 'de-DE', 'RU' -> 'tr', 'de', 'ru'. Bilinmiyorsa None."""
    if not code:
        return None
    short = code.strip().lower().replace("-", "_").split(".")[0].split("_")[0]
    return short if short in LANGUAGES else None


def _from_argv(argv) -> Optional[str]:
    for i, arg in enumerate(argv):
        if arg == "--":
            break
        if arg == "--lang" and i + 1 < len(argv):
            return argv[i + 1]
        if arg.startswith("--lang="):
            return arg.split("=", 1)[1]
    return None


def saved_language() -> Optional[str]:
    try:
        return normalize(json.loads(config_path().read_text(encoding="utf-8")).get("lang"))
    except (OSError, ValueError, AttributeError):
        return None


def save_language(code: str) -> Path:
    path = config_path()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            data = {}
    except (OSError, ValueError):
        data = {}
    data["lang"] = code
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def system_language() -> Optional[str]:
    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        code = normalize(os.environ.get(var))
        if code:
            return code
        if os.environ.get(var):          # C, POSIX gibi değerler: daha düşük önceliğe geçme
            return None
    return None


def detect(argv=None) -> str:
    argv = sys.argv[1:] if argv is None else argv
    return (normalize(_from_argv(argv)) or normalize(os.environ.get("ELEKTRO_LANG"))
            or saved_language() or system_language() or DEFAULT)


_current = detect()


def get_language() -> str:
    return _current


def set_language(code: str) -> None:
    global _current
    lang = normalize(code)
    if lang is None:
        raise ValueError(code)
    _current = lang


def t(key: str, **kwargs) -> str:
    """Anahtarın geçerli dildeki karşılığı (yoksa İngilizcesi)."""
    msg = _CATALOGS[_current].get(key)
    if msg is None:
        msg = _CATALOGS[DEFAULT][key]
    return msg.format(**kwargs) if kwargs else msg


def pct(value: str) -> str:
    """Yüzde gösterimi: tr '%5', diğerleri '5%'."""
    return t("fmt.pct", v=value)


def upper(text: str) -> str:
    """Dile duyarlı büyük harf (Türkçede i -> İ)."""
    if _current == "tr":
        text = text.replace("i", "İ")
    return text.upper()


def catalogs() -> dict:
    return _CATALOGS
