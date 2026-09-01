# -*- coding: utf-8 -*-
"""Scrape Chinese new/hot books: 博客來 first, then 金石堂／讀冊 if quota remains."""
from __future__ import annotations

import argparse
import json
import re
import ssl
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime
from html import unescape
from pathlib import Path
from typing import Callable

HAS_HAN = re.compile(r"[\u4e00-\u9fff]")
PUNCT = re.compile(r"[\s\W_]+", re.UNICODE)
DATE_RE = re.compile(r"(20\d{2})[./年\-](\d{1,2})[./月\-](\d{1,2})")
PRODUCT_ID_RE = re.compile(r"/products/([A-Z0-9]+)", re.I)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

CATEGORY_LABELS = {
    "01_business_startup": "商業理財",
    "02_psychology_growth": "心理勵志",
    "03_natural_science": "自然科學",
    "04_healthcare": "醫療保健",
    "05_food_wellness": "飲食養生",
    "06_computer_info": "電腦資訊",
    "07_other": "其他",
}

DEFAULT_TAGS = {
    "01_business_startup": ["商業", "投資", "創業", "理財"],
    "02_psychology_growth": ["心理", "勵志", "成長", "情緒"],
    "03_natural_science": ["科學", "自然", "科普"],
    "04_healthcare": ["醫療", "健康", "保健"],
    "05_food_wellness": ["飲食", "營養", "養生"],
    "06_computer_info": ["電腦", "資訊", "科技"],
    "07_other": ["其他", "生活", "人文"],
}

BOOKS_URLS = {
    "01_business_startup": [
        "https://www.books.com.tw/web/books_nbtopm_02/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_02/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/books_topm_02/?o=5&v=1",
    ],
    "02_psychology_growth": [
        "https://www.books.com.tw/web/books_nbtopm_07/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_07/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/books_topm_07/?o=5&v=1",
    ],
    "03_natural_science": [
        "https://www.books.com.tw/web/books_nbtopm_06/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_06/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/06/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/books_topm_06/?o=5&v=1",
    ],
    "04_healthcare": [
        "https://www.books.com.tw/web/books_nbtopm_08/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_08/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/08/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/books_topm_08/?o=5&v=1",
    ],
    "05_food_wellness": [
        "https://www.books.com.tw/web/books_nbtopm_09/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_09/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/09/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/books_topm_09/?o=5&v=1",
    ],
    "06_computer_info": [
        "https://www.books.com.tw/web/books_nbtopm_19/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_19/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/19/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/books_topm_19/?o=5&v=1",
    ],
    "07_other": [
        "https://www.books.com.tw/web/books_nbtopm_01/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_04/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_05/?o=5&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/04/?o=1&page=1&v=1",
    ],
}

KINGSTONE_URLS = {
    "01_business_startup": [
        "https://www.kingstone.com.tw/newbook/book/business/",
        "https://www.kingstone.com.tw/monthpublish/book/ea/",
    ],
    "02_psychology_growth": [
        "https://www.kingstone.com.tw/newbook/book/psycho/",
        "https://www.kingstone.com.tw/monthpublish/book/eg/",
    ],
    "03_natural_science": [
        "https://www.kingstone.com.tw/newbook/book/nature/",
        "https://www.kingstone.com.tw/monthpublish/book/ei/",
    ],
    "04_healthcare": [
        "https://www.kingstone.com.tw/newbook/book/health/",
        "https://www.kingstone.com.tw/monthpublish/book/ek/",
    ],
    "05_food_wellness": [
        "https://www.kingstone.com.tw/newbook/book/food/",
        "https://www.kingstone.com.tw/monthpublish/book/el/",
    ],
    "06_computer_info": [
        "https://www.kingstone.com.tw/newbook/book/computer/",
        "https://www.kingstone.com.tw/monthpublish/book/en/",
    ],
    "07_other": [
        "https://www.kingstone.com.tw/newbook/book/literature/",
        "https://www.kingstone.com.tw/newbook/book/humanity/",
    ],
}

