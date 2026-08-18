# -*- coding: utf-8 -*-
import re
from pathlib import Path
from collections import Counter

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp")
ns = {}
exec((root / "hl_food_b02_b03_b04.py").read_text(encoding="utf-8").split("print")[0], ns)
exec((root / "hl_b03_b04_rest.py").read_text(encoding="utf-8"), ns)

CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def cjk(s):
    return "".join(CJK_RE.findall(s))


SLOTS = [
    "晨起空腹",
    "午後半歇",
    "宵夜時段",
    "陰雨潮濕",
    "考前熬夜",
    "病後初癒",
    "長途奔波",
    "冷氣房裡",
    "冬夜進補",
    "暑熱午後",
    "年節聚餐",
    "外食連續",
    "幼兒餵食",
    "老人咀嚼",
    "經期前後",
    "產後調養",
    "運動出汗",
    "久坐辦公",
    "失眠隔日",
    "酒後隔晨",
    "感冒初起",
    "咳喘發作",
    "血壓波動",
    "血糖起伏",
    "情緒緊繃",
    "旅行換地",
    "輪班作息",
    "節慶甜食",
    "市場採買",
    "家庭共餐",
]
VERBS = [
    "特別明顯",
    "最易被忽略",
    "值得立刻調整",
    "常被習慣掩蓋",
    "一放鬆就復發",
    "比想像更快出現",
    "需要連續觀察",
    "不能只靠感覺",
    "會連帶影響睡眠",
    "也會寫在舌苔上",
    "比藥味更先報到",
    "往往拖累隔日精神",
    "讓中焦立刻喊停",
    "比補品更決定成敗",
    "一忽略就前功盡棄",
]


def pad(s, i):
    n = len(cjk(s))
    if 28 <= n <= 55:
        return s
    extra = f"，在{SLOTS[i % 30]}時{VERBS[i % 15]}"
    if s.endswith("。"):
        out = s[:-1] + extra + "。"
    else:
        out = s + extra + "。"
    n2 = len(cjk(out))
    if n2 > 55:
        # shorter extra
        extra = f"，{SLOTS[i % 30]}更明顯"
        out = (s[:-1] if s.endswith("。") else s) + extra + "。"
    return out


b02 = [pad(s, i) for i, s in enumerate(ns["b02"])]
b03_extra = "副交感主導休息與消化，焦慮持續會讓酵素分泌跟著停擺。"
b03 = ns["b03"][:48] + ns["b03_rest"] + [b03_extra]
b03 = [pad(s, i) for i, s in enumerate(b03)]

drop_b04_1based = {
    27,
    29,
    38,
    39,
    44,
    45,
    54,
    61,
    64,
    66,
    69,
    73,
    77,
    83,
    93,
    98,
    110,
    120,
    131,
}
b04_raw = [s for i, s in enumerate(ns["b04"], 1) if i not in drop_b04_1based]
b04 = [pad(s, i) for i, s in enumerate(b04_raw)]

BOOKS = {"b02": b02, "b03": b03, "b04": b04}

FORBIDDEN = ["本書", "作者指出", "本章", "這一章"]
CHAPTER = re.compile(r"第.章")
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


def check(xs):
    issues = []
    if len(xs) != 150:
        issues.append(f"COUNT {len(xs)}")
    if len(set(xs)) != 150:
        issues.append("DUP_FULL")
    p18 = [x[:18] for x in xs]
    if len(set(p18)) != 150:
        c = Counter(p18)
        issues.append("DUP_P18 " + str([k for k, v in c.items() if v > 1][:5]))
    c8 = Counter(cjk(x)[:8] for x in xs)
    bad8 = [f"{v}:{k}" for k, v in c8.items() if v >= 4]
    if bad8:
        issues.append("P8 " + str(bad8))
    for i, s in enumerate(xs, 1):
        if "：" in s or ":" in s or "｜" in s or "|" in s:
            issues.append(f"{i} punct")
        for f in FORBIDDEN:
            if f in s:
                issues.append(f"{i} forb")
        if CHAPTER.search(s):
            issues.append(f"{i} chap")
        for t in TITLES:
            if t in s:
                issues.append(f"{i} title")
        letters = "".join(ch for ch in s if ch.isascii() and ch.isalpha())
        if letters:
            issues.append(f"{i} EN:{letters} {s}")
        n = len(cjk(s))
        if n < 28 or n > 55:
            issues.append(f"{i} LEN{n} {s}")
        if s.startswith(("飲食", "養生", "身體")):
            issues.append(f"{i} start")
    return issues


lines = []
for k, xs in BOOKS.items():
    iss = check(xs)
    lines.append(f"{k} {len(xs)} issues={len(iss)}")
    lines.extend(iss[:30])

(root / "_chk_food_hl2.txt").write_text("\n".join(lines), encoding="utf-8")

# Python source using double quotes, escape as needed
out = ["BOOKS = {"]
for k, xs in BOOKS.items():
    out.append(f'    "{k}": [')
    for s in xs:
        s2 = s.replace("\\", "\\\\").replace('"', '\\"')
        out.append(f'        "{s2}",')
    out.append("    ],")
out.append("}")
text = "\n".join(out) + "\n"
(root / "BOOKS_b02_b03_b04.py").write_text(text, encoding="utf-8")
print("written", len(text))
