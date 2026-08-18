# -*- coding: utf-8 -*-
from importlib.machinery import SourceFileLoader
from pathlib import Path

src = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\hl_b08_b09_b10.py")
fix = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_fix_hl_b08_10.py")
theme = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_retheme_hl.py")

ns = {}
exec(fix.read_text(encoding="utf-8").split("def apply_repl")[0], ns)
ns2 = {}
exec(theme.read_text(encoding="utf-8").split("m = SourceFileLoader")[0], ns2)

ALL_PADS = set(ns["PADS"]) | set(ns2.get("P08", [])) | set(ns2.get("P09", [])) | set(ns2.get("P10", []))
# theme file exec first part may not include P08 if split is wrong
text = theme.read_text(encoding="utf-8")
for name in ("P08", "P09", "P10"):
    if name in ns2:
        ALL_PADS.update(ns2[name])

# parse P08/P09/P10 from theme file directly
import re as _re
for block in _re.findall(r"P0[89] = \"\"\"(.*?)\"\"\"", text, _re.S):
    ALL_PADS.update(x.strip() for x in block.strip().splitlines() if x.strip())
for block in _re.findall(r"P10 = \"\"\"(.*?)\"\"\"", text, _re.S):
    ALL_PADS.update(x.strip() for x in block.strip().splitlines() if x.strip())

PADS = sorted(ALL_PADS, key=len, reverse=True)
m = SourceFileLoader("hl", str(src)).load_module()

GEN = {
    "b08": [
        "，並依體質與節氣斟酌",
        "，食療仍以當季新鮮為先",
        "，禁忌欄比食譜步驟更重要",
        "，份量以能消化為上限",
        "，挑選烹煮都要對準時令",
        "，合寒熱比跟風進補穩當",
    ],
    "b09": [
        "，養胃節奏比補品堆疊重要",
        "，順食中庸才能長久",
        "，胃氣能化才談其他補法",
        "，熱食細嚼比空胃硬補妥當",
        "，正餐仍在藥膳香料之前",
        "，腹感與二便用來校對對錯",
    ],
    "b10": [
        "，此為該派主張而非醫令",
        "，重點在潔氣減渣與呼吸",
        "，讀作宇宙論實踐宣稱即可",
        "，固體負擔被其說成退化方向",
        "，揮發性氣體才被稱為真養分",
        "，實踐仍以空氣品質與減量為核",
    ],
}


def strip_pads(s):
    changed = True
    while changed:
        changed = False
        for p in PADS:
            if p and s.endswith(p) and len(s) - len(p) >= 18:
                s = s[: -len(p)]
                changed = True
                break
        for p in sum(GEN.values(), []):
            if s.endswith(p) and len(s) - len(p) >= 18:
                s = s[: -len(p)]
                changed = True
                break
    return s


def extend(s, pads):
    if 28 <= len(s) <= 55:
        return s
    t = s
    i = hash(s) % len(pads)
    guard = 0
    while len(t) < 28 and guard < 6:
        extra = pads[i % len(pads)]
        i += 1
        if extra in t:
            continue
        if len(t) + len(extra) <= 55:
            t += extra
        else:
            t = (t + extra)[:55]
        guard += 1
    if not (28 <= len(t) <= 55):
        raise RuntimeError(len(t), t)
    return t


out = {k: [extend(strip_pads(s), GEN[k]) for s in xs] for k, xs in m.BOOKS.items()}
lines = ["# -*- coding: utf-8 -*-", "BOOKS = {"]
for k, xs in out.items():
    lines.append(f"{k!r}: [")
    for s in xs:
        lines.append(f"    {s!r},")
    lines.append("],")
lines.append("}")
src.write_text("\n".join(lines) + "\n", encoding="utf-8")
print({k: (len(v), min(map(len, v)), max(map(len, v))) for k, v in out.items()})