TAAZE_URLS = {
    "01_business_startup": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=102000&d=",
        "https://www.taaze.tw/rwdList.html?t=24&k=&c=102000",
    ],
    "02_psychology_growth": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=111000&d=",
        "https://www.taaze.tw/rwdList.html?t=24&k=&c=111000",
    ],
    "03_natural_science": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=104000&d=",
        "https://www.taaze.tw/rwdList.html?t=24&k=&c=104000",
    ],
    "04_healthcare": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=108000&d=",
        "https://www.taaze.tw/rwdList.html?t=24&k=&c=108000",
    ],
    "05_food_wellness": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=109000&d=",
        "https://www.taaze.tw/rwdList.html?t=24&k=&c=109000",
    ],
    "06_computer_info": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=119000&d=",
        "https://www.taaze.tw/rwdList.html?t=24&k=&c=119000",
    ],
    "07_other": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=101000&d=",
        "https://www.taaze.tw/rwdList.html?t=24&k=&c=101000",
    ],
}

LogFn = Callable[[str], None]
StopFn = Callable[[], bool]


def normalized_key(title: str, author: str) -> str:
    value = unicodedata.normalize("NFKC", f"{title}|{author}").casefold()
    return PUNCT.sub("", value)


def has_han(title: str) -> bool:
    return bool(HAS_HAN.search(title or ""))


def strip_html(html: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_iso_date(text: str) -> str:
    match = DATE_RE.search(text or "")
    if not match:
        return ""
    return f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"


def in_date_range(published: str, from_date: str, to_date: str) -> bool:
    if not published:
        return True
    try:
        value = date.fromisoformat(published)
        start = date.fromisoformat(from_date)
        end = date.fromisoformat(to_date)
    except ValueError:
        return True
    return start <= value <= end


def fetch_html(url: str, referer: str = "") -> str:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
    }
    if referer:
        headers["Referer"] = referer
    request = urllib.request.Request(url, headers=headers)
    contexts = [ssl.create_default_context(), ssl._create_unverified_context()]
    last_error: Exception | None = None
    for context in contexts:
        try:
            with urllib.request.urlopen(request, timeout=12, context=context) as response:
                raw = response.read()
            return raw.decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            continue
    raise last_error or RuntimeError(f"無法讀取 {url}")


def parse_books_list(html: str) -> list[dict]:
    items: list[dict] = []
    seen: set[str] = set()
    patterns = [
        r'<h4>\s*<a href="(https://www\.books\.com\.tw/products/[A-Z0-9]+)[^"]*"[^>]*>(.*?)</a>\s*</h4>(.*?)</ul>',
        r'<h3>\s*<a href="(https://www\.books\.com\.tw/products/[A-Z0-9]+)[^"]*"[^>]*>(.*?)</a>\s*</h3>(.*?)</ul>',
        r'<a href="(https://www\.books\.com\.tw/products/[A-Z0-9]+)[^"]*"[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</a>(.{0,1200})',
        r'href="(https://www\.books\.com\.tw/products/[A-Z0-9]+)[^"]*"[^>]*>(.*?)</a>',
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, html, re.S | re.I):
            url = match.group(1).split("?")[0]
            if url in seen:
                continue
            title = strip_html(match.group(2))
            if not title or not has_han(title) or len(title) < 2:
                continue
            block = match.group(3) if match.lastindex and match.lastindex >= 3 else ""
            author = ""
            published = ""
            if block:
                author_match = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", block)
                if author_match:
                    author = strip_html(author_match.group(1)).strip(" /|,，、")
                date_match = re.search(r"出版日期[：:]\s*([0-9]{4}/[0-9]{1,2}/[0-9]{1,2})", block)
                if date_match:
                    published = parse_iso_date(date_match.group(1))
            seen.add(url)
            items.append(
                {
                    "title": title,
                    "author": author,
                    "sourceUrl": url,
                    "published": published,
                    "sourceSite": "博客來",
                }
            )
    return items


