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
SKIP = ("簡體", "简体", "漫畫", "Minecraft")


def parse_sanmin_urls(html: str) -> list[str]:
    urls = re.findall(r"https://www\.sanmin\.com\.tw/product/index/\d+", html)
    seen = []
    used = set()
    for url in urls:
        if url in used:
            continue
        used.add(url)
        seen.append(url)
    return seen


def parse_sanmin_detail(html: str) -> tuple[str, str, str]:
    title = ""
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if title_match:
        title = s.strip_html(title_match.group(1))
    author = ""
    for pat in (
        r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)",
        r"編[著譯者]*[：:]\s*(?:<a[^>]*>)?([^<]+)",
    ):
        m = re.search(pat, html)
        if m:
            author = s.strip_html(m.group(1)).strip(" /|,，、")
            if author and s.has_han(author) or author:
                break
    published = s.parse_iso_date(html)
    return title, author, published


def main() -> None:
    existing_keys = s.load_existing_keys(ROOT)
    seen: set[str] = set()
    found: list[dict] = []

    def take(item: dict, source_name: str) -> None:
        if len(found) >= 6:
            return
        title = str(item.get("title") or "")
        if any(x in title for x in SKIP):
            return
        item = dict(item)
        item["sourceName"] = source_name
        key = s._accept_item(item, existing_keys, seen, FROM_DATE, TO_DATE, "06_computer_info")
        if not key:
            return
        seen.add(key)
        cand = s.to_candidate(item, "06_computer_info", FROM_DATE, TO_DATE)
        cand["workId"] = WORK_ID
        found.append(cand)
        print("ACCEPT", cand.get("published"), cand["title"], cand["author"])

    # 博客來舊品
    pages = [
        "https://www.books.com.tw/web/sys_saletopb/books/19/?o=1&v=1",
        "https://www.books.com.tw/web/books_topm_19/?o=5&v=1",
        "https://www.books.com.tw/web/books_topm_19/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/books_topm_19/?o=5&page=3&v=1",
    ]
    parsed = []
    for _url, html in s._fetch_pages_parallel(pages, "https://www.books.com.tw/", print):
        parsed.extend(s.parse_books_list(html))
    for item in parsed:
        pid = s.BOOKS_PID_RE.search(item.get("sourceUrl") or "")
        if pid and pid.group(1) >= "0010930000":
            continue
        take(item, "博客來中文書－電腦資訊經典暢銷榜")

    queries = [
        "https://www.sanmin.com.tw/search/index?kw=Linux&kind=1",
        "https://www.sanmin.com.tw/search/index?kw=Excel&kind=1",
        "https://www.sanmin.com.tw/search/index?kw=Java&kind=1",
        "https://www.sanmin.com.tw/search/index?kw=%E8%B3%87%E6%96%99%E7%B5%90%E6%A7%8B&kind=1",
        "https://www.sanmin.com.tw/search/index?kw=Photoshop&kind=1",
        "https://www.sanmin.com.tw/search/index?kw=%E7%A8%8B%E5%BC%8F%E8%A8%AD%E8%A8%88&kind=1",
    ]
    urls: list[str] = []
    for page in queries:
        try:
            html = s.fetch_html(page, referer="https://www.sanmin.com.tw/")
        except Exception as exc:  # noqa: BLE001
            print("FAIL", page, exc)
            continue
        found_urls = parse_sanmin_urls(html)
        print(page, "urls", len(found_urls))
        urls.extend(found_urls)

    uniq = []
    used = set()
    for url in urls:
        if url in used:
            continue
        used.add(url)
        uniq.append({"title": "", "author": "", "sourceUrl": url, "published": "", "sourceSite": "三民"})

    extra = s._enrich_parallel(
        uniq[:24],
        parse_sanmin_detail,
        "https://www.sanmin.com.tw/",
        12,
        None,
        print,
        "三民",
    )
    for item in extra:
        take(item, "三民暢銷－電腦資訊")

    print("TOTAL", len(found))
    payload = json.dumps(found, ensure_ascii=False, indent=2)
    (ROOT / "tools" / ".findbook_candidates_findbook-20260913-1938.json").write_text(
        json.dumps({"06_computer_info": found}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
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
        raise SystemExit(f"committed {len(committed)}")
    print("IDS", ",".join(committed))


if __name__ == "__main__":
    main()
