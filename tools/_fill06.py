# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import findbook_scraper as s  # noqa: E402
import findbook_writer as w  # noqa: E402

WORK_ID = "findbook-20260913-1938"
FROM_DATE = "1986-09-13"
TO_DATE = "2021-09-13"


def parse_sanmin(html: str) -> list[dict]:
    items = []
    seen = set()
    for match in re.finditer(r'href="(/product/index/\d+)"', html, re.I):
        url = "https://www.sanmin.com.tw" + match.group(1)
        if url in seen:
            continue
        seen.add(url)
        items.append(
            {
                "title": "",
                "author": "",
                "sourceUrl": url,
                "published": "",
                "sourceSite": "三民",
            }
        )
    return items


def parse_sanmin_detail(html: str) -> tuple[str, str, str]:
    title = ""
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if title_match:
        title = s.strip_html(title_match.group(1))
    author = ""
    for pat in (
        r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)",
        r"著[者]?[：:]\s*(?:<a[^>]*>)?([^<]+)",
        r'"author"\s*:\s*"([^"]+)"',
    ):
        author_match = re.search(pat, html)
        if author_match:
            author = s.strip_html(author_match.group(1)).strip(" /|,，、")
            if author:
                break
    published = s.parse_iso_date(html)
    return title, author, published


def pid_ok(url: str) -> bool:
    match = s.BOOKS_PID_RE.search(url)
    if not match:
        return True
    return match.group(1) < "0010930000"


def take(item: dict, existing_keys: set[str], seen: set[str], found: list, source_name: str) -> None:
    if len(found) >= 6:
        return
    item = dict(item)
    item["sourceName"] = source_name
    if item.get("sourceSite") == "博客來" and not pid_ok(item.get("sourceUrl") or ""):
        return
    if re.search(r"简体|簡體|漫畫|Minecraft", str(item.get("title") or "")):
        return
    key = s._accept_item(item, existing_keys, seen, FROM_DATE, TO_DATE, "06_computer_info")
    if not key:
        return
    seen.add(key)
    cand = s.to_candidate(item, "06_computer_info", FROM_DATE, TO_DATE)
    cand["workId"] = WORK_ID
    found.append(cand)
    print("ACCEPT", cand.get("published"), "|", cand["title"], "|", cand["author"], "|", cand["sourceUrl"])


def main() -> None:
    existing_keys = s.load_existing_keys(ROOT)
    seen: set[str] = set()
    found: list[dict] = []

    print("博客來 old pid")
    pages = [
        "https://www.books.com.tw/web/sys_saletopb/books/19/?o=1&v=1",
        "https://www.books.com.tw/web/books_topm_19/?o=5&v=1",
        "https://www.books.com.tw/web/books_topm_19/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/books_topm_19/?o=5&page=3&v=1",
    ]
    parsed = []
    for _url, html in s._fetch_pages_parallel(pages, "https://www.books.com.tw/", print):
        parsed.extend(s.parse_books_list(html))
    print("parsed", len(parsed))
    for item in parsed:
        take(item, existing_keys, seen, found, "博客來中文書－電腦資訊經典暢銷榜")

    if len(found) < 6:
        print("三民 product pages")
        search_urls = [
            "https://www.sanmin.com.tw/search/index?kw=%E7%A8%8B%E5%BC%8F%E8%A8%AD%E8%A8%88&kind=1",
            "https://www.sanmin.com.tw/search/index?kw=Excel&kind=1",
            "https://www.sanmin.com.tw/search/index?kw=Linux&kind=1",
            "https://www.sanmin.com.tw/search/index?kw=%E8%B3%87%E6%96%99%E7%B5%90%E6%A7%8B&kind=1",
        ]
        need = []
        for page in search_urls:
            html = s.fetch_html(page, referer="https://www.sanmin.com.tw/")
            rows = parse_sanmin(html)
            print("sanmin", page, "rows", len(rows))
            need.extend(rows)
        extra = s._enrich_parallel(
            need[:20],
            parse_sanmin_detail,
            "https://www.sanmin.com.tw/",
            8,
            None,
            print,
            "三民",
        )
        for item in extra:
            take(item, existing_keys, seen, found, "三民暢銷－電腦資訊")

    print("TOTAL", len(found))
    if len(found) < 5:
        raise SystemExit("computer quota unmet")

    committed = []
    for candidate in found:
        if len(committed) >= 5:
            break
        result = w.reserve_one(ROOT, "06_computer_info", candidate, FROM_DATE, TO_DATE)
        print(result)
        if result.get("status") == "committed":
            committed.append(result["id"])
    if len(committed) != 5:
        raise SystemExit(f"computer committed {len(committed)}")
    print("IDS", ",".join(committed))


if __name__ == "__main__":
    main()