def parse_books_detail(html: str) -> tuple[str, str, str]:
    title = ""
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if title_match:
        title = strip_html(title_match.group(1))
    author = ""
    author_match = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", html)
    if author_match:
        author = strip_html(author_match.group(1)).strip(" /|,，、")
    published = ""
    date_match = re.search(r"出版日期[：:]\s*([0-9]{4}/[0-9]{1,2}/[0-9]{1,2})", html)
    if date_match:
        published = parse_iso_date(date_match.group(1))
    if not published:
        published = parse_iso_date(strip_html(html[:8000]))
    return title, author, published


def parse_kingstone_list(html: str) -> list[dict]:
    items: list[dict] = []
    seen: set[str] = set()
    for match in re.finditer(
        r'<a[^>]+href="(https://www\.kingstone\.com\.tw/basic/\d+/?)[^"]*"[^>]*>(.*?)</a>',
        html,
        re.S | re.I,
    ):
        url = match.group(1).split("?")[0]
        if url in seen:
            continue
        title = strip_html(match.group(2))
        if not title or not has_han(title) or len(title) < 2:
            continue
        seen.add(url)
        items.append(
            {
                "title": title,
                "author": "",
                "sourceUrl": url,
                "published": "",
                "sourceSite": "金石堂",
            }
        )
    return items


def parse_kingstone_detail(html: str) -> tuple[str, str, str]:
    title = ""
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if title_match:
        title = strip_html(title_match.group(1))
    author = ""
    author_match = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", html)
    if author_match:
        author = strip_html(author_match.group(1)).strip(" /|,，、")
    return title, author, parse_iso_date(html)


def parse_taaze_list(html: str) -> list[dict]:
    items: list[dict] = []
    seen: set[str] = set()
    for match in re.finditer(
        r'href="(https://www\.taaze\.tw/products/\d+\.html)"[^>]*>\s*(.*?)\s*</a>',
        html,
        re.S | re.I,
    ):
        url = match.group(1)
        if url in seen:
            continue
        title = strip_html(match.group(2))
        if not title or not has_han(title) or len(title) < 2:
            continue
        seen.add(url)
        items.append(
            {
                "title": title,
                "author": "",
                "sourceUrl": url,
                "published": "",
                "sourceSite": "讀冊",
            }
        )
    return items


def parse_taaze_detail(html: str) -> tuple[str, str, str]:
    title = ""
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if title_match:
        title = strip_html(title_match.group(1))
    author = ""
    author_match = re.search(r"作者[：:]\s*([^<\n]+)", html)
    if author_match:
        author = strip_html(author_match.group(1)).strip(" /|,，、")
    return title, author, parse_iso_date(html)


def _stopped(should_stop: StopFn | None) -> bool:
    return bool(should_stop and should_stop())


def _log(log: LogFn | None, message: str) -> None:
    if log:
        log(message)


def enrich_if_needed(
    item: dict,
    parse_detail,
    referer: str,
    should_stop: StopFn | None,
) -> dict:
    """Fill author from the detail page only when the list row has no author."""
    if item.get("author"):
        return item
    if _stopped(should_stop):
        return item
    html = fetch_html(item["sourceUrl"], referer=referer)
    title, author, published = parse_detail(html)
    if title:
        item["title"] = title
    if author:
        item["author"] = author
    if published:
        item["published"] = published
    return item


def to_candidate(item: dict, category_id: str, from_date: str, to_date: str) -> dict:
    label = CATEGORY_LABELS[category_id]
    published = str(item.get("published") or "")
    today = datetime.now().date().isoformat()
    if published:
        date_note = (
            f"來源標示出版日期為 {published}；擷取日期 {today}，"
            f"落在 {from_date} 至 {to_date} 的搜尋區間內。"
        )
    else:
        date_note = "來源未提供明確日期"
    title = str(item["title"]).strip()
    author = str(item["author"]).strip()
    extra = [part for part in title.replace("：", " ").replace(":", " ").split() if has_han(part)][:3]
    tags = list(DEFAULT_TAGS[category_id]) + extra
    return {
        "title": title,
        "author": author,
        "sourceName": str(item.get("sourceName") or f"{item.get('sourceSite')}新書－{label}"),
        "sourceUrl": str(item["sourceUrl"]).strip(),
        "sourceDateNote": date_note,
        "tags": tags,
        "summary": (
            f"整理「{title}」在{label}領域的核心觀念、判斷方法、適用情境與可實踐行動。"
        ),
        "published": published,
        "sourceSite": item.get("sourceSite", ""),
    }


