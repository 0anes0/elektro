"""Devre dosyasını terminalden çözer: elektro sim devre.json"""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import List, Optional

import typer
from rich.table import Table

from elektro.circuit import probes as prb
from elektro.circuit.model import Circuit, CircuitError
from elektro.circuit.plot import series_from
from elektro.circuit.solver import dc_operating_point, run_analysis
from elektro.i18n import t
from elektro.plot import PlotError, multi, plot_path
from elektro.ui import cli_parser, console, emit, err_console, fail, json_mode, plot_saved, print_json, theory, warn
from elektro.units import format_si


def sim(
    file: Path = typer.Argument(..., exists=True, dir_okay=False, help=t("sim.arg")),
    analysis: Optional[str] = typer.Option(None, "--analysis", "-a", help=t("sim.opt.analysis")),
    probe: Optional[List[str]] = typer.Option(None, "--probe", "-p", help=t("sim.opt.probe")),
    plot: Optional[Path] = typer.Option(None, "--plot", parser=cli_parser(plot_path), metavar=t("plot.metavar"),
                                        help=t("plot.opt")),
    csv_path: Optional[Path] = typer.Option(None, "--csv", metavar=t("plot.metavar"), help=t("sim.opt.csv")),
    spice: bool = typer.Option(False, "--spice", help=t("sim.opt.spice")),
):
    try:
        circuit = Circuit.load(file)
        for note in circuit.notes:
            warn(note)
        if analysis is not None:
            circuit.analysis = "" if analysis.strip().lower() in ("", ".op", "op") else analysis.strip()
        if spice:
            sys.stdout.write(circuit.to_spice(file.stem))
            return
        extra = [prb.normalize(x) for x in probe or []]
        has_source = any(c.kind in ("V", "I") for c in circuit.components)
        result = dc_operating_point(circuit) if has_source else None
        sweep = run_analysis(circuit, circuit.analysis) if has_source and circuit.analysis else None
    except CircuitError as e:
        fail(str(e))
    readings = prb.read_all(circuit, result, extra)
    if sweep is not None:
        _print_sweep(file, circuit, sweep, extra, plot, csv_path)
        return
    if result is None:
        _print_probes(readings, {"file": str(file), "analysis": "req"})
        return
    for w in result.warnings:
        warn(w)
    nodes = Table(title=t("sim.nodes"), box=None, header_style="bold", title_justify="left", min_width=24)
    nodes.add_column(t("ckt.node"), style="magenta")
    nodes.add_column("V", justify="right", style="bold green")
    for name, v in sorted(result.voltages.items()):
        if name != "0":
            nodes.add_row(name, format_si(v, "V"))
    parts = Table(title=t("sim.elements"), box=None, header_style="bold", title_justify="left")
    for col in ("", t("ckt.nodes"), "V", "I", "P"):
        parts.add_column(col, justify="left" if col in ("", t("ckt.nodes")) else "right")
    for ref, e in result.elements.items():
        pins = " – ".join("GND" if n == "0" else n for n in e["nodes"])
        parts.add_row(ref, pins, format_si(e["v"], "V"), format_si(e["i"], "A"), format_si(e["p"], "W"))
    data = {"file": str(file), "analysis": "op", "voltages": result.voltages, "elements": result.elements,
            "probes": [{"expr": r.expr, "value": r.value, "unit": r.unit, "error": r.error} for r in readings],
            "warnings": result.warnings}
    emit(nodes, data)
    if not json_mode():
        console.print()
        console.print(parts)
        if readings:
            console.print()
            console.print(_probe_table(readings))
    theory(t("sim.note"))


