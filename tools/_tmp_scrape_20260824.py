# -*- coding: utf-8 -*-
"""Scrape Chinese new/hot books for FindBook 2026-08-24 batch (first 3 categories)."""
from __future__ import annotations

import json
import re
import time
import unicodedata
import urllib.error
import urllib.request
from datetime import date
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tools" / ".findbook_scrape_20260824.json"
PUNCT = re.compile(r"[\s\W_]+", re.UNICODE)
CJK = re.compile(r"[\u4e00-\u9fff]")
UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
}
FROM_DATE = date(2026, 7, 25)
TO_DATE = date(2026, 8, 24)
NEED = 8

URLS = {
    "01_business_startup": [
        "https://www.books.com.tw/web/books_nbtopm_02/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_02/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/books_nbtopm_02/?o=5&page=3&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=2&v=1",
        "https://www.books.com.tw/web/books_topm_02/?o=5&v=1",
        "https://www.books.com.tw/web/china_nbtopm_06/?o=5&v=1",
    ],
    "02_psychology_growth": [
        "https://www.books.com.tw/web/books_nbtopm_07/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_07/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=1&page=2&v=1",
        "https://www.books.com.tw/web/books_topm_07/?o=5&v=1",
        "https://www.books.com.tw/web/china_nbtopm_07/?o=5&v=1",
    ],
    "03_natural_science": [
        "https://www.books.com.tw/web/books_nbtopm_06/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_06/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/06/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/06/?o=1&page=2&v=1",
        "https://www.books.com.tw/web/books_topm_06/?o=5&v=1",
        "https://www.books.com.tw/web/china_nbtopm_10/?o=5&v=1",
    ],
}

KINGSTONE = {
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
}

TAAZE = {
    "01_business_startup": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=102000&d=",
    ],
    "02_psychology_growth": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=111000&d=",
    ],
    "03_natural_science": [
        "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=104000&d=",
    ],
}

LABELS = {
    "01_business_startup": "商業理財",
    "02_psychology_growth": "心理勵志",
    "03_natural_science": "自然科學",
}


def normalized_key(title: str, author: str) -> str:
    value = unicodedata.normalize("NFKC", f"{title}|{author}").casefold()
    return PUNCT.sub("", value)


