# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import NATURAL_COLON_SUFFIXES, NUMBER_RE, validate_highlights

BOOKS = [
    ("01_business_startup-20260830-06", "四騎士主宰的未來：解析地表最強四巨頭Amazon、Apple、Facebook、Google的兆演算法，你不可不知道的生存策略與關鍵能力", "史考特．蓋洛威", ROOT / "tools/_tmp_batchB_06.txt"),
    ("01_business_startup-20260830-07", "高績效心智：全新聰明工作學，讓你成為最厲害的1%", "莫頓．韓森", ROOT / "tools/_tmp_batchB_07.txt"),
    ("01_business_startup-20260830-13", "任務就要按時完成", "中島聰", ROOT / "tools/_tmp_batchB_13.txt"),
]

FORBIDDEN = ("本書", "作者指出", "本章", "這一章", "｜")


def load_bodies(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8").splitlines()
    bodies = []
    for line in raw:
        text = line.strip()
        if not text or text == ")":
            continue
        bodies.append(text)
    return bodies


def extra_checks(book_id: str, bodies: list[str], title: str, author: str) -> list[str]:
    errs = []
    if len(bodies) != 150:
        errs.append(f"{book_id} count={len(bodies)}")
    short_colon = []
    for i, body in enumerate(bodies, 1):
        if any(x in body for x in FORBIDDEN):
            errs.append(f"{book_id} #{i} forbidden token: {body[:40]}")
        if re.search(r".{1,8}面第\d+步[，,]", body) or re.match(r"^第\d+步[，,]", body):
            errs.append(f"{book_id} #{i} step wording")
        if len(body) < 12:
            errs.append(f"{book_id} #{i} short body")
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES):
            short_colon.append((i, match.group(1)))
        if re.search(r"[A-Za-z]{4,}", body):
            errs.append(f"{book_id} #{i} latin: {body}")
    if len(short_colon) >= 3:
        errs.append(f"{book_id} short-colon {len(short_colon)}: {short_colon}")
    elif short_colon:
        errs.append(f"{book_id} short-colon warn {short_colon}")
    if len(set(bodies)) != len(bodies):
        errs.append(f"{book_id} duplicate bodies")
    starts = Counter(b[:18] for b in bodies if len(b) >= 18)
    bad = [(k, v) for k, v in starts.items() if v >= 4]
    if bad:
        errs.append(f"{book_id} repeated starts: {bad}")
    for label, value in (("title", title), ("author", author)):
        if value and sum(value in b for b in bodies) >= 2:
            errs.append(f"{book_id} repeats full {label}")
    return errs


def main() -> int:
    all_errs = []
    for book_id, title, author, path in BOOKS:
        bodies = load_bodies(path)
        print(f"{book_id} lines={len(bodies)}")
        all_errs.extend(extra_checks(book_id, bodies, title, author))
        highlights = [f"{i:03d}、{body}" for i, body in enumerate(bodies, 1)]
        if len(bodies) == 150:
            try:
                validate_highlights(book_id, highlights, title, author)
                print(f"{book_id} validate_highlights OK")
            except ValueError as exc:
                all_errs.append(str(exc))
    if all_errs:
        print("ERRORS:")
        for err in all_errs:
            print(" -", err)
        return 1
    print("ALL OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
