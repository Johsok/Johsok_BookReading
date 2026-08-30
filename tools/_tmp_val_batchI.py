# -*- coding: utf-8 -*-
import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from findbook_writer import validate_highlights
from _gen_batchI_holiday import BODIES

BOOK_ID = "01_business_startup-20260830-19"
TITLE = "世界頂尖人士如何度過他們的「假日」：被媒體譽為一年之初的必讀之書，引發壓倒性話題"
AUTHOR = "越川慎司"

print("count", len(BODIES), "unique", len(set(BODIES)))
print("min", min(len(b) for b in BODIES), "max", max(len(b) for b in BODIES))
starts = Counter(b[:18] for b in BODIES)
print("top starts", starts.most_common(8))
for i, b in enumerate(BODIES, 1):
    if TITLE in b or AUTHOR in b or "本書" in b or "作者指出" in b or "本章" in b or "這一章" in b or "｜" in b:
        print("forbidden", i, b)
    if "：" in b[:13] or ":" in b[:13]:
        print("colon?", i, b[:20])
highlights = [f"{i:03d}、{b}" for i, b in enumerate(BODIES, 1)]
validate_highlights(BOOK_ID, highlights, TITLE, AUTHOR)
print("OK")
out = Path(__file__).with_name(".findbook_results_20260830_batchI.json")
out.write_text(
    json.dumps([{"id": BOOK_ID, "highlights": highlights}], ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)
print("wrote", out)
