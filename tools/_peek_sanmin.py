# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import findbook_scraper as s  # noqa: E402

url = "https://www.sanmin.com.tw/product/index/015588991"
html = s.fetch_html(url, referer="https://www.sanmin.com.tw/")
print("len", len(html))
title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
print("h1", s.strip_html(title_match.group(1)) if title_match else None)
for pat in [
    r"作者[：:]\s*(?:<a[^>]*>)?([^<]+)",
    r"編[著譯者]*[：:]\s*(?:<a[^>]*>)?([^<]+)",
    r"出版日期[：:]\s*([^<\n]+)",
    r"出版日期",
]:
    m = re.search(pat, html)
    print(pat, s.strip_html(m.group(1)) if m and m.lastindex else (m.group(0)[:40] if m else None))
# print a snippet around 作者
idx = html.find("作者")
print("idx", idx)
if idx >= 0:
    print(html[idx:idx+400])
