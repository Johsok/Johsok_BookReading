# -*- coding: utf-8 -*-
"""Scrape Books.com.tw / Kingstone for 2026-08-18 evening FindBook batch."""
from __future__ import annotations

import json
import re
import time
import unicodedata
import urllib.request
from datetime import date
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tools" / ".findbook_scrape_20260818_2102.json"
PUNCT = re.compile(r"[\s\W_]+", re.UNICODE)
CJK = re.compile(r"[\u4e00-\u9fff]")
UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}
FROM_DATE = date(2026, 7, 19)
TO_DATE = date(2026, 8, 18)

URLS = {
    "01_business_startup": [
        "https://www.books.com.tw/web/books_nbtopm_02/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_02/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/books_nbtopm_02/?o=5&page=3&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=1",
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


def parse_books_list(html: str) -> list[dict]:
    items = []
    seen_urls: set[str] = set()
    for match in re.finditer(
        r'<h4>\s*<a href="(https://www\.books\.com\.tw/products/[A-Z0-9]+)[^"]*"[^>]*>(.*?)</a>\s*</h4>'
        r'(.*?)</ul>',
        html,
        re.S,
    ):
        source_url = match.group(1)
        if source_url in seen_urls:
            continue
        title = clean(match.group(2))
        if not title or not CJK.search(title):
            continue
        block = match.group(3)
        author_match = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", block)
        if not author_match:
            continue
        author = clean(author_match.group(1)).strip(" /|,，、")
        if not author:
            continue
        date_match = re.search(r"出版日期[：:]\s*([0-9]{4}/[0-9]{1,2}/[0-9]{1,2})", block)
        published = date_match.group(1).replace("/", "-") if date_match else ""
        if published:
            parts = published.split("-")
            published = f"{parts[0]}-{int(parts[1]):02d}-{int(parts[2]):02d}"
        seen_urls.add(source_url)
        items.append(
            {
                "title": title,
                "author": author,
                "sourceUrl": source_url,
                "published": published,
                "sourceSite": "博客來",
            }
        )
    return items


def parse_kingstone_list(html: str) -> list[dict]:
    items = []
    seen_urls: set[str] = set()
    for match in re.finditer(
        r'<a[^>]+href="(https://www\.kingstone\.com\.tw/basic/\d+/?)[^"]*"[^>]*>(.*?)</a>',
        html,
        re.S,
    ):
        source_url = match.group(1).split("?")[0]
        if source_url in seen_urls:
            continue
        title = clean(match.group(2))
        if not title or not CJK.search(title) or len(title) < 2:
            continue
        seen_urls.add(source_url)
        items.append(
            {
                "title": title,
                "author": "",
                "sourceUrl": source_url,
                "published": "",
                "sourceSite": "金石堂",
            }
        )
    return items


def parse_books_detail(html: str) -> tuple[str, str]:
    author = ""
    author_match = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", html)
    if author_match:
        author = clean(author_match.group(1)).strip(" /|,，、")
    date_match = re.search(r"出版日期[：:]\s*([0-9]{4}/[0-9]{1,2}/[0-9]{1,2})", html)
    published = ""
    if date_match:
        parts = date_match.group(1).split("/")
        published = f"{parts[0]}-{int(parts[1]):02d}-{int(parts[2]):02d}"
    return author, published


def parse_kingstone_detail(html: str) -> tuple[str, str, str]:
    title = ""
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if title_match:
        title = clean(title_match.group(1))
    author = ""
    author_match = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", html)
    if author_match:
        author = clean(author_match.group(1)).strip(" /|,，、")
    date_match = re.search(
        r"出版日[期期]?[：:]\s*([0-9]{4})[./年-]([0-9]{1,2})[./月-]([0-9]{1,2})",
        html,
    )
    published = ""
    if date_match:
        published = f"{date_match.group(1)}-{int(date_match.group(2)):02d}-{int(date_match.group(3)):02d}"
    return title, author, published


def in_range(published: str) -> bool:
    if not published:
        return True
    try:
        y, m, d = [int(x) for x in published.split("-")]
        value = date(y, m, d)
    except ValueError:
        return True
    return FROM_DATE <= value <= TO_DATE


def main() -> None:
    manifest = json.loads((ROOT / "data.json").read_text(encoding="utf-8-sig"))
    existing = {
        normalized_key(str(book.get("title", "")), str(book.get("author", "")))
        for book in manifest.get("books", [])
    }
    log_lines = [f"existing={len(existing)}"]
    results: dict[str, list[dict]] = {}

    for category_id, urls in URLS.items():
        found: list[dict] = []
        seen: set[str] = set()
        for url in urls:
            try:
                html = fetch(url)
            except Exception as exc:  # noqa: BLE001
                log_lines.append(f"FAIL\t{category_id}\t{url}\t{exc}")
                continue
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
                item["sourceName"] = f"博客來中文書－{LABELS[category_id]}新書／分類頁"
                found.append(item)
                added += 1
            log_lines.append(
                f"page\t{category_id}\tparsed={len(parsed)}\tadded={added}\ttotal={len(found)}"
            )
            time.sleep(0.4)
        results[category_id] = found
        log_lines.append(f"CAT\t{category_id}\t{len(found)}")

    # Fill details for books missing dates; keep only in-range after detail fetch.
    for category_id, items in results.items():
        kept: list[dict] = []
        for item in items:
            if not item["published"] or not item["author"]:
                try:
                    html = fetch(item["sourceUrl"])
                    author, published = parse_books_detail(html)
                    if author:
                        item["author"] = author
                    if published:
                        item["published"] = published
                    time.sleep(0.25)
                except Exception as exc:  # noqa: BLE001
                    log_lines.append(f"DETAIL_FAIL\t{item['sourceUrl']}\t{exc}")
            key = normalized_key(item["title"], item["author"])
            if key in existing:
                continue
            if item["published"] and not in_range(item["published"]):
                continue
            if not CJK.search(item["title"]):
                continue
            kept.append(item)
            if len(kept) >= 12:
                break
        results[category_id] = kept
        log_lines.append(f"KEPT\t{category_id}\t{len(kept)}")

    # Kingstone fallback if a category is still short.
    for category_id, urls in KINGSTONE.items():
        if len(results.get(category_id, [])) >= 8:
            continue
        seen = {
            normalized_key(item["title"], item["author"])
            for item in results.get(category_id, [])
        }
        for url in urls:
            try:
                html = fetch(url)
            except Exception as exc:  # noqa: BLE001
                log_lines.append(f"KS_FAIL\t{category_id}\t{url}\t{exc}")
                continue
            parsed = parse_kingstone_list(html)
            log_lines.append(f"ks_page\t{category_id}\tparsed={len(parsed)}")
            for item in parsed:
                if len(results[category_id]) >= 12:
                    break
                try:
                    detail = fetch(item["sourceUrl"])
                    title, author, published = parse_kingstone_detail(detail)
                    time.sleep(0.25)
                except Exception as exc:  # noqa: BLE001
                    log_lines.append(f"KS_DETAIL_FAIL\t{item['sourceUrl']}\t{exc}")
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
            if len(results[category_id]) >= 12:
                break

    payload = {"log": log_lines, "results": results}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = ROOT / "tools" / ".findbook_scrape_20260818_2102_summary.txt"
    lines = []
    for category_id, items in results.items():
        lines.append(f"{category_id}\t{len(items)}")
        for item in items:
            lines.append(
                f"  {item.get('published') or 'no-date'}\t{item['title']}\t{item['author']}\t{item['sourceUrl']}"
            )
    lines.extend(log_lines)
    summary.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    for category_id, items in results.items():
        print(f"{category_id} {len(items)}")


if __name__ == "__main__":
    main()
