# -*- coding: utf-8 -*-
"""Overwrite chatgptHighlights for 03_natural_science-20260717-81..90."""
from __future__ import annotations

import json
import os
import re
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\03_natural_science")
UPDATED = "2026-08-18"
CAPTURED = "2026-08-18T15:40:00+08:00"
BANNED = ("本書", "作者指出", "本章", "這一章", "｜")
COLON_RE = re.compile(r"[：:]")
STEP_RE = re.compile(r".面第\d+步")


def numbered(items: list[str]) -> list[str]:
    return [f"{i:03d}、{t}" for i, t in enumerate(items, 1)]


def validate(name: str, items: list[str], title: str = "", author: str = "") -> None:
    if len(items) != 150:
        raise SystemExit(f"{name}: expected 150, got {len(items)}")
    for i, text in enumerate(items, 1):
        for b in BANNED:
            if b in text:
                raise SystemExit(f"{name} #{i}: banned `{b}`")
        if COLON_RE.search(text):
            raise SystemExit(f"{name} #{i}: colon found")
        if STEP_RE.search(text):
            raise SystemExit(f"{name} #{i}: step pattern")
        if re.match(r"^\d{3}、", text):
            raise SystemExit(f"{name} #{i}: already numbered?")
        if len(text.strip()) < 12:
            raise SystemExit(f"{name} #{i}: too short")
    dups = [k for k, v in Counter(items).items() if v > 1]
    if dups:
        raise SystemExit(f"{name}: duplicate lines: {dups[:3]}")

    def cjk_prefix(s: str, n: int = 8) -> str:
        chars = re.findall(r"[\u4e00-\u9fff]", s)
        return "".join(chars[:n])

    open_c = Counter(cjk_prefix(t) for t in items if cjk_prefix(t))
    bad = [(k, v) for k, v in open_c.items() if v >= 4]
    if bad:
        raise SystemExit(f"{name}: repeated openings: {bad[:5]}")
    starts = Counter(t[:18] for t in items if len(t) >= 18)
    if starts and starts.most_common(1)[0][1] >= 4:
        raise SystemExit(f"{name}: repeated 18-char starts: {starts.most_common(1)}")
    for label, value in (("title", title), ("author", author)):
        if value and sum(value in t for t in items) >= 2:
            raise SystemExit(f"{name}: repeated {label}")


def atomic_write(path: Path, data: dict) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


def write_book(filename: str, highlights: list[str], tags: list[str], summary: str) -> dict:
    path = ROOT / filename
    with path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)
    validate(filename, highlights, data.get("title", ""), data.get("author", ""))
    data["chatgptHighlights"] = numbered(highlights)
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = CAPTURED
    data["updatedAt"] = UPDATED
    data["tags"] = tags
    data["summary"] = summary
    atomic_write(path, data)
    return {"file": filename, "count": 150, "ok": True, "title": data.get("title")}


from _hl_81_85 import BOOKS_81_85  # noqa: E402
from _hl_86_90 import BOOKS_86_90  # noqa: E402


def main() -> None:
    results = []
    for item in BOOKS_81_85 + BOOKS_86_90:
        results.append(write_book(*item))
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
