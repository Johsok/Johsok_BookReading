# -*- coding: utf-8 -*-
import re
from pathlib import Path
from collections import Counter

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp")
ns = {}
exec((root / "hl_food_b02_b03_b04.py").read_text(encoding="utf-8").split("print")[0], ns)
exec((root / "hl_b03_b04_rest.py").read_text(encoding="utf-8"), ns)

b02 = ns["b02"]
b03 = ns["b03"][:49] + ns["b03_rest"]
b04 = ns["b04"]

BOOKS = {"b02": b02, "b03": b03, "b04": b04}

FORBIDDEN = ["本書", "作者指出", "本章", "這一章"]
CHAPTER = re.compile(r"第.章")
CJK = re.compile(r"[\u4e00-\u9fff]")
TITLES = [
    "飲食養生法",
    "這樣吃就對了",
    "提升生命能量的飲食養生術",
    "食經概論",
    "飲食養生大全",
    "陳存仁",
    "吳季華",
    "謝文全",
]


def cjk_chars(s):
    return "".join(CJK.findall(s))


def check(key, xs):
    issues = []
    if len(xs) != 150:
        issues.append(f"COUNT {len(xs)}")
    if len(set(xs)) != len(xs):
        issues.append("DUP_FULL")
        c = Counter(xs)
        issues.extend(f"  fulldup {v} {k}" for k, v in c.items() if v > 1)
    p18 = [x[:18] for x in xs]
    if len(set(p18)) != len(p18):
        issues.append("DUP_P18")
        c = Counter(p18)
        issues.extend(f"  p18 {v} {k}" for k, v in c.items() if v > 1)
    p8 = [cjk_chars(x)[:8] for x in xs]
    c8 = Counter(p8)
    bad8 = [(k, v) for k, v in c8.items() if v >= 4]
    if bad8:
        issues.append("P8_GE4")
        issues.extend(f"  {v} {k}" for k, v in bad8)
    for i, s in enumerate(xs, 1):
        if "：" in s or ":" in s:
            issues.append(f"{i} COLON {s}")
        if "｜" in s or "|" in s:
            issues.append(f"{i} PIPE {s}")
        for f in FORBIDDEN:
            if f in s:
                issues.append(f"{i} FORB {f} {s}")
        if CHAPTER.search(s):
            issues.append(f"{i} CHAPTER {s}")
        for t in TITLES:
            if t in s:
                issues.append(f"{i} TITLE {t} {s}")
        if re.search(r".面第.步", s) or re.search(r"第\d+步", s):
            issues.append(f"{i} STEP {s}")
        letters = "".join(ch for ch in s if ch.isascii() and ch.isalpha())
        if letters:
            issues.append(f"{i} EN:{letters} {s}")
        n = len(cjk_chars(s))
        if n < 12:
            issues.append(f"{i} SHORT{n} {s}")
        if n < 28 or n > 55:
            issues.append(f"{i} LEN{n} {s}")
        if s.startswith(("飲食", "養生", "身體")):
            issues.append(f"{i} BADSTART {s}")
    return issues


out = []
for k, xs in BOOKS.items():
    out.append(f"=== {k} {len(xs)} ===")
    iss = check(k, xs)
    out.extend(iss if iss else ["OK"])

(root / "_chk_food_hl.txt").write_text("\n".join(out), encoding="utf-8")

py = ["BOOKS = {"]
for k, xs in BOOKS.items():
    py.append(f'    "{k}": [')
    for s in xs:
        py.append(f"        {s!r},")
    py.append("    ],")
py.append("}")
(root / "BOOKS_b02_b03_b04.py").write_text("\n".join(py) + "\n", encoding="utf-8")
print("\n".join(out))
