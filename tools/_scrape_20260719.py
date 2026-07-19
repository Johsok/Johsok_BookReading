# -*- coding: utf-8 -*-
"""Scrape Books.com.tw for new Chinese book candidates (fixed author parsing)."""
from __future__ import annotations

import json
import re
import unicodedata
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUNCT = re.compile(r"[\s\W_]+", re.UNICODE)
CJK = re.compile(r"[\u4e00-\u9fff]")
UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}

URLS = {
    "01_business_startup": [
        "https://www.books.com.tw/web/books_nbtopm_02/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_02/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/books_nbtopm_02/?o=5&page=3&v=1",
        "https://www.books.com.tw/web/books_bmidm_0209/?o=5&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=3&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=4&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/02/?o=1&page=5&v=1",
    ],
    "02_psychology_growth": [
        "https://www.books.com.tw/web/books_nbtopm_07/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_07/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=1&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=1&page=3&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=1&page=4&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=1&page=5&v=1",
    ],
    "03_natural_science": [
        "https://www.books.com.tw/web/books_nbtopm_06/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_06/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/books_nbtopm_06/?o=5&page=3&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/06/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/sys_topme/books/06/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/sys_topme/books/06/?o=1&page=2&v=1",
    ],
    "04_healthcare": [
        "https://www.books.com.tw/web/books_nbtopm_08/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_08/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/08/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/08/?o=1&page=2&v=1",
        "https://www.books.com.tw/web/sys_topme/books/08/?o=1&page=1&v=1",
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
        "https://www.books.com.tw/web/books_nbtopm_04/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_04/?o=5&page=2&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/04/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/sys_nbmidme/books/04/?o=1&page=2&v=1",
        "https://www.books.com.tw/web/sys_compub/books/04/?o=1&page=1&v=1",
    ],
}

LABELS = {
    "01_business_startup": "商業理財",
    "02_psychology_growth": "心理勵志",
    "03_natural_science": "自然科學",
    "04_healthcare": "醫療保健",
    "05_food_wellness": "飲食養生",
    "06_computer_info": "電腦資訊",
    "07_other": "其他",
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


def parse_items(html: str) -> list[dict]:
    """Parse books.com.tw list cards: h4 title + msg author."""
    items = []
    seen_urls: set[str] = set()
    for match in re.finditer(
        r'<h4>\s*<a href="(https://www\.books\.com\.tw/products/\d+)[^"]*"[^>]*>(.*?)</a>\s*</h4>'
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
        author = ""
        author_match = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", block)
        if author_match:
            author = clean(author_match.group(1))
        if not author:
            continue
        author = author.strip(" /|,，、")
        seen_urls.add(source_url)
        items.append({"title": title, "author": author, "sourceUrl": source_url})
    return items


def main() -> None:
    manifest = json.loads((ROOT / "data.json").read_text(encoding="utf-8-sig"))
    existing = {
        normalized_key(str(book.get("title", "")), str(book.get("author", "")))
        for book in manifest.get("books", [])
    }
    print(f"existing={len(existing)}")

    results: dict[str, list[dict]] = {}
    for category_id, urls in URLS.items():
        found: list[dict] = []
        seen: set[str] = set()
        for url in urls:
            try:
                html = fetch(url)
            except Exception as exc:  # noqa: BLE001
                print(f"FAIL\t{category_id}\t{url}\t{exc}")
                continue
            parsed = parse_items(html)
            new_count = 0
            for item in parsed:
                key = normalized_key(item["title"], item["author"])
                if key in existing or key in seen:
                    continue
                seen.add(key)
                item["sourcePage"] = url
                item["sourceName"] = f"博客來中文書－{LABELS[category_id]}分類頁"
                found.append(item)
                new_count += 1
            print(f"page\t{category_id}\tparsed={len(parsed)}\tnew={new_count}\ttotal={len(found)}")
        results[category_id] = found
        print(f"CAT\t{category_id}\t{len(found)}")

    out = ROOT / "tools" / ".findbook_scrape_20260719.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote\t{out}")
    for category_id, items in results.items():
        sample = items[0]["title"] if items else None
        print(f"summary\t{category_id}\t{len(items)}\t{sample}")


if __name__ == "__main__":
    main()
