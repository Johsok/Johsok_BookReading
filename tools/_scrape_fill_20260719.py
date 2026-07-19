# -*- coding: utf-8 -*-
"""Fill missing candidates for psychology (+1) and natural science (+10)."""
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
    "02_psychology_growth": [
        "https://www.books.com.tw/web/books_topm_07/?o=5&v=1",
        "https://www.books.com.tw/web/books_bmidm_0701/?o=5&v=1",
        "https://www.books.com.tw/web/books_bmidm_0705/?o=5&v=1",
        "https://www.books.com.tw/web/sys_topme/books/07/?o=5&v=1",
        "https://www.books.com.tw/web/sys_topme/books/07/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/china_nbtopm_07/?o=5&v=1",
        "https://www.books.com.tw/web/sys_midme/china/0405/?o=5&v=1",
    ],
    "03_natural_science": [
        "https://www.books.com.tw/web/books_topm_06/?o=5&v=1",
        "https://www.books.com.tw/web/books_bmidm_0601/?o=5&v=1",
        "https://www.books.com.tw/web/books_bmidm_0602/?o=5&v=1",
        "https://www.books.com.tw/web/books_bmidm_0603/?o=5&v=1",
        "https://www.books.com.tw/web/books_bmidm_0605/?o=5&v=1",
        "https://www.books.com.tw/web/sys_topme/books/06/?o=5&v=1",
        "https://www.books.com.tw/web/sys_topme/books/06/?o=1&page=1&v=1",
        "https://www.books.com.tw/web/sys_topme/books/06/?o=1&page=2&v=1",
        "https://www.books.com.tw/web/china_nbtopm_10/?o=5&v=1",
        "https://www.books.com.tw/web/sys_pcbtopm/china/10/?o=5&v=1",
        "https://www.books.com.tw/web/sys_topme/china/10/?o=5&v=1",
        "https://www.books.com.tw/web/books_nbtopm_06/?o=1&v=1",
        "https://www.books.com.tw/web/books_nbtopm_06/?o=3&v=1",
    ],
}

LABELS = {
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


def parse_items(html: str) -> list[dict]:
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
        author_match = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", block)
        if not author_match:
            continue
        author = clean(author_match.group(1)).strip(" /|,，、")
        if not author:
            continue
        seen_urls.add(source_url)
        items.append({"title": title, "author": author, "sourceUrl": source_url})
    return items


def main() -> None:
    manifest = json.loads((ROOT / "data.json").read_text(encoding="utf-8-sig"))
    existing = {
        normalized_key(str(book.get("title", "")), str(book.get("author", "")))
        for book in manifest.get("books", [])
    }
    current = json.loads((ROOT / "tools" / ".findbook_scrape_20260719.json").read_text(encoding="utf-8"))
    for category_id, urls in URLS.items():
        found = current.setdefault(category_id, [])
        seen = {normalized_key(item["title"], item["author"]) for item in found}
        for url in urls:
            try:
                html = fetch(url)
            except Exception as exc:  # noqa: BLE001
                print(f"FAIL\t{category_id}\t{url}\t{exc}")
                continue
            parsed = parse_items(html)
            added = 0
            for item in parsed:
                key = normalized_key(item["title"], item["author"])
                if key in existing or key in seen:
                    continue
                seen.add(key)
                item["sourcePage"] = url
                item["sourceName"] = f"博客來中文書－{LABELS[category_id]}分類頁"
                found.append(item)
                added += 1
            print(f"page\t{category_id}\tparsed={len(parsed)}\tadded={added}\ttotal={len(found)}")
        print(f"CAT\t{category_id}\t{len(found)}")

    out = ROOT / "tools" / ".findbook_scrape_20260719.json"
    out.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")
    print("done")
    for category_id in ("02_psychology_growth", "03_natural_science"):
        items = current.get(category_id, [])
        print(category_id, len(items))
        for item in items[:12]:
            print(" -", item["title"][:40], "/", item["author"][:20])


if __name__ == "__main__":
    main()
