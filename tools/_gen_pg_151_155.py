# -*- coding: utf-8 -*-
"""Rewrite 150 unique Traditional Chinese highlights for psychology books 151-155."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
from findbook_writer import validate_highlights  # noqa: E402
import _hl_pg_151 as b151
import _hl_pg_152 as b152
import _hl_pg_153 as b153
import _hl_pg_154 as b154
import _hl_pg_155 as b155

FORBIDDEN = ("本書", "作者指出", "本章", "這一章", "第X章")
CHAPTER_RE = re.compile(r"第[一二三四五六七八九十\d]+章")
LATIN = re.compile(r"[A-Za-z]{3,}")
SIMP_HINT = re.compile(r"[这说们来对为时过还发经与从后面对开关问头条样种点动]")


def extra_checks(book_id: str, title: str, author: str, bodies: list[str]) -> None:
    """Flag leftover English, forbidden tokens, and weak uniqueness."""
    if len(bodies) != 150:
        raise ValueError(f"{book_id} need 150 got {len(bodies)}")
    if len(set(bodies)) != 150:
        dup = [item for item, count in Counter(bodies).items() if count > 1]
        raise ValueError(f"{book_id} duplicate bodies: {dup[:5]}")
    starts = Counter(body[:18] for body in bodies if len(body) >= 18)
    bad_starts = [(key, count) for key, count in starts.items() if count >= 4]
    if bad_starts:
        raise ValueError(f"{book_id} repeated starts: {bad_starts[:5]}")
    for index, body in enumerate(bodies, 1):
        if len(body) < 12:
            raise ValueError(f"{book_id} #{index} too short: {body}")
        if LATIN.search(body):
            raise ValueError(f"{book_id} #{index} latin: {body}")
        if "｜" in body or "**" in body or "`" in body:
            raise ValueError(f"{book_id} #{index} bad mark: {body}")
        if any(token in body for token in FORBIDDEN) or CHAPTER_RE.search(body):
            raise ValueError(f"{book_id} #{index} forbidden: {body}")
        if title and title in body:
            raise ValueError(f"{book_id} #{index} full title")
        if author and author in body:
            raise ValueError(f"{book_id} #{index} full author")


def complete_one(book_id: str, title: str, author: str, bodies: list[str]) -> str:
    """Validate, write results JSON, and run findbook_writer complete."""
    extra_checks(book_id, title, author, bodies)
    highlights = [f"{index:03d}、{body}" for index, body in enumerate(bodies, 1)]
    validate_highlights(book_id, highlights, title, author)
    results = TOOLS / f".findbook_results_grok_{book_id}.json"
    results.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(TOOLS / "findbook_writer.py"),
            "--root",
            str(ROOT),
            "complete",
            "--category-id",
            "02_psychology_growth",
            "--results",
            str(results),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    sys.stdout.write(proc.stdout or "")
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or "")
        raise SystemExit(f"{book_id} writer failed")
    return f"written\t{book_id}"


def main() -> None:
    """Write all five books through findbook_writer."""
    packs = [
        (b151.BOOK_ID, b151.TITLE, b151.AUTHOR, b151.BODIES),
        (b152.BOOK_ID, b152.TITLE, b152.AUTHOR, b152.BODIES),
        (b153.BOOK_ID, b153.TITLE, b153.AUTHOR, b153.BODIES),
        (b154.BOOK_ID, b154.TITLE, b154.AUTHOR, b154.BODIES),
        (b155.BOOK_ID, b155.TITLE, b155.AUTHOR, b155.BODIES),
    ]
    for book_id, title, author, bodies in packs:
        print(f"count\t{book_id}\t{len(bodies)}")
        extra_checks(book_id, title, author, bodies)
        complete_one(book_id, title, author, bodies)
    print("done")


if __name__ == "__main__":
    main()
