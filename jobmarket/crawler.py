from __future__ import annotations

import csv
import json
import math
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse, parse_qs, parse_qsl, urlencode
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

from .config import RAW_LIVE
from .schema import COLUMNS

USER_AGENT = "IT4930-Student-Research/1.0 (educational; respect robots.txt)"

# Ghi nho: cac mau duong dan co the thay doi theo thoi gian.
JOB_PATTERNS = {
    "itviec": re.compile(r"^/it-jobs/[^/]+-\d{3,8}/?$", re.I),
    "topcv": re.compile(r"^/viec-lam/[^/]+/\d+\.html$", re.I),
    "careerviet": re.compile(r"^/vi/tim-viec-lam/[^/]+\.[a-z0-9]+\.html$", re.I),
}


def _source(url: str) -> str:
    host = (urlparse(url).hostname or "").lower()
    if host == "itviec.com" or host.endswith(".itviec.com"):
        return "itviec"
    if host == "topcv.vn" or host.endswith(".topcv.vn"):
        return "topcv"
    if host == "careerviet.vn" or host.endswith(".careerviet.vn"):
        return "careerviet"
    if host == "linkedin.com" or host.endswith(".linkedin.com"):
        return "linkedin"
    return host


def _canonical_url(url: str) -> str:
    p = urlparse(url)
    return urlunparse((p.scheme, p.netloc, p.path, "", "", ""))


def _is_job_url(url: str) -> bool:
    source = _source(url)
    pattern = JOB_PATTERNS.get(source)
    return bool(pattern and pattern.fullmatch(urlparse(url).path))


def find_job_links(html: str, listing_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    found, seen = [], set()
    for a in soup.select("a[href]"):
        href = a.get("href", "").strip()
        if not href or href.startswith(("javascript:", "mailto:", "#")):
            continue
        url = _canonical_url(urljoin(listing_url, href))
        if _source(url) != _source(listing_url):
            continue
        if _is_job_url(url) and url not in seen:
            seen.add(url)
            found.append(url)
    return found


def find_next_page(html: str, current_url: str) -> str | None:
    """Find a next link; use numbered pagination controls where present."""
    soup = BeautifulSoup(html, "html.parser")
    candidates = soup.select("a[rel~=next], a[aria-label], a.next")
    for a in candidates:
        label = " ".join([
            " ".join(a.get("rel", [])), a.get("aria-label", ""),
            a.get_text(" ", strip=True),
        ]).lower()
        if not any(k in label for k in ("next", "tiếp", "sau", "»", "›")):
            continue
        href = a.get("href")
        if not href:
            continue
        url = urljoin(current_url, href)
        target = urlparse(url)
        current = urlparse(current_url)
        if target.scheme in {'http', 'https'} and target.hostname == current.hostname and target.path == current.path and url != current_url:
            return url
    parsed = urlparse(current_url)
    if _source(current_url) == 'careerviet':
        match = re.search(r'-trang-(\d+)-vi\.html$', parsed.path, re.I)
        current_page = int(match.group(1)) if match else 1
        expected = re.sub(r'(?:-trang-\d+)?-vi\.html$', f'-trang-{current_page + 1}-vi.html', parsed.path, flags=re.I)
        if expected != parsed.path and parsed.path.startswith('/viec-lam/'):
            # Prefer an actual link when the site exposes one.
            for a in soup.select('a[href]'):
                target = urlparse(urljoin(current_url, a['href']))
                if target.scheme in {'http', 'https'} and target.hostname == parsed.hostname and target.path == expected:
                    return target.geturl()
            # Some listing responses omit navigation. Try the observed URL pattern;
            # caller stops when a page fails or contains no previously unseen jobs.
            return parsed._replace(path=expected, fragment='').geturl()
    else:
        values = parse_qs(parsed.query).get('page', ['1'])
        current_page = int(values[0]) if values[0].isdigit() else 1
        for a in soup.select('a[href]'):
            if a.get_text(strip=True) != str(current_page + 1): continue
            target = urlparse(urljoin(current_url, a['href']))
            if target.hostname == parsed.hostname and target.path == parsed.path and parse_qs(target.query).get('page') == [str(current_page + 1)]:
                return target.geturl()
        # Explicit fallback for known listing paths. Preserve filters, replace only
        # page and remove selected-job UI state; repeated/empty pages stop the crawl.
        site = _source(current_url)
        is_listing = (site == 'itviec' and parsed.path.rstrip('/') == '/it-jobs') or (
            site == 'topcv' and (parsed.path.rstrip('/') == '/viec-lam' or parsed.path.startswith('/tim-viec-lam-')))
        if is_listing and parsed.scheme in {'http', 'https'}:
            params = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True) if k not in {'page', 'job_selected'}]
            params.append(('page', str(current_page + 1)))
            return parsed._replace(query=urlencode(params, doseq=True), fragment='').geturl()
    return None


