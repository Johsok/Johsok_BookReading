# -*- coding: utf-8 -*-
"""Validate, write results, and complete books 147-150."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from findbook_writer import validate_highlights  # noqa: E402
from _hl_147 import BODIES as B147
from _hl_148 import BODIES as B148
from _hl_149 import BODIES as B149
from _hl_150 import BODIES as B150

META = {
    "01_business_startup-20260716-147": (
        "華爾街最長勝的投資家族：富過三代的價值投資傳奇，戴維斯王朝的致富之道",
        "約翰．羅斯柴爾德",
        B147,
    ),
    "01_business_startup-20260716-148": (
        "有錢人的幸福，和你想的不一樣：不只變有錢，還能長智慧！",
        "克里斯多福‧厄爾曼",
        B148,
    ),
    "01_business_startup-20260716-149": (
        "光速交易：超高速演算法如何改變金融市場？",
        "唐納・麥肯錫",
        B149,
    ),
    "01_business_startup-20260716-150": (
        "進化的力量3：情緒經濟",
        "劉潤",
        B150,
    ),
}


def pack(bodies: list[str]) -> list[str]:
    return [f"{i:03d}、{body}" for i, body in enumerate(bodies, 1)]


def write_and_complete(book_id: str, title: str, author: str, bodies: list[str]) -> None:
    if len(bodies) != 150:
        raise SystemExit(f"{book_id} count={len(bodies)} (need 150)")
    highlights = validate_highlights(book_id, pack(bodies), title, author)
    results_path = TOOLS / f".findbook_results_grok_{book_id}.json"
    results_path.write_text(
        json.dumps({"id": book_id, "source": "grok", "highlights": highlights}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    subprocess.run(
        [
            sys.executable,
            str(TOOLS / "findbook_writer.py"),
            "--root",
            str(ROOT),
            "complete",
            "--category-id",
            "01_business_startup",
            "--results",
            str(results_path),
        ],
        check=True,
    )
    book = json.loads(
        (ROOT / "Books" / "01_business_startup" / f"{book_id}.json").read_text(encoding="utf-8-sig")
    )
    n = len(book.get("chatgptHighlights", []))
    src = book.get("highlightsSource")
    if n != 150 or src != "grok" or book.get("chatgptStatus") != "complete":
        raise SystemExit(f"verify failed {book_id} n={n} src={src} status={book.get('chatgptStatus')}")
    print(f"written/{book_id}/150/grok")


def main() -> None:
    for book_id, (title, author, bodies) in META.items():
        write_and_complete(book_id, title, author, bodies)


if __name__ == "__main__":
    main()