def _fetch_pages_parallel(pages: list[str], referer: str, log: LogFn | None) -> list[tuple[str, str]]:
    """Fetch list pages in parallel. Failed URLs are skipped."""
    if not pages:
        return []
    results: list[tuple[str, str]] = []

    def _one(url: str) -> tuple[str, str]:
        return url, fetch_html(url, referer=referer)

    workers = min(4, len(pages))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_one, url): url for url in pages}
        for future in as_completed(futures):
            url = futures[future]
            try:
                results.append(future.result())
            except Exception as exc:  # noqa: BLE001
                _log(log, f"列表失敗：{url} ({exc})")
    return results


def _accept_item(
    item: dict,
    existing_keys: set[str],
    seen_keys: set[str],
    from_date: str,
    to_date: str,
) -> str:
    """Return the dedupe key if the row is usable; otherwise empty."""
    title = str(item.get("title") or "")
    author = str(item.get("author") or "")
    if not has_han(title) or not author:
        return ""
    key = normalized_key(title, author)
    if key in existing_keys or key in seen_keys:
        return ""
    published = str(item.get("published") or "")
    if published and not in_date_range(published, from_date, to_date):
        return ""
    return key


def _enrich_parallel(
    items: list[dict],
    parse_detail,
    referer: str,
    limit: int,
    should_stop: StopFn | None,
    log: LogFn | None,
    source_site: str,
) -> list[dict]:
    """Fetch detail pages only for rows still missing an author."""
    if not items or limit <= 0:
        return []
    filled: list[dict] = []

    def _one(raw: dict) -> dict:
        return enrich_if_needed(raw, parse_detail, referer, should_stop)

    workers = min(4, len(items), max(1, limit))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_one, raw) for raw in items]
        for future in as_completed(futures):
            if _stopped(should_stop) or len(filled) >= limit:
                break
            try:
                item = future.result()
            except Exception as exc:  # noqa: BLE001
                _log(log, f"{source_site} 詳情失敗：{exc}")
                continue
            if item.get("author"):
                filled.append(item)
    return filled


def _collect_from_pages(
    pages: list[str],
    parse_list,
    parse_detail,
    source_site: str,
    source_name: str,
    referer: str,
    category_id: str,
    from_date: str,
    to_date: str,
    existing_keys: set[str],
    seen_keys: set[str],
    buffer: int,
    should_stop: StopFn | None,
    log: LogFn | None,
) -> list[dict]:
    found: list[dict] = []
    if not pages or buffer <= 0 or _stopped(should_stop):
        return found

    parsed_items: list[dict] = []
    for page_url, html in _fetch_pages_parallel(pages, referer, log):
        parsed = parse_list(html)
        _log(log, f"{source_site} {page_url} 解析 {len(parsed)} 筆")
        parsed_items.extend(parsed)

    ready: list[dict] = []
    missing_author: list[dict] = []
    for raw in parsed_items:
        title = str(raw.get("title") or "")
        if not has_han(title):
            continue
        if raw.get("author"):
            ready.append(raw)
        else:
            missing_author.append(raw)

    def _take(item: dict) -> bool:
        if len(found) >= buffer or _stopped(should_stop):
            return False
        key = _accept_item(item, existing_keys, seen_keys, from_date, to_date)
        if not key:
            return False
        seen_keys.add(key)
        item["sourceSite"] = source_site
        item["sourceName"] = source_name
        found.append(to_candidate(item, category_id, from_date, to_date))
        return True

    for raw in ready:
        if not _take(raw) and len(found) >= buffer:
            break

    remaining = buffer - len(found)
    if remaining > 0 and missing_author and not _stopped(should_stop):
        extra = missing_author[: remaining * 2]
        for item in _enrich_parallel(
            extra, parse_detail, referer, remaining, should_stop, log, source_site
        ):
            if not _take(item) and len(found) >= buffer:
                break
    return found