def _objects(obj):
    if isinstance(obj, list):
        for x in obj:
            yield from _objects(x)
    elif isinstance(obj, dict):
        yield obj
        for key in ("@graph", "mainEntity"):
            if key in obj:
                yield from _objects(obj[key])


def _first(value):
    return value[0] if isinstance(value, list) and value else value


def _address(job: dict) -> str:
    loc = _first(job.get("jobLocation") or job.get("applicantLocationRequirements"))
    if not isinstance(loc, dict):
        return str(loc or "")
    address = loc.get("address", loc)
    if isinstance(address, dict):
        parts = [address.get(k) for k in ("streetAddress", "addressLocality", "addressRegion", "addressCountry")]
        return ", ".join(dict.fromkeys(p.strip() for p in parts if isinstance(p, str) and p.strip()))
    return str(address or "")


def _salary(job: dict):
    """Lay luong thang neu JSON-LD co unitText thich hop; khong tu quy doi."""
    salary = _first(job.get("baseSalary")) or {}
    if not isinstance(salary, dict):
        return None, None, None
    value = salary.get("value", {})
    if not isinstance(value, dict):
        value = {"value": value}
    currency = salary.get("currency") or value.get("currency") or ""
    unit = str(value.get("unitText") or salary.get("unitText") or "").upper()
    if unit and unit not in {"MONTH", "MONTHLY", "PER MONTH", "THÁNG"}:
        return None, None, currency or None
    # Khong dung 'or' voi 0 vi se lam sai gia tri 0
    vmin = value.get("minValue", value.get("value", ""))
    vmax = value.get("maxValue", value.get("value", ""))
    def number(v):
        if isinstance(v, bool) or not isinstance(v, (int, float, str)): return None
        try: n = float(v)
        except (ValueError, TypeError): return None
        return n if math.isfinite(n) and n > 0 else None
    return number(vmin), number(vmax), currency or None


def _experience_years(value):
    """Return numeric years only for unambiguous structured experience."""
    if isinstance(value, dict):
        months = value.get('monthsOfExperience')
        if isinstance(months, (int, float)) and not isinstance(months, bool) and math.isfinite(months) and 0 <= months <= 540:
            return months / 12
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and 0 <= value <= 45:
        return value
    return None


def _raw_value(value):
    """Preserve structured JSON-LD as JSON text without inventing values."""
    if value is None or value == '' or value == [] or value == {}:
        return None
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(',', ':'))
    return str(value)


def _salary_period(salary):
    salary = _first(salary)
    if not isinstance(salary, dict): return None
    value = salary.get('value')
    unit = (value.get('unitText') if isinstance(value, dict) else None) or salary.get('unitText')
    return str(unit).strip().upper() if isinstance(unit, str) and unit.strip() else None


def _visible_salary(soup: BeautifulSoup):
    """Fallback cho luong VND dang '12 - 20 trieu', chi tim gan tieu de tin."""
    h1 = soup.find("h1")
    if h1 is None:
        return "", "", ""
    parent = h1
    # Gioi han trong vung gan tieu de, tranh lay luong cua tin goi y.
    for _ in range(3):
        parent = parent.parent or parent
    text = parent.get_text(" ", strip=True)[:650]
    m = re.search(r"(\d{1,3}(?:[.,]\d+)?)\s*[-–]\s*"
                  r"(\d{1,3}(?:[.,]\d+)?)\s*(?:triệu|trieu|tr)\b", text, re.I)
    if not m:
        return "", "", ""
    return float(m.group(1).replace(",", ".")) * 1_000_000, \
           float(m.group(2).replace(",", ".")) * 1_000_000, "VND"


