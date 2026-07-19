# -*- coding: utf-8 -*-
"""Build highlights JSON and run findbook_writer complete."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NUMBER_RE = re.compile(r"^\d{3}、")
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
FORBIDDEN = ("本書", "作者指出", "本章", "這一章")


def validate(highlights: list[str], title: str = "", author: str = "") -> None:
    if len(highlights) != 150:
        raise ValueError(f"count {len(highlights)}")
    short: list[int] = []
    bodies: list[str] = []
    for i, line in enumerate(highlights, 1):
        exp = f"{i:03d}、"
        if not line.startswith(exp):
            raise ValueError(f"num {i}")
        if "\n" in line or "\r" in line or "｜" in line:
            raise ValueError(f"format {i}")
        body = NUMBER_RE.sub("", line, 1).strip()
        if len(body) < 12:
            raise ValueError(f"short {i}: {body}")
        if any(p in body for p in FORBIDDEN):
            raise ValueError(f"forbidden {i}")
        if re.search(r".{1,8}面第\d+步[，,]", body) or re.match(r"^第\d+步[，,]", body):
            raise ValueError(f"step {i}")
        m = re.match(r"^([^：:]{1,12})[：:]", body)
        if m and not m.group(1).endswith(NATURAL):
            short.append(i)
        bodies.append(body)
    if len(short) >= 3:
        raise ValueError(f"colon {short}")
    if len(set(bodies)) != len(bodies):
        raise ValueError("dup body")
    rep = Counter(b[:18] for b in bodies if len(b) >= 18)
    if rep and rep.most_common(1)[0][1] >= 4:
        raise ValueError(f"rep start {rep.most_common(5)}")
    for label, value in (("書名", title), ("作者", author)):
        if value and sum(value in b for b in bodies) >= 2:
            raise ValueError(f"repeat {label}")


def complete(book_id: str, title: str, author: str, raw: list[str]) -> None:
    if len(raw) != 150:
        raise SystemExit(f"{book_id} RAW count {len(raw)}")
    highlights = [f"{i:03d}、{text}" for i, text in enumerate(raw, 1)]
    validate(highlights, title, author)
    out = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    out.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "findbook_writer.py"),
        "complete",
        "--category-id",
        "01_business_startup",
        "--results",
        str(out),
    ]
    print("wrote", out)
    subprocess.check_call(cmd, cwd=str(ROOT))
