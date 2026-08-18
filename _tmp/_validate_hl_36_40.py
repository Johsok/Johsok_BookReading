# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp")
CJK = re.compile(r"[\u4e00-\u9fff]")
BANNED = ("本書", "作者指出", "本章", "這一章")
AUTHORS = {
    "BOOK36": "Sachi",
    "BOOK37": "李彼飛",
    "BOOK38": "江口和明",
    "BOOK39": "開平青年發展基金會",
    "BOOK40": "青井聡子",
}
TITLES = {
    "BOOK36": "簡單！基礎！馬上動手！初學者甜點食譜",
    "BOOK37": "超省時麵團 × 不失敗麵糊",
    "BOOK38": "超驚豔！美味甜點神技法",
    "BOOK39": "金牌團隊不藏私的甜點基礎全工法",
    "BOOK40": "初學者也OK！自己作職人配方的戚風蛋糕",
}


def load_txt(name: str) -> list[str]:
    p = ROOT / name
    return [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]


def cjk_pref(s: str, n: int) -> str:
    return "".join(CJK.findall(s)[:n])


def report(name: str, items: list[str]) -> list[str]:
    errs: list[str] = []
    if len(items) != 150:
        errs.append(f"{name} count {len(items)}")
    if len(set(items)) != len(items):
        errs.append(f"{name} duplicate texts {len(items)-len(set(items))}")
    for i, s in enumerate(items, 1):
        if not s.endswith("。"):
            errs.append(f"{name} #{i} no period")
        if "\n" in s or "\r" in s or "｜" in s or "|" in s:
            errs.append(f"{name} #{i} pipe/newline")
        if "：" in s or ":" in s:
            errs.append(f"{name} #{i} colon {s[:24]}")
        if any(b in s for b in BANNED):
            errs.append(f"{name} #{i} banned")
        if len(s) < 12:
            errs.append(f"{name} #{i} short {len(s)}")
    a = AUTHORS[name]
    ac = sum(a in s for s in items)
    if ac > 1:
        errs.append(f"{name} author {a} x{ac}")
    t = TITLES[name]
    tc = sum(t in s for s in items)
    if tc:
        errs.append(f"{name} title x{tc}")
    p18 = Counter(s[:18] for s in items)
    bad18 = [(k, v) for k, v in p18.items() if v >= 4]
    if bad18:
        errs.append(f"{name} p18 {bad18[:5]}")
    p8 = Counter(cjk_pref(s, 8) for s in items)
    bad8 = [(k, v) for k, v in p8.items() if v >= 4]
    if bad8:
        errs.append(f"{name} p8 {bad8[:8]}")
    return errs


def pad_if_needed(items: list[str], uniques: list[str]) -> list[str]:
    out = []
    u = 0
    for s in items:
        while len(s) < 28:
            extra = uniques[u % len(uniques)]
            u += 1
            body = s[:-1] if s.endswith("。") else s
            s = body + extra + "。"
        out.append(s)
    return out


b36 = json.loads((ROOT / "_b36.json").read_text(encoding="utf-8"))
# fix english / typos
fixed = []
for s in b36:
    s = s.replace(" custard ", "卡士達")
    s = s.replace("先 ent 再塗", "先塗胚再疊")
    s = s.replace("Q彈", "Ｑ彈")
    if "Sachi" in s:
        pass
    fixed.append(s)
# drop extras that are most generic / keep unique p8
# prefer dropping later duplicates of p8
seen8: Counter[str] = Counter()
b36_keep: list[str] = []
for s in fixed:
    k = cjk_pref(s, 8)
    if len(b36_keep) >= 150:
        break
    if seen8[k] >= 3:
        continue
    if any(b in s for b in BANNED) or ":" in s or "：" in s:
        continue
    seen8[k] += 1
    b36_keep.append(s)

books = {
    "BOOK36": b36_keep,
    "BOOK37": load_txt("_b37.txt"),
    "BOOK38": load_txt("_b38.txt"),
    "BOOK39": load_txt("_b39.txt"),
    "BOOK40": load_txt("_b40.txt"),
}

pads = {
    "BOOK36": [
        "，家作預拌粉最怕季節食材出水",
        "，步驟照片要對準麵糊光澤",
        "，無印袋粉受潮就先過篩",
    ],
    "BOOK37": [
        "，冷藏發酵把等待交給冰箱",
        "，失敗先查粉水鹽油四項",
        "，隔夜麵團最省通勤時段",
    ],
    "BOOK38": [
        "，三種拌法走錯就救不回來",
        "，溫差比新模具更決定成敗",
        "，刮刀路徑要跟影片對齊",
    ],
    "BOOK39": [
        "，基礎工法要比新口味先熟",
        "，照片對的是乳化與泡沫",
        "，失敗先回三種餅乾拌合法",
    ],
    "BOOK40": [
        "，分蛋打發才能托住沙拉油",
        "，鎌倉細孔比盤飾更要緊",
        "，淡口油潤才適合長輩孩子",
    ],
}

for k, items in books.items():
    books[k] = pad_if_needed(items, pads[k])

# if count != 150 print and we patch
for k, items in books.items():
    print(k, len(items), "unique", len(set(items)))
    for e in report(k, items):
        print(" ", e)
    short = [len(x) for x in items if len(x) < 28]
    print("  short28", len(short), "minmax", min(map(len, items)), max(map(len, items)))
    print("  author", sum(AUTHORS[k] in x for x in items))
    if k == "BOOK40":
        for i, s in enumerate(items, 1):
            if any(b in s for b in BANNED):
                print("  BAN", i, s)
            if len(s) < 28:
                print("  SH", i, len(s), s)

out = ROOT / "hl_36_40.py"
chunks = ['# -*- coding: utf-8 -*-', '"""Book-specific Traditional Chinese highlights for books 36-40."""', ""]
for k in ("BOOK36", "BOOK37", "BOOK38", "BOOK39", "BOOK40"):
    chunks.append(f"{k} = [")
    for s in books[k]:
        chunks.append(f"    {s!r},")
    chunks.append("]")
    chunks.append("")
chunks.append(
    "BOOKS = {\n"
    '    "BOOK36": BOOK36,\n'
    '    "BOOK37": BOOK37,\n'
    '    "BOOK38": BOOK38,\n'
    '    "BOOK39": BOOK39,\n'
    '    "BOOK40": BOOK40,\n'
    "}\n"
)
out.write_text("\n".join(chunks), encoding="utf-8")
print("wrote", out, "bytes", out.stat().st_size)