def _print_sweep(file: Path, circuit: Circuit, sweep, extra: List[str], plot: Optional[Path],
                 csv_path: Optional[Path]) -> None:
    exprs = prb.trace_exprs(circuit, sweep) + [e for e in extra if prb.needs_result(e)]
    traces = prb.traces(circuit, sweep, exprs)
    ac = sweep.kind == "ac"
    for w in sweep.warnings:
        warn(w)
    for tr in traces:
        if tr.error:
            warn(f"{tr.expr}: {tr.error}")
    good = [tr for tr in traces if tr.values is not None]
    if json_mode():
        print_json({"file": str(file), "analysis": sweep.label, "x": sweep.x, "x_unit": sweep.x_unit,
                    "traces": [{"expr": tr.expr, "unit": tr.unit,
                                **({"mag": [abs(v) for v in tr.values],
                                    "phase_deg": [math.degrees(math.atan2(v.imag, v.real)) for v in tr.values]}
                                   if ac else {"values": tr.values})} for tr in good]})
    else:
        title = f"{sweep.label}  ({len(sweep.x)} {t('sim.points')})"
        tbl = Table(title=title, box=None, header_style="bold", title_justify="left", min_width=len(title) + 2)
        tbl.add_column("", style="magenta")
        cols = ([t("sim.max_db"), t("sim.at"), t("sim.last")] if ac else ["min", "max", t("sim.last")])
        for col in cols:
            tbl.add_column(col, justify="right")
        for tr in good:
            if ac:
                db = [20 * math.log10(abs(v)) if abs(v) > 1e-30 else -600 for v in tr.values]
                k = max(range(len(db)), key=lambda i: db[i])
                tbl.add_row(tr.expr, _db(db[k]), format_si(sweep.x[k], "Hz"), _db(db[-1]))
            else:
                scale = max((abs(v) for v in tr.values), default=0.0)
                tbl.add_row(*[tr.expr] + [format_si(_snap(v, scale), tr.unit)
                                          for v in (min(tr.values), max(tr.values), tr.values[-1])])
        console.print(tbl)
    if plot is not None and good:
        series = series_from(good, "mag")
        y_label = series[0].unit if len({s.unit for s in series}) == 1 else ""
        try:
            out = multi(plot, f"{file.stem}  {sweep.label}", sweep.x, [(s.label, s.ys) for s in series],
                        t("plot.freq") if ac else (t("plot.time") if sweep.kind == "tran" else t("sim.sweep_x")),
                        sweep.x_unit, y_label, log_x=ac)
        except (PlotError, OSError) as e:
            fail(str(e))
        plot_saved(out)
    if csv_path is not None and good:
        try:
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                head = [sweep.x_unit or "x"]
                for tr in good:
                    head += [f"{tr.expr} |{tr.unit}|", f"{tr.expr} phase(deg)"] if ac else [f"{tr.expr} ({tr.unit})"]
                writer.writerow(head)
                for k, x in enumerate(sweep.x):
                    row = [f"{x:.9g}"]
                    for tr in good:
                        v = tr.values[k]
                        row += ([f"{abs(v):.9g}", f"{math.degrees(math.atan2(v.imag, v.real)):.6g}"] if ac
                                else [f"{v:.9g}"])
                    writer.writerow(row)
        except OSError as e:
            fail(str(e))
        (err_console if json_mode() else console).print(f"[green]✓[/] {t('sim.csv_saved', path=csv_path)}")


def _snap(value: float, scale: float) -> float:
    """Sayısal artıkları sıfırla: 1 V'luk bir eğride 1e-15 V → 0."""
    return 0.0 if abs(value) < scale * 1e-9 else value


def _db(value: float) -> str:
    return f"{value:.2f} dB".replace("-0.00", "0.00")


def _probe_table(readings) -> Table:
    tbl = Table(title=t("ckt.probes"), box=None, header_style="bold", title_justify="left")
    tbl.add_column("", style="magenta")
    tbl.add_column("", justify="right", style="bold green")
    for r in readings:
        tbl.add_row(r.expr, f"[red]{r.error}[/]" if r.error else format_si(r.value, r.unit))
    return tbl


def _print_probes(readings, data: dict) -> None:
    """Kaynaksız (yalnızca dirençli) devre: sadece probe'lar."""
    if not readings:
        fail(t("sim.need_req"))
    data["probes"] = [{"expr": r.expr, "value": r.value, "unit": r.unit, "error": r.error} for r in readings]
    emit(_probe_table(readings), data)


def examples_cmd(
    name: Optional[str] = typer.Argument(None, help=t("ex.arg")),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help=t("ex.opt.output")),
):
    from elektro.circuit import examples
    if name is None:
        tbl = Table(box=None, header_style="bold")
        tbl.add_column("", style="cyan")
        tbl.add_column("")
        tbl.add_column("", style="dim")
        for key, (cat, _) in examples.EXAMPLES.items():
            tbl.add_row(key, t(f"ex.{key}"), t(f"ex.cat.{cat}"))
        emit(tbl, [{"name": k, "category": c, "title": t(f"ex.{k}")} for k, (c, _) in examples.EXAMPLES.items()])
        theory(t("ex.usage"))
        return
    key = name.lower().replace("-", "_")
    if key not in examples.EXAMPLES:
        fail(t("ex.unknown", name=name, options=", ".join(examples.names())))
    path = output or Path(f"{key}.json")
    try:
        examples.build(key).save(path)
    except OSError as e:
        fail(str(e))
    console.print(f"[green]✓[/] {t('ex.saved', path=path)}")
    console.print(f"[dim]elektro tui {path}   ·   elektro sim {path}[/]")
