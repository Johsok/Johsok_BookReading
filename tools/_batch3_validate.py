# -*- coding: utf-8 -*-
import importlib.util
import re
from collections import Counter
from pathlib import Path

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
FORBIDDEN = ("本書", "作者指出", "本章", "這一章")


def check(lines, title="", author=""):
    issues = []
    if len(lines) != 150:
        issues.append(f"count={len(lines)}")
    if len(set(lines)) != len(lines):
        issues.append("dup")
    short_colon = []
    for i, body in enumerate(lines, 1):
        if len(body) < 12:
            issues.append(f"short{i}")
        if any(p in body for p in FORBIDDEN):
            issues.append(f"forbid{i}")
        if "｜" in body:
            issues.append(f"bar{i}")
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL):
            short_colon.append(i)
    if len(short_colon) >= 3:
        issues.append(f"colon{len(short_colon)}:{short_colon[:10]}")
    starts = Counter(body[:18] for body in lines if len(body) >= 18)
    if starts and starts.most_common(1)[0][1] >= 4:
        issues.append(f"start:{starts.most_common(1)[0]}")
    for label, value in (("title", title), ("author", author)):
        if value and sum(value in body for body in lines) >= 2:
            issues.append(f"repeat_{label}")
    return issues


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LINES


jobs = [
    ("37", "tools/_batch3_book37.py", "理財關鍵100：學校不會教，簡單易學，為自己開創複利人生！", "葉怡成"),
    ("38", "tools/_batch3_book38.py", "人生的五種財富【實踐套書】（《人生的五種財富》+《人生的五種財富【實作練習本】》共兩冊）", "薩希．布魯姆"),
    ("39", "tools/_batch3_book39.py", "思考致富：全球3億人瘋傳的財富翻倍公式", "拿破崙．希爾"),
    ("40", "tools/_batch3_book40.py", "人腦與AI腦的新協作革命：從分析師到創造者的工作模式根本改變", "陳永隆,曾憲鈺,蔡承佳"),
]
lines_out = []
for key, path, title, author in jobs:
    issues = check(load(Path(path)), title, author)
    lines_out.append(f"{key}: {'OK' if not issues else issues}")
Path("tools/_batch3_validate.txt").write_text("\n".join(lines_out), encoding="utf-8")
print("\n".join(lines_out))