def _company_from_html(soup: BeautifulSoup, source: str) -> str:
    selectors = {
        "itviec": [],
        "topcv": [],
        "careerviet": [],
    }
    selectors[source] = selectors.get(source, []) + [
        ".company-name", ".job-company-name", "[class*='company-name']"
    ]
    for selector in selectors[source]:
        el = soup.select_one(selector)
        if el:
            name = el.get_text(" ", strip=True)
            if name and len(name) < 160:
                return name
    return ""


def parse_job_html(html: str, url: str, source: str | None = None) -> dict | None:
    """Extract a raw-schema record from a job detail page."""
    soup = BeautifulSoup(html, "html.parser")
    site = source or _source(url)
    job = None
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or script.get_text())
        except (ValueError, TypeError):
            continue
        for item in _objects(data):
            kinds = item.get("@type", [])
            if isinstance(kinds, str):
                kinds = [kinds]
            if any(str(kind).split("/")[-1] == "JobPosting" for kind in kinds):
                job = item
                break
        if job:
            break

    result = dict.fromkeys(COLUMNS, None)
    result["source"], result["url"] = site, _canonical_url(url)

    if job:
        org = _first(job.get("hiringOrganization"))
        result['salary_raw'] = _raw_value(job.get('baseSalary'))
        result['salary_period'] = _salary_period(job.get('baseSalary'))
        result['experience_raw'] = _raw_value(job.get('experienceRequirements'))
        result.update({
            "job_title": job.get("title", ""),
            "company_name": org.get("name", "") if isinstance(org, dict) else str(org or ""),
            "location": _address(job),
            "experience_required": _experience_years(job.get("experienceRequirements")),
            "job_type": job.get("employmentType", ""),
            "posted_date": str(job.get("datePosted") or "")[:10],
            "job_description": BeautifulSoup(str(job.get("description") or ""),
                                             "html.parser").get_text(" ", strip=True),
        })
        result["salary_min"], result["salary_max"], result["salary_currency"] = _salary(job)
        skills = job.get("skills") or ""
        result["skills"] = ", ".join(map(str, skills)) if isinstance(skills, list) else str(skills)
    else:
        h1 = soup.find("h1")
        result["job_title"] = h1.get_text(" ", strip=True) if h1 else ""
        result["company_name"] = _company_from_html(soup, site)

    if not result["job_title"]:
        h1 = soup.find("h1")
        result["job_title"] = h1.get_text(" ", strip=True) if h1 else None
    if not result["company_name"]:
        result["company_name"] = _company_from_html(soup, site)
    # Free-text fallback can match unrelated salary and period; keep unknown values missing.
    for key, value in result.items():
        if value == "" or value == [] or value == {}:
            result[key] = None
    # Khong tao 'tin tuyen dung' tu trang danh sach hoac HTML khong co du thong tin.
    if not result["job_title"] or not result["company_name"]:
        return None
    return result


def _allowed(url: str, session: requests.Session, robots_cache: dict) -> bool:
    parts = urlparse(url)
    root = f"{parts.scheme}://{parts.netloc}"
    if root not in robots_cache:
        robots = session.get(root + "/robots.txt", timeout=15)
        if robots.status_code != 200:
            raise RuntimeError(f"Khong xac minh duoc robots.txt: HTTP {robots.status_code}")
        rp = RobotFileParser()
        rp.parse(robots.text.splitlines())
        robots_cache[root] = rp
    return bool(robots_cache[root].can_fetch(USER_AGENT, url))


