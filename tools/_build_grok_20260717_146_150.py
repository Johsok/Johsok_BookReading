# -*- coding: utf-8 -*-
"""Build and validate Grok highlight JSON for 20260717-146..150."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402

BOOKS = {
    "02_psychology_growth-20260717-146": (
        "一本書終結你的拖延症【漫畫版】：透過「小行動」打開大腦的行動開關，懶人也能變身「行動派」的37個科學方法",
        "大平信孝",
    ),
    "02_psychology_growth-20260717-147": (
        "情緒使你更強大：重設情緒原始碼，開啟不內耗、不糾結、不委屈的新人生",
        "茱莉亞．迪甘吉",
    ),
    "02_psychology_growth-20260717-148": (
        "解答之書：專屬於你的人生答案(柔紋皮面燙金＋方背穿線精裝)",
        "卡羅．波特",
    ),
    "02_psychology_growth-20260717-149": (
        "逆境翻身：用心理韌性打造贏家心態",
        "陳泰廷",
    ),
    "02_psychology_growth-20260717-150": (
        "讓情緒流動：耶魯大學情緒素養課2 自我覺察工具 ✕ 情境對話練習，鍛鍊調節情緒的能力與韌性，建立溫暖自在的好關係",
        "馬克．布雷克特",
    ),
}

SIMP = re.compile(r"[这们来说为会对时关机还过后从开关学动体经现实觉处进选择调练脑与于当种样点问题应该认识绪强设码开启纠结个条发发后里里]")
# lighter simplified detector for common leaks
SIMP_WORDS = (
    "等于", "后", "这", "个", "为", "会", "说", "让", "从", "开", "关", "学", "习",
    "动", "还", "过", "时", "对", "经", "现", "实", "觉", "处", "们", "来", "进",
    "选", "择", "调", "练", "脑", "体", "与", "于", "当", "种", "样", "点", "问",
    "题", "应", "该", "认", "识", "绪", "强", "内", "设", "码", "开", "启", "纠",
    "结", "发", "后", "里",
)


def load_bodies(book_id: str) -> list[str]:
    path = ROOT / "tools" / f"_bodies_{book_id}.txt"
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return lines


def extra_checks(book_id: str, bodies: list[str], title: str, author: str) -> list[str]:
    errors = []
    if len(bodies) != 150:
        errors.append(f"{book_id} count={len(bodies)}")
    starts = Counter(b[:18] for b in bodies if len(b) >= 18)
    dup_starts = [(s, n) for s, n in starts.items() if n >= 3]
    if dup_starts:
        errors.append(f"{book_id} start repeats (>=3): {dup_starts[:8]}")
    for i, body in enumerate(bodies, 1):
        if "codetime" in body or "不等于" in body:
            errors.append(f"{book_id}#{i} ascii/simplified leak: {body}")
        if title and title in body:
            errors.append(f"{book_id}#{i} full title")
        if author and author in body:
            errors.append(f"{book_id}#{i} author")
    return errors


def main() -> int:
    all_errors = []
    for book_id, (title, author) in BOOKS.items():
        bodies = load_bodies(book_id)
        all_errors.extend(extra_checks(book_id, bodies, title, author))
        highlights = [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]
        try:
            validate_highlights(book_id, highlights, title, author)
        except Exception as exc:
            all_errors.append(f"{book_id} validate: {exc}")
            continue
        out = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
        out.write_text(
            json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"ok {book_id} -> {out.name}")
    if all_errors:
        print("ERRORS:")
        for err in all_errors:
            print(" -", err)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
