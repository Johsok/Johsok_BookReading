# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import findbook_scraper as s  # noqa: E402

html = s.fetch_html(
    "https://search.books.com.tw/search/query/key/C%E8%AA%9E%E8%A8%80/cat/19/sort/1/v/1/page/1",
    referer="https://search.books.com.tw/",
)
print("search len", len(html))
for pat in ["products/", "item=", "0010", "mid=", "exen"]:
    print(pat, html.count(pat))
# unique hrefs containing 001
hrefs = set(re.findall(r'https?://[^"\']+', html))
print("http links", len(hrefs))
for u in sorted(hrefs):
    if any(x in u for x in ("product", "item", "0010", "book")):
        print(u[:140])

print("--- sanmin ---")
html2 = s.fetch_html(
    "https://www.sanmin.com.tw/search/index?kw=Linux&kind=1",
    referer="https://www.sanmin.com.tw/",
)
urls = re.findall(r"https://www\.sanmin\.com\.tw/product/index/\d+", html2)
print("sanmin product urls", len(urls), urls[:8])
print("relative", re.findall(r"/product/index/\d+", html2)[:8])
