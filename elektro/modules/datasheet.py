"""Komponent datasheet'ini bulur ve indirir.

Kaynaklar sırasıyla denenir:
  1. Üretici siteleri (bilinen URL kalıpları: TI, Espressif, Diodes, onsemi, Nexperia)
  2. JLCPCB/LCSC parça veritabanı
  3. DuckDuckGo araması (bot korumasına takılırsa atlanır)

Her aday indirilmeden önce gerçekten PDF olup olmadığı dosya imzasından (%PDF) kontrol edilir.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Optional
from urllib.parse import parse_qs, quote_plus, unquote, urljoin, urlparse

import requests
import typer
from bs4 import BeautifulSoup
from rich.progress import BarColumn, DownloadColumn, Progress, TextColumn, TransferSpeedColumn

from elektro.ui import console, fail

USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
TIMEOUT = 15
MAX_HTML = 3 * 1024 * 1024

# {l}: küçük harf, {u}: büyük harf parça adı
MANUFACTURER_PATTERNS = [
    ("Texas Instruments", "https://www.ti.com/lit/ds/symlink/{l}.pdf"),
    ("Espressif", "https://www.espressif.com/sites/default/files/documentation/{l}_datasheet_en.pdf"),
    ("onsemi", "https://www.onsemi.com/pdf/datasheet/{l}-d.pdf"),
    ("Diodes Inc.", "https://www.diodes.com/assets/Datasheets/{u}.pdf"),
    ("Nexperia", "https://assets.nexperia.com/documents/data-sheet/{u}.pdf"),
]

JLC_API = "https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList"


class SearchBlocked(Exception):
    pass


@dataclass
class Candidate:
    url: str
    source: str
    label: str = ""


def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/pdf,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    return s


def normalize(part: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", part.upper())


# --- Kaynaklar -------------------------------------------------------------------

def _starts_with_pdf(session: requests.Session, url: str) -> bool:
    try:
        with session.get(url, stream=True, timeout=TIMEOUT, allow_redirects=True) as r:
            if r.status_code != 200:
                return False
            return next(r.iter_content(5), b"") == b"%PDF-"
    except requests.RequestException:
        return False


def manufacturer_candidates(session: requests.Session, part: str) -> List[Candidate]:
    slug = part.strip()
    if not re.fullmatch(r"[A-Za-z0-9._-]+", slug):
        return []
    urls = [(name, tpl.format(l=slug.lower(), u=slug.upper())) for name, tpl in MANUFACTURER_PATTERNS]
    with ThreadPoolExecutor(len(urls)) as pool:
        ok = list(pool.map(lambda nu: _starts_with_pdf(session, nu[1]), urls))
    return [Candidate(url, name, slug.upper()) for (name, url), good in zip(urls, ok) if good]


def jlcpcb_candidates(session: requests.Session, part: str, limit: int = 30) -> List[Candidate]:
    try:
        r = session.post(JLC_API, json={"keyword": part, "currentPage": 1, "pageSize": limit},
                         timeout=TIMEOUT)
        r.raise_for_status()
        items = ((r.json().get("data") or {}).get("componentPageInfo") or {}).get("list") or []
    except (requests.RequestException, ValueError):
        return []

    q = normalize(part)
    scored = []
    for it in items:
        url = it.get("dataManualUrl")
        model = it.get("componentModelEn") or ""
        m = normalize(model)
        if not url or not m:
            continue
        if m == q:
            score = 0
        elif m.startswith(q):
            score = 1 + (len(m) - len(q)) / 100
        elif q in m:
            score = 3
        elif m in q:
            score = 4
        else:
            continue
        brand = it.get("componentBrandEn") or ""
        scored.append((score, Candidate(url, "LCSC", f"{model} ({brand})" if brand else model)))
    scored.sort(key=lambda x: x[0])
    return [c for _, c in scored]


def _ddg_unwrap(href: str) -> str:
    if href.startswith("//"):
        href = "https:" + href
    parsed = urlparse(href)
    if parsed.netloc.endswith("duckduckgo.com") and parsed.path.startswith("/l/"):
        target = parse_qs(parsed.query).get("uddg")
        if target:
            return unquote(target[0])
    return href


def duckduckgo_candidates(session: requests.Session, part: str, limit: int = 10) -> List[Candidate]:
    query = f"{part} datasheet filetype:pdf"
    endpoints = [
        ("post", "https://html.duckduckgo.com/html/", "a.result__a"),
        ("get", "https://lite.duckduckgo.com/lite/", "a.result-link"),
    ]
    for method, url, selector in endpoints:
        try:
            if method == "post":
                r = session.post(url, data={"q": query}, timeout=TIMEOUT)
            else:
                r = session.get(url, params={"q": query}, timeout=TIMEOUT)
        except requests.RequestException:
            continue
        if r.status_code == 202 or "anomaly" in r.text[:20000]:
            continue
        soup = BeautifulSoup(r.text, "html.parser")
        links = [_ddg_unwrap(a["href"]) for a in soup.select(selector) if a.get("href")]
        links = [u for u in links if u.startswith("http")]
        if links:
            return [Candidate(u, "DuckDuckGo", urlparse(u).netloc) for u in links[:limit]]
    raise SearchBlocked()


def iter_candidates(session: requests.Session, part: str, verbose: bool = True) -> Iterator[Candidate]:
    seen = set()

    def fresh(cands):
        for c in cands:
            if c.url not in seen:
                seen.add(c.url)
                yield c

    def step(title):
        if verbose:
            console.print(f"[dim]• {title}[/]")

    step("Üretici siteleri kontrol ediliyor")
    yield from fresh(manufacturer_candidates(session, part))
    step("LCSC/JLCPCB parça veritabanı aranıyor")
    yield from fresh(jlcpcb_candidates(session, part))
    step("DuckDuckGo'da aranıyor")
    try:
        yield from fresh(duckduckgo_candidates(session, part))
    except SearchBlocked:
        step("DuckDuckGo şu an bot koruması gösteriyor, atlandı")


# --- İndirme -----------------------------------------------------------------------

_PDF_IN_HTML = re.compile(r"https?://[^\s\"'<>]+?\.pdf(?:\?[^\s\"'<>]*)?", re.I)


def find_pdf_link(html: str, base_url: str) -> Optional[str]:
    """HTML sayfası içinde PDF bağlantısı arar (ör. LCSC görüntüleyici sayfası)."""
    for m in _PDF_IN_HTML.finditer(html):
        link = m.group(0).replace("&amp;", "&")
        if "viewer.html" in link or link.rstrip("/") == base_url.rstrip("/"):
            continue
        return link
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all(["a", "iframe", "embed"], href=True) + soup.find_all(["iframe", "embed"], src=True):
        href = a.get("href") or a.get("src")
        if href and ".pdf" in href.lower() and not href.lower().startswith("javascript"):
            return urljoin(base_url, href)
    return None


def fetch_pdf(session: requests.Session, url: str, dest: Path, depth: int = 0) -> Optional[str]:
    """URL'den PDF indirir. Başarılıysa gerçek PDF adresini döndürür."""
    try:
        r = session.get(url, stream=True, timeout=TIMEOUT, allow_redirects=True)
    except requests.RequestException:
        return None
    with r:
        if r.status_code != 200:
            return None
        chunks = r.iter_content(64 * 1024)
        first = next(chunks, b"")
        if first[:5] == b"%PDF-":
            total = int(r.headers.get("content-length") or 0) or None
            tmp = tempfile.NamedTemporaryFile(delete=False, dir=dest.parent, prefix=".elektro-", suffix=".part")
            tmp_path = Path(tmp.name)
            try:
                with tmp, Progress(
                    TextColumn("  [cyan]{task.description}"), BarColumn(), DownloadColumn(),
                    TransferSpeedColumn(), console=console, transient=True,
                ) as progress:
                    task = progress.add_task(dest.name, total=total)
                    tmp.write(first)
                    progress.update(task, advance=len(first))
                    for chunk in chunks:
                        tmp.write(chunk)
                        progress.update(task, advance=len(chunk))
                os.replace(tmp_path, dest)
            except (requests.RequestException, OSError):
                return None
            finally:
                tmp_path.unlink(missing_ok=True)
            return r.url
        if depth > 0 or "html" not in r.headers.get("content-type", "").lower():
            return None
        html = first + b"".join(_limited(chunks, MAX_HTML))
        link = find_pdf_link(html.decode(r.encoding or "utf-8", "replace"), r.url)
    if link:
        return fetch_pdf(session, link, dest, depth + 1)
    return None


