"""Ortak terminal çıktısı yardımcıları."""

from __future__ import annotations

import base64
import io
import json
import math
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.errors import MarkupError
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from typer.core import TyperGroup

from elektro.i18n import t
from elektro.units import parse_value



class _ElektroConsole(Console):
    """Rapor modunda (--md, --latex, --report) çıktıyı Markdown/LaTeX'e çeviren konsol.

    Modüller sonuçları hep `console.print(...)` ile yazdığı için çeviri tek yerde yapılır.
    """

    def print(self, *objects, **kwargs):
        if _fmt is None or self.stderr:
            return super().print(*objects, **kwargs)
        if not _to_stdout:                 # yalnızca --report: terminale normal çıktı da
            super().print(*objects, **kwargs)
        for obj in objects:
            block = to_report(obj, _fmt)
            if block.strip():
                _report_block(block)


console = _ElektroConsole(highlight=False)
err_console = Console(stderr=True, highlight=False)


# --- JSON modu --------------------------------------------------------------------
# `--json` verildiğinde sonuçlar tablo yerine makine okunur JSON olarak yazılır.
_json = False


def set_json(enabled: bool) -> None:
    global _json
    _json = enabled


def json_mode() -> bool:
    return _json


def _clean(value):
    """JSON'a uygun hale getir (inf/nan → null, tuple → list)."""
    if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
        return None
    if isinstance(value, dict):
        return {k: _clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_clean(v) for v in value]
    return value


def print_json(data) -> None:
    print(json.dumps(_clean(data), ensure_ascii=False, indent=2))


# --- Rapor modu (--md, --latex, --report, --copy) ------------------------------------------

_fmt: Optional[str] = None          # None | "md" | "latex"
_to_stdout = False                  # True: rapor metni terminale yazılır (--md/--latex)
_report_file: Optional[Path] = None
_copy = False
_command: Optional[List[str]] = None
_buffer: List[str] = []


def set_report(fmt: Optional[str], to_stdout: bool = True, file: Optional[Path] = None,
               copy: bool = False) -> None:
    global _fmt, _to_stdout, _report_file, _copy
    _fmt, _to_stdout, _report_file, _copy = fmt, to_stdout, file, copy
    _buffer.clear()
    with console._record_buffer_lock:
        console._record_buffer.clear()
    console.record = copy and fmt is None


def report_mode() -> Optional[str]:
    return _fmt


def set_command(args: Optional[List[str]]) -> None:
    """Rapor başlığında gösterilecek komut satırı (execute() tarafından verilir)."""
    global _command
    out, skip = [], False
    for a in args or []:
        if skip:
            skip = False
        elif a in ("--report", "--lang"):
            skip = True
        elif a not in REPORT_FLAGS and not a.startswith(("--report=", "--lang=")):
            out.append(a)
    _command = out or None


def _report_block(block: str) -> None:
    if not _buffer and _command:
        cmd = "elektro " + " ".join(shlex.quote(a) for a in _command)
        header = f"`$ {cmd}`" if _fmt == "md" else "\\noindent\\texttt{" + latex_escape("$ " + cmd) + "}"
        _emit(header)
    _emit(block)


def _emit(block: str) -> None:
    text = block.rstrip("\n") + "\n\n"
    _buffer.append(text)
    if _to_stdout:
        console.file.write(text)


REPORT_FLAGS = ("--md", "--latex", "--copy", "--json")


def _plain(obj) -> str:
    if obj is None:
        return ""
    if isinstance(obj, Text):
        return obj.plain
    if isinstance(obj, str):
        try:
            return Text.from_markup(obj).plain
        except MarkupError:
            return obj
    return str(obj)


_LATEX_SPECIAL = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
                  "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
_LATEX_SYMBOLS = {
    "Ω": r"$\Omega$", "µ": r"$\mu$", "μ": r"$\mu$", "°": r"$^\circ$", "±": r"$\pm$", "²": r"$^2$",
    "³": r"$^3$", "√": r"$\surd$", "φ": r"$\varphi$", "θ": r"$\theta$", "π": r"$\pi$", "τ": r"$\tau$",
    "ω": r"$\omega$", "λ": r"$\lambda$", "Δ": r"$\Delta$", "Γ": r"$\Gamma$", "η": r"$\eta$",
    "κ": r"$\kappa$", "∠": r"$\angle$", "·": r"$\cdot$", "×": r"$\times$", "≈": r"$\approx$",
    "≥": r"$\geq$", "≤": r"$\leq$", "→": r"$\rightarrow$", "↔": r"$\leftrightarrow$", "∞": r"$\infty$",
    "−": "-", "…": r"\ldots{}", "✓": "", "✗": "x", "⚠": "", "█": "",
}


