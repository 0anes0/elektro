"""Kalıcı kullanıcı durumu: değişkenler (@vin) ve hesap geçmişi."""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from elektro.i18n import config_path, t

LOCAL_FILE = ".elektro.json"
HISTORY_LIMIT = 500
_VAR_RE = re.compile(r"@([A-Za-z_][A-Za-z0-9_]*)")
NAME_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# --- Değişkenler ----------------------------------------------------------------------

def local_file(start: Optional[Path] = None) -> Optional[Path]:
    """Bulunulan klasörden yukarı doğru ilk .elektro.json (git gibi)."""
    here = (start or Path.cwd()).resolve()
    for folder in (here, *here.parents):
        candidate = folder / LOCAL_FILE
        if candidate.is_file():
            return candidate
    return None


def load_vars() -> Tuple[Dict[str, str], Dict[str, str]]:
    """(genel, yerel) değişkenler."""
    global_vars = _read_json(config_path()).get("vars") or {}
    local = local_file()
    local_vars = (_read_json(local).get("vars") or {}) if local else {}
    return dict(global_vars), dict(local_vars)


def all_vars() -> Dict[str, str]:
    global_vars, local_vars = load_vars()
    return {**global_vars, **local_vars}


def set_var(name: str, value: str, local: bool = False) -> Path:
    if not NAME_RE.fullmatch(name):
        raise ValueError(t("vars.bad_name", name=name))
    path = (local_file() or Path.cwd() / LOCAL_FILE) if local else config_path()
    data = _read_json(path)
    data.setdefault("vars", {})[name] = value
    _write_json(path, data)
    return path


def unset_var(name: str) -> bool:
    removed = False
    for path in filter(None, (local_file(), config_path())):
        data = _read_json(path)
        if name in (data.get("vars") or {}):
            del data["vars"][name]
            _write_json(path, data)
            removed = True
    return removed


def expand_vars(args: List[str]) -> List[str]:
    """Argümanlardaki @isim ifadelerini değerleriyle değiştirir."""
    if not any("@" in a for a in args):
        return args
    values = all_vars()

    def sub(m):
        name = m.group(1)
        if name not in values:
            raise KeyError(name)
        return str(values[name])

    return [_VAR_RE.sub(sub, a) for a in args]


# --- Geçmiş --------------------------------------------------------------------------------

def state_dir() -> Path:
    base = os.environ.get("XDG_STATE_HOME") or os.path.join(os.path.expanduser("~"), ".local", "state")
    return Path(base) / "elektro"


def history_file() -> Path:
    return state_dir() / "history.jsonl"


def read_history() -> List[dict]:
    try:
        lines = history_file().read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    out = []
    for line in lines:
        try:
            entry = json.loads(line)
            if isinstance(entry.get("args"), list):
                out.append(entry)
        except ValueError:
            continue
    return out


def add_history(args: List[str]) -> None:
    try:
        entries = read_history()
        entries.append({"time": time.time(), "args": args})
        entries = entries[-HISTORY_LIMIT:]
        path = history_file()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in entries), encoding="utf-8")
    except OSError:
        pass        # geçmiş yazılamazsa komut yine de başarılıdır


def clear_history() -> None:
    try:
        history_file().unlink()
    except OSError:
        pass