def _limited(chunks, limit):
    size = 0
    for c in chunks:
        size += len(c)
        if size > limit:
            return
        yield c


def open_file(path: Path) -> None:
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    if shutil.which(opener):
        subprocess.Popen([opener, str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        console.print(f"[yellow]'{opener}' bulunamadı, dosyayı elle aç: {path}[/]")


def manual_links(part: str) -> List[str]:
    q = quote_plus(part)
    return [
        f"https://octopart.com/search?q={q}",
        f"https://www.lcsc.com/search?q={q}",
        f"https://www.alldatasheet.com/view.jsp?Searchword={q}",
        f"https://www.google.com/search?q={q}+datasheet+filetype%3Apdf",
    ]


# --- Komut -----------------------------------------------------------------------

def datasheet(
    part: str = typer.Argument(..., help="Parça adı, örn: lm358, ne555, ams1117, esp32"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Kayıt yolu (varsayılan: <parça>_datasheet.pdf)"),
    open_after: bool = typer.Option(False, "--open", help="İndirdikten sonra PDF'i aç"),
    list_only: bool = typer.Option(False, "--list", "-l", help="İndirmeden bulunan adayları listele"),
    force: bool = typer.Option(False, "--force", "-f", help="Dosya varsa üzerine yaz"),
    max_try: int = typer.Option(15, "--max", "-n", help="Denenecek en fazla aday sayısı"),
):
    """Komponent datasheet'ini bulup bulunduğun klasöre indirir.

    Önce üretici sitelerine, sonra LCSC parça veritabanına, en son
    DuckDuckGo aramasına bakar. İnen dosyanın gerçekten PDF olduğu doğrulanır.

    Örnekler:
      elektro datasheet lm358
      elektro datasheet ams1117 --open
      elektro datasheet 2n2222 -o transistor.pdf
      elektro datasheet esp32 --list
    """
    part = part.strip()
    if not part:
        fail("parça adı boş olamaz")
    session = make_session()

    if list_only:
        console.print(f"[bold]'{part}' için adaylar:[/]\n")
        found = False
        for i, c in enumerate(iter_candidates(session, part, verbose=False), 1):
            found = True
            console.print(f"{i:>2}. [cyan]{c.source:<17}[/] {c.label}\n    [dim]{c.url}[/]")
            if i >= max_try:
                break
        if not found:
            console.print("[red]Aday bulunamadı.[/]")
            raise typer.Exit(1)
        return

    safe = re.sub(r"[^\w.-]", "_", part.lower())
    dest = (output or Path(f"{safe}_datasheet.pdf")).expanduser()
    if dest.is_dir():
        dest = dest / f"{safe}_datasheet.pdf"
    dest = dest.resolve()
    if dest.exists() and not force:
        console.print(f"[yellow]Dosya zaten var:[/] {dest}\n[dim]Tekrar indirmek için --force kullan.[/]")
        if open_after:
            open_file(dest)
        return
    if not dest.parent.is_dir():
        fail(f"klasör yok: {dest.parent}")

    console.print(f"[bold]🔍 '{part}' için datasheet aranıyor[/]")
    tried = 0
    try:
        for cand in iter_candidates(session, part):
            tried += 1
            console.print(f"  [dim]{tried:>2}.[/] {cand.source}: {cand.label or urlparse(cand.url).netloc}")
            real_url = fetch_pdf(session, cand.url, dest)
            if real_url:
                size = dest.stat().st_size
                console.print(f"[bold green]✓ İndirildi[/] [dim]({size / 1024:.0f} KB, {urlparse(real_url).netloc})[/]")
                console.print(f"  {dest}")
                if open_after:
                    open_file(dest)
                return
            console.print("      [dim]PDF alınamadı, sıradaki deneniyor[/]")
            if tried >= max_try:
                break
    except KeyboardInterrupt:
        console.print("\n[yellow]İptal edildi.[/]")
        raise typer.Exit(130)

    if tried == 0:
        console.print("\n[bold red]Hiçbir kaynakta sonuç bulunamadı.[/] İnternet bağlantını ya da parça adını kontrol et.")
    else:
        console.print("\n[bold red]Bulunan adayların hiçbirinden PDF indirilemedi.[/]")
    console.print("[dim]Elle aramak için:[/]")
    for link in manual_links(part):
        console.print(f"  {link}")
    raise typer.Exit(1)
