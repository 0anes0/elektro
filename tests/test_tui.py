"""Terminal arayüzü: form → komut satırı, çalıştırma, arama, devre tuvali, geçmiş."""

import asyncio

import pytest
import typer

from elektro import cli, state, tui
from elektro.ui import set_json, set_report


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "cfg"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.chdir(tmp_path)
    yield
    set_json(False)
    set_report(None)


def _params(path):
    return {p.name: p for p in tui.form_params(tui.find_command(path))}


def test_command_groups_cover_visible_commands():
    names = {path[0] for _, items in tui.command_groups() for path, _ in items}
    root = typer.main.get_command(cli.app)
    visible = {n for n, c in root.commands.items() if not c.hidden and n not in tui.HIDDEN}
    assert names == visible
    assert "tui" not in names and "shell" not in names


def test_build_args():
    p = _params(("filter", "rc"))
    args = tui.build_args(("filter", "rc"), [(p["r"], "1k"), (p["c"], " 100n "), (p["fc"], ""), (p["high"], True)])
    assert args == ["filter", "rc", "--r", "1k", "--c", "100n", "--high"]
    p = _params(("opamp", "sum"))
    args = tui.build_args(("opamp", "sum"), [(p["rf"], "10k"), (p["rin"], "10k 20k"), (p["vin"], "1 0.5")])
    assert args == ["opamp", "sum", "--rf", "10k", "--rin", "10k", "--rin", "20k", "--vin", "1", "--vin", "0.5"]
    p = _params(("resistor", "decode"))
    assert tui.build_args(("resistor", "decode"), [(p["bands"], "bn bk rd gd")]) == \
        ["resistor", "decode", "bn", "bk", "rd", "gd"]


def test_run_captured():
    code, out = tui.run_captured(["ohm", "-v", "12", "-r", "1k"], 80)
    assert code == 0 and "12 mA" in out
    code, out = tui.run_captured(["ohm", "-v", "abc"], 80)
    assert code != 0
    code, out = tui.run_captured(["ohm"], 80)          # sihirbaz: girdi yok, takılmamalı
    assert code != 0


def _run(coro):
    return asyncio.run(coro)


def test_app_form_run_and_history():
    async def scenario():
        app = tui.ElektroApp()
        async with app.run_test(size=(140, 45)) as pilot:
            await pilot.pause()
            app.load_command(("ohm",))
            await pilot.pause()
            fields = dict((p.name, w) for p, w in app.fields)
            fields["v"].value = "12"
            fields["r"].value = "1k"
            await pilot.pause()
            assert app.query_one("#cmdline").value == "elektro ohm --voltage 12 --resistance 1k"
            await pilot.press("ctrl+r")
            await app.workers.wait_for_complete()
            await pilot.pause()
            text = "\n".join(line.text for line in app.query_one("#output").lines)
            assert "12 mA" in text and "144 mW" in text

            app.query_one("#cmdline").value = "elektro shell"
            app.action_run()
            await pilot.pause()
            text = "\n".join(line.text for line in app.query_one("#output").lines)
            assert "shell" in text.splitlines()[-1]

            await pilot.press("f4")
            await pilot.pause()
            table = app.query_one("#history-table")
            assert table.row_count == 1
            await pilot.press("enter")
            await pilot.pause()
            assert app.query_one("#cmdline").value == "elektro ohm --voltage 12 --resistance 1k"
    _run(scenario())
    assert state.read_history()[-1]["args"] == ["ohm", "--voltage", "12", "--resistance", "1k"]


def test_app_search_and_canvas():
    async def scenario():
        app = tui.ElektroApp()
        async with app.run_test(size=(120, 40)) as pilot:
            await pilot.pause()
            app.query_one("#search").value = "pinout"
            await pilot.pause()
            leaves = []

            def walk(node):
                for c in node.children:
                    if c.data:
                        leaves.append(c.data)
                    walk(c)
            walk(app.query_one("#commands").root)
            assert ("pinout",) in leaves and ("ohm",) not in leaves

            await pilot.press("f3")
            await pilot.press("v", "r", "right", "right", "right", "r", "ctrl+r")
            await pilot.press("left", "left", "left", "down", "down", "w", "right", "right", "right", "enter",
                              "escape", "left", "left", "left", "g", "f5")
            await pilot.pause()
            editor = app.query_one("#editor")
            assert editor.result is not None and editor.error is None
            assert editor.result.voltages["F3"] == pytest.approx(2.5, rel=1e-6)   # 1k / 1k bölücü, düğüm F3
            await pilot.press("ctrl+z")
            await pilot.pause()
            assert not any(c.kind == "GND" for c in editor.circuit.components)
    _run(scenario())
