# -*- coding: utf-8 -*-
import json
import re
from collections import Counter
from pathlib import Path

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
FORBIDDEN = ("本書", "作者指出", "本章", "這一章")
CHAPTER = re.compile(r"第[0-9一二三四五六七八九十百]+章")
SIMP_HINT = re.compile(
    r"[国发时会业说对们长经产这从关还过个开为来门问东车价质盘损仓单场账户钱买卖规则标准录图报际计设认读写语号码库级类区线点击扩摊获论观护优势败负责务实现术称总额费资债润亏险证汇预测据档条页链结构层维运营销购储备复杂简显隐稳变换转递迟达远进退选择适应该让给贝风头态频宽窄涨跌创闭锁钥扫描识别离职银联团组织训练试验状况环戏剧众连专义词编辑译导检监]"
)

JOBS = [
    (
        "07",
        Path(__file__).with_name("03_natural_science-20260709-07.json"),
        "人類大歷史（增訂版）：從野獸到扮演上帝 【簡體版書名：人類簡史】",
        "哈拉瑞",
        ["人類簡史"],
    ),
    (
        "08",
        Path(__file__).with_name("03_natural_science-20260709-08.json"),
        "鯨．豚：超圖解海洋巨物的美麗與神祕",
        "雅曼汀．德洛內",
        [],
    ),
]


def check(path, title, author, extra_forbid):
    data = json.loads(path.read_text(encoding="utf-8"))
    hs = data["highlights"]
    issues = []
    if data.get("id") != path.stem:
        issues.append(f"id mismatch {data.get('id')}")
    if len(hs) != 150:
        issues.append(f"count={len(hs)}")
    if len(set(hs)) != len(hs):
        issues.append("full-line dup")
    bodies = []
    nums = []
    short_colon = []
    for i, line in enumerate(hs, 1):
        m = re.match(r"^(\d{3})、(.*)$", line)
        if not m:
            issues.append(f"fmt{i}")
            continue
        n, body = m.group(1), m.group(2)
        nums.append(n)
        bodies.append(body)
        if int(n) != i:
            issues.append(f"num{i}={n}")
        if "\n" in body:
            issues.append(f"newline{i}")
        if len(body) < 12:
            issues.append(f"short{i}:{len(body)}:{body}")
        if any(p in body for p in FORBIDDEN):
            issues.append(f"forbid{i}")
        if "｜" in body:
            issues.append(f"bar{i}")
        if CHAPTER.search(body):
            issues.append(f"chapter{i}")
        if "面第" in body and "步" in body:
            issues.append(f"step{i}")
        for w in extra_forbid:
            if w in body:
                issues.append(f"extra:{w}:{i}")
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL):
            short_colon.append(i)
        simp = SIMP_HINT.findall(body)
        if simp:
            issues.append(f"simp{i}:{''.join(simp[:8])}")
    if nums != [f"{i:03d}" for i in range(1, 151)]:
        issues.append("number sequence")
    if len(short_colon) >= 3:
        issues.append(f"colon{len(short_colon)}:{short_colon[:12]}")
    starts = Counter(b[:18] for b in bodies if len(b) >= 18)
    top = starts.most_common(3)
    if top and top[0][1] >= 4:
        issues.append(f"start:{top[0]}")
    two = Counter(b[:2] for b in bodies)
    two_top = [(k, v) for k, v in two.most_common(8) if v >= 6]
    if title and sum(title in b for b in bodies) >= 2:
        issues.append("repeat_title")
    if author and sum(author in b for b in bodies) >= 2:
        issues.append(f"repeat_author:{sum(author in b for b in bodies)}")
    ten = Counter(b[:10] for b in bodies)
    ten_dups = [(k, v) for k, v in ten.most_common(5) if v >= 3]
    zhi = [i for i, b in enumerate(bodies, 1) if b.startswith("智人")]
    jp = [i for i, b in enumerate(bodies, 1) if b.startswith("鯨豚")]
    return {
        "issues": issues,
        "top18": top,
        "two_ge6": two_top,
        "ten_ge3": ten_dups,
        "author_count": sum(author in b for b in bodies),
        "title_count": sum(title in b for b in bodies),
        "min_len": min(len(b) for b in bodies),
        "max_len": max(len(b) for b in bodies),
        "start_zhi": zhi,
        "start_jp": jp,
        "count": len(hs),
    }


for key, path, title, author, extra in JOBS:
    result = check(path, title, author, extra)
    print(f"=== {key} count={result['count']} ===")
    print("OK" if not result["issues"] else result["issues"])
    print("top18", result["top18"])
    print("two_ge6", result["two_ge6"])
    print("ten_ge3", result["ten_ge3"])
    print("author_count", result["author_count"], "title_count", result["title_count"])
    print("min_len", result["min_len"], "max_len", result["max_len"])
    print("start_智人", result["start_zhi"], "start_鯨豚", result["start_jp"])
