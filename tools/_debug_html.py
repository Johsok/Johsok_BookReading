# -*- coding: utf-8 -*-
from pathlib import Path
import re

html = Path("tools/_sample_page.html").read_text(encoding="utf-8")
for pat in [
    'class="title"',
    "mod_b",
    "msg",
    "type02_txt",
    "info",
    "book_name",
    "prod_name",
    "<h4",
    "author",
]:
    print(pat, html.count(pat))

idxs = [m.start() for m in re.finditer("0011055524", html)]
print("occ", len(idxs), idxs[:8])
# take a later occurrence that is likely in the list body
idx = idxs[min(5, len(idxs) - 1)]
chunk = html[max(0, idx - 200) : idx + 2000]
Path("tools/_sample_chunk2.html").write_text(chunk, encoding="utf-8")
print("---CHUNK---")
print(chunk)

# also find h4 near products
pairs = 0
for m in re.finditer(r'href="(https://www\.books\.com\.tw/products/\d+)"', html):
    start = m.start()
    window = html[start : start + 1200]
    if "<h4" in window:
        pairs += 1
        if pairs <= 2:
            print("PAIR", m.group(1))
            print(window[:400])
print("pairs_with_h4", pairs)
