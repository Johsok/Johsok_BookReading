# -*- coding: utf-8 -*-
"""Write extracted Grok lines into reserved book JSON files."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_highlights import extract_highlights, write_highlights  # noqa: E402


def apply_file(book_id: str, name: str) -> None:
    text = (Path(__file__).parent / name).read_text(encoding="utf-8")
    lines = extract_highlights(text)
    print(book_id, len(lines), flush=True)
    if len(lines) != 150:
        raise SystemExit(f"{book_id} extracted {len(lines)}")
    print(write_highlights(ROOT, book_id, lines), flush=True)


if __name__ == "__main__":
    for book_id, name in [
        item.split("=", 1) for item in sys.argv[1:]
    ]:
        apply_file(book_id, name)
