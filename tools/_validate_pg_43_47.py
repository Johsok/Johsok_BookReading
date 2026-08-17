# -*- coding: utf-8 -*-
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402
from collections import Counter

text = Path(__file__).with_name("_gen_pg_43_47.py").read_text(encoding="utf-8")
ns = {}
start = text.find("B43 = [")
end = text.find("\nBOOKS =")
exec(text[start:end], ns)

meta = [
    ("02_psychology_growth-20260716-43", "全球人才搶著學！密涅瓦的思考習慣訓練", "李佳達、劉劭穎、黃禮宏", "B43"),
    ("02_psychology_growth-20260716-44", "原子習慣WORKBOOK【實踐本‧附練習別冊】", "詹姆斯．克利爾", "B44"),
    ("02_psychology_growth-20260716-45", "我們為什麼對好事麻木、對壞事容忍？：習慣化如何左右人生 (二手書)", "塔莉．沙羅特、凱斯．桑思坦", "B45"),
    ("02_psychology_growth-20260716-46", "鬆綁你的焦慮習慣：善用好奇心打破擔憂與恐懼的迴圈，有效戒除壞習慣的實證法則 (二手書)", "賈德森．布魯爾", "B46"),
    ("02_psychology_growth-20260716-47", "與成功有約：高效能人士的七個習慣（30週年全新增訂版） (二手書)", "史蒂芬．柯維、西恩．柯維", "B47"),
]
for book_id, title, author, key in meta:
    bodies = ns[key]
    hl = [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]
    try:
        validate_highlights(book_id, hl, title, author)
        starts = Counter(b[:18] for b in bodies)
        top = starts.most_common(3)
        print("OK", book_id, "top_starts", top)
    except Exception as e:
        print("FAIL", book_id, e)
        starts = Counter(b[:18] for b in bodies)
        print("  top", starts.most_common(8))
        short = [b for b in bodies if len(b) < 12]
        print("  short", short)
        dups = [b for b, c in Counter(bodies).items() if c > 1]
        print("  dups", dups)
