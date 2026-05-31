from urllib.parse import urljoin

import httpx
import requests
from bs4 import BeautifulSoup


GUPY_SEARCH_URL = "https://portal.gupy.io/job-search/term={search_term}"
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}


def build_search_url(search_term: str) -> str:
    return GUPY_SEARCH_URL.format(search_term=search_term.replace(" ", "%20"))


def fetch_html(url: str) -> str:
    try:
        response = requests.get(url, headers=BROWSER_HEADERS, timeout=20)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        with httpx.Client(headers=BROWSER_HEADERS, timeout=20, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.text


def parse_gupy_jobs(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    seen_urls = set()

    for anchor in soup.select("a[href]"):
        href = anchor.get("href", "")
        text = " ".join(anchor.get_text(" ", strip=True).split())

        if not href or not text:
            continue

        absolute_url = urljoin("https://portal.gupy.io", href)
        if "gupy.io" not in absolute_url or absolute_url in seen_urls:
            continue

        href_lower = absolute_url.lower()
        if not any(part in href_lower for part in ("/jobs/", "/job/", "job-search")):
            continue

        company = None
        container = anchor.find_parent(["article", "li", "div"])
        if container:
            company_el = container.select_one('[data-testid*="company"], .company, [class*="company"]')
            if company_el:
                company = company_el.get_text(" ", strip=True) or None

        jobs.append({"title": text, "company": company, "url": absolute_url})
        seen_urls.add(absolute_url)

    return jobs


def scrape_gupy(search_term: str, url: str | None = None) -> list[dict]:
    target_url = url or build_search_url(search_term)
    return parse_gupy_jobs(fetch_html(target_url))
