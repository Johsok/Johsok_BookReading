# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
import ssl
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import findbook_scraper as s  # noqa: E402

existing = s.load_existing_keys(ROOT)
print("keys", len(existing))
for title, author in [
    ("C語言教學手冊（四版）", "洪維恩"),
    ("C語言教學手冊", "洪維恩"),
]:
    print("dup?", title, s.normalized_key(title, author) in existing)


def peek(url: str, label: str, n: int = 2500) -> str:
    html = s.fetch_html(url)
    print(label, "len", len(html), "title", s.strip_html((re.search(r"<title>(.*?)</title>", html, re.S | re.I) or re.match("a", "b")).group(1) if re.search(r"<title>(.*?)</title>", html, re.S | re.I) else ""))
    return html


html = peek(
    "https://www.sanmin.com.tw/search/index?kw=%E7%A8%8B%E5%BC%8F%E8%A8%AD%E8%A8%88&kind=1",
    "sanmin",
)
# href samples
hrefs = re.findall(r'href="([^"]+)"', html)
print("href sample")
for href in hrefs[:40]:
    if any(x in href.lower() for x in ("prod", "book", "search", "category")):
        print(" ", href[:120])

# product-like
for pat in ["Product", "product", "ISBN", "isbn", "bookNo"]:
    print(pat, html.lower().count(pat.lower()))

html2 = peek(
    "https://search.books.com.tw/search/query/key/程式設計/cat/19/sort/1/v/1/page/1",
    "books-search",
)
print("books parse", len(s.parse_books_list(html2)))
print("product links", len(re.findall(r"books\.com\.tw/products/001\d+", html2)))

html3 = peek("https://www.bookwalker.com.tw/search?c=6", "bookwalker")
print("bw product", len(re.findall(r"/product/", html3)))
for m in re.finditer(r'href="(/[^"]+)"[^>]*>(.{4,80})</a>', html3):
    title = s.strip_html(m.group(2))
    if s.has_han(title):
        print("BW", m.group(1)[:70], title[:40])
        break
