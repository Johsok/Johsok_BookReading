# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from findbook_writer import validate_highlights
from _hl_g11 import BODIES as B11
from _hl_g12 import BODIES as B12
from _hl_g13 import BODIES as B13
from _hl_g14 import BODIES as B14
from _hl_g04 import BODIES as B04

BOOKS = [
    ("02_psychology_growth-20260830-11", B11, "我喜歡這個功利的世界：這個世上，只要你敢，再大的不可能，都會變成可能", "咪蒙"),
    ("02_psychology_growth-20260830-12", B12, "超快速讀書法", "宇都出雅巳"),
    ("02_psychology_growth-20260830-13", B13, "驚人的油漆式速讀術：全民必備高效率記憶工具書！", "吳燦銘"),
    ("02_psychology_growth-20260830-14", B14, "一日一行動的奇蹟：我這樣化習慣為複利，9個月購置新屋，一年讀完520本書", "柳根瑢"),
    ("04_healthcare-20260830-03", B04, "即刻救牙！良心牙醫教你一口好牙咬到100歲！", "木野孔司、齊藤博"),
]

for book_id, bodies, title, author in BOOKS:
    print(f"{book_id} count={len(bodies)} unique={len(set(bodies))} min={min(len(b) for b in bodies)}")
    highlights = [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]
    try:
        validate_highlights(book_id, highlights, title, author)
        print("  OK")
    except ValueError as exc:
        print(f"  FAIL {exc}")