def scrape_category(
    category_id: str,
    from_date: str,
    to_date: str,
    existing_keys: set[str],
    quota: int,
    should_stop: StopFn | None = None,
    log: LogFn | None = None,
) -> list[dict]:
    """Find extra Chinese candidates for one category. Caller stops at quota after reserve."""
    if category_id not in CATEGORY_LABELS:
        raise ValueError(f"未知主題：{category_id}")
    buffer = quota + 1
    label = CATEGORY_LABELS[category_id]
    seen_keys: set[str] = set()
    collected: list[dict] = []

    sources = [
        (
            BOOKS_URLS[category_id],
            parse_books_list,
            parse_books_detail,
            "博客來",
            f"博客來中文書－{label}新書／暢銷頁",
            "https://www.books.com.tw/",
        ),
        (
            KINGSTONE_URLS[category_id],
            parse_kingstone_list,
            parse_kingstone_detail,
            "金石堂",
            f"金石堂新書－{label}",
            "https://www.kingstone.com.tw/",
        ),
        (
            TAAZE_URLS[category_id],
            parse_taaze_list,
            parse_taaze_detail,
            "讀冊",
            f"讀冊新書－{label}",
            "https://www.taaze.tw/",
        ),
    ]
    for pages, parse_list, parse_detail, site, name, referer in sources:
        if _stopped(should_stop) or len(collected) >= buffer:
            break
        _log(log, f"開始抓 {site}／{label}，目標緩衝 {buffer} 本")
        batch = _collect_from_pages(
            pages,
            parse_list,
            parse_detail,
            site,
            name,
            referer,
            category_id,
            from_date,
            to_date,
            existing_keys,
            seen_keys,
            buffer - len(collected),
            should_stop,
            log,
        )
        collected.extend(batch)
        _log(log, f"{site}／{label} 累計合格 {len(collected)} 本")
    return collected


def load_existing_keys(root: Path) -> set[str]:
    """Build title+author keys from data.json only; do not open book files."""
    manifest = json.loads((root / "data.json").read_text(encoding="utf-8-sig"))
    return {
        normalized_key(str(book.get("title", "")), str(book.get("author", "")))
        for book in manifest.get("books", [])
    }


def scrape_categories(
    category_ids: list[str],
    from_date: str,
    to_date: str,
    existing_keys: set[str],
    quota: int,
    should_stop: StopFn | None = None,
    log: LogFn | None = None,
) -> dict[str, list[dict]]:
    """Scrape several categories in parallel."""
    results: dict[str, list[dict]] = {}
    if not category_ids:
        return results
    workers = min(4, len(category_ids))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(
                scrape_category,
                category_id,
                from_date,
                to_date,
                existing_keys,
                quota,
                should_stop,
                log,
            ): category_id
            for category_id in category_ids
        }
        for future in as_completed(futures):
            category_id = futures[future]
            results[category_id] = future.result()
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="FindBook list-page scraper")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--category-ids", required=True, help="Comma-separated categoryId list")
    parser.add_argument("--quota", type=int, required=True)
    parser.add_argument("--from-date", required=True)
    parser.add_argument("--to-date", required=True)
    parser.add_argument("--out", required=True, help="JSON object keyed by categoryId")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    category_ids = [item.strip() for item in args.category_ids.split(",") if item.strip()]
    existing_keys = load_existing_keys(root)
    payload = scrape_categories(
        category_ids,
        args.from_date,
        args.to_date,
        existing_keys,
        args.quota,
        log=print,
    )
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(len(items) for items in payload.values())
    print(f"wrote {out_path} categories={len(payload)} candidates={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
