# -*- coding: utf-8 -*-
from collections import Counter
from importlib.machinery import SourceFileLoader
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
code = (ROOT / "tools" / "_gen_batch46.py").read_text(encoding="utf-8")
loc = {"__file__": str(ROOT / "tools" / "_gen_batch46.py")}
exec(code.replace("assert len(BOOK46) == 150, len(BOOK46)", ""), loc, loc)
books = {
    "46": loc["BOOK46"],
    "47": SourceFileLoader("b47", str(ROOT / "tools/_batch46_b47.py")).load_module().BOOK47,
    "48": SourceFileLoader("b48", str(ROOT / "tools/_batch46_b48.py")).load_module().BOOK48,
    "49": SourceFileLoader("b49", str(ROOT / "tools/_batch46_b49.py")).load_module().BOOK49,
    "50": SourceFileLoader("b50", str(ROOT / "tools/_batch46_b50.py")).load_module().BOOK50,
}
suf = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
for label, bodies in books.items():
    starts = Counter(b[:18] for b in bodies if len(b) >= 18)
    sc = []
    for i, b in enumerate(bodies, 1):
        m = re.match(r"^([^：:]{1,12})[：:]", b)
        if m and not m.group(1).endswith(suf):
            sc.append(i)
    bad = [i for i, b in enumerate(bodies, 1) if len(b) < 12 or "本書" in b or "｜" in b]
    print(label, len(bodies), len(set(bodies)), "top", starts.most_common(3), "colon", sc, "bad", bad)
