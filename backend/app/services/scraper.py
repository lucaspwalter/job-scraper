from urllib.parse import quote_plus

import httpx


GUPY_API_URL = "https://portal.gupy.io/api/job-search/v1/jobs?jobName={search_term}&limit=20"
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def build_search_url(search_term: str) -> str:
    return GUPY_API_URL.format(search_term=quote_plus(search_term))


def fetch_jobs(search_term: str) -> list[dict]:
    with httpx.Client(headers=BROWSER_HEADERS, timeout=20, follow_redirects=True) as client:
        response = client.get(build_search_url(search_term))
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type:
            raise RuntimeError("Gupy API did not return JSON")

        data = response.json()

    if isinstance(data, list):
        return data

    return data.get("data", data.get("jobs", []))


def scrape_gupy(search_term: str, url: str | None = None) -> list[dict]:
    jobs = []

    for job in fetch_jobs(search_term):
        title = job.get("name")
        job_url = job.get("jobUrl")

        if not title or not job_url:
            continue

        jobs.append(
            {
                "title": title,
                "company": job.get("careerPageName"),
                "url": job_url,
            }
        )

    return jobs
