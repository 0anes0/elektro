import requests
import os
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from elektro.modules.utils import console
from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn


def get_headers():
    """Gercekci tarayici headeri"""
    return {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }


def duckduckgo_search(query: str, limit: int = 15):
    """DuckDuckGo ile PDF datasheet ara"""
    search_query = f"{query} datasheet filetype:pdf"
    url = "https://html.duckduckgo.com/html/"
    data = {"q": search_query}
    
    try:
        response = requests.post(url, data=data, headers=get_headers(), timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        console.print(f"[red]Arama hatasi: {e}[/]")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    
    for link in soup.find_all('a', class_='result__a', href=True):
        href = link['href']
        if href.startswith('//'):
            href = 'https:' + href
        results.append(href)
    
    return results[:limit]


def find_pdf_url(page_url: str):
    """Sayfada gercek PDF linkini bul"""
    try:
        resp = requests.get(page_url, headers=get_headers(), timeout=15, allow_redirects=True)
        resp.raise_for_status()
    except Exception:
        return None
    
    content_type = resp.headers.get('content-type', '').lower()
    if 'pdf' in content_type:
        return page_url
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    for link in soup.find_all('a', href=True):
        href = link['href'].lower()
        if href.endswith('.pdf'):
            return urljoin(resp.url, link['href'])
    
    for link in soup.find_all('a', href=True):
        text = link.get_text().lower()
        href = link['href'].lower()
        if any(word in text for word in ['pdf', 'download', 'datasheet', 'data sheet']):
            if not href.startswith('javascript'):
                return urljoin(resp.url, link['href'])
    
    return None


def download_file(url: str, filepath: str):
    """PDF'yi indir, progress bar goster"""
    try:
        with requests.get(url, headers=get_headers(), stream=True, timeout=60) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            
            if total == 0:
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return True
            
            with Progress(
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                "[progress.percentage]{task.percentage:>3.1f}%",
                "•",
                DownloadColumn(),
            ) as progress:
                task = progress.add_task(f"[cyan]{os.path.basename(filepath)}", total=total)
                
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            progress.update(task, advance=len(chunk))
        
        return True
    except Exception as e:
        console.print(f"[red]Indirme basarisiz: {e}[/]")
        return False


def download_datasheet(component: str, output: str = None, max_try: int = 10):
    """Ana datasheet indirme fonksiyonu"""
    safe_name = re.sub(r'[^\w\-_]', '_', component.lower())
    if not output:
        output = f"{safe_name}_datasheet.pdf"
    
    filepath = os.path.join(os.getcwd(), output)
    
    console.print(f"[bold]🔍 '{component}' icin datasheet araniyor...[/]\n")
    
    results = duckduckgo_search(component, limit=max_try)
    if not results:
        console.print("[red]Arama sonucu bulunamadi. Internet baglantinizi kontrol edin.[/]")
        return False
    
    console.print(f"[dim]{len(results)} aday link bulundu. Indirme deneniyor...[/]\n")
    
    for i, result in enumerate(results, 1):
        parsed = urlparse(result)
        console.print(f"[dim]{i}. Kontrol: {parsed.netloc}[/]")
        
        pdf_url = find_pdf_url(result)
        if not pdf_url:
            continue
        
        console.print(f"   [green]↳ PDF bulundu, indiriliyor...[/]")
        
        success = download_file(pdf_url, filepath)
        if success:
            size = os.path.getsize(filepath)
            console.print(f"\n[bold green]✅ Indirme tamamlandi![/]")
            console.print(f"   [cyan]Dosya:[/] {filepath}")
            console.print(f"   [cyan]Boyut:[/] {size/1024:.1f} KB")
            console.print(f"   [cyan]Kaynak:[/] {urlparse(pdf_url).netloc}")
            return True
    
    console.print("\n[bold red]❌ Hicbir linkte basarili indirme yapilamadi.[/]")
    console.print("[dim]Not: Bazi uretici siteleri bot korumasi kullanir.[/]")
    return False