def clean(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def parse_date(text: str) -> str:
    match = re.search(r"(20\d{2})[./年\-](\d{1,2})[./月\-](\d{1,2})", text)
    if not match:
        return ""
    return f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"


def in_range(published: str) -> bool:
    if not published:
        return True
    try:
        y, m, d = [int(x) for x in published.split("-")]
        value = date(y, m, d)
    except ValueError:
        return True
    return FROM_DATE <= value <= TO_DATE


def parse_books_list(html: str) -> list[dict]:
    items = []
    seen: set[str] = set()
    patterns = [
        r'<h4>\s*<a href="(https://www\.books\.com\.tw/products/[A-Z0-9]+)[^"]*"[^>]*>(.*?)</a>\s*</h4>(.*?)</ul>',
        r'<h3>\s*<a href="(https://www\.books\.com\.tw/products/[A-Z0-9]+)[^"]*"[^>]*>(.*?)</a>\s*</h3>(.*?)</ul>',
        r'<a href="(https://www\.books\.com\.tw/products/[A-Z0-9]+)[^"]*"[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</a>(.{0,900})',
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, html, re.S | re.I):
            url = match.group(1)
            if url in seen:
                continue
            title = clean(match.group(2))
            if not title or not CJK.search(title):
                continue
            block = match.group(3)
            author = ""
            am = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", block)
            if am:
                author = clean(am.group(1)).strip(" /|,，、")
            published = ""
            dm = re.search(r"出版日期[：:]\s*([0-9]{4}/[0-9]{1,2}/[0-9]{1,2})", block)
            if dm:
                published = parse_date(dm.group(1))
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
    tm = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if tm:
        title = clean(tm.group(1))
    author = ""
    am = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", html)
    if am:
        author = clean(am.group(1)).strip(" /|,，、")
    published = ""
    dm = re.search(r"出版日期[：:]\s*([0-9]{4}/[0-9]{1,2}/[0-9]{1,2})", html)
    if dm:
        published = parse_date(dm.group(1))
    return title, author, published


def parse_kingstone_list(html: str) -> list[dict]:
    items = []
    seen: set[str] = set()
    for match in re.finditer(
        r'<a[^>]+href="(https://www\.kingstone\.com\.tw/basic/\d+/?)[^"]*"[^>]*>(.*?)</a>',
        html,
        re.S,
    ):
        url = match.group(1).split("?")[0]
        if url in seen:
            continue
        title = clean(match.group(2))
        if not title or not CJK.search(title) or len(title) < 2:
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
    tm = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if tm:
        title = clean(tm.group(1))
    author = ""
    am = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", html)
    if am:
        author = clean(am.group(1)).strip(" /|,，、")
    published = parse_date(html)
    return title, author, published


def parse_taaze_list(html: str) -> list[dict]:
    items = []
    seen: set[str] = set()
    for match in re.finditer(
        r'href="(https://www\.taaze\.tw/products/\d+\.html)"[^>]*>\s*(.*?)\s*</a>',
        html,
        re.S,
    ):
        url = match.group(1)
        if url in seen:
            continue
        title = clean(match.group(2))
        if not title or not CJK.search(title) or len(title) < 4:
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
    tm = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if tm:
        title = clean(tm.group(1))
    author = ""
    am = re.search(r"作者[：:]\s*([^<\n]+)", html)
    if am:
        author = clean(am.group(1)).strip(" /|,，、")
    published = parse_date(html)
    return title, author, published


def main() -> None:
    manifest = json.loads((ROOT / "data.json").read_text(encoding="utf-8-sig"))
    existing = {
        normalized_key(str(book.get("title", "")), str(book.get("author", "")))
        for book in manifest.get("books", [])
    }
    log: list[str] = [f"existing={len(existing)}"]
    results: dict[str, list[dict]] = {}
    html_sample = ROOT / "tools" / ".findbook_scrape_20260824_sample.html"

    for category_id, urls in URLS.items():
        found: list[dict] = []
        seen: set[str] = set()
        for url in urls:
            try:
                html = fetch(url)
            except Exception as exc:  # noqa: BLE001
                log.append(f"FAIL\t{category_id}\t{url}\t{exc}")
                continue
            if not html_sample.exists():
                html_sample.write_text(html[:8000], encoding="utf-8")
            parsed = parse_books_list(html)
            added = 0
            for item in parsed:
                key = normalized_key(item["title"], item["author"])
                if key in existing or key in seen:
                    continue
                if item["published"] and not in_range(item["published"]):
                    continue
                seen.add(key)
                item["sourcePage"] = url
                item["sourceName"] = f"博客來中文書－{LABELS[category_id]}新書／暢銷頁"
                found.append(item)
                added += 1
            log.append(
                f"page\t{category_id}\tparsed={len(parsed)}\tadded={added}\ttotal={len(found)}"
            )
            time.sleep(0.35)
        results[category_id] = found
        log.append(f"CAT\t{category_id}\t{len(found)}")

    for category_id, items in results.items():
        kept: list[dict] = []
        for item in items:
            if len(kept) >= NEED:
                break
            if not item["published"] or not item["author"]:
                try:
                    html = fetch(item["sourceUrl"])
                    title, author, published = parse_books_detail(html)
                    if title:
                        item["title"] = title
                    if author:
                        item["author"] = author
                    if published:
                        item["published"] = published
                    time.sleep(0.25)
                except Exception as exc:  # noqa: BLE001
                    log.append(f"DETAIL_FAIL\t{item['sourceUrl']}\t{exc}")
            key = normalized_key(item["title"], item["author"])
            if key in existing or not item["author"] or not CJK.search(item["title"]):
                continue
            if item["published"] and not in_range(item["published"]):
                continue
            kept.append(item)
        results[category_id] = kept
        log.append(f"KEPT\t{category_id}\t{len(kept)}")

    for category_id, urls in KINGSTONE.items():
        if len(results.get(category_id, [])) >= NEED:
            continue
        seen = {
            normalized_key(item["title"], item["author"])
            for item in results.get(category_id, [])
        }
        for url in urls:
            if len(results[category_id]) >= NEED:
                break
            try:
                html = fetch(url)
            except Exception as exc:  # noqa: BLE001
                log.append(f"KS_FAIL\t{category_id}\t{url}\t{exc}")
                continue
            parsed = parse_kingstone_list(html)
            log.append(f"ks_page\t{category_id}\tparsed={len(parsed)}")
            for item in parsed:
                if len(results[category_id]) >= NEED:
                    break
                try:
                    detail = fetch(item["sourceUrl"])
                    title, author, published = parse_kingstone_detail(detail)
                    time.sleep(0.25)
                except Exception as exc:  # noqa: BLE001
                    log.append(f"KS_DETAIL_FAIL\t{item['sourceUrl']}\t{exc}")
                    continue
                title = title or item["title"]
                if not title or not CJK.search(title) or not author:
                    continue
                key = normalized_key(title, author)
                if key in existing or key in seen:
                    continue
                if published and not in_range(published):
                    continue
                seen.add(key)
                results[category_id].append(
                    {
                        "title": title,
                        "author": author,
                        "sourceUrl": item["sourceUrl"],
                        "published": published,
                        "sourceSite": "金石堂",
                        "sourcePage": url,
                        "sourceName": f"金石堂新書－{LABELS[category_id]}",
                    }
                )
            time.sleep(0.35)

    for category_id, urls in TAAZE.items():
        if len(results.get(category_id, [])) >= NEED:
            continue
        seen = {
            normalized_key(item["title"], item["author"])
            for item in results.get(category_id, [])
        }
        for url in urls:
            if len(results[category_id]) >= NEED:
                break
            try:
                html = fetch(url)
            except Exception as exc:  # noqa: BLE001
                log.append(f"TZ_FAIL\t{category_id}\t{url}\t{exc}")
                continue
            parsed = parse_taaze_list(html)
            log.append(f"tz_page\t{category_id}\tparsed={len(parsed)}")
            for item in parsed:
                if len(results[category_id]) >= NEED:
                    break
                try:
                    detail = fetch(item["sourceUrl"])
                    title, author, published = parse_taaze_detail(detail)
                    time.sleep(0.25)
                except Exception as exc:  # noqa: BLE001
                    log.append(f"TZ_DETAIL_FAIL\t{item['sourceUrl']}\t{exc}")
                    continue
                title = title or item["title"]
                if not title or not CJK.search(title) or not author:
                    continue
                key = normalized_key(title, author)
                if key in existing or key in seen:
                    continue
                if published and not in_range(published):
                    continue
                seen.add(key)
                results[category_id].append(
                    {
                        "title": title,
                        "author": author,
                        "sourceUrl": item["sourceUrl"],
                        "published": published,
                        "sourceSite": "讀冊",
                        "sourcePage": url,
                        "sourceName": f"讀冊新書－{LABELS[category_id]}",
                    }
                )

    payload = {"log": log, "results": results}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT}")
    for line in log:
        print(line)
    for category_id, items in results.items():
        print(f"RESULT {category_id} {len(items)}")
        for item in items:
            print(
                f"  {item.get('published') or 'no-date'}\t{item['title']}\t{item['author']}\t{item['sourceUrl']}"
            )


if __name__ == "__main__":
    main()