def crawl_urls(urls: list[str], delay: float = 2.0, max_jobs: int = 25,
               max_pages: int = 1) -> tuple[list[dict], list[dict]]:
    """URL dau vao co the la listing URL HOAC direct job URL.

    max_pages=1: trang listing dau tien. max_pages=2: them toi da 1 trang next.
    """
    if delay < 1 or max_jobs < 0 or max_pages < 0:
        raise ValueError("Can delay >= 1, max_jobs >= 0, max_pages >= 0")
    records, errors, robots_cache = [], [], {}
    visited_jobs, blocked_sites = set(), set()
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "vi,en;q=0.8"})

    def fetch(url: str) -> str:
        if not _allowed(url, session, robots_cache):
            raise PermissionError("robots.txt khong cho phep truy cap URL nay")
        try:
            response = session.get(url, timeout=20)
            if response.status_code in {401, 403, 429}:
                raise PermissionError(f"Website gioi han truy cap: HTTP {response.status_code}")
            response.raise_for_status()
            if _source(response.url) != _source(url):
                raise PermissionError("Redirect sang website khac")
            return response.text
        finally:
            time.sleep(delay)

    for seed_url in dict.fromkeys(urls):
        if max_jobs and len(records) >= max_jobs:
            break
        site = _source(seed_url)
        if site == "linkedin":
            errors.append({"url": seed_url,
                           "reason": "LinkedIn cam crawling khong duoc cap phep; bo qua."})
            continue
        if site not in JOB_PATTERNS:
            errors.append({"url": seed_url, "reason": "Nguon chua duoc ho tro."})
            continue
        if site in blocked_sites:
            continue
        if urlparse(seed_url).scheme not in {"http", "https"}:
            errors.append({"url": seed_url, "reason": "URL phai bat dau bang http(s)."})
            continue

        job_urls = []
        if _is_job_url(seed_url):
            job_urls = [_canonical_url(seed_url)]
        else:
            page_url, seen_pages = seed_url, set()
            seen_links = set()
            while not max_pages or len(seen_pages) < max_pages:
                if page_url in seen_pages:
                    break
                seen_pages.add(page_url)
                try:
                    html = fetch(page_url)
                except (requests.RequestException, RuntimeError, PermissionError) as exc:
                    errors.append({"url": page_url, "reason": str(exc)})
                    if isinstance(exc, PermissionError):
                        blocked_sites.add(site)
                    break
                links = find_job_links(html, page_url)
                print(f"[LIST] {site}: {page_url} -> {len(links)} links")
                fresh = [link for link in links if link not in seen_links]
                if not fresh:
                    errors.append({"url": page_url, "reason": "Trang khong co link moi; dung de tranh lap hoac bo qua loi HTML."})
                    break
                seen_links.update(fresh)
                job_urls.extend(links)
                next_url = find_next_page(html, page_url)
                if not next_url:
                    print(f"[LIST] {site}: khong tim thay lien ket trang tiep theo; chua the xac nhan da du tat ca trang")
                    break
                page_url = next_url
            if not job_urls:
                errors.append({"url": seed_url,
                               "reason": "Khong tim thay link tin chi tiet trong HTML. "
                                         "Hay xem lai HTML/selector, URL va quyen truy cap."})

        for job_url in dict.fromkeys(job_urls):
            if (max_jobs and len(records) >= max_jobs) or site in blocked_sites:
                break
            if job_url in visited_jobs:
                continue
            visited_jobs.add(job_url)
            try:
                html = fetch(job_url)
                record = parse_job_html(html, job_url, site)
                if record is None:
                    errors.append({"url": job_url, "reason": "Khong trich xuat du title + company"})
                    continue
                record['crawled_at'] = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
                records.append(record)
                print(f"[OK] {len(records)}: {record['job_title'][:70]}")
            except (requests.RequestException, RuntimeError, PermissionError) as exc:
                errors.append({"url": job_url, "reason": str(exc)})
                if isinstance(exc, PermissionError):
                    blocked_sites.add(site)

    return records, errors


def crawl_offline_html(folder: Path) -> tuple[list[dict], list[dict]]:
    """Chi de kiem thu parser, KHONG phai du lieu crawl live."""
    records, errors = [], []
    for path in sorted(folder.glob("*.html")):
        record = parse_job_html(path.read_text(encoding="utf-8"),
                                f"https://offline.fixture/{path.name}", "offline_fixture")
        if record:
            record['crawled_at'] = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
            records.append(record)
        else:
            errors.append({"url": str(path), "reason": "Khong parse duoc HTML fixture"})
    return records, errors


def save_crawl(records: list[dict], errors: list[dict], mode: str) -> dict:
    RAW_LIVE.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = RAW_LIVE / f"{mode}_{stamp}.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    result = {"mode": mode, "timestamp_utc": stamp, "rows": len(records),
              "errors": errors, "file": str(path)}
    (RAW_LIVE / f"{mode}_{stamp}_log.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result
