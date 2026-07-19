# -*- coding: utf-8 -*-
"""Scrape alternate sources: Kingstone, Taaze for remaining quotas."""
from __future__ import annotations

import json
import re
import time
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
    ),
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
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


def parse_kingstone(html: str) -> list[dict]:
    items = []
    seen = set()
    # Kingstone product cards vary; try multiple patterns
    for match in re.finditer(
        r'href="(https://www\.kingstone\.com\.tw/basic/\d+/[^"]*)"[^>]*>'
        r'(.*?)</a>',
        html,
        re.S,
    ):
        url = match.group(1).split("?")[0]
        title = clean(match.group(2))
        if not title or not CJK.search(title) or len(title) < 4:
            continue
        if url in seen:
            continue
        # author often nearby in parent block — take next 600 chars after link
        start = match.end()
        window = html[start : start + 800]
        author = ""
        am = re.search(r"作者[：:]\s*([^<\n]+)", window)
        if am:
            author = clean(am.group(1))
        if not author:
            am = re.search(r'class="[^"]*author[^"]*"[^>]*>(.*?)</', window, re.S)
            if am:
                author = clean(am.group(1))
        if not author or len(author) < 2:
            continue
        author = author.split("/")[0].strip(" /|,，、")
        seen.add(url)
        items.append({"title": title, "author": author, "sourceUrl": url})
    return items


def parse_taaze(html: str) -> list[dict]:
    items = []
    seen = set()
    for match in re.finditer(
        r'href="(https://www\.taaze\.tw/products/\d+\.html)"[^>]*>\s*(.*?)\s*</a>',
        html,
        re.S,
    ):
        url = match.group(1)
        title = clean(match.group(2))
        if not title or not CJK.search(title) or len(title) < 4:
            continue
        if url in seen:
            continue
        window = html[match.end() : match.end() + 900]
        author = ""
        am = re.search(r"作者[：:]\s*([^<\n]+)", window)
        if am:
            author = clean(am.group(1))
        if not author:
            continue
        seen.add(url)
        items.append({"title": title, "author": author.strip(" /|,，、"), "sourceUrl": url})
    return items


def parse_books(html: str) -> list[dict]:
    items = []
    seen = set()
    for match in re.finditer(
        r'<h4>\s*<a href="(https://www\.books\.com\.tw/products/\d+)[^"]*"[^>]*>(.*?)</a>\s*</h4>'
        r'(.*?)</ul>',
        html,
        re.S,
    ):
        url = match.group(1)
        if url in seen:
            continue
        title = clean(match.group(2))
        if not title or not CJK.search(title):
            continue
        am = re.search(r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)", match.group(3))
        if not am:
            continue
        author = clean(am.group(1)).strip(" /|,，、")
        seen.add(url)
        items.append({"title": title, "author": author, "sourceUrl": url})
    return items


SOURCES = {
    "02_psychology_growth": [
        ("kingstone", "https://www.kingstone.com.tw/book/book_page.asp?id_class1=4&id_class2=41", "灰熊/金石堂心理"),
        ("kingstone", "https://www.kingstone.com.tw/book/?class_id=41", "金石堂心理"),
        ("taaze", "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=111000&d=", "讀冊心理"),
        ("books", "https://www.books.com.tw/web/books_nbtopm_07/?o=5&page=1&v=1", "博客來心理"),
        ("books", "https://www.books.com.tw/web/sys_nbmidme/books/07/?o=5&v=1", "博客來心理新書"),
    ],
    "03_natural_science": [
        ("kingstone", "https://www.kingstone.com.tw/book/?class_id=23", "金石堂自然科學"),
        ("taaze", "https://www.taaze.tw/rwd_listView.html?t=11&k=&c=104000&d=", "讀冊自然科普"),
        ("books", "https://www.books.com.tw/web/books_topm_06/?o=5&v=1", "博客來自然科學"),
        ("books", "https://www.books.com.tw/web/books_nbtopm_06/?o=5&v=1", "博客來自然新書"),
        ("books", "https://www.books.com.tw/web/sys_topme/books/06/?o=5&page=1&v=1", "博客來自然暢銷"),
        ("books", "https://www.books.com.tw/web/china_nbtopm_10/?o=5&v=1", "博客來簡體科普"),
    ],
}


PARSERS = {
    "kingstone": parse_kingstone,
    "taaze": parse_taaze,
    "books": parse_books,
}


def main() -> None:
    manifest = json.loads((ROOT / "data.json").read_text(encoding="utf-8-sig"))
    existing = {
        normalized_key(str(book.get("title", "")), str(book.get("author", "")))
        for book in manifest.get("books", [])
    }
    current = json.loads((ROOT / "tools" / ".findbook_scrape_20260719.json").read_text(encoding="utf-8"))

    time.sleep(2)
    for category_id, sources in SOURCES.items():
        found = current.setdefault(category_id, [])
        seen = {normalized_key(item["title"], item["author"]) for item in found}
        for kind, url, label in sources:
            try:
                html = fetch(url)
            except Exception as exc:  # noqa: BLE001
                print(f"FAIL\t{category_id}\t{kind}\t{exc}")
                time.sleep(1)
                continue
            Path(f"tools/_alt_{category_id}_{kind}.html").write_text(html, encoding="utf-8")
            parsed = PARSERS[kind](html)
            added = 0
            for item in parsed:
                key = normalized_key(item["title"], item["author"])
                if key in existing or key in seen:
                    continue
                seen.add(key)
                item["sourcePage"] = url
                item["sourceName"] = f"{label}分類頁"
                found.append(item)
                added += 1
            print(f"page\t{category_id}\t{kind}\tparsed={len(parsed)}\tadded={added}\ttotal={len(found)}")
            time.sleep(1.2)
        print(f"CAT\t{category_id}\t{len(found)}")

    out = ROOT / "tools" / ".findbook_scrape_20260719.json"
    out.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")
    for category_id in ("02_psychology_growth", "03_natural_science"):
        items = current.get(category_id, [])
        print(f"summary\t{category_id}\t{len(items)}")


if __name__ == "__main__":
    main()