def latex_escape(text: str) -> str:
    return "".join(_LATEX_SPECIAL.get(c) or _LATEX_SYMBOLS.get(c, c) for c in text)


def _md_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", "<br>").strip()


def _is_bar(text: str) -> bool:
    return not text.strip(" █▏▎▍▌▋▊▉")


def _table(table: Table, fmt: str, title: Optional[str]) -> str:
    cols = []
    for col in table.columns:
        cells = [_plain(c) for c in col._cells]
        header = _plain(col.header) if table.show_header else ""
        if not header and all(_is_bar(c) for c in cells):
            continue                       # metin grafik sütunları (█) rapora girmez
        cols.append((header, cells, col.justify))
    if not cols:
        return ""
    headers = [h for h, _, _ in cols]
    if not any(headers):
        headers = [t("report.quantity"), t("report.value")] if len(cols) == 2 else [""] * len(cols)
    rows = list(zip(*[cells for _, cells, _ in cols]))
    title = title or _plain(table.title) or None
    if fmt == "md":
        out = [f"**{title}**", ""] if title else []
        out.append("| " + " | ".join(_md_cell(h) for h in headers) + " |")
        out.append("|" + "|".join("---:" if j == "right" else ":---:" if j == "center" else "---"
                                  for _, _, j in cols) + "|")
        out += ["| " + " | ".join(_md_cell(c) for c in row) + " |" for row in rows]
        return "\n".join(out)
    align = "".join("r" if j == "right" else "c" if j == "center" else "l" for _, _, j in cols)
    out = ["\\begin{table}[h]", "\\centering"]
    if title:
        out.append("\\caption{" + latex_escape(title) + "}")
    out += ["\\begin{tabular}{" + align + "}", "\\hline"]
    if any(headers):
        out += [" & ".join("\\textbf{" + latex_escape(h) + "}" for h in headers) + " \\\\", "\\hline"]
    out += [" & ".join(latex_escape(c.replace("\n", " ").strip()) for c in row) + " \\\\" for row in rows]
    out += ["\\hline", "\\end{tabular}", "\\end{table}"]
    return "\n".join(out)


def _text(text: str, fmt: str) -> str:
    lines = [ln.rstrip() for ln in text.strip("\n").splitlines()]
    if fmt == "md":
        return "  \n".join(lines)
    return "\n\n".join(latex_escape(ln) for ln in lines if ln.strip())


def _verbatim(text: str, fmt: str) -> str:
    text = text.rstrip()
    if fmt == "md":
        return f"```\n{text}\n```"
    return f"\\begin{{verbatim}}\n{text}\n\\end{{verbatim}}"


def _render_plain(obj) -> str:
    buf = io.StringIO()
    Console(file=buf, width=100, color_system=None, force_terminal=False, highlight=False).print(obj)
    return buf.getvalue()


def to_report(obj, fmt: str) -> str:
    """Bir rich nesnesini (Panel, Table, metin) Markdown veya LaTeX'e çevirir."""
    if isinstance(obj, Panel):
        title = _plain(obj.title)
        inner = obj.renderable
        if isinstance(inner, Table):
            parts = [_table(inner, fmt, title)]
        else:
            heading = (f"**{title}**" if fmt == "md" else "\\paragraph{" + latex_escape(title) + "}") if title else ""
            parts = [heading, to_report(inner, fmt)]
        if obj.subtitle:
            parts.append(_text(_plain(obj.subtitle), fmt))
        return "\n\n".join(p for p in parts if p)
    if isinstance(obj, Table):
        return _table(obj, fmt, None)
    if isinstance(obj, (str, Text)):
        text = _plain(obj)
        # Kutu çizimi içeren metinler (pinout, K-haritası) olduğu gibi kalsın
        if any(ch in text for ch in "┌┐└┘│─┤├"):
            return _verbatim(text, fmt)
        return _text(text, fmt)
    return _verbatim(_render_plain(obj), fmt)


def plot_saved(path: Path) -> None:
    """--plot ile kaydedilen grafiği bildirir; Markdown raporuna resim olarak ekler."""
    msg = f"[green]✓[/] {t('plot.saved', path=path)}"
    if _json:
        err_console.print(msg)
        return
    if _fmt is None:
        console.print(msg)
        return
    if not _to_stdout:
        Console.print(console, msg)
    if _fmt == "md":
        _report_block(f"![{Path(path).stem}]({path})")
    elif Path(path).suffix.lower() in (".png", ".pdf"):
        _report_block("\\begin{figure}[h]\n\\centering\n\\includegraphics[width=\\linewidth]{"
                      + str(path) + "}\n\\end{figure}")
    else:
        _report_block(_text(t("plot.saved", path=path), "latex"))


