from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

base_url = "https://only.digital"
visited = set()
to_visit = {base_url}
printed_info = set()

def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")

def fetch_links_and_check_footer(url):
    norm_url = normalize_url(url)
    links, has_footer = [], False
    try:
        resp = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.find_all("a", href=True):
            u = normalize_url(urljoin(url, a["href"]))
            if u.startswith(base_url):
                links.append(u)
        has_footer = bool(soup.find("footer"))
        if has_footer and norm_url not in printed_info:
            print(f"[INFO] Footer found on: {norm_url}")
            printed_info.add(norm_url)
    except Exception as e:
        print(f"[ERROR] {url}: {e}")
    return norm_url, links, has_footer

def get_pages_with_footer():
    results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        while to_visit:
            batch = list(to_visit); to_visit.clear()
            futures = [executor.submit(fetch_links_and_check_footer, u) for u in batch]
            for f in futures:
                url, links, has_footer = f.result()
                visited.add(url)
                results[url] = has_footer
                for l in links:
                    if l not in visited and l not in to_visit:
                        to_visit.add(l)

    return sorted(u for u, ok in results.items() if ok)

