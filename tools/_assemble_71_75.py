# -*- coding: utf-8 -*-
"""Assemble 5 result JSON files, validate, ready for findbook_writer."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights

LATIN = re.compile(r"[A-Za-z]{4,}")
FORBIDDEN = ("本書", "作者指出", "本章", "這一章")
BAD_SUBS = ("hen", "millimetre", "rumination", "sweeping", "口号", "开不开")


def load_raw_blocks() -> dict[str, list[str]]:
    text = (ROOT / "tools" / "_rewrite_71_75.py").read_text(encoding="utf-8")
    parts = text.split("r'''")
    book_ids = [
        "02_psychology_growth-20260717-71",
        "02_psychology_growth-20260717-72",
    ]
    out: dict[str, list[str]] = {}
    for i, part in enumerate(parts[1:3]):
        body = part.split("'''", 1)[0]
        out[book_ids[i]] = [ln.strip() for ln in body.strip().splitlines() if ln.strip()]
    out["02_psychology_growth-20260717-73"] = load_txt("_hl_73.txt")
    out["02_psychology_growth-20260717-74"] = load_txt("_hl_74.txt")
    out["02_psychology_growth-20260717-75"] = load_txt("_hl_75.txt")
    return out


def load_txt(name: str) -> list[str]:
    return [ln.strip() for ln in (ROOT / "tools" / name).read_text(encoding="utf-8").splitlines() if ln.strip()]


def clean_line(body: str) -> str | None:
    if len(body) < 12:
        return None
    if any(p in body for p in FORBIDDEN):
        return None
    if "｜" in body or "\n" in body:
        return None
    if LATIN.search(body):
        return None
    if any(b in body for b in BAD_SUBS):
        return None
    if re.search(r".{1,8}面第\d+步[，,]", body) or re.match(r"^第\d+步[，,]", body):
        return None
    match = re.match(r"^([^：:]{1,12})[：:]", body)
    if match and not match.group(1).endswith(("是", "為", "在於", "說", "問", "提醒", "表示", "指出")):
        return None
    return body


def pick_150(lines: list[str]) -> list[str]:
    chosen: list[str] = []
    seen: set[str] = set()
    start_count: Counter[str] = Counter()
    for raw in lines:
        body = clean_line(raw)
        if not body or body in seen:
            continue
        key = body[:18] if len(body) >= 18 else body
        if start_count[key] >= 2:
            continue
        seen.add(body)
        start_count[key] += 1
        chosen.append(body)
        if len(chosen) == 150:
            break
    return chosen


META = {
    "02_psychology_growth-20260717-71": ("流下來的眼淚就當給自己澆澆水", "木木の口袋"),
    "02_psychology_growth-20260717-72": ("世界很吵，心很安靜：品讀20杯陶淵明的酒", "費勇"),
    "02_psychology_growth-20260717-73": ("東方夢，西方解：看東西方如何解讀夢的訊號", "周季元"),
    "02_psychology_growth-20260717-74": ("情緒掌控，決定你的人生格局", "宋曉東"),
    "02_psychology_growth-20260717-75": ("奧運金牌選手的「心靈肌肉」鍛鍊法", "韓德賢、金雅朗"),
}


def main() -> int:
    blocks = load_raw_blocks()
    errors = []
    written = []
    for book_id, (title, author) in META.items():
        lines = blocks[book_id]
        if book_id.endswith(("-74", "-75")) or len(lines) != 150:
            lines = pick_150(lines)
        print(f"{book_id} picked={len(lines)} from_raw={len(blocks[book_id])}")
        if len(lines) != 150:
            errors.append(f"{book_id} only {len(lines)} lines")
            continue
        hs = [f"{i:03d}、{b}" for i, b in enumerate(lines, 1)]
        try:
            validate_highlights(book_id, hs, title, author)
        except ValueError as exc:
            errors.append(str(exc))
            starts = Counter(b[:18] for b in lines)
            print("  start", starts.most_common(5))
            continue
        out = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
        out.write_text(
            json.dumps({"id": book_id, "highlights": hs}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        written.append(book_id)
        print(f"  wrote {out.name}")
    print("written", written)
    print("errors", errors)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