def copy_to_clipboard(text: str) -> bool:
    """Panoya kopyalar: wl-copy, xclip, xsel, pbcopy; hiçbiri yoksa OSC 52 terminal dizisi."""
    candidates = []
    if os.environ.get("WAYLAND_DISPLAY"):
        candidates.append(["wl-copy"])
    if os.environ.get("DISPLAY"):
        candidates += [["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]]
    candidates.append(["pbcopy"])
    for cmd in candidates:
        if shutil.which(cmd[0]):
            try:
                subprocess.run(cmd, input=text, text=True, check=True, timeout=5,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            except (OSError, subprocess.SubprocessError):
                continue
    if sys.stderr.isatty():
        sys.stderr.write("\033]52;c;" + base64.b64encode(text.encode()).decode() + "\a")
        sys.stderr.flush()
        return True
    return False


def finish_output() -> None:
    """Komut bittiğinde: rapor dosyasına ekle, panoya kopyala."""
    if _fmt and _report_file and _buffer:
        try:
            with open(_report_file, "a", encoding="utf-8") as f:
                f.write("".join(_buffer))
            err_console.print(f"[green]✓[/] {t('report.appended', path=_report_file)}")
        except OSError as e:
            err_console.print(f"[bold red]{t('ui.error')}:[/] {e}")
    if _copy:
        text = "".join(_buffer) if _fmt else console.export_text(clear=True)
        if text.strip():
            ok = copy_to_clipboard(text)
            err_console.print(f"[green]✓[/] {t('report.copied')}" if ok
                              else f"[yellow]{t('ui.warning')}:[/] {t('report.no_clipboard')}")


def result_panel(title: str, rows: dict, data: Optional[dict] = None, note: Optional[str] = None) -> None:
    """Sonuç panelini yazar; JSON modunda `data`yı (yoksa satırları) JSON olarak basar."""
    if _json:
        print_json(data if data is not None else {k: str(v) for k, v in rows.items()})
        return
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column(style="cyan", justify="right")
    table.add_column(style="bold green")
    for key, value in rows.items():
        table.add_row(key, value if isinstance(value, Text) else str(value))
    console.print(Panel(table, title=f"[bold]{title}[/]", border_style="green",
                        subtitle=note, expand=False))


def emit(renderable, data) -> None:
    """Tablo gibi bir çıktıyı yazar; JSON modunda yerine `data`yı basar."""
    if _json:
        print_json(data)
    else:
        console.print(renderable)


def theory(*lines: str) -> None:
    if _json:
        return
    console.print()
    for line in lines:
        console.print(f"[dim]{line}[/]")


def fail(message: str, code: int = 1) -> "typer.Exit":
    err_console.print(f"[bold red]{t('ui.error')}:[/] {message}")
    raise typer.Exit(code)


def warn(message: str) -> None:
    (err_console if _json else console).print(f"[yellow]{t('ui.warning')}:[/] {message}")


def cli_parser(fn):
    """Ayrıştırıcının ValueError mesajını kullanıcıya ulaştırır.

    Typer/Click, parser= ile verilen fonksiyonlardaki ValueError'ı yakalayıp sadece
    "Invalid value" der; BadParameter'a çevirince asıl açıklama görünür.
    """
    def wrapper(value):
        try:
            return fn(value)
        except ValueError as e:
            raise typer.BadParameter(str(e))
    wrapper.__name__ = getattr(fn, "__name__", "parser")
    return wrapper


def eng(help_text: str) -> dict:
    """Mühendislik gösterimini (1k, 100n, 4k7) kabul eden seçenekler için ortak ayarlar."""
    return {"parser": cli_parser(parse_value), "metavar": t("ui.metavar.value"), "help": help_text}


class DefaultCommandGroup(TyperGroup):
    """İlk argüman bir alt komut değilse `default_command`'ı çalıştırır.

    Böylece `elektro resistor k s r a` ile `elektro resistor decode k s r a` aynı işi yapar.
    """

    default_command: str = ""

    def parse_args(self, ctx, args):
        if args and self.default_command and args[0] not in self.commands and not args[0].startswith("-"):
            args.insert(0, self.default_command)
        return super().parse_args(ctx, args)


def default_group(command: str) -> type:
    return type(f"DefaultGroup_{command}", (DefaultCommandGroup,), {"default_command": command})
